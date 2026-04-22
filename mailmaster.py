import sys
import os
import argparse
from excel_processor import run_pro_validation

def update_config(smtps_file, leads_file):
    config_path = "dummy.config"
    if not os.path.exists(config_path):
        print("[!] dummy.config not found. Run 'python mailmaster.py send' once to generate it.")
        return

    with open(config_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.startswith("smtps_list_file:"):
            new_lines.append(f"smtps_list_file: {os.path.abspath(smtps_file)}\n")
        elif line.startswith("mails_list_file:"):
            new_lines.append(f"mails_list_file: {os.path.abspath(leads_file)}\n")
        else:
            new_lines.append(line)

    with open(config_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print(f"[+] Updated dummy.config with:")
    print(f"    - SMTPs: {smtps_file}")
    print(f"    - Leads: {leads_file}")

def main():
    parser = argparse.ArgumentParser(description="MailMaster - Unified Email Validation & Bulk Sending")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: Validate Excel
    val_parser = subparsers.add_parser("validate", help="Clean an Excel list of emails")
    val_parser.add_argument("file", help="Path to your Excel (.xlsx) file")

    # Command: Setup Config
    setup_parser = subparsers.add_parser("setup", help="Quickly configure your campaign")
    setup_parser.add_argument("--smtps", required=True, help="Path to validated SMTP list")
    setup_parser.add_argument("--leads", required=True, help="Path to cleaned leads text file")

    # Command: Check SMTP
    smtp_parser = subparsers.add_parser("check-smtp", help="Validate your SMTP credentials")
    smtp_parser.add_argument("file", help="Path to your smtp_list.txt (host:port:user:pass)")

    # Command: Start Mailer
    mail_parser = subparsers.add_parser("send", help="Start the bulk mailing campaign")

    # Command: Scan for Spam
    scan_parser = subparsers.add_parser("scan", help="Scan an email template for spam score")
    scan_parser.add_argument("file", help="Path to your email template (.html or .txt)")

    args = parser.parse_args()

    if args.command == "validate":
        run_pro_validation(args.file)
    elif args.command == "setup":
        update_config(args.smtps, args.leads)
    elif args.command == "check-smtp":
        os.system(f"python core/smtp_checker.py {args.file}")
    elif args.command == "send":
        os.system("python core/mailer.py")
    elif args.command == "scan":
        scanner_bin = os.path.join("core", "spamscanner.exe")
        if not os.path.exists(scanner_bin):
            print("[*] SpamScanner binary not found. Downloading...")
            os.makedirs("core", exist_ok=True)
            cmd = f'Invoke-WebRequest -Uri "https://github.com/spamscanner/spamscanner/releases/latest/download/spamscanner-win-x64.exe" -OutFile "{scanner_bin}"'
            os.system(f'powershell -Command "{cmd}"')
        
        if os.path.exists(scanner_bin):
            os.system(f"{scanner_bin} scan {args.file}")
        else:
            print("[!] Error: Could not download/run SpamScanner.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
