#!/usr/bin/with-contenv bashio

# Read HA addon options
OPENAI_API_KEY=$(bashio::config 'openai_api_key' '')
OPENAI_MODEL=$(bashio::config 'openai_model' 'gpt-4o-mini')

export OPENAI_API_KEY
export OPENAI_MODEL
export HOST=0.0.0.0
export PORT=3001
export DB_PATH=/data/training.db
export NODE_ENV=production
export CORS_ORIGIN=*

bashio::log.info "Starting Training App on port 3001..."

cd /app
exec node --import tsx/esm server/src/index.ts
