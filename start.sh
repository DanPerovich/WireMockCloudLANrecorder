java -jar wiremock-standalone-3.5.2.jar --port 8080 --root-dir /app/mappings &
while sleep 5; do :; done
python3 wiremockcloudLANrecorder.py

