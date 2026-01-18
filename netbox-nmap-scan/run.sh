#!/usr/bin/with-contenv bashio

# Activate virtual environment
source /opt/venv/bin/activate

# Get configuration
NETBOX_URL=$(bashio::config 'netbox_url')
NETBOX_TOKEN=$(bashio::config 'netbox_token')
SCAN_INTERVAL=$(bashio::config 'scan_interval')
LOG_LEVEL=$(bashio::config 'log_level')
ENABLE_DNS=$(bashio::config 'enable_dns')
ADD_LAST_SCAN_TIME=$(bashio::config 'add_last_scan_time')
SHOW_PROGRESS=$(bashio::config 'show_progress')
NMAP_OPTIONS=$(bashio::config 'nmap_options' '-sn')

# Validate required configuration
if [ -z "$NETBOX_URL" ]; then
    bashio::log.fatal "Netbox URL is required!"
    exit 1
fi

if [ -z "$NETBOX_TOKEN" ]; then
    bashio::log.fatal "Netbox API token is required!"
    exit 1
fi

# Convert boolean values to Python format
ENABLE_DNS_PY=$([ "$ENABLE_DNS" = "true" ] && echo "True" || echo "False")
ADD_LAST_SCAN_TIME_PY=$([ "$ADD_LAST_SCAN_TIME" = "true" ] && echo "True" || echo "False")
SHOW_PROGRESS_PY=$([ "$SHOW_PROGRESS" = "true" ] && echo "True" || echo "False")

# Generate var.ini from template
bashio::log.info "Generating var.ini configuration..."
cat > /app/var.ini << EOF
[credentials]
url = ${NETBOX_URL}
token = ${NETBOX_TOKEN}

[options]
enable_dns = ${ENABLE_DNS_PY}
add_last_scan_time = ${ADD_LAST_SCAN_TIME_PY}
show_progress = ${SHOW_PROGRESS_PY}
EOF

# Set log level
case "$LOG_LEVEL" in
    debug)
        export PYTHONVERBOSE=1
        ;;
esac

bashio::log.info "Starting Netbox Nmap Scanner..."
bashio::log.info "Netbox URL: ${NETBOX_URL}"
bashio::log.info "Scan interval: ${SCAN_INTERVAL} seconds"
bashio::log.info "DNS resolution: ${ENABLE_DNS}"
bashio::log.info "Add last scan time: ${ADD_LAST_SCAN_TIME}"
bashio::log.info "Show progress: ${SHOW_PROGRESS}"

# Main loop - ensure previous scan completes before starting next
while true; do
    bashio::log.info "Starting network scan..."
    
    # Run the main scanner script and wait for completion
    cd /app
    python3 main.py
    EXIT_CODE=$?
    
    if [ $EXIT_CODE -eq 0 ]; then
        bashio::log.info "Scan completed successfully"
    else
        bashio::log.error "Scan failed with exit code ${EXIT_CODE}"
    fi
    
    bashio::log.info "Waiting ${SCAN_INTERVAL} seconds until next scan..."
    sleep "$SCAN_INTERVAL"
done
