#!/bin/bash
FLAGS=(
	--onefile
	--include-data-files=agent_config.json=agent_config.json
)
python -m nuitka "${FLAGS[@]}" "$1"
if [ $? -eq 0 ]; then
	echo -e "Compiled!"
else
	echo -e "Error!"
fi
