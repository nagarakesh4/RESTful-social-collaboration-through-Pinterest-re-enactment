#!/bin/bash
#
# test client access to our service

echo -e "\n to retrieve details of a pin"

curl -X GET http://localhost:8080/v1/pin/pin4

