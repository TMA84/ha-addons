#!/usr/bin/with-contenv bashio

# Get configuration
SUPERUSER_NAME=$(bashio::config 'superuser_name')
SUPERUSER_EMAIL=$(bashio::config 'superuser_email')
SUPERUSER_PASSWORD=$(bashio::config 'superuser_password')
SECRET_KEY=$(bashio::config 'secret_key')
ALLOWED_HOSTS=$(bashio::config 'allowed_hosts')

# Generate secret key if not provided
if [ -z "$SECRET_KEY" ]; then
    SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))')
    bashio::log.info "Generated new secret key"
fi

# Export environment variables
export SUPERUSER_NAME="$SUPERUSER_NAME"
export SUPERUSER_EMAIL="$SUPERUSER_EMAIL"
export SUPERUSER_PASSWORD="$SUPERUSER_PASSWORD"
export SECRET_KEY="$SECRET_KEY"
export ALLOWED_HOSTS="$ALLOWED_HOSTS"
export DB_HOST="localhost"
export DB_NAME="netbox"
export DB_USER="netbox"
export DB_PASSWORD="netbox"
export REDIS_HOST="localhost"
export REDIS_PORT="6379"

bashio::log.info "Starting NetBox..."

# Start NetBox using docker-compose
cd /opt/netbox
docker-compose up
