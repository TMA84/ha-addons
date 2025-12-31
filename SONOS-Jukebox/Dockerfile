ARG BUILD_FROM
FROM $BUILD_FROM

# Install dependencies
RUN apk add --no-cache nodejs npm git jq curl && \
    rm -rf /var/cache/apk/*

WORKDIR /app

# Force fresh clone with cache bust - v2.2.4
RUN rm -rf /tmp/repo && \
    git clone --no-cache --depth 1 https://github.com/TMA84/Sonos-Jukebox.git /tmp/repo && \
    cp -r /tmp/repo/* . && \
    rm -rf /tmp/repo && \
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