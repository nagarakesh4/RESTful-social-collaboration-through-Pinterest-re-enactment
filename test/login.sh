#!/bin/bash
#
# test client access to our service

echo -e "\n logging into into userdb"
#edit the "username and Password" of your choice to login as different users

curl -H "content-Type: application/json" -d '{"username":"san","password":"jose"}' -X POST http://localhost:8080/v1/login

