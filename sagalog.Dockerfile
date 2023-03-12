FROM python:3.10

EXPOSE 8004/tcp

COPY sagalog-requirements.txt ./
RUN pip install --no-cache-dir -r sagalog-requirements.txt

COPY . .

WORKDIR "/src"

CMD [ "uvicorn", "sagalog.main:app", "--host", "localhost", "--port", "8004", "--reload"]