# ultra_instinct_core.py

import subprocess
import os # Already imported, but good to ensure it's seen for os.path.isfile, os.path.getsize
from datetime import datetime # Already imported

# === CUSTOM EXCEPTION === #
class ToolError(Exception):
    """Custom exception for tool execution errors."""
    pass

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
    "xsstrike": "tools/XSStrike/xsstrike.py",
    "secretfinder": "tools/SecretFinder/SecretFinder.py"
}

# === HELPER FUNCTIONS === #
def run_command(command, output_file=None):
    print(f"[+] Running: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            error_message = f"[-] Command '{command}' failed with return code {result.returncode}.\n"
            error_message += f"[-] Stderr: {result.stderr.strip()}"
            print(error_message)
            raise ToolError(f"Command '{command}' failed.")

        if output_file:
            with open(output_file, "w") as f:
                f.write(result.stdout)
        # Optionally print stderr even on success if it contains warnings
        if result.stderr:
            print(f"[stderr (warnings/info)]: {result.stderr.strip()}")
        return result.stdout
    except FileNotFoundError as e:
        print(f"[-] Error: Command not found or path incorrect for '{command}'. {e}")
        raise ToolError(f"Command not found for '{command}'.")
    except Exception as e: # Catch other potential errors during subprocess.run
        print(f"[-] An unexpected error occurred while running '{command}': {e}")
        raise ToolError(f"Unexpected error for '{command}': {e}")


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


# === MODULES === #
def run_subfinder(domain):
    output = os.path.join(OUTPUT_DIR, "subdomains.txt")
    cmd = f"{TOOLS_PATH['subfinder']} -d {domain} -silent"
    return run_command(cmd, output)


def run_httpx():
    input_file = os.path.join(OUTPUT_DIR, "subdomains.txt")
    if not os.path.isfile(input_file) or os.path.getsize(input_file) == 0:
        print(f"[-] Input file for Httpx not found or is empty: {input_file}")
        return "SKIPPED"
    output = os.path.join(OUTPUT_DIR, "live_hosts.txt")
    cmd = f"{TOOLS_PATH['httpx']} -l {input_file} -ports 80,443,8080,8000,8888 -threads 200 -silent -o {output}"
    run_command(cmd, output)
    return "Success"


def run_nuclei():
    input_file = os.path.join(OUTPUT_DIR, "subdomains.txt")
    if not os.path.isfile(input_file) or os.path.getsize(input_file) == 0:
        print(f"[-] Input file for Nuclei not found or is empty: {input_file}")
        return "SKIPPED"

    output = os.path.join(OUTPUT_DIR, "nuclei_results.txt")
    cmd = f"{TOOLS_PATH['nuclei']} -l {input_file} -o {output}"
    run_command(cmd, output)
    return "Success"


def run_waybackurls():
    input_file = os.path.join(OUTPUT_DIR, "subdomains.txt")
    if not os.path.isfile(input_file) or os.path.getsize(input_file) == 0:
        print(f"[-] Input file for Waybackurls not found or is empty: {input_file}")
        return "SKIPPED"
    output = os.path.join(OUTPUT_DIR, "waybackurls.txt")
    cmd = f"cat {input_file} | {TOOLS_PATH['waybackurls']} > {output}"
    run_command(cmd) # Output is redirected, so stdout to file is not needed from run_command
    return "Success"


def run_gf_patterns():
    input_file = os.path.join(OUTPUT_DIR, "waybackurls.txt")
    if not os.path.isfile(input_file) or os.path.getsize(input_file) == 0:
        print(f"[-] Input file for GF patterns not found or is empty: {input_file}")
        return "SKIPPED"
    patterns = ["xss", "sqli", "redirect"]
    for pattern in patterns:
        output = os.path.join(OUTPUT_DIR, f"gf_{pattern}.txt")
        cmd = f"cat {input_file} | {TOOLS_PATH['gf']} {pattern} > {output}"
        run_command(cmd) # Output is redirected
    return "Success"


def run_sqlmap():
    input_file = os.path.join(OUTPUT_DIR, "gf_sqli.txt")
    if not os.path.isfile(input_file) or os.path.getsize(input_file) == 0:
        print(f"[-] Input file for SQLMap not found or is empty: {input_file}")
        return "SKIPPED"
    with open(input_file) as f:
        urls = f.readlines()
    if not urls:
        print(f"[-] No URLs found in {input_file} for SQLMap.")
        return "SKIPPED"
    for i, url in enumerate(urls):
        output = os.path.join(OUTPUT_DIR, f"sqlmap_{i}.txt")
        cmd = f"{TOOLS_PATH['sqlmap']} -u \"{url.strip()}\" --batch --level=2 --risk=2"
        run_command(cmd, output)
    return "Success"


def run_xsstrike():
    input_file = os.path.join(OUTPUT_DIR, "gf_xss.txt")
    if not os.path.isfile(input_file) or os.path.getsize(input_file) == 0:
        print(f"[-] Input file for XSStrike not found or is empty: {input_file}")
        return "SKIPPED"
    with open(input_file) as f:
        urls = f.readlines()
    if not urls:
        print(f"[-] No URLs found in {input_file} for XSStrike.")
        return "SKIPPED"
    for i, url in enumerate(urls):
        output = os.path.join(OUTPUT_DIR, f"xsstrike_{i}.txt")
        cmd = f"python3 {TOOLS_PATH['xsstrike']} -u \"{url.strip()}\" --crawl --fuzzer"
        run_command(cmd, output)
    return "Success"


def run_secretfinder():
    input_file = os.path.join(OUTPUT_DIR, "gf_redirect.txt")
    if not os.path.isfile(input_file) or os.path.getsize(input_file) == 0:
        print(f"[-] Input file for SecretFinder not found or is empty: {input_file}")
        return "SKIPPED"
    with open(input_file) as f:
        urls = f.readlines()
    if not urls:
        print(f"[-] No URLs found in {input_file} for SecretFinder.")
        return "SKIPPED"
    for i, url in enumerate(urls):
        output = os.path.join(OUTPUT_DIR, f"secretfinder_{i}.txt")
        cmd = f"python3 {TOOLS_PATH['secretfinder']} -i \"{url.strip()}\" -o cli"
        run_command(cmd, output)
    return "Success"


# === MAIN EXECUTION === #
def main():
    ensure_output_dir()
    tool_statuses = {}

    print("\n=== ULTRA INSTINCT AI AGENT INITIATED ===")
    print(f"Target: {TARGET}\n")

    try:
        print("[1] Running Subfinder...")
        run_subfinder(TARGET) # Assuming run_subfinder calls run_command which can raise ToolError
        tool_statuses["Subfinder"] = "Success"
    except ToolError as e:
        print(f"[-] Subfinder failed: {e}. Continuing with next tool.")
        tool_statuses["Subfinder"] = "Failed"

    try:
        print("[2] Probing with Httpx...")
        result = run_httpx()
        if result == "SKIPPED":
            tool_statuses["Httpx"] = "Skipped"
            print("[-] Httpx was skipped due to missing input.")
        else:
            tool_statuses["Httpx"] = "Success"
    except ToolError as e:
        print(f"[-] Httpx failed: {e}. Continuing with next tool.")
        tool_statuses["Httpx"] = "Failed"

    try:
        print("[3] Running Nuclei for Vulnerabilities...")
        result = run_nuclei()
        if result == "SKIPPED":
            tool_statuses["Nuclei"] = "Skipped"
            # Message already printed by run_nuclei
        else:
            tool_statuses["Nuclei"] = "Success"
    except ToolError as e:
        print(f"[-] Nuclei failed: {e}. Continuing with next tool.")
        tool_statuses["Nuclei"] = "Failed"

    try:
        print("[4] Collecting URLs with Waybackurls...")
        result = run_waybackurls()
        if result == "SKIPPED":
            tool_statuses["Waybackurls"] = "Skipped"
            print("[-] Waybackurls was skipped due to missing input.")
        else:
            tool_statuses["Waybackurls"] = "Success"
    except ToolError as e:
        print(f"[-] Waybackurls failed: {e}. Continuing with next tool.")
        tool_statuses["Waybackurls"] = "Failed"

    try:
        print("[5] Running GF Patterns for Vulnerable Params...")
        result = run_gf_patterns()
        if result == "SKIPPED":
            tool_statuses["GF Patterns"] = "Skipped"
            # Message already printed by run_gf_patterns
        else:
            tool_statuses["GF Patterns"] = "Success"
    except ToolError as e:
        print(f"[-] GF Patterns failed: {e}. Continuing with next tool.")
        tool_statuses["GF Patterns"] = "Failed"

    try:
        print("[6] Running SQLMap on GF filtered URLs...")
        result = run_sqlmap()
        if result == "SKIPPED":
            tool_statuses["SQLMap"] = "Skipped"
            # Message already printed by run_sqlmap or it prints no URLs
        else:
            tool_statuses["SQLMap"] = "Success"
    except ToolError as e:
        print(f"[-] SQLMap failed: {e}. Continuing with next tool.")
        tool_statuses["SQLMap"] = "Failed"

    try:
        print("[7] Running XSStrike on GF filtered URLs...")
        result = run_xsstrike()
        if result == "SKIPPED":
            tool_statuses["XSStrike"] = "Skipped"
            # Message already printed by run_xsstrike
        else:
            tool_statuses["XSStrike"] = "Success"
    except ToolError as e:
        print(f"[-] XSStrike failed: {e}. Continuing with next tool.")
        tool_statuses["XSStrike"] = "Failed"

    try:
        print("[8] Running SecretFinder on Redirect URLs...")
        result = run_secretfinder()
        if result == "SKIPPED":
            tool_statuses["SecretFinder"] = "Skipped"
            # Message already printed by run_secretfinder
        else:
            tool_statuses["SecretFinder"] = "Success"
    except ToolError as e:
        print(f"[-] SecretFinder failed: {e}. Continuing with next tool.")
        tool_statuses["SecretFinder"] = "Failed"

    print("\n\n=== SCAN SUMMARY ===")
    if not tool_statuses:
        print("No tools were run.")
    else:
        for tool, status in tool_statuses.items():
            print(f"- {tool}: {status}")

    print(f"\n[+] Full scan attempt finished. Results stored in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()