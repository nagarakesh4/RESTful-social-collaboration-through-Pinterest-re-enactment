#!/bin/bash
#
# test client access to our service

echo -e "\n getting all boards"

curl -X GET http://localhost:8080/v1/boards
