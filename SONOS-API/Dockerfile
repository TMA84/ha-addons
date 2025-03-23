ARG BUILD_FROM
FROM $BUILD_FROM

# install node
RUN apk add --no-cache nodejs npm 
RUN apk update
WORKDIR /app

COPY node-sonos-http-api /app

RUN apk add --no-cache curl && \
  mkdir cache && \
  chown -R node:node static cache && \
  npm install --production && \
  rm -rf /tmp/* /root/.npm

EXPOSE 5005

USER node

HEALTHCHECK --interval=1m --timeout=2s \
  CMD curl -LSfs http://localhost:5005/zones || exit 1

CMD npm start