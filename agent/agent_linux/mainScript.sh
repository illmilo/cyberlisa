#!/bin/bash

DIR="$(dirname "$0")"
chmod +x "$DIR/nuitkaScript.sh"
chmod +x "$DIR/LinuxScript.sh"

"$DIR/nuitkaScript.sh" main.py && "$DIR/LinuxScript.sh"
