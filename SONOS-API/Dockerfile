ARG BUILD_FROM
FROM $BUILD_FROM

# Install dependencies in single layer
RUN apk add --no-cache nodejs npm curl && \
    apk update && \
    rm -rf /var/cache/apk/*

WORKDIR /app

# Copy package files first for better caching
COPY node-sonos-http-api/package*.json ./
RUN npm ci --only=production && \
    npm cache clean --force && \
    rm -rf /tmp/* /root/.npm

# Copy application code
COPY node-sonos-http-api ./
RUN mkdir -p cache

EXPOSE 5005

HEALTHCHECK --interval=1m --timeout=2s \
  CMD curl -LSfs http://localhost:5005/zones || exit 1

CMD npm start