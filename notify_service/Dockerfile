FROM python:3.11

ENV APP_DIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'config.settings'

WORKDIR /opt/app

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

#EXPOSE 8000

RUN chmod u+x $APP_DIR/start-django.sh

ENTRYPOINT ["/opt/app/start-django.sh"]
