FROM python:3.8-slim-buster
WORKDIR /usr/src/app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY ./server/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./server/app.py app.py
COPY ./server/oai.py oai.py
# if you want to pass in env vars
# without using docker run
# COPY ./server/.env .env
EXPOSE 8080
CMD ["python", "app.py"]