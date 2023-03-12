FROM python:3.10-alpine

RUN apk update && apk add python3-dev \
                        gcc \
                        libc-dev

EXPOSE 8004/tcp

COPY requirements.txt ./
RUN pip install --upgrade --no-cache-dir pip setuptools wheel
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY sagalog-requirements.txt ./
RUN pip install --no-cache-dir -r sagalog-requirements.txt

COPY . .

WORKDIR "/src"

CMD [ "uvicorn", "sagalog.main:app", "--host", "0.0.0.0", "--port", "8004"]