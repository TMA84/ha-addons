ARG BUILD_FROM
FROM $BUILD_FROM

ARG CACHEBUST=1

# Install dependencies
RUN apk add --no-cache \
    bash \
    bc \
    coreutils \
    curl \
    git \
    tzdata

# Ensure GNU date is used instead of BusyBox date
RUN ln -sf /usr/bin/date /bin/date

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

# Install supercronic (cron for containers, multi-arch)
RUN ARCH=$(uname -m) && \
    case "$ARCH" in \
      aarch64) SC_ARCH="linux-arm64" ;; \
      x86_64)  SC_ARCH="linux-amd64" ;; \
      armv7l)  SC_ARCH="linux-arm" ;; \
      *)       SC_ARCH="linux-amd64" ;; \
    esac && \
    wget -q "https://github.com/aptible/supercronic/releases/download/v0.2.33/supercronic-${SC_ARCH}" -O /usr/local/bin/supercronic && \
    chmod +x /usr/local/bin/supercronic

# Clone the evcc-grafana-dashboards repository
WORKDIR /app
RUN echo "Force rebuild: $CACHEBUST" && \
    git clone --depth 1 https://github.com/ha-puzzles/evcc-grafana-dashboards.git . && \
    chmod +x scripts/evcc-influx-aggregate.sh

# Copy addon files
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
