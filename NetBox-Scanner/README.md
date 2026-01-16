# NetBox Scanner Home Assistant Add-on

A network scanner that automatically discovers devices and updates NetBox with the findings. This addon uses Nmap to scan specified networks and synchronizes the results with your NetBox instance.

## Features

- Automatic network scanning using Nmap
- Synchronization with NetBox IPAM
- Configurable scan intervals
- Multiple network support
- Automatic cleanup of stale entries
- Tag-based management in NetBox

## Prerequisites

This addon requires a running NetBox instance. You can use the NetBox addon from this repository or connect to an external NetBox server.

## Installation

1. Add this repository to your Home Assistant instance
2. Install the NetBox Scanner addon
3. Configure the addon with your NetBox details
4. Start the addon

## Configuration

### Required Settings

- **NetBox Address**: URL of your NetBox instance (e.g., http://netbox:8000)
- **NetBox Token**: API token from NetBox (create in NetBox under Admin > API Tokens)
- **Scan Interval**: Time in seconds between scans (default: 3600 = 1 hour)
- **Networks**: Comma-separated list of networks to scan (e.g., "192.168.1.0/24,10.0.0.0/24")
- **Cleanup**: Whether to remove stale entries from NetBox (yes/no)

## First Time Setup

1. Install and configure NetBox (either the addon or external instance)
2. Create an API token in NetBox:
   - Log into NetBox
   - Go to Admin > API Tokens
   - Create a new token with write permissions
3. In NetBox, create a tag called "nmap" (Admin > Tags)
4. Configure this addon with the NetBox URL and token
5. Specify the networks you want to scan
6. Start the addon

## Usage

Once started, the addon will:
1. Scan the specified networks using Nmap
2. Discover active hosts
3. Update NetBox with the findings
4. Tag all entries with "nmap" for tracking
5. Wait for the scan interval
6. Repeat

All discovered hosts will appear in NetBox under IPAM > IP Addresses with the "nmap" tag.

## Notes

- The scanner only discovers hosts that respond to ping
- Hosts are created as /32 entries in NetBox
- Only entries tagged with "nmap" will be managed by the scanner
- Manual entries in NetBox without the tag will not be affected
- If cleanup is enabled, hosts that disappear from scans will be removed from NetBox

## Support

For issues and feature requests, visit: https://github.com/TMA84/ha-addons
For NetBox Scanner documentation, visit: https://github.com/lopes/netbox-scanner
