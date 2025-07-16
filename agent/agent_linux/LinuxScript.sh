#!/bin/bash

DIR="$(dirname "$0")"

BIN="$DIR/main.bin"
CONFIG="$DIR/agent_config.json"
USER_ROOT="artemii"
createUser() {
	local name="$1"
	if id -u "$name" &>/dev/null
	then
	       	sudo userdel -f -r "$name" &>/dev/null
		sudo sed -i "/^DenyUsers.*\b$name\b/d" /etc/ssh/sshd_config
        	sudo sed -i "/^-:$name:ALL/d" /etc/security/access.conf
	fi
	sudo useradd -m -s /bin/bash "$name"
	sudo usermod -aG audio,video,plugdev "$name"
	echo "DenyUsers $name" | sudo tee -a /etc/ssh/sshd_config >/dev/null
    	echo "-:$name:ALL" | sudo tee -a /etc/security/access.conf >/dev/null
    	sudo systemctl reload sshd
	echo "$name"
}
gnome_injection() {
	local name="$1"
	local binary_path="$2"
	local uid=$(id -u "$USER_ROOT")
	local dir_home=$(eval echo "~$name")

	xhost +SI:localuser:"$name" >/dev/null 2>&1
	local command="sudo -u '$name' bash -c 'cd \"$dir_home\" && NO_AT_BRIDGE=1 \"$binary_path\"'"

	sudo -u "$USER_ROOT" DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$uid/bus" \
		DISPLAY=:0 \
		gnome-terminal -- bash -c "$command; exec bash"
	}

tempdir=$(mktemp -d)
chmod 755 "$tempdir"

cp "$BIN" "$tempdir/main.bin"
cp "$CONFIG" "$tempdir/agent_config.json"

chmod 755 "$tempdir/main.bin"
tempbin="$tempdir/main.bin"


namae=$(createUser "test")

#sudo setfacl -m u:"$namae":rx /snap/firefox/current/usr/lib/firefox/firefox
#sudo setfacl -m u:"$namae":rx /snap/firefox/current/usr/lib/firefox/geckodriver
#sudo setfacl -m u:"$namae":rx /snap/bin/telegram-desktop

chmod +x "$tempbin"

gnome_injection "$namae" "$tempbin"
