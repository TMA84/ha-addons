# Home-Assistant-Add-on für den Druck-Konfigurator (https://github.com/TMA84/druck-konfigurator).
# Baut dasselbe wie das Dockerfile des Projekts: Ubuntu 24.04, OrcaSlicer (Kommandozeile, ohne Bildschirm)
# für die Kostenkalkulation und Python für den Server (LAN-Modus der Anycubic-Werksfirmware).
ARG BUILD_FROM=ubuntu:24.04
FROM ${BUILD_FROM}

ARG BUILD_ARCH=amd64
ARG DRUCK_REF=main
ARG ORCA_VERSION=2.4.2

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      ca-certificates curl python3 python3-venv \
      libgtk-3-0t64 libwebkit2gtk-4.1-0 libglu1-mesa libegl1 libgl1 libopengl0 libglx0 \
      libgstreamer1.0-0 libgstreamer-plugins-base1.0-0 libsecret-1-0 libmspack0t64 libsoup-3.0-0 \
      libwayland-client0 libwayland-egl1 libwayland-server0 libxkbcommon0 libdbus-1-3 libsm6 libice6 fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# OrcaSlicer als entpacktes AppImage (braucht kein FUSE)
RUN set -e; \
    case "$BUILD_ARCH" in aarch64|arm64) f="OrcaSlicer_Linux_AppImage_Ubuntu2404_aarch64_V${ORCA_VERSION}.AppImage" ;; \
                          *)             f="OrcaSlicer_Linux_AppImage_Ubuntu2404_V${ORCA_VERSION}.AppImage" ;; esac; \
    curl -fsSL -o /tmp/orca.AppImage "https://github.com/OrcaSlicer/OrcaSlicer/releases/download/v${ORCA_VERSION}/$f"; \
    chmod +x /tmp/orca.AppImage; cd /opt; /tmp/orca.AppImage --appimage-extract >/dev/null; \
    mv squashfs-root orca; rm /tmp/orca.AppImage; chmod -R a+rX /opt/orca

# Das Tool selbst: Stand von GitHub (DRUCK_REF = Branch oder Tag)
RUN mkdir /app && curl -fsSL "https://github.com/TMA84/druck-konfigurator/archive/${DRUCK_REF}.tar.gz" \
      | tar -xz -C /app --strip-components=1 \
    && python3 -m venv /opt/venv && /opt/venv/bin/pip install --no-cache-dir -r /app/requirements.txt

ENV KONFIGURATOR_HOST=0.0.0.0 \
    KONFIGURATOR_PORT=8765 \
    ORCA_PATH=/opt/orca/AppRun \
    DATA_DIR=/data \
    HOME=/tmp \
    PYTHONUNBUFFERED=1 \
    PATH=/opt/venv/bin:$PATH

COPY run.sh /run.sh
RUN chmod +x /run.sh
WORKDIR /app
EXPOSE 8765
CMD ["/run.sh"]
