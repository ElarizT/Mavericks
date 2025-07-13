#!/bin/bash
TOKEN="$GITHUB_TOKEN"
if [[ -z "$TOKEN" ]]; then
  echo "GITHUB_TOKEN is not set"
  exit 1
fi

REPO="genai-works-org/genai-agentos"

function gh_curl() {
  curl -sL -H "Authorization: token $TOKEN" \
       -H "Accept: application/vnd.github+json" \
       -H "X-GitHub-Api-Version: 2022-11-28" \
       $@
}

LATEST_TAG=$(gh_curl https://api.github.com/repos/$REPO/releases/latest | jq -r .tag_name 2>/dev/null || echo "")

echo "Latest tag: $LATEST_TAG"
UNIX_BINARY_NAME="genai-unix-$LATEST_TAG.bin" 

# Get latest release download URL
URL=$(gh_curl https://api.github.com/repos/$REPO/releases/latest \
    | jq -r \
  ".assets[] | select(.name == \"$UNIX_BINARY_NAME\") | .url")

echo "Download URL: $URL"
OUTPUT_NAME='genai'


echo "Downloading binary..."


curl -L -H "Accept: application/octet-stream" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "$URL" -o "$OUTPUT_NAME"

chmod +x "$OUTPUT_NAME"
sudo mv $OUTPUT_NAME /usr/local/bin/

