ARG BUILD_FROM
ARG JUKEBOX_VERSION=latest

# Stage 1: Get the pre-built app from GHCR
FROM ghcr.io/tma84/sonos-jukebox:${JUKEBOX_VERSION} AS app

# Stage 2: Build the HA add-on
FROM $BUILD_FROM

# Install Node.js runtime
RUN apk add --no-cache nodejs npm

WORKDIR /app

# Copy the pre-built application from the GHCR image
COPY --from=app /app /app

# Apply server patch for HA compatibility
COPY server-patch.js /tmp/server-patch.js
RUN node /tmp/server-patch.js && rm /tmp/server-patch.js

# Copy run script
COPY run.sh /run.sh
RUN chmod +x /run.sh

EXPOSE 8200

CMD ["/run.sh"]
