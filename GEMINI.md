# Project: Raspberry Pi Router & Network Management

This project configures a Raspberry Pi as a functional network router and security hub. It includes tools for managing a Wi-Fi hotspot, DNS filtering with Pi-hole, and general network monitoring.

## Core Guides & Documentation
- **Network Fundamentals:** ./background.txt (IP, DHCP, DNS, WiFi Bands/Channels, NetworkManager basics)
- **Pi-hole Setup:** ./pi_hole_set_up.txt (Installation, Static IP, Port 53 conflicts, Admin Webpage)
- **Router & OS Setup:** ./router_set_up.txt (OS Image, SSH, Hotspot control overview, Monitoring commands)
- **Linux CLI Guide:** ./gemini_cli_tool_linux.txt (Gemini CLI installation, usage, and extensions on Linux)

## Automation Scripts
- **Hotspot Activation:** ./scripts/activate_hotspot.py (Python/nmcli automation)
- **Hotspot Deactivation:** ./scripts/delete_hotspot.sh (Cleanup script)
- **Configuration:** ./scripts/hotspot_config.xml (SSID, Password, Band, and Upstream settings)
- **Boot Environment:** ./boot_files/ contains bash environment customizations (aliases, bashrc)

## Project Context
- **Hotspot Control:** Use the scripts in ./scripts/ to manage the Access Point. Configuration is handled via the XML file.
- **Environment:** Primarily Linux-based (Raspberry Pi OS Lite), utilizing 'nmcli' for most network operations.

## File Opening Preferences
- **All Files:** Use micro (no specific path required)

## General Preferences
- When the user asks you to show content, prefer using the editors list in this file rether then cat, echo etc ...
- When using toold open them with the tool path. Espessially, when calling python, use the path listed here.
- Use friendly response style, when explaining complex material use simple examples
- If have doubts, prefer ask for clarification over guessing

## Code Preferences
- Prefer Python 3.14 syntax
- Add minimal necessary comments only
- Use human-like readable syntax (avoid overly compact one-liners)
- Prefer readable and maintainable code over micro-optimizations

## Python Code Structure Convention
- When generating Python code, organize the file using section headers
- Common sections:
  - DEFINES_AND_IMPORTS
  - FUNCTIONS_AND_CLASSES
  - MAIN
- Use clear titled separators in the following format:
  # ============
  # SECTION_NAME
  # ============
- For runnable Python scripts:
  - Define a main() function
  - Use the standard entry point guard:
    if __name__ == "__main__":
        main()
- Avoid placing executable logic outside of main() in runnable scripts