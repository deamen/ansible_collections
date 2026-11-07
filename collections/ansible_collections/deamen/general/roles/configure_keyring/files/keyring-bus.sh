# shellcheck shell=sh
# Deployed by deamen.general.configure_keyring
# Point CLI tools at the session bus started by keyring-unlock, once it is running.
if [ -S "/run/user/$(id -u)/bus" ]; then
    DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$(id -u)/bus"
    export DBUS_SESSION_BUS_ADDRESS
fi
