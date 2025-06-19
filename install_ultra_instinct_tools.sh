#!/bin/bash
set -e

echo "🔥 Installing Ultra Instinct Bug Hunter Dependencies..."

# Update and install essentials
sudo apt update && sudo apt install -y git python3 python3-pip figlet lolcat boxes curl jq


# Install Go tools
echo "[*] Installing Go-based tools..."
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest
go install github.com/tomnomnom/gf@latest
go install github.com/tomnomnom/waybackurls@latest

# Setup gf patterns
echo "[*] Setting up gf patterns..."
mkdir -p ~/.gf
cp -r ~/go/pkg/mod/github.com/tomnomnom/gf*/examples ~/.gf 2>/dev/null || true

# Install XSStrike
echo "[*] Installing XSStrike..."
git clone https://github.com/s0md3v/XSStrike.git tools/XSStrike || true
pip3 install -r tools/XSStrike/requirements.txt

# Install SecretFinder
echo "[*] Installing SecretFinder..."
git clone https://github.com/m4ll0k/SecretFinder.git tools/SecretFinder || true
pip3 install -r tools/SecretFinder/requirements.txt

# Install SQLMap
echo "[*] Installing SQLMap..."
sudo apt-get update && sudo apt-get install -y sqlmap

echo "✅ Ultra Instinct tools installed!"
figlet "Ready to Hunt" | lolcat
