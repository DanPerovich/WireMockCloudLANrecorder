# WireMock Cloud LAN Recorder
This utility is used to record internal network dependencies that cannot be reached by WireMock Cloud due to network constraints.  By using this Docker-based utility on a workstation with internal network access, you can record the traffic from a consumer to the API to be mocked, and automatically upload it to your existing WireMock Cloud account.

## Requirements:
-Docker
-Existing WireMock Cloud account
-Your WireMockCloud account API Token, found at <https://app.wiremock.cloud/account/api>
-The cname (ex. https://`q9l5g`.wiremockapi.cloud or https://`academy`.wiremockapi.cloud ) of an existing WireMock Cloud mock API

### Runing the utility
`docker run -p 8080:8080 -it wiremockcloudlanrec`

### Building the Docker Image
`docker build -t wiremockcloudlanrec .`