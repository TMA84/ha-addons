ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache \
    nodejs \
    npm 

# Set the working directory inside the container
WORKDIR /app

# Download and unzip the Sonos-Kids-Controller repository
COPY src /app/Sonos-Kids-Controller/
COPY config /app/Sonos-Kids-Controller/server/config/ 

# Install Ionic globally
RUN npm install -g @ionic/cli

# Change directory to the Sonos-Kids-Controller source
WORKDIR /app/Sonos-Kids-Controller

# Install project dependencies
RUN npm install

# Build the project using Ionic
RUN ionic build --prod

# Create the configuration file
RUN cd server/config && cp config-example.json config.json

# Copy run script
COPY run.sh /

## Expose service on port 8200
EXPOSE 8200

# Define the command to run the application
RUN chmod a+x /run.sh
CMD ["/run.sh"]