#!/bin/sh

# TUDO SERÁ EXECUTADO QUANDO DER DOKERCOMPOSEUP

# O shell irá encerrar a execução do script quando um comando falhar
set -e

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    echo "🟡 Waiting for Postgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT) ..."
    sleep 2
done

echo "✅ Postgres Database Started Successfully ($POSTGRES_HOST:$POSTGRES_PORT)"

collectstatic.sh
migrate.sh
runserver.sh