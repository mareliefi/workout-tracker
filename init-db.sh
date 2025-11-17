#!/bin/bash
set -e

# Load environment variables from .env if it exists
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

echo "🗄️  Initializing Postgres..."

# Default values
POSTGRES_USER=${POSTGRES_USER:-marli}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-kaaskrul6}
POSTGRES_DB=${POSTGRES_DB:-workout_tracker}
DB_PORT=${DB_PORT:-5432}

# Wait until Postgres is ready
until pg_isready -U "$POSTGRES_USER" -d "postgres" > /dev/null 2>&1; do
    echo "⏳ Waiting for Postgres to be ready..."
    sleep 2
done

# Create main database if it doesn't exist
echo "📀 Ensuring main database '$POSTGRES_DB' exists..."
psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "postgres" <<-EOSQL
DO
\$do\$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = '$POSTGRES_DB') THEN
      CREATE DATABASE $POSTGRES_DB;
   END IF;
END
\$do\$;
EOSQL
echo "✅ Main database '$POSTGRES_DB' exists."

echo "🎉 Postgres initialization complete!"







