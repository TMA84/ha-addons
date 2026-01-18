# Netbox Nmap Scanner Add-on

Automatically maintain an up-to-date inventory of active IP addresses in your network using Netbox and nmap.

This Home Assistant add-on wraps the [netbox-nmap-scan](https://github.com/LoH-lu/netbox-nmap-scan) tool, which scans your network prefixes and keeps your Netbox instance synchronized with the current state of your network.

## Features

- Automatic network scanning using nmap
- Synchronization with Netbox IP address inventory
- Configurable scan intervals
- Support for excluding specific prefixes
- Detailed logging

## Prerequisites

Before using this add-on, you need:

1. A running Netbox instance
2. A Netbox API token with appropriate permissions
3. Netbox configured with:
   - Tags for marking scanned IPs (e.g., "active", "inactive")
   - Prefixes with active status to scan

## Configuration

### Required Options

- **netbox_url**: The URL of your Netbox instance (e.g., `https://netbox.example.com`)
- **netbox_token**: Your Netbox API token

### Optional Options

- **scan_interval**: Time in seconds between scans (default: 3600, min: 60, max: 86400)
- **log_level**: Logging level (debug, info, warning, error)
- **enable_dns**: Enable DNS resolution during scanning (default: true)
- **add_last_scan_time**: Add last scan timestamp to IP addresses in Netbox (default: true)
- **show_progress**: Show progress during script execution (default: true)
- **exclude_prefixes**: List of prefixes to exclude from scanning
- **nmap_options**: Nmap command-line options (default: "-sn" for ping scan)

### Example Configuration

```yaml
netbox_url: "https://netbox.example.com"
netbox_token: "your-api-token-here"
scan_interval: 3600
log_level: "info"
enable_dns: true
add_last_scan_time: true
show_progress: true
exclude_prefixes:
  - "10.0.0.0/8"
  - "192.168.1.0/24"
nmap_options: "-sn -T4"
```

## How It Works

1. The add-on generates a `var.ini` configuration file from your Home Assistant settings
2. Connects to your Netbox instance using the provided URL and API token
3. Retrieves all prefixes with active status
4. Scans each prefix using nmap with the specified options
5. Updates Netbox with the scan results (including DNS names if enabled)
6. Optionally adds last scan timestamp to each IP address
7. Waits for the configured interval before the next scan
8. Each scan completes fully before the next one starts (cronjob-style execution)

## Network Requirements

This add-on requires `host_network: true` to properly scan your local network.

## Support

For issues related to:
- The add-on itself: Open an issue in this repository
- The underlying tool: Visit [netbox-nmap-scan](https://github.com/LoH-lu/netbox-nmap-scan)

## Credits

This add-on is based on [netbox-nmap-scan](https://github.com/LoH-lu/netbox-nmap-scan) by LoH-lu.
