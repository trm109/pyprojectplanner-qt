FROM python:3.12

#WORKDIR /app

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt
RUN pip install fastapi

COPY ./server.py ./server.py
COPY ./data/kanban.db ./data/kanban.db

EXPOSE 8000

CMD [ "fastapi", "run", "server.py" ]
