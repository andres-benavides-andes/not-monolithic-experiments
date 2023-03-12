from .mensajes import Mensaje

class ComandoIntegracion(Mensaje):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)