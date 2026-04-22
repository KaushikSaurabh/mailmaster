# MailMaster 📧

A unified tool for high-performance email database management and bulk delivery. This project wraps advanced validation and mailing engines into a simple Excel-compatible interface.

## 🚀 Features
- **Excel Processing:** Automatically extract emails from `.xlsx` files and output cleaned versions.
- **Smart Validation:** Removes dangerous trap emails, administrative addresses, and security-firm hosted accounts.
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

**2. Check SMTPs:**
```bash
python mailmaster.py check-smtp "smtps.txt"
```

**3. Run Campaign:**
```bash
python mailmaster.py send
```

## ⚖️ Credits
This tool utilizes powerful core modules developed by **[aels](https://github.com/aels)**.
- **Validation Engine:** Based on [Validol](https://github.com/aels/mailtools/tree/main/remove-dangerous-emails).
- **Mailing Engine:** Based on [MadCat Mailer](https://github.com/aels/mailtools/tree/main/mass-mailer).
- **SMTP Checker:** Based on [SMTP Checker](https://github.com/aels/mailtools/tree/main/smtp-checker).

## ⚠️ Legal Notice
For educational purposes only. Do not use for illegal activities or spamming without consent.
