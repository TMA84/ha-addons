ARG BUILD_FROM
FROM $BUILD_FROM

ARG CACHEBUST=1

# Install Python
RUN apk add --no-cache \
    python3 \
    py3-pip

# Create virtual environment and install dependencies
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
RUN pip3 install --no-cache-dir flask requests

# Copy addon files
WORKDIR /app
COPY web.py /app/
COPY run.sh /
RUN chmod a+x /run.sh

EXPOSE 9876

CMD [ "/run.sh" ]
