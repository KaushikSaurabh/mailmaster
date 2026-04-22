# MailMaster 📧

A unified tool for high-performance email database management and bulk delivery. This project wraps advanced validation, spam scanning, and mailing engines into a simple interface with robust Excel support.

## 🚀 Features
- **Multi-Sheet Excel Processing:** Automatically extract emails from **all worksheets** in an `.xlsx` file. It preserves all original data and tracks the source sheet for every row.
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
Processes all sheets and generates SAFE/DANGEROUS Excel files + a CLEAN `.txt` list for the mailer.
```bash
python mailmaster.py validate "your_database.xlsx"
```

**2. Configure your campaign:**
Link your validated SMTPs and cleaned text list to the mailer.
```bash
python mailmaster.py setup --smtps "validated_smtps.txt" --leads "your_database_CLEAN_LIST.txt"
```

**3. Scan your Email Template for Spam Score:**
```bash
python mailmaster.py scan "template.html"
```

**4. Check SMTPs:**
```bash
python mailmaster.py check-smtp "smtps.txt"
```

**5. Run Campaign:**
```bash
python mailmaster.py send
```

## ⚖️ Credits
This tool utilizes powerful core modules developed by:
- **[aels](https://github.com/aels)**: Validation Engine, Mailing Engine, and SMTP Checker.
- **[Forward Email (SpamScanner)](https://github.com/spamscanner/spamscanner)**: AI-powered Spam Scanning engine.

## ⚠️ Legal Notice
For educational purposes only. Do not use for illegal activities or spamming without consent.
