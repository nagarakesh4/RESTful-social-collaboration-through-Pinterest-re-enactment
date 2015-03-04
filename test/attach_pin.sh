#!/bin/bash
#
# test client access to our service

echo -e "\n attaching a pin to a board"
#edit the "pinid value,user1 and board4" to add pin in the 'user and board' of your choice.

curl -H "Content-Type: application/json" -X PUT -d '{"pinid":"pin1"}' http://localhost:8080/v1/user/user1/board/board4

