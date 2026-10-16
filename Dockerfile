FROM python:3.14


WORKDIR /backend


COPY ./requirements.txt /requirements.txt


RUN pip install --no-cache-dir --upgrade -r /requirements.txt


COPY ./backend/ /backend/


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
