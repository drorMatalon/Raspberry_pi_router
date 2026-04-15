# ====================
# DEFINES_AND_IMPORTS
# ====================
import subprocess
import re
import sys

VALID_INF = ["wlan0", "wlan1", "eth0"]

# =====================
# FUNCTIONS_AND_CLASSES
# =====================

def run_command(command):
    try:
        result = subprocess.run(
            command.split(), 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )
        return result.stdout
    except Exception as e:
        print(f"Error running command '{command}': {e}")
        return ""

def get_channel(interface="wlan0"):
    output = run_command(f"iw dev {interface} info")
    match = re.search(r"channel\s+(\d+)", output)
    if match:
        return match.group(1)
    return "Unknown"

def parse_protocol(bitrate_str):
    if "HE" in bitrate_str:
        return "802.11ax (Wi-Fi 6)"
    elif "VHT" in bitrate_str:
        return "802.11ac (Wi-Fi 5)"
    elif "HT" in bitrate_str:
        return "802.11n (Wi-Fi 4)"
    elif "MCS" in bitrate_str:
        return "802.11n (Wi-Fi 4)"
    else:
        return "802.11a/b/g (Legacy)"

def parse_bandwidth(bitrate_str):
    match = re.search(r"(\d+)MHz", bitrate_str)
    if match:
        return match.group(1) + " MHz"
    return "20 MHz (Default)"

def get_connected_users(interface="wlan0"):
    channel = get_channel(interface)
    output = run_command(f"iw dev {interface} station dump")
    
    stations = []
    current_station = None
    
    for line in output.split('\n'):
        line = line.strip()
        if line.startswith("Station"):
            if current_station:
                stations.append(current_station)
            
            mac = line.split()[1]
            current_station = {
                "MAC": mac, 
                "Channel": channel, 
                "Protocol": "Unknown", 
                "Bandwidth": "Unknown"
            }
            
        elif line.startswith("tx bitrate:") and current_station:
            bitrate_info = line.split(":", 1)[1].strip()
            current_station["Protocol"] = parse_protocol(bitrate_info)
            current_station["Bandwidth"] = parse_bandwidth(bitrate_info)
            
    if current_station:
        stations.append(current_station)
        
    return stations

# ====
# MAIN
# ====

def main():
    if len(sys.argv) != 2:
        print("Error: Exactly one interface argument is required.")
        print("Usage: python track_users.py [interface]")
        print(f"Allowed interfaces: {', '.join(VALID_INF)}")
        sys.exit(1)
        
    interface = sys.argv[1]
    
    if interface not in VALID_INF:
        print(f"Error: Invalid interface '{interface}'.")
        print("Usage: python track_users.py [interface]")
        print(f"Allowed interfaces: {', '.join(VALID_INF)}")
        sys.exit(1)
    
    print("=================================================================")
    print(f"Tracking Connected Users on Interface: {interface}")
    print("=================================================================")
    print(f"{'MAC Address':<20} | {'Channel':<10} | {'Bandwidth':<15} | {'Protocol'}")
    print("-" * 65)
    
    users = get_connected_users(interface)
    
    if not users:
        print("No users currently connected or unable to retrieve data.")
        print("Make sure you are running with sufficient privileges (e.g., sudo) and the interface is an AP.")
    else:
        for user in users:
            print(f"{user['MAC']:<20} | {user['Channel']:<10} | {user['Bandwidth']:<15} | {user['Protocol']}")
    
    print("=================================================================")

if __name__ == "__main__":
    main()
