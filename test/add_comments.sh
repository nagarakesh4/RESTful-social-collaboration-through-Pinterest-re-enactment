#!/bin/bash
#
# test client access to our service

echo -e "\n to add comments for a pin"
#edit the "comment" input of your choice to add different users
curl -H "Content-Type: application/json" -X POST -d '{"comment":"i am google"}' http://localhost:8080/v1/user/user4/pin/pin4/comment

