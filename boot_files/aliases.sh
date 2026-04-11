# =======
# Editors
# =======

alias ge='gedit'
alias mic='micro'
alias vs='code'

# ====
# Code
# ====

alias py='python3'
alias cv='python3 -m venv venv && source venv/bin/activate'
alias av='source venv/bin/activate'

# =========
# Downloads
# =========

alias get_pi_hole='curl -sSL https://install.pi-hole.net | bash'
alias get_argon='curl https://download.argon40.com/argon1.sh | bash'
alias get_sw_cli='sudo apt update && sudo apt install -y micro curl'
alias get_sw_gui='sudo apt update && sudo apt install -y gedit code'

# ======
# status
# ======

system_status() {
    echo -e "\n\033[1;33m--- SYSTEM MONITOR ---\033[0m"    
    if [ -f /sys/class/thermal/thermal_zone0/temp ]; then
        local temp=$(cat /sys/class/thermal/thermal_zone0/temp)
        echo -e "Temperature: $((temp/1000))°C"
    fi
    echo -e "CPU Load:    $(uptime | awk -F'load average:' '{ print $2 }' | cut -d, -f1)"
    echo -e "RAM Usage:   $(free -m | awk '/Mem:/ { printf "%dMB / %dMB (%.2f%%)\n", $3, $2, $3*100/$2 }')"
    echo -e "\033[1;33m----------------------\033[0m\n"
}
alias status='system_status'