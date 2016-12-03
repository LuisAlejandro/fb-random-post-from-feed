#!/bin/bash

PATH="/bin:/usr/bin:/usr/sbin"

curl --insecure --location --silent --fail "http://${OPENSHIFT_APP_DNS}/" >/dev/null