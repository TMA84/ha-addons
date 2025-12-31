ARG BUILD_FROM
FROM $BUILD_FROM

# Install dependencies
RUN apk add --no-cache nodejs npm git jq curl && \
    rm -rf /var/cache/apk/*

WORKDIR /app

# Clone and setup Sonos-Jukebox v2.2.1
RUN git clone https://github.com/TMA84/Sonos-Jukebox.git . && \
    git checkout v2.2.1 && \
    rm -f package-lock.json && \
    npm install && \
    npm run build && \
    npm prune --production && \
    npm cache clean --force

# Copy and apply server patch for Home Assistant compatibility
COPY server-patch.js /tmp/server-patch.js
RUN node /tmp/server-patch.js && rm /tmp/server-patch.js

# Copy run script
COPY run.sh /run.sh
RUN chmod +x /run.sh

EXPOSE 8200

CMD ["/run.sh"]