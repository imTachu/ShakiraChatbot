#!/usr/bin/env bash

set -e -u -o pipefail

cd "$(dirname "${0}")"

# Claim a non-existent temporary file.
ARTIFACT="$(mktemp)"
rm -f "$ARTIFACT"
trap 'rm -f -- "$ARTIFACT"' INT TERM HUP EXIT

# Package the code.
zip -r "${ARTIFACT}" chatbot resources

# Add dependencies.
cd $VIRTUAL_ENV/lib/python2.7/site-packages
zip -r9 "${ARTIFACT}" *

# Deploy the code.
aws lambda update-function-code \
  --region us-east-1 \
  --function-name arn:aws:lambda:us-east-1:${AWS_ACCOUNT_ID}:function:Shakira-Botcontrol \
  --zip-file "fileb://${ARTIFACT}"
