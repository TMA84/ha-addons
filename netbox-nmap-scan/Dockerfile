ARG BUILD_FROM
FROM $BUILD_FROM

# Install requirements
RUN apk add --no-cache \
    python3 \
    py3-pip \
    nmap \
    git

# Clone the netbox-nmap-scan repository
WORKDIR /app
RUN git clone https://github.com/LoH-lu/netbox-nmap-scan.git .

# Create virtual environment and install Python dependencies
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy configuration template and run script
COPY var.ini.template /app/
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
