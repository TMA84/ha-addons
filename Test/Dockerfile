ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk update && \
    apk add --no-cache nodejs npm wget unzip

# Set the working directory inside the container
WORKDIR /app

COPY src/package.json /sonos-kids-controller/package.json

# Install Ionic globally
RUN npm install -g @ionic/cli

# Download and unzip the Sonos-Kids-Controller repository
COPY src /sonos-kids-controller/

# Change directory to the Sonos-Kids-Controller source
WORKDIR /app/Sonos-Kids-Controller-master

# Install project dependencies
RUN npm install

# Build the project using Ionic
RUN ionic build --prod

# Create the configuration file
RUN cd server/config && cp config-example.json config.json

# Define the command to run the application
CMD ["npm", "start"]