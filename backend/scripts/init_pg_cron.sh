#!/bin/bash
set -e

echo "Initializing pg_cron extension in database '$POSTGRES_DB'..."

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname postgres <<-EOSQL
    CREATE EXTENSION IF NOT EXISTS pg_cron;
    GRANT USAGE ON SCHEMA cron TO $POSTGRES_USER;
EOSQL

echo "pg_cron extension created."

echo "Appending cron.database_name setting to postgresql.conf..."

# Append the cron.database_name setting to the main postgresql.conf file.
# $PGDATA is the standard environment variable pointing to the PostgreSQL data directory.
# This ensures pg_cron uses the correct database for its metadata and job execution context.
echo "cron.database_name = '$POSTGRES_DB'" >> "$PGDATA/postgresql.conf"

echo "cron.database_name set to '$POSTGRES_DB' in $PGDATA/postgresql.conf."

echo "pg_cron initialization complete in $POSTGRES_DB."