ARG BUILD_FROM
FROM $BUILD_FROM

# Install dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    postgresql \
    postgresql-client \
    redis \
    git \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev \
    libffi-dev \
    openssl-dev \
    jpeg-dev \
    zlib-dev \
    && rm -rf /var/cache/apk/*

WORKDIR /opt

# Clone NetBox
RUN git clone --depth 1 --branch v4.2.0 https://github.com/netbox-community/netbox.git

WORKDIR /opt/netbox

# Install NetBox Python dependencies
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# Copy run script
COPY run.sh /run.sh
RUN chmod +x /run.sh

EXPOSE 8000

CMD ["/run.sh"]
