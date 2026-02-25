ARG BUILD_FROM
FROM $BUILD_FROM

ARG EBUSD_VERSION=26.1

ENV LANG C.UTF-8

RUN apk add --no-cache \
        libcurl \
        libmicrohttpd \
        libstdc++ \
        mosquitto-libs \
        openssl \
    && apk add --no-cache --virtual .build-deps \
        autoconf \
        automake \
        build-base \
        curl-dev \
        git \
        libmicrohttpd-dev \
        libtool \
        linux-headers \
        mosquitto-dev \
        openssl-dev \
    && git clone --depth 1 --branch "${EBUSD_VERSION}" https://github.com/john30/ebusd.git /tmp/ebusd \
    && cd /tmp/ebusd \
    && ./autogen.sh \
    && ./configure --prefix=/usr --sysconfdir=/etc --localstatedir=/var \
    && make -j"$(nproc)" \
    && make install \
    && (strip /usr/bin/ebusd /usr/bin/ebusctl || true) \
    && cd / \
    && rm -rf /tmp/ebusd \
    && apk del .build-deps

LABEL Description="ebusd"

COPY run.sh /
RUN chmod a+x /run.sh
CMD [ "/run.sh" ]

# Health check
HEALTHCHECK --interval=5m --timeout=3s --start-period=90s \
   CMD nc -z 127.0.0.1 8888 || exit 1
