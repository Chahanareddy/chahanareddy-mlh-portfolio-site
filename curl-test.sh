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

echo
echo "Retrieving timeline posts..."

GET_RESPONSE=$(curl -s "$BASE_URL")

echo "GET response:"
echo "$GET_RESPONSE"

echo
echo "Checking whether the new post was added..."

if echo "$GET_RESPONSE" | grep -q "$CONTENT"; then
  echo "PASS: Timeline post was added successfully."
  exit 0
else
  echo "FAIL: Timeline post was not found."
  exit 1
fi