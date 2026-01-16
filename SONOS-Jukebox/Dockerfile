ARG BUILD_FROM
FROM $BUILD_FROM

# Cache bust argument
ARG CACHEBUST=20260116-1800

# Install only essential dependencies
RUN apk add --no-cache nodejs npm git && \
    rm -rf /var/cache/apk/*

WORKDIR /app

# Clone repository (shallow clone for speed)
RUN echo "Force rebuild: $CACHEBUST" && \
    git clone --depth 1 https://github.com/TMA84/Sonos-Jukebox.git . && \
    echo "Current version: $(cat package.json | grep version)"

# Install and build with optimizations
RUN npm install --omit=dev --legacy-peer-deps && \
    npm run build && \
    rm -rf node_modules && \
    npm install --production --legacy-peer-deps

# Fix paths for Home Assistant ingress
RUN sed -i 's|<base href="/">|<base href="./">|g' /app/www/index.html

# Fix API paths in built JavaScript files
COPY fix-api-paths.sh /tmp/fix-api-paths.sh
RUN chmod +x /tmp/fix-api-paths.sh && \
    /tmp/fix-api-paths.sh && \
    rm /tmp/fix-api-paths.sh

# Apply server patch
COPY server-patch.js /tmp/server-patch.js
RUN node /tmp/server-patch.js && rm /tmp/server-patch.js

# Copy run script
COPY run.sh /run.sh
RUN chmod +x /run.sh

EXPOSE 8200

CMD ["/run.sh"]
