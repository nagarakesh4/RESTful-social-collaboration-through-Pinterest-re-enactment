#!/bin/bash
#
# test client access to our service

echo -e "\n creating a user in userdb"
#edit the "name,username and Password" of your choice to add different users
curl -i -H "Content-Type: application/json" -X POST -d '{"name":"robert","username":"san","password":"jose"}' http://localhost:8080/v1/reg

