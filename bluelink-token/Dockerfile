ARG BUILD_FROM
FROM $BUILD_FROM

ARG CACHEBUST=1

# Install dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    chromium \
    chromium-chromedriver \
    git

# Create virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"

# Install Python dependencies
RUN pip3 install --no-cache-dir \
    selenium \
    requests \
    flask

# Clone the bluelink token script
WORKDIR /app
RUN echo "Force rebuild: $CACHEBUST" && \
    git clone --depth 1 https://github.com/RustyDust/bluelink_refresh_token.git /app/bluelink

# Copy addon files
COPY web.py /app/
COPY run.sh /
RUN chmod a+x /run.sh

EXPOSE 9876

CMD [ "/run.sh" ]
