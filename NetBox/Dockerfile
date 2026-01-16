ARG BUILD_FROM
FROM $BUILD_FROM

# Install dependencies
RUN apk add --no-cache \
    postgresql-client \
    python3 \
    py3-pip \
    git \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    && rm -rf /var/cache/apk/*

WORKDIR /opt

# Clone NetBox
RUN git clone --depth 1 --branch master https://github.com/netbox-community/netbox-docker.git netbox

WORKDIR /opt/netbox

# Copy run script
COPY run.sh /run.sh
RUN chmod +x /run.sh

EXPOSE 8000

CMD ["/run.sh"]
