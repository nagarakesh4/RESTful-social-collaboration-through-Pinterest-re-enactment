#!/bin/bash
#
# test client access to our service

echo -e "\n deleting selected board"

curl -X DELETE http://localhost:8080/v1/user/user1/board/board5

