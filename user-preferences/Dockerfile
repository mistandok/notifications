FROM python:3.11-slim

ENV APP_DIR /opt/user-preferences/src

ENV PYTHONPATH "${PYTHONPATH}:/opt"

WORKDIR $APP_DIR

COPY requirements.txt requirements.txt

RUN  apt-get update \
     && apt-get -y install libpq-dev gcc \
     && apt-get install acl \
     && apt install -y netcat \
     && groupadd -r web \
     && useradd -d $APP_DIR -r -g web web \
     && chown web:web -R $APP_DIR \
     && pip install --upgrade pip

RUN pip install -r $APP_DIR/requirements.txt

COPY . $APP_DIR

RUN chmod u+x $APP_DIR/start-fastapi.sh

ENTRYPOINT ["/opt/user-preferences/src/start-fastapi.sh"]
