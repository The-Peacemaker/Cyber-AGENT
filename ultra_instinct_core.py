# ultra_instinct_core.py

import subprocess
import os
from datetime import datetime

# === CONFIGURATION === #
TARGET = "mastercard.com"
OUTPUT_DIR = f"reports/{TARGET}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
TOOLS_PATH = {
    "subfinder": "subfinder",
    "httpx": "httpx",  # switched back to httpx CLI
    "nuclei": "nuclei",
    "gf": "gf",
    "waybackurls": "waybackurls",
    "sqlmap": "sqlmap",
    "xsstrike": "xsstrike",
    "secretfinder": "SecretFinder.py"
}

# === HELPER FUNCTIONS === #
def run_command(command, output_file=None):
    print(f"[+] Running: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if output_file:
            with open(output_file, "w") as f:
                f.write(result.stdout)
        if result.stderr:
            print(f"[stderr] {result.stderr}")
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


#def run_httpx():
#    input_file = os.path.join(OUTPUT_DIR, "subdomains.txt")
#   output = os.path.join(OUTPUT_DIR, "live_hosts.txt")
#    cmd = f"{TOOLS_PATH['httpx']} -l {input_file} -ports 80,443,8080,8000,8888 -threads 200 -silent -o {output}"
#    return run_command(cmd, output)


def run_nuclei():
    input_file = os.path.join(OUTPUT_DIR, "subdomains.txt")
    output = os.path.join(OUTPUT_DIR, "nuclei_results.txt")
    cmd = f"{TOOLS_PATH['nuclei']} -l {input_file} -o {output}"
    return run_command(cmd, output)


def run_waybackurls():
    input_file = os.path.join(OUTPUT_DIR, "subdomains.txt")
    output = os.path.join(OUTPUT_DIR, "waybackurls.txt")
    cmd = f"cat {input_file} | {TOOLS_PATH['waybackurls']} > {output}"
    return run_command(cmd)


def run_gf_patterns():
    input_file = os.path.join(OUTPUT_DIR, "waybackurls.txt")
    patterns = ["xss", "sqli", "redirect"]
    for pattern in patterns:
        output = os.path.join(OUTPUT_DIR, f"gf_{pattern}.txt")
        cmd = f"cat {input_file} | {TOOLS_PATH['gf']} {pattern} > {output}"
        run_command(cmd)


def run_sqlmap():
    input_file = os.path.join(OUTPUT_DIR, "gf_sqli.txt")
    if not os.path.isfile(input_file):
        return
    with open(input_file) as f:
        urls = f.readlines()
    for i, url in enumerate(urls):
        output = os.path.join(OUTPUT_DIR, f"sqlmap_{i}.txt")
        cmd = f"{TOOLS_PATH['sqlmap']} -u \"{url.strip()}\" --batch --level=2 --risk=2"
        run_command(cmd, output)


def run_xsstrike():
    input_file = os.path.join(OUTPUT_DIR, "gf_xss.txt")
    if not os.path.isfile(input_file):
        return
    with open(input_file) as f:
        urls = f.readlines()
    for i, url in enumerate(urls):
        output = os.path.join(OUTPUT_DIR, f"xsstrike_{i}.txt")
        cmd = f"python3 {TOOLS_PATH['xsstrike']} -u \"{url.strip()}\" --crawl --fuzzer"
        run_command(cmd, output)


def run_secretfinder():
    input_file = os.path.join(OUTPUT_DIR, "gf_redirect.txt")
    if not os.path.isfile(input_file):
        return
    with open(input_file) as f:
        urls = f.readlines()
    for i, url in enumerate(urls):
        output = os.path.join(OUTPUT_DIR, f"secretfinder_{i}.txt")
        cmd = f"python3 {TOOLS_PATH['secretfinder']} -i \"{url.strip()}\" -o cli"
        run_command(cmd, output)


# === MAIN EXECUTION === #
def main():
    ensure_output_dir()

    print("\n=== ULTRA INSTINCT AI AGENT INITIATED ===")
    print(f"Target: {TARGET}\n")

    print("[1] Running Subfinder...")
    run_subfinder(TARGET)

   # print("[2] Probing with Httpx...")
   # run_httpx()

    print("[3] Running Nuclei for Vulnerabilities...")
    run_nuclei()

    print("[4] Collecting URLs with Waybackurls...")
    run_waybackurls()

    print("[5] Running GF Patterns for Vulnerable Params...")
    run_gf_patterns()

    print("[6] Running SQLMap on GF filtered URLs...")
    run_sqlmap()

    print("[7] Running XSStrike on GF filtered URLs...")
    run_xsstrike()

    print("[8] Running SecretFinder on Redirect URLs...")
    run_secretfinder()

    print("\n[+] Full scan complete. Results stored in:", OUTPUT_DIR)


if __name__ == "__main__":
    main()