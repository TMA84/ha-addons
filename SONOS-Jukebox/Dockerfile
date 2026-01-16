ARG BUILD_FROM
FROM $BUILD_FROM

# Cache bust argument
ARG CACHEBUST=20260116-1700

# Install dependencies
RUN apk add --no-cache \
    nodejs \
    npm \
    git \
    jq \
    curl \
    python3 \
    make \
    g++ \
    && rm -rf /var/cache/apk/*

WORKDIR /app

# Clone repository
RUN echo "Force rebuild: $CACHEBUST" && \
    git clone --depth 1 https://github.com/TMA84/Sonos-Jukebox.git . && \
    echo "Current version: $(cat package.json | grep version)"

# Install dependencies with optimizations
RUN npm ci --prefer-offline --no-audit --legacy-peer-deps || \
    (rm -f package-lock.json && npm install --legacy-peer-deps)

# Build the application
RUN npm run build

# Prune dev dependencies
RUN npm prune --production

# Fix paths for Home Assistant ingress - use relative paths
RUN sed -i 's|<base href="/">|<base href="./">|g' /app/www/index.html && \
    echo "Fixed base href for ingress compatibility"

# Copy and apply server patch for Home Assistant compatibility
COPY server-patch.js /tmp/server-patch.js
RUN node /tmp/server-patch.js && rm /tmp/server-patch.js

# Copy run script
COPY run.sh /run.sh
RUN chmod +x /run.sh

EXPOSE 8200

CMD ["/run.sh"]
