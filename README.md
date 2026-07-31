
# 🔍 DNS Lookup Tool

A command-line DNS lookup tool written in Python using the `dnspython` library.

## ✨ Features

- Supports **8 record types** : A, AAAA, MX, NS, TXT, CNAME, SOA, PTR
- **Interactive mode** for easy exploration of multiple record types
- **Command-line mode** for quick lookups and scripting
- Reverse DNS lookup (PTR) to resolve IP addresses to domain names
- Graceful error handling (timeout, non-existent domains, etc.)

## 🚀 Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/dns-lookup.git
cd dns-lookup

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

python dns_lookup.py
