ARG BUILD_FROM
FROM $BUILD_FROM

# Install dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    nmap \
    git \
    && rm -rf /var/cache/apk/*

# Clone netbox-scanner from GitHub
WORKDIR /opt
RUN git clone https://github.com/lopes/netbox-scanner.git

WORKDIR /opt/netbox-scanner

# Install Python dependencies
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# Copy run script
COPY run.sh /run.sh
RUN chmod +x /run.sh

CMD ["/run.sh"]
