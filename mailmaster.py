import sys
import os
import argparse
from excel_processor import run_pro_validation

def main():
    parser = argparse.ArgumentParser(description="MailMaster - Unified Email Validation & Bulk Sending")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: Validate Excel
    val_parser = subparsers.add_parser("validate", help="Clean an Excel list of emails")
    val_parser.add_argument("file", help="Path to your Excel (.xlsx) file")

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
