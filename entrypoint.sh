#!/usr/bin/env bash

if [ "${1}" == "bash" ]; then
    bash
elif [ "${1}" == "tail" ]; then
    ${*}
else
    python3 ${1}
fi
