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

    args = parser.parse_args()

    if args.command == "validate":
        run_pro_validation(args.file)
    elif args.command == "check-smtp":
        os.system(f"python core/smtp_checker.py {args.file}")
    elif args.command == "send":
        os.system("python core/mailer.py")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
