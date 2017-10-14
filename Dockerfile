FROM python:3.6-alpine3.6

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ARG PYTHON_REQUIREMENTS=./requirements/production.txt
COPY requirements/ ./requirements
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev make \
    && pip install --use-wheel --no-cache-dir -r ${PYTHON_REQUIREMENTS} \
    && apk del build-deps

COPY . .

EXPOSE 8000

CMD ["make", "run"]
