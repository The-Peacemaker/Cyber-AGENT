#!/bin/bash

echo "🧠 Activating Ultra Instinct AI Agent..."
figlet "Ultra Instinct" | lolcat

# Check Python file exists
SCRIPT="ultra_instinct_core.py"
if [ ! -f "$SCRIPT" ]; then
    echo "❌ Error: $SCRIPT not found in the current directory!"
    exit 1
fi

# Optional: let user enter target
read -p "🌐 Enter your target domain (e.g., example.com): " target
sed -i "s/^TARGET = .*/TARGET = \"$target\"/" "$SCRIPT"

# Run the agent
echo "🚀 Running the scan on $target..."
python3 "$SCRIPT"

echo "🎯 Scan completed. Check your reports folder."
