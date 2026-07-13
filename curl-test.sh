#!/bin/bash

BASE_URL="http://127.0.0.1:5000/api/timeline_post"

RANDOM_NUMBER=$RANDOM
NAME="TestUser$RANDOM_NUMBER"
EMAIL="test$RANDOM_NUMBER@example.com"
CONTENT="Random timeline post $RANDOM_NUMBER"

echo "Creating timeline post..."

POST_RESPONSE=$(curl -s -X POST "$BASE_URL" \
  -d "name=$NAME" \
  -d "email=$EMAIL" \
  -d "content=$CONTENT")

echo "POST response:"
echo "$POST_RESPONSE"

POST_ID=$(echo "$POST_RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin)['id'])")

if [ -z "$POST_ID" ]; then
  echo "FAIL: Could not read the new post ID."
  exit 1
fi

echo
echo "Created post ID: $POST_ID"
echo "Retrieving timeline posts..."

GET_RESPONSE=$(curl -s "$BASE_URL")

echo "GET response:"
echo "$GET_RESPONSE"

echo
echo "Checking whether the new post was added..."

if echo "$GET_RESPONSE" | grep -q "$CONTENT"; then
  echo "PASS: Timeline post was added successfully."
else
  echo "FAIL: Timeline post was not found."
  exit 1
fi

echo
echo "Deleting test post..."

DELETE_RESPONSE=$(curl -s -X DELETE "$BASE_URL/$POST_ID")

echo "DELETE response:"
echo "$DELETE_RESPONSE"

echo
echo "Checking whether the post was deleted..."

FINAL_GET_RESPONSE=$(curl -s "$BASE_URL")

if echo "$FINAL_GET_RESPONSE" | grep -q "$CONTENT"; then
  echo "FAIL: Timeline post still exists after deletion."
  exit 1
else
  echo "PASS: Timeline post was deleted successfully."
fi