# Not-monolithic-experiments
Entrega 4 y 5 para la materia de diseño y construcción de aplicaciones no monolíticas

# Utilizar en despliegue cloud

## Plataforma de despliegue
- Utilizamos un cluster de kubernetes en GCP y una base de datos manejada de MySQL en GCP
- Para el broker de eventos de pulsar utilizamos un cluster manejado en streamnative.com


Endpoints:
- BFF: http://34.75.144.91/v1
- Sagalog: http://34.23.53.24/transactions


# Operaciones de ejecucion
## Coleccion postman
La coleccion se encuentra ```postman/NoMonolitos.postman_collection.json```

## Como ejecutar una mutacion al BFF?
El BFF expone GraphQL y tiene una interfaz grafica en la url o puede ejecutar la coleccion de postman:
- http://34.75.144.91/v1

Desde alli puede ejecutar la siguiente mutacion
```
mutation {
  crearOrden(idUsuario: "123", simError: "", items: [
    {
      direccionRecogida: "Direccion recogida 123",
      direccionEntrega: "Direccion entrega 123",
      tamanio: "5kg",
      telefono: "3210003212"
    }
  ])
  {
    mensaje
    codigo
  }
}
```

Puede cambiar los parametros de idUsuario, agregar o quitar los items que desee cambiando los respectivos paramétros, lo más importante de esa petición es el **simError**, este es el parámetro que permite simular un error en alguno de los servicios y por ende generar eventos de compensación para revertir la orden.

Los valores de simError son: ordenes, centrodistribucion y entregas que son los respectivos microservicios, si desea que la transacción sea exitosa reemplace por una string vacía

## Como consultar el saga log?
El saga log expone un endpoint en la siguiente url:
- Sagalog: ```GET http://34.23.53.24/transactions```
- Sagalog de una transaccion en especifica: ```GET http://34.23.53.24/transactions/<order_guid>```

En el primer endpoint vemos todas los eventos que se han escuchado mientras que en el segundo obtenemos el sagalog de una transaccion especifica

# Ejecución en Maquina local 

## Requisitos
- Docker
- docker-compose
- Python y un ambiente basado en Linux (la libreria pulsar-client[avro] solo esta disponible para sistema macOs y Linux) - Puede utilizar WSL en windows que es el mecanismo que usamos o gitpod
- Instalar las dependencias de python que estan en el archivo requirements.txt, para esto puede crear un ambiente virtual de python nuevo
## Levantar Broker de mensajería
Desde el directorio principal ejecute el siguiente comando.

```bash
docker-compose --profile pulsar up
```

Este comando descarga las imagenes y levanta el broker de eventos pulsar
## Levantar bases de datos
Desde el directorio principal ejecute el siguiente comando.

```bash
docker-compose --profile db up
```

Este comando descarga las imágenes e instala las dependencias de la base datos.
Este va a crear el servidor de base de datos con las bases de datos independientes para cada microservicio

## Microservicio de Ordenes 
Desde el directorio principal ejecute el siguiente comando.
``` bash
flask --app src/ordenes/api run --port=5000
```

Esto va a ejecutar el microservicio de Ordenes
## Microservicio de Centro de distribucion
Desde el directorio principal ejecute el siguiente comando.
``` bash
flask --app src/centrodistribucion/api run --port=5001
```
Esto va a ejecutar el microservicio de Centro de distribucion
## Microservicio de Entregas 

Desde el directorio principal ejecute el siguiente comando.
``` bash
flask --app src/entregas/api run --port=5002
```
Esto va a ejecutar el microservicio de Entregas

## Envio comando de creacion de orden
Desde el directorio principal ejecute el siguiente comando.
``` bash
python src/test-eventos/envio-crearorden.py
```

## BFF: Web

Desde el directorio `src` ejecute el siguiente comando
```bash
uvicorn bff_web.main:app --host localhost --port 8003 --reload
```

### Crear imagen Docker

Desde el directorio principal ejecute el siguiente comando.

```bash
docker build . -f bff.Dockerfile -t ordenes/bff
```

### Ejecutar contenedora (sin compose)

Desde el directorio principal ejecute el siguiente comando.

```bash
docker run ordenes/bff
```

## Sagalog:

Desde el directorio `src` ejecute el siguiente comando
```bash
uvicorn sagalog.main:app --host localhost --port 8004 --reload
```

### Crear imagen Docker

Desde el directorio principal ejecute el siguiente comando.

```bash
docker build . -f sagalog.Dockerfile -t ordenes/sagalog
```

### Ejecutar contenedora (sin compose)

Desde el directorio principal ejecute el siguiente comando.

```bash
docker run ordenes/sagalog
```

Esto va a publicar un comando en el topico de comandos de eventos con la informacion necesario para crear un evento de alli se realiza la coreografia en una transaccion larga pasando por cada microservicio para entregar la orden

## Overview diagrama arquitectura

![arquitectura](docs/entrega5.png "Arquitectura")

Se usa un patrón de Sagas utilizando Coreografía, donde el fundamento de la coreografía es que cada quién sabe cómo coordinarse por lo tal el saga log es un observador del estado de la transacción aunque puede tomar parte activa en situaciones donde la coreografía no vaya en buen camino, de esta manera logramos que en la transacción larga consigamos atomicidad creando la Orden

# Escenarios de arquitectura
Algunos escenarios fueron modificados debido a que escenarios propuestos en la entrega pasada no reflejaban.


## Escenario Mantenibilidad - Facilidad de integración
Se espera que el sistema sea capaz de integrarse con cualquier sistema tercero en un tiempo menor o igual a 2 meses, para así, poder brindar servicios de cadena de 
suministro interactuando con el sistema integrado.

¿Cómo se cumple?

Existe un desacoplamiento del sistema existente mediante el uso de una arquitectura basada en evento utilizando tópico donde el punto de acoplamiento ahora es la definición de una interfaz en el tópico de Centro de Distribución para recibir eventos de ordenes utilizando un schema Avro completamente versionada, lo cual permite que cualquier nuevo sistema solo deba integrarse utilizando dicho schema con el tópico que es un elemento de infraestructura sin lógica de negocio.

## Escenario Disponibilidad - Resiliencia a particiones
Se espera que después que una orden haya sido recibida esta sea procesada el 99.999% de las veces dado que alguno de los microservicios de ordenes, centro de distribución o entregas no esté funcionando

¿Cómo se cumple el atributo de disponibilidad?

Los microservicios son completamente stateless, asíncronos y por lo tanto desacoplados, por lo cual, podemos particionar el sistema tumbando cualquiera de los microservicios mencionados y ningún Evento/Comando va a perderse, el procesamiento del microservicio puede fallar pero si no se completó los eventos estos no son eliminados y cuando se recupere va a volverse a procesar con lo cual no existe perdida de mensajes y se procesan el 99.999% de los mensajes (Pueden existir edge cases donde incluso la infraestructura colapse por eso se eligen esos SLA)

## Escenario Escalabilidad - Recibir ordenes
Se espera que el sistema frente a un aumento de transacciones de pedidos de 328.000 pedidos por día en temporada pueda procesar la creación de pedidos en menos de 2 minutos el 99.99% de las veces.

¿Cómo se cumple el atributo de escalabilidad?

Al existir un broker de mensajería que es un elemento de plataforma altamente escalable y disponible, para la creación de orden se necesita que el microservicio de ordenes que procesa los comandos de creación de orden pueda escalar, esto es posible con un patrón de una arquitectura orientada a eventos debido a que los componentes consumidores son stateless y se puede configurar políticas de autoescalado horizontal basado en el número de comandos sin procesar que estén el tópico de ordenes.

# Almacenamiento
## Topología de administración de datos
Se utiliza una topología híbrida donde cada servicio tiene su propia base de datos independiente que no se comunica entre sí, lo cual puede ser referido como un namespace, pero coexisten en el mismo servidor, esto debido a la facilidad y flexbilidad para mantener y monitorear los cambios en un único servidor de base de datos.

Esto aplica para los 3 microservicios.
## Capa de datos
Se utiliza un modelo CRUD donde se crean los objetos en la base de datos de cada microservicio y de allí se genera un evento que también se persiste en la base de datos y se publica al tópico de eventos correspondiente, pero el tópico no es persistente y no generamos proyecciones para generar el estado de la base de datos que contiene el estado de la orden.

Esto aplica para los 3 microservicios.

# Mapa de contexto As-To-Be modificado
Teniendo en cuenta los comentarios del tutor en las entregas y adaptandolo a una comunicación orientada a los eventos, en base a los experimentos, el mapa de contexto resultante es el siguiente:

![mapa_de_contexto_as_to_be](docs/mapa_contexto_as_to_be.png "mapa_de_contexto_as_to_be")

Entre los cambios que se tiene son:
* Se elimina el dominio Ordenes y el mapa de contexto PlanificacionOrden ahora pertenece al dominio de Logística. Este mapa de contexto en base a la orden generada elabora un plan para la entrega de productos/bienes. 
* Se agrega contexto de AbastecimientoPorTerceros, que apoya al contexto Abastecimiento en caso no se pueda abastecer con las existencias de la compañia. Esto se hace con el fin de tener contextos separados, uno específico para atender operaciones con bodegas externas y el otro que trabajaría con los otros contextos enfocados en las bodegas internas.
* Se evita el uso de patrón de comunicación Shared Kernel debido a que es un patrón no recomendable para un arquitectura basada en eventos.
* Se agrega contexto de AdministracionUltimaMilla, que en base a los despachos comunicados por DespachoAlimentos o DespachoPedidos (bienes) genera un comando para que EntregaPersonalPropio o EntregaPorTerceros, según convenga, se hagan cargo de entregar lo solicitado en la orden del cliente.


# Actividades realizadas por cada miembro
Miguel y Ayrton: Implementación de microservicio de Entregas utilizando los principios de DDD, con patrones de Comandos y Eventos, eventos de dominio e integración para la comunicación interna dentro del microservicio y externa con el tópico donde se publican los eventos relacionados a que la orden fue entregada, persistencia de los objetos y eventos en la base de datos utilizando CRUD en un mecanismo de unidad de trabajo.

Andres: Implementación de microservicio de Ordenes utilizando los principios de DDD, con patrones de Comandos y Eventos, eventos de dominio e integración para la comunicación interna dentro del microservicio y externa con el tópico donde se publican los eventos relacionados a que una orden fue creada, persistencia de los objetos y eventos en la base de datos utilizando CRUD en un mecanismo de unidad de trabajo.

Pedro: Implementación de microservicio de Centro de distribucion utilizando los principios de DDD, con patrones de Comandos y Eventos, eventos de dominio e integración para la comunicación interna dentro del microservicio y externa con el tópico donde se publican los eventos relacionados a tener una orden lista para entregar, persistencia de los objetos y eventos en la base de datos utilizando CRUD en un mecanismo de unidad de trabajo.

# Servicios desplegados en plataforma local
Para la entrega parcial 4, se ejecuta de manera local utilizando gitpod o en maquina local, mientras que en la entrega 5 se va acabar la implementación de despliegue en la nube.
