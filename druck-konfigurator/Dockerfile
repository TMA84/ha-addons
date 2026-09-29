# Home-Assistant-Add-on für den Druck-Konfigurator (https://github.com/TMA84/druck-konfigurator).
# Baut auf dem fertigen Image des Projekts auf (GHCR, amd64/arm64, mit OrcaSlicer) – hier nur Start-Skript und
# Add-on-Optionen. Das Add-on-Image baut .github/workflows/build-druck-konfigurator-ghcr.yml.
ARG BUILD_FROM
ARG DRUCK_VERSION=latest
FROM ghcr.io/tma84/druck-konfigurator:${DRUCK_VERSION}

# Home Assistant legt /data für root an
USER root
ENV DATA_DIR=/data
COPY run.sh /run.sh
RUN chmod +x /run.sh
CMD ["/run.sh"]
