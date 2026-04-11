#!/bin/bash

# =========================================================
# This script completely deletes the Wi-Fi hotspot connection
# =========================================================

echo "Deleting the 'Hotspot' Wi-Fi connection..."
echo "Running command: sudo nmcli connection delete id Hotspot"
sudo nmcli connection delete id Hotspot

if [ $? -eq 0 ]; then
    echo "Success! The hotspot configuration has been deleted."
else
    echo "Failed to delete the hotspot. (It may not exist)"
fi
