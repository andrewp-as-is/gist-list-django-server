FROM andrewpasis/python:3.8-alpine-psycopg2

COPY ./ /code/
WORKDIR /code/

RUN pip install -r /code/requirements.txt

EXPOSE 8080
ENTRYPOINT ["/bin/sh","/code/entrypoint.sh"]
