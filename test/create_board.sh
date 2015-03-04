#!/bin/bash
#
# test client access to our service

echo -e "\n creating a board "

#edit the "user1" with the user of your choice to create a board  

curl -H "Content-Type: application/json" -X POST -d '{"boardname":"map"}' http://localhost:8080/v1/user/user1/board

