#!/bin/bash

DIR_PATH="$(dirname "$(realpath "$0")")"
sudo find "$DIR_PATH" -name "near*20*"  -exec echo "{}" \;