ARG BUILD_FROM
FROM $BUILD_FROM

# Install dependencies
RUN apk add --no-cache nodejs npm git && \
    rm -rf /var/cache/apk/*

WORKDIR /app

# Clone and setup Sonos-Jukebox
RUN git clone https://github.com/TMA84/Sonos-Jukebox.git . && \
    rm -f package-lock.json && \
    npm install && \
    npm run build && \
    npm prune --production && \
    npm cache clean --force

# Copy run script
COPY run.sh /run.sh
RUN chmod +x /run.sh

EXPOSE 8200

CMD ["/run.sh"]