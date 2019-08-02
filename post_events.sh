#!/bin/sh

curl -X POST \
  http://54.196.4.13:9966/v1/DebugEvents \
  -H ': ' \
  -H 'Content-Type: application/json' \
  -H 'I-Twilio-Role: flex' \
  -H 'cache-control: no-cache' \
  -d '{
    "account_sid": "AC4f9e27551dbee0bb83834ae41255cc9e",
    "correlation_sid": "FT31efa6d50eb3e3e152ac1a49778b77fd",
    "resource_sid" :  "FN3c92882bda4e562ec5d3b32c97a8f0b2",
    "level": "ERROR",
    "code": 45002,
    "message": "Custom message",
    "product_name": "flex"
}
'
