FROM python:3.10-alpine

RUN apk update && apk add python3-dev \
                        gcc \
                        libc-dev

EXPOSE 8004/tcp

COPY sagalog-requirements.txt ./
RUN pip install --no-cache-dir -r sagalog-requirements.txt

COPY . .

WORKDIR "/src"

CMD [ "uvicorn", "sagalog.main:app", "--host", "localhost", "--port", "8004"]