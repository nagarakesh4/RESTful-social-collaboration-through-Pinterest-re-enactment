#!/bin/bash
#
# test client access to our service

echo -e "\n to retrieve user info"

curl -X GET http://localhost:8080/v1/user/user2
