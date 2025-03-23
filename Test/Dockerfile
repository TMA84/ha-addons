ARG BUILD_FROM=ghcr.io/hassio-addons/base-nodejs/{arch}:stable
FROM $BUILD_FROM

# Set the working directory inside the container
WORKDIR /app

# Download and unzip the Sonos-Kids-Controller repository
COPY src /app/Sonos-Kids-Controller/

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

## Expose service on port 8200
EXPOSE 8200

# Define the command to run the application
CMD ["npm", "start"]