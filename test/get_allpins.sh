#!/bin/bash
#
# test client access to our service

echo -e "\n getting all pins "

curl -X GET http://localhost:8080/v1/pins

