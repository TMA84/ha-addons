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

# Install InfluxDB 1.8 client
RUN apk add --no-cache influxdb-client || \
    (wget -q https://dl.influxdata.com/influxdb/releases/influxdb-1.8.10-static_linux_$(uname -m | sed 's/aarch64/arm64/;s/x86_64/amd64/').tar.gz -O /tmp/influx.tar.gz && \
    tar xzf /tmp/influx.tar.gz -C /tmp && \
    cp /tmp/influxdb-*/influx /usr/local/bin/ && \
    rm -rf /tmp/influx* )

# Clone the evcc-grafana-dashboards repository
WORKDIR /app
RUN echo "Force rebuild: $CACHEBUST" && \
    git clone --depth 1 https://github.com/ha-puzzles/evcc-grafana-dashboards.git . && \
    chmod +x scripts/evcc-influx-aggregate.sh

# Copy addon files
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
