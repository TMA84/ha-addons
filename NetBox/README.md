# NetBox Home Assistant Add-on

NetBox is an IP address management (IPAM) and data center infrastructure management (DCIM) tool. Initially conceived by the network engineering team at DigitalOcean, NetBox was developed specifically to address the needs of network and infrastructure engineers.

## Features

- IP address management (IPAM)
- Data center infrastructure management (DCIM)
- Device and rack management
- Cable management
- Virtualization tracking
- Circuit management
- Power tracking
- RESTful API
- Webhooks for automation

## Installation

1. Add this repository to your Home Assistant instance
2. Install the NetBox addon
3. Configure the addon with your preferences
4. Start the addon
5. Access NetBox at the provided URL

## Configuration

### Required Settings

- **Superuser Name**: Admin username for NetBox (default: admin)
- **Superuser Email**: Admin email address
- **Superuser Password**: Admin password (change from default!)
- **Secret Key**: Django secret key (auto-generated if empty)
- **Allowed Hosts**: Hosts allowed to access NetBox (default: *)

## First Time Setup

1. Start the addon
2. Wait for initialization to complete (may take a few minutes)
3. Access the web interface
4. Log in with your superuser credentials
5. Begin configuring your infrastructure

## Usage

NetBox provides a comprehensive web interface for managing your network infrastructure. Access it through the Web UI button in Home Assistant or directly at port 8000.

## Support

For issues and feature requests, visit: https://github.com/TMA84/ha-addons
For NetBox documentation, visit: https://docs.netbox.dev/
