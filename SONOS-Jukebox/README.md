# SONOS Jukebox Home Assistant Add-on

A touch-based Sonos jukebox interface designed for kids and families.

## Features

- Touch-friendly interface optimized for tablets
- Spotify integration for music search and playback
- Multi-client support with individual configurations
- PIN-protected admin functions
- Album and artist browsing
- Custom playlists and favorites

## Quick Start

### Accessing Local Music Files

This addon has access to your Home Assistant media folder. Your music files will be available at `/media/music` inside the addon.

To add music files:

1. Place your music files in Home Assistant's media folder (typically `/media` on your host)
2. Files will be automatically accessible to the addon at `/media/music`
3. The addon can then serve these files to your Sonos system

Example folder structure:
```
/media/music/
  ├── Artist1/
  │   └── Album1/
  │       └── track.mp3
  └── Artist2/
      └── Album2/
          └── song.mp3
```

## Configuration

### Required Settings

- **Spotify Client ID**: Get from Spotify Developer Dashboard
- **Spotify Client Secret**: Get from Spotify Developer Dashboard
- **Sonos API Server**: IP address of your Sonos HTTP API server
- **Default Room**: Name of the default Sonos speaker/room

### Optional Settings

- **Sonos API Port**: Port of Sonos HTTP API (default: 5005)
- **Admin PIN**: PIN for admin functions (default: 1234)

## Prerequisites

This addon requires the SONOS API addon to be installed and running first.

## Usage

1. Install and configure the SONOS API addon
2. Configure this addon with your Spotify credentials
3. Access the web interface at the provided URL
4. Set up your rooms and create playlists for your kids

## Support

For issues and feature requests, visit: https://github.com/TMA84/ha-addons