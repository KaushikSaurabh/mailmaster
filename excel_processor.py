import pandas as pd
import subprocess
import os
import re
import sys

def find_email_column(df):
    common_names = ['email', 'e-mail', 'mail', 'email address', 'subscriber email']
    for col in df.columns:
        if str(col).lower() in common_names:
            return col
    email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    max_emails = 0
    best_col = None
    for col in df.columns:
        email_count = df[col].astype(str).str.contains(email_regex, na=False).sum()
        if email_count > max_emails:
            max_emails = email_count
            best_col = col
    return best_col

def run_pro_validation(excel_path):
    print(f"[*] Reading: {excel_path}")
    df = pd.read_excel(excel_path)
    email_col = find_email_column(df)
    if not email_col:
        print("[!] Error: Could not find an Email column.")
        return
    print(f"[+] Found email data in column: '{email_col}'")
    df[email_col] = df[email_col].astype(str).str.strip()
    unique_emails = df[email_col].unique()
    temp_txt = "temp_emails_for_validol.txt"
    with open(temp_txt, 'w', encoding='utf-8') as f:
        for email in unique_emails:
            if '@' in email:
                f.write(f"{email}\n")
    validator_path = os.path.join(os.path.dirname(__file__), "core", "validator.py")
    print("[*] Launching Validol...")
    try:
        process = subprocess.Popen(
            [sys.executable, validator_path, temp_txt],
            stdin=subprocess.PIPE,
            stdout=sys.stdout,
            stderr=sys.stderr,
            text=True
        )
        process.communicate(input="\n\n")
        safe_file = "temp_emails_for_validol_safe.txt"
        dang_file = "temp_emails_for_validol_dangerous.txt"
        if os.path.exists(safe_file) and os.path.exists(dang_file):
            with open(safe_file, 'r', encoding='utf-8') as f:
                safe_emails = set(line.strip() for line in f if line.strip())
            with open(dang_file, 'r', encoding='utf-8') as f:
                dang_emails = set(line.split('|')[0].strip() for line in f if line.strip())
            
            # Save the SAFE list as a clean TEXT file for the mailer to use
            base_name = os.path.splitext(excel_path)[0]
            clean_text_list = f"{base_name}_CLEAN_LIST.txt"
            with open(clean_text_list, 'w', encoding='utf-8') as f:
                for email in sorted(list(safe_emails)):
                    f.write(f"{email}\n")
            
            safe_df = df[df[email_col].isin(safe_emails)]
            dang_df = df[df[email_col].isin(dang_emails)]
            safe_output = f"{base_name}_SAFE.xlsx"
            dang_output = f"{base_name}_DANGEROUS.xlsx"
            safe_df.to_excel(safe_output, index=False)
            dang_df.to_excel(dang_output, index=False)
            print(f"\n[SUCCESS] Separation complete!")
            print(f"[+] Clean TEXT list for mailer: {clean_text_list}")
            print(f"[+] Safe EXCEL database: {safe_output}")
            print(f"[+] Dangerous EXCEL database: {dang_output}")
        else:
            print("[!] Error: Validol failed.")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        for f in [temp_txt, "temp_emails_for_validol_safe.txt", "temp_emails_for_validol_dangerous.txt"]:
            if os.path.exists(f): os.remove(f)
