# /bin/bash
IP=$1

RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

info() {
    printf "\n\n${BLUE}[*] $1${NC}\n\n"
}

mkdir scan

#
# NMAP scan for top ports
#
info "Scanning top 100 ports"
sudo nmap --top-ports 100 -oA scan/scantop $IP

#
# NMAP detail scan for top ports
#
TOP_PORTS=$(grep -o "^[0-9]*" scan/scantop.nmap | tr "\n" "," | sed 's/.$//')
info "Detailed scanning of top ports: $TOP_PORTS"
sudo nmap -sC -sV -p $TOP_PORTS -oA scan/scantopdetail $IP

#
# Look for known vulnerabilities using searchsploit
#
info "Running searchspoit"
searchsploit --nmap scan/scantopdetail.xml --exclude="apache"


#
# NMAP full TCP scan
#
info "Scanning the whole TCP port range"
nmap -p- -v -Pn -oA scan/scanall $IP | grep -e "Stats" -e "Timing" -e "Discovered"
PORTS=$(grep -o "^[0-9]*" scan/scanall.nmap | tr "\n" "," | sed 's/.$//')
printf "\nDetails in scan/scanall.nmap"

# Print result
info "All found open ports: $PORTS"

