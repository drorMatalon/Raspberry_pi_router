# =======
# Imports
# =======
import xml.etree.ElementTree as ET
import sys
import subprocess
import os

# ==================
# Parameters parsing
# ==================

def parse_xml(xml_file):
    """
    Parses the given XML file, extracts the needed configuration parameters,
    and validates them. If a parameter is missing or invalid, the script exits with an error.
    """
    params = {
        "ssid": "",
        "password": "",
        "band": "",
        "channel": "",
        "auto_connect": "",
        "source": "",
        "upstream_ssid": "",
        "upstream_password": ""
    }

    if not os.path.exists(xml_file):
        print(f"Error: Configuration file '{xml_file}' not found.")
        sys.exit(1)
        
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        sys.exit(1)

    for param in params.keys():
        element = root.find(param)
        if element is not None and element.text:
            params[param] = element.text.strip()
        else:
            if param not in ["upstream_ssid", "upstream_password"]:
                print(f"Error: Missing required parameter '{param}' in XML configuration.")
                sys.exit(1)

    # Validate band
    if params["band"] not in ["2.4", "5"]:
        print(f"Error: Invalid band '{params['band']}'. Must be '2.4' or '5'.")
        sys.exit(1)

    # Validate auto_connect
    if params["auto_connect"] not in ["yes", "no"]:
        print(f"Error: Invalid auto_connect '{params['auto_connect']}'. Must be 'yes' or 'no'.")
        sys.exit(1)

    # Validate source
    if params["source"] not in ["ethernet", "wifi"]:
        print(f"Error: Invalid source '{params['source']}'. Must be 'ethernet' or 'wifi'.")
        sys.exit(1)

    if params["source"] == "wifi":
        if not params.get("upstream_ssid") or not params.get("upstream_password"):
            print("Error: Missing 'upstream_ssid' or 'upstream_password' for wifi source.")
            sys.exit(1)


    return params
        
# ================
# Router setup
# ================

def run_nmcli_command(command_list):
    """
    Executes a shell command using subprocess and returns its output.
    If the command fails, it prints an error and exits the script.
    """
    print(f"Running command: {' '.join(command_list)}")
    try:
        result = subprocess.run(
            command_list, 
            check=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {' '.join(command_list)}")
        print(f"Details: {e.stderr.strip()}")
        sys.exit(1)

def setup_hotspot(params):
    """
    Configures the Raspberry Pi as a Wi-Fi hotspot using nmcli based on the provided parameters.
    It creates a new connection, sets its properties, and activates it.
    """

    # Parameters loading
    ssid = params["ssid"]
    password = params["password"]
    band = "bg" if params["band"] == "2.4" else "a"     # In nmcli 2.4 GHz  is 'bg', 5 GHz is 'a'
    auto_connect = params["auto_connect"]
    
    # If source is wifi, connect the external dongle (wlan1) to the upstream network
    if params["source"] == "wifi":
        upstream_ssid = params["upstream_ssid"]
        upstream_password = params["upstream_password"]
        print(f"Connecting wlan1 to upstream network '{upstream_ssid}'...")
        run_nmcli_command([
            "nmcli", "device", "wifi", "connect", upstream_ssid, 
            "password", upstream_password, "ifname", "wlan1"
        ])
        print("Connected to upstream network.")

    print(f"Setting up hotspot '{ssid}'...")
    con_name = "Hotspot"

    # Step 1: Check if a connection with this name already exists and delete it if so
    print("Cleaning up old configurations...")
    delete_cmd = ["nmcli", "connection", "delete", "id", con_name]
    print(f"Running command: {' '.join(delete_cmd)}")
    subprocess.run(
        delete_cmd, 
        stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL
    )
    
    # Step 2: Create a new Wi-Fi hotspot connection
    print("Creating the new hotspot connection...")
    run_nmcli_command([
        "nmcli", "connection", "add", 
        "type", "wifi", 
        "ifname", "wlan0", 
        "con-name", con_name,
        "autoconnect", auto_connect, 
        "ssid", ssid
    ])

    # Step 3: Configure it as an Access Point (hotspot)
    print(f"Configuring connection as Access Point on band {params['band']}GHz...")
    
    # Base modify commands
    modify_cmd = [
        "nmcli", "connection", "modify", con_name, 
        "802-11-wireless.mode", "ap", 
        "802-11-wireless.band", band, 
        "ipv4.method", "shared"
    ]
    
    # Append the channel if it's explicitly set (not 'auto')
    if params["channel"].lower() != "auto":
        modify_cmd.extend(["802-11-wireless.channel", params["channel"]])
        print(f"Setting specific channel: {params['channel']}")
        
    run_nmcli_command(modify_cmd)

    # Step 4: Set the Wi-Fi security protocol and password
    print("Setting Wi-Fi password...")
    run_nmcli_command([
        "nmcli", "connection", "modify", con_name, 
        "wifi-sec.key-mgmt", "wpa-psk", 
        "wifi-sec.psk", password
    ])

    # Step 5: Activate the connection
    print("Activating the hotspot...")
    run_nmcli_command(["nmcli", "connection", "up", con_name])
    
    print(f"\nSuccess! Hotspot '{ssid}' successfully created and activated as a router.")

def main():
    """
    Main execution flow: determines the XML path, parses it, and sets up the router.
    """
    xml_file_path = "hotspot_config.xml"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_xml_path = os.path.join(script_dir, xml_file_path)
    
    print(f"Reading configuration from {full_xml_path}...")
    params = parse_xml(full_xml_path)
    
    setup_hotspot(params)

if __name__ == '__main__':
    main()