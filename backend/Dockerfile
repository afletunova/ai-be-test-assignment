FROM python:3.14-slim

WORKDIR /backend

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY ./rag /rag
COPY ./rest /rest
COPY ./entrypoint.sh /entrypoint.sh
COPY ./main.py /main.py

RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
