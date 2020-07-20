#!/usr/bin/env bash
set -e

rm -rf gcp_credentials.json

cat << EOF >> gcp_credentials.json
$GOOGLE_APPLICATION_CREDENTIALS
EOF

docker-compose up --build