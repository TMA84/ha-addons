ARG BUILD_FROM
FROM $BUILD_FROM

# Cache bust argument - updated for production build fix
ARG CACHEBUST=20260117-0100

# Install only essential dependencies
RUN apk add --no-cache nodejs npm git && \
    rm -rf /var/cache/apk/*

WORKDIR /app

# Clone repository (shallow clone for speed)
RUN echo "Force rebuild: $CACHEBUST" && \
    git clone --depth 1 https://github.com/TMA84/Sonos-Jukebox.git . && \
    echo "Current version: $(cat package.json | grep version)"

# Install all dependencies (including dev for build)
RUN npm install --legacy-peer-deps

# Build with production configuration and relative base href for ingress compatibility
RUN npm run build -- --configuration production --base-href="./" && \
    npm prune --production --legacy-peer-deps

# Verify base href was set correctly
RUN grep 'base href' /app/www/index.html

# Apply server patch
COPY server-patch.js /tmp/server-patch.js
RUN node /tmp/server-patch.js && rm /tmp/server-patch.js

# Copy run script
COPY run.sh /run.sh
RUN chmod +x /run.sh

EXPOSE 8200

CMD ["/run.sh"]
