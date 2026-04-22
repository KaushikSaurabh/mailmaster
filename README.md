# MailMaster 📧

A unified tool for high-performance email database management and bulk delivery. This project wraps advanced validation, spam scanning, and mailing engines into a simple interface.

## 🚀 Features
- **Excel Processing:** Automatically extract emails from `.xlsx` files and output cleaned versions.
- **Smart Validation:** Removes dangerous trap emails, administrative addresses, and security-firm hosted accounts.
- **Spam Scanning:** Analyze your email templates for spam scores using AI-powered detection (phishing, toxicity, and Bayesian filters).
- **Bulk Delivery:** Multithreaded SMTP mailer with advanced obfuscation to bypass spam filters.
- **SMTP Verification:** Validates your SMTP credentials before you start a campaign.

## 🛠️ Installation
1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install pandas openpyxl psutil requests dnspython IP2Location pyarrow
   ```

## 📖 Usage
Use the master entry point `mailmaster.py`:

**1. Clean your Excel list:**
```bash
python mailmaster.py validate "your_database.xlsx"
```

**2. Scan your Email Template for Spam Score:**
*The engine will automatically download on its first run.*
```bash
python mailmaster.py scan "template.html"
```

**3. Check SMTPs:**
```bash
python mailmaster.py check-smtp "smtps.txt"
```

**4. Run Campaign:**
```bash
python mailmaster.py send
```

## ⚖️ Credits
This tool utilizes powerful core modules developed by:
- **[aels](https://github.com/aels)**: Validation Engine, Mailing Engine, and SMTP Checker.
- **[Forward Email (SpamScanner)](https://github.com/spamscanner/spamscanner)**: AI-powered Spam Scanning engine.

## ⚠️ Legal Notice
For educational purposes only. Do not use for illegal activities or spamming without consent.
