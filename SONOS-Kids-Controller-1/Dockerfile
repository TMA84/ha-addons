ARG BUILD_FROM
FROM $BUILD_FROM

# Set environment variables
ENV TZ=Europe/Berlin \
    LANG=de_DE.UTF-8 \
    LANGUAGE=de_DE.UTF-8 \
    LC_ALL=de_DE.UTF-8

# Install dependencies and Ionic in single layer
RUN apk add --no-cache nodejs npm && \
    apk update && \
    npm install -g @ionic/cli && \
    rm -rf /var/cache/apk/* /root/.npm

WORKDIR /app/Sonos-Kids-Controller

# Copy package files first for better caching
COPY src/package*.json ./
RUN npm ci && npm cache clean --force

# Copy source and config
COPY src ./
COPY config ./server/config

# Build the project
RUN ionic build --prod && \
    rm -rf node_modules/@ionic/cli* && \
    npm prune --production

# Create the configuration file
#RUN cd server/config && cp config-example.json config.json

# Copy run script
COPY run.sh /

## Expose service on port 8200
EXPOSE 8200

# Define the command to run the application
RUN chmod a+x /run.sh
CMD ["/run.sh"]