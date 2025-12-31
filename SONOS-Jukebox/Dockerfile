ARG BUILD_FROM
FROM $BUILD_FROM

# Cache bust argument
ARG CACHEBUST=20251231-1915

# Install dependencies
RUN apk add --no-cache nodejs npm git jq curl && \
    rm -rf /var/cache/apk/*

WORKDIR /app

# Force fresh clone with cache bust
RUN echo "Force rebuild: $CACHEBUST" && \
    git clone https://github.com/TMA84/Sonos-Jukebox.git . && \
    git checkout master && \
    echo "Current version: $(cat package.json | grep version)" && \
    rm -f package-lock.json && \
    npm cache clean --force && \
    npm install && \
    npm run build && \
    npm prune --production

# Copy and apply server patch for Home Assistant compatibility
COPY server-patch.js /tmp/server-patch.js
RUN node /tmp/server-patch.js && rm /tmp/server-patch.js

# Copy run script
COPY run.sh /run.sh
RUN chmod +x /run.sh

EXPOSE 8200

CMD ["/run.sh"]