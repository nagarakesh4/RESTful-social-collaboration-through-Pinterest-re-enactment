#!/bin/bash
#
# test client access to our service

echo -e "\n uploading a pin"

#edit the "pinurl and user1" of your choice to add pins from that url to respective user

curl -H "Content-Type: application/json" -X POST -d '{"pinurl":"/home/rakesh/Desktop/app/project/v3/img/google_img.jpg"}' http://localhost:8080/v1/user/user1/pin/upload

