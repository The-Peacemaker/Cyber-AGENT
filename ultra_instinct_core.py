# ultra_instinct_core.py

import subprocess
import os
from datetime import datetime

# === CONFIGURATION === #
TARGET = "example.com"
OUTPUT_DIR = f"reports/{TARGET}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
TOOLS_PATH = {
    "subfinder": "subfinder",
    "httpx": "httpx",
    "nuclei": "nuclei",
    "gf": "gf",
    "waybackurls": "waybackurls"
}

# === HELPER FUNCTIONS === #
def run_command(command, output_file=None):
    print(f"[+] Running: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if output_file:
            with open(output_file, "w") as f:
                f.write(result.stdout)
        return result.stdout
    except Exception as e:
        print(f"[-] Error: {e}")
        return ""


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


# === MODULES === #
def run_subfinder(domain):
    output = os.path.join(OUTPUT_DIR, "subdomains.txt")
    cmd = f"{TOOLS_PATH['subfinder']} -d {domain} -silent"
    return run_command(cmd, output)


def run_httpx():
    input_file = os.path.join(OUTPUT_DIR, "subdomains.txt")
    output = os.path.join(OUTPUT_DIR, "live_hosts.txt")
    cmd = f"{TOOLS_PATH['httpx']} -l {input_file} -silent -o {output}"
    return run_command(cmd)


def run_nuclei():
    input_file = os.path.join(OUTPUT_DIR, "live_hosts.txt")
    output = os.path.join(OUTPUT_DIR, "nuclei_results.txt")
    cmd = f"{TOOLS_PATH['nuclei']} -l {input_file} -o {output}"
    return run_command(cmd)


# === MAIN EXECUTION === #
def main():
    ensure_output_dir()

    print("\n=== ULTRA INSTINCT AI AGENT INITIATED ===")
    print(f"Target: {TARGET}\n")

    print("[1] Running Subfinder...")
    run_subfinder(TARGET)

    print("[2] Probing with Httpx...")
    run_httpx()

    print("[3] Running Nuclei for Vulnerabilities...")
    run_nuclei()

    print("\n[+] Recon complete. Results stored in:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
