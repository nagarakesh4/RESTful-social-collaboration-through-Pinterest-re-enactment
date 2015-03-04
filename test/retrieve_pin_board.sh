#!/bin/bash
#
# test client access to our service

echo -e "\n to retrieve pins from a board"

curl -X GET http://localhost:8080/v1/boards/board4

