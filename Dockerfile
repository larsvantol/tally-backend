# pull official base image
FROM python:3.11.4-slim-buster as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

# # lint
# RUN pip install --upgrade pip
# RUN pip install flake8==6.0.0
# COPY . /usr/src/app/
# RUN flake8 --ignore=E501,F401 .

# install python dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt




# pull official base image
FROM python:3.11.4-slim-buster

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache /wheels/*


# copy docker-entrypoint.sh
COPY ./docker-entrypoint.sh .
RUN sed -i 's/\r$//g'  $APP_HOME/docker-entrypoint.sh
RUN chmod +x  $APP_HOME/docker-entrypoint.sh

# copy project
COPY ./tally/ $APP_HOME
COPY ./prod.env ./prod.env

RUN set -a && \
    . ./prod.env && \
    python manage.py collectstatic --noinput --no-post-process


# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

# run docker-entrypoint.sh
ENTRYPOINT ["/home/app/web/docker-entrypoint.sh"]
CMD ["gunicorn", "-b=0.0.0.0:8000", "tally.wsgi:application"]
EXPOSE 8000
