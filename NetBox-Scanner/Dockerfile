ARG BUILD_FROM
FROM $BUILD_FROM

# Install dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    nmap \
    && rm -rf /var/cache/apk/*

# Install netbox-scanner
RUN pip3 install --no-cache-dir --break-system-packages netbox-scanner

# Copy run script
COPY run.sh /run.sh
RUN chmod +x /run.sh

CMD ["/run.sh"]
