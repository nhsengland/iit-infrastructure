#!/bin/sh

curl --data "{}" http://localhost/api/action/send_email_notifications --header "Authorization: {{ ADMIN_API_KEY }}"
