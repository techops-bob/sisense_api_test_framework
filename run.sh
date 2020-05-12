#!/usr/bin/env bash
set -e

rm -rf gcp_credentials.json

cat << EOF >> gcp_credentials.json
$GCP_CREDENTIALS
EOF

docker-compose stop && docker-compose rm -f && docker-compose up --no-recreate --abort-on-container-exit

exitcode=$(docker inspect -f '{{ .State.ExitCode }}' test_app)
if [[ $exitcode != 0 ]]; then exit $exitcode; fi