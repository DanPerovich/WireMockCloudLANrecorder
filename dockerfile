FROM alpine:3.14

RUN apk update \
  && apk upgrade \
  && apk add --update openjdk11 tzdata curl unzip bash \
  && rm -rf /var/cache/apk/*

# Set the working directory inside the container
WORKDIR /app

# Copy the WireMock standalone JAR file into the container
COPY wiremock-standalone-3.5.2.jar /app/
COPY start.sh /app/

# Expose port 8080 for WireMock
EXPOSE 8080

# Install Python 3 and pip for managing Python packages
RUN apk add --no-cache python3 py3-pip

# Copy the Python script into the container
COPY wiremockcloudLANrecorder.py /app/

# Install required Python packages
RUN pip3 install requests

# Start WireMock standalone server and run the Python script when the container starts
CMD /app/start.sh
