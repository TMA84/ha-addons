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

bashio::log.info "Initializing PostgreSQL..."

# Initialize PostgreSQL
mkdir -p /data/postgres
chown -R postgres:postgres /data/postgres

# Initialize database if not exists
if [ ! -d "/data/postgres/base" ]; then
    su-exec postgres initdb -D /data/postgres
    su-exec postgres pg_ctl -D /data/postgres start
    sleep 3
    su-exec postgres createdb netbox
    su-exec postgres psql -c "CREATE USER netbox WITH PASSWORD 'netbox';"
    su-exec postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE netbox TO netbox;"
else
    su-exec postgres pg_ctl -D /data/postgres start
    sleep 3
fi

bashio::log.info "Starting Redis..."
redis-server --daemonize yes

# Create NetBox configuration
mkdir -p /opt/netbox/netbox/netbox
cat > /opt/netbox/netbox/netbox/configuration.py << EOF
ALLOWED_HOSTS = ['*']
DATABASE = {
    'NAME': 'netbox',
    'USER': 'netbox',
    'PASSWORD': 'netbox',
    'HOST': 'localhost',
    'PORT': '',
    'CONN_MAX_AGE': 300,
}
REDIS = {
    'tasks': {
        'HOST': 'localhost',
        'PORT': 6379,
        'PASSWORD': '',
        'DATABASE': 0,
        'SSL': False,
    },
    'caching': {
        'HOST': 'localhost',
        'PORT': 6379,
        'PASSWORD': '',
        'DATABASE': 1,
        'SSL': False,
    }
}
SECRET_KEY = '${SECRET_KEY}'
EOF

cd /opt/netbox/netbox

bashio::log.info "Running database migrations..."
python3 manage.py migrate --noinput

bashio::log.info "Collecting static files..."
python3 manage.py collectstatic --noinput

bashio::log.info "Creating superuser..."
python3 manage.py shell << PYEOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='${SUPERUSER_NAME}').exists():
    User.objects.create_superuser('${SUPERUSER_NAME}', '${SUPERUSER_EMAIL}', '${SUPERUSER_PASSWORD}')
    print('Superuser created')
else:
    print('Superuser already exists')
PYEOF

bashio::log.info "Starting NetBox on port 8000..."
python3 manage.py runserver 0.0.0.0:8000
