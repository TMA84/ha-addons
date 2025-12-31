# SONOS Jukebox Home Assistant Add-on

A touch-based Sonos jukebox interface designed for kids and families with complete audiobook and radio support.

## Features

- Touch-friendly interface optimized for tablets
- **Complete audiobook support** with chapter-based playback
- **TuneIn Radio integration** with station search (no API keys needed)
- **Library management** with edit functionality for existing items
- Spotify integration for music, podcasts, and audiobooks
- Multi-client support with individual configurations
- PIN-protected admin functions
- **SQLite database** for robust data storage
- Album, artist, podcast, and audiobook browsing

## What's New in Version 2.2.1

### 🔄 Migration & Upgrade Features
- **Automatic migration from JSON to SQLite** - Seamless upgrade path for existing users
- **Legacy data preservation** - All library items, clients, and settings automatically migrated
- **Zero-downtime upgrades** - Migration happens during normal server startup
- **Safe migration process** - Uses INSERT OR REPLACE to prevent data duplication
- **Comprehensive migration support** - Handles config.json, pin.json, and all client data files

### 🛡️ Backward Compatibility
- **Automatic detection** of legacy JSON configuration files
- **Graceful error handling** for malformed or missing legacy files
- **Migration logging** for debugging and verification
- **Home Assistant addon support** - Seamless upgrade for HA users

## What's New in Version 2.2.0

### 🎧 Complete Audiobook Support
- Search and play Spotify audiobooks with automatic chapter detection
- Chapter-based playback compatible with Sonos speakers
- Unified search interface for all content types

### 📻 TuneIn Radio Integration  
- Live radio station search by name or genre
- No API configuration required - works out of the box
- Direct streaming through Sonos speakers

### ✏️ Library Management
- Edit existing library items (artist, title, category, source)
- In-place editing directly from the config page
- Cancel functionality for easy editing workflow

### 🗄️ Modern Database Architecture
- **Persistent SQLite database** stored in Home Assistant config
- All data survives addon updates and restarts
- Better performance and data integrity

## Data Persistence

The addon stores all data in a **persistent SQLite database** located at:
```
/share/sonos-jukebox/data/database.sqlite
```

This ensures:
- **All your library items survive addon updates**
- **Client configurations are preserved**
- **No data loss during restarts**
- **Better performance** than JSON-based storage

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
4. Create client profiles and add content:
   - **Music**: Albums and artists from Spotify
   - **Audiobooks**: Spotify audiobooks with chapter support
   - **Podcasts**: Podcast shows with episode listings
   - **Radio**: TuneIn radio stations (no setup required)
5. Use the edit functionality to modify existing library items

## File Structure

The addon creates a single persistent directory:
```
/share/sonos-jukebox/
└── data/
    └── database.sqlite # SQLite database (all data & config)
```

All configuration and data is stored in the SQLite database:
- **Spotify credentials** (stored in config table)
- **Sonos settings** (stored in config table)  
- **Client profiles** (stored in clients table)
- **Library items** (stored in media_items table)

## Support

For issues and feature requests, visit: https://github.com/TMA84/ha-addons
