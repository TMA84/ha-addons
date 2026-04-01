ARG BUILD_FROM
ARG TRAINING_VERSION=main

# Stage 1: Get the pre-built app from GHCR
FROM ghcr.io/tma84/training:${TRAINING_VERSION} AS app

# Stage 2: Build the HA add-on
FROM $BUILD_FROM

RUN apk add --no-cache nodejs npm

WORKDIR /app

COPY --from=app /app /app
COPY run.sh /run.sh
RUN chmod +x /run.sh

EXPOSE 3001

CMD ["/run.sh"]
