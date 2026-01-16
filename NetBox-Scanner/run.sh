#!/usr/bin/with-contenv bashio

# Get configuration
NETBOX_ADDRESS=$(bashio::config 'netbox_address')
NETBOX_TOKEN=$(bashio::config 'netbox_token')
SCAN_INTERVAL=$(bashio::config 'scan_interval')
NETWORKS=$(bashio::config 'networks')
CLEANUP=$(bashio::config 'cleanup')

# Create config directory
mkdir -p /config/netbox-scanner

# Create configuration file
cat > /config/netbox-scanner/netbox-scanner.conf << EOF
[NETBOX]
address = ${NETBOX_ADDRESS}
token = ${NETBOX_TOKEN}
tls_verify = no

[NMAP]
path = /usr/bin/nmap
unknown = UNKNOWN
tag = nmap
cleanup = ${CLEANUP}
EOF

# Create networks file
echo "$NETWORKS" | tr ',' '\n' > /config/netbox-scanner/networks.txt

bashio::log.info "NetBox Scanner configuration created"
bashio::log.info "NetBox Address: ${NETBOX_ADDRESS}"
bashio::log.info "Scan Interval: ${SCAN_INTERVAL} seconds"
bashio::log.info "Networks: ${NETWORKS}"

# Run scanner in loop
while true; do
    bashio::log.info "Starting network scan..."
    
    cd /config/netbox-scanner
    netbox-scanner nmap
    
    if [ $? -eq 0 ]; then
        bashio::log.info "Scan completed successfully"
    else
        bashio::log.error "Scan failed"
    fi
    
    bashio::log.info "Waiting ${SCAN_INTERVAL} seconds until next scan..."
    sleep ${SCAN_INTERVAL}
done
