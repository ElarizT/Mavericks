#!/bin/bash

# This is a script that is designed to be used only within github actions 
# (`gh` is accesible from within workflow and does not require an installation)

set -e

# Fetch the latest release tag
LATEST_TAG=$(gh release list --limit 1 --json tagName --jq '.[0].tagName' 2>/dev/null || echo "")

if [[ -z "$LATEST_TAG" ]]; then
  NEW_VERSION="0.0.1"
else
  VERSION_PART=$(echo "$LATEST_TAG" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
  IFS='.' read -r MAJOR MINOR PATCH <<< "$VERSION_PART"
  NEW_PATCH=$((PATCH + 1))
  NEW_VERSION="${MAJOR}.0.${NEW_PATCH}"
fi

# echo "Next version: $NEW_VERSION"
echo "$NEW_VERSION" # exporting VERSION to GITHUB_ENV container with env vars
