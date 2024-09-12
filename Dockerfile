# alpine image -> bare minimum
FROM python:3.9-alpine3.13
LABEL maintainer="kostopoulos.e@gmail.com"

# output directly to console
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# By default, DEV is false. We'll update it to true when using docker-compose
ARG DEV=false

# create virtual env in docker to store dependencies -> not necessary but ensure consistency 
# upgrade pip inside venv
# install requirements inside venv, if DEV=true then also install dev requirements
# remove tmp files to keep images lightweight
# adduser django-user in the image -> don't use root user-> more secure if compromised
RUN python -m venv /py && \ 
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# update PATH for executables        
ENV PATH="/py/bin:$PATH"

USER django-user