ARG BUILD_FROM
FROM $BUILD_FROM

ARG CACHEBUST=1

# Install dependencies
RUN apk add --no-cache \
    bash \
    bc \
    curl \
    git \
    tzdata \
    supercronic

# Install InfluxDB 1.8 client (multi-arch)
RUN ARCH=$(uname -m) && \
    case "$ARCH" in \
      aarch64) INFLUX_ARCH="arm64" ;; \
      x86_64)  INFLUX_ARCH="amd64" ;; \
      armv7l)  INFLUX_ARCH="armhf" ;; \
      *)       INFLUX_ARCH="amd64" ;; \
    esac && \
    wget -q "https://dl.influxdata.com/influxdb/releases/influxdb-1.8.10_linux_${INFLUX_ARCH}.tar.gz" -O /tmp/influx.tar.gz && \
    tar xzf /tmp/influx.tar.gz -C /tmp && \
    cp /tmp/influxdb-1.8.10-1/usr/bin/influx /usr/local/bin/ && \
    chmod +x /usr/local/bin/influx && \
    rm -rf /tmp/influx*

# Clone the evcc-grafana-dashboards repository
WORKDIR /app
RUN echo "Force rebuild: $CACHEBUST" && \
    git clone --depth 1 https://github.com/ha-puzzles/evcc-grafana-dashboards.git . && \
    chmod +x scripts/evcc-influx-aggregate.sh

# Copy addon files
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
