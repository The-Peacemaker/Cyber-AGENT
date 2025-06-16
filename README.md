

# 🧠💥 Ultra Instinct - Automated AI Recon & Vulnerability Hunter

> “When logic is too slow, instincts take over.” — Built by **The-Peacemaker**

**Ultra Instinct** is an elite-level, fully automated AI-powered vulnerability hunting framework. It combines the most powerful open-source hacking tools into a single unstoppable recon and exploitation machine. You give it a domain — it hunts, finds, reports. Like a true bug bounty sensei.

---
🚀 Workflow Blueprint (Auto Recon + Vuln Hunting Agent)
```
[Target Input]
      ↓
[Recon & Enum (Subfinder, httpx, gau)]
      ↓
[Param Discovery (waybackurls, gf, paramspider)]
      ↓
[Run Scanners (nuclei, XSStrike, SQLMap, SecretFinder)]
      ↓
[Analyze Output with AI Agent]
      ↓
[Generate Summary Report (markdown/pdf)]
      ↓
[Store to Notes App or Folder]

```

INDEX
```
ultra-instinct-ai-agent/
├── agent_core.py
├── recon_tools/
│   ├── subfinder_runner.py
│   └── nuclei_runner.py
├── report_writer/
│   └── ai_writer.py
├── templates/
│   └── report_template.md
└── main.py

```

## ⚔️ Features

- 🌐 Subdomain Enumeration with **Subfinder**
- 🔎 Live Host Probing using **HTTPX**
- 🧨 Vulnerability Detection with **Nuclei**
- 🕵️ Historical URL Extraction via **WaybackURLs**
- 🎯 Param Hunting using **GF** Patterns
- 🔥 SQL Injection Detection using **SQLMap**
- ⚡ XSS Exploitation with **XSStrike**
- 🧬 Secret and Token Discovery via **SecretFinder**
- 📁 Clean, Timestamped Report Folders

---

## 🔗 Tools Powered By

- [Subfinder](https://github.com/projectdiscovery/subfinder)
- [HTTPX](https://github.com/projectdiscovery/httpx)
- [Nuclei](https://github.com/projectdiscovery/nuclei)
- [WaybackURLs](https://github.com/tomnomnom/waybackurls)
- [GF](https://github.com/tomnomnom/gf)
- [SQLMap](https://github.com/sqlmapproject/sqlmap)
- [XSStrike](https://github.com/s0md3v/XSStrike)
- [SecretFinder](https://github.com/m4ll0k/SecretFinder)

---

## ⚙️ How to Use

### 1. Clone the Beast
```
git clone https://github.com/The-Peacemaker/ultra-instinct
cd ultra-instinct

```
### 2. Install The Tools
```
./install_ultra_instinct_tools.sh
```
### 3. TO RUN
```
run_ultra_instinct.sh
```

```
Check the reports/ folder for everything:

markdown
Copy
Edit
reports/
 └── example.com_20250616_123456/
     ├── subdomains.txt
     ├── live_hosts.txt
     ├── nuclei_results.txt
     ├── waybackurls.txt
     ├── gf_xss.txt
     ├── sqlmap_*.txt
     └── ...
```
### UPCOMING FEATURES
```
🔐 Burp Suite API Integration

🧠 AI-based Report Summarization

📊 PDF Reports with Risk Score

☁️ Cloud Storage + Telegram/Slack Alerts

🧬 Agent Mode for Continuous Recon
```

### 👑 Author
The-Peacemaker
Cybersecurity researcher • Bug bounty hunter 
GitHub: @The-Peacemaker
