import pandas as pd
import subprocess
import os
import re
import sys

def find_email_column(df):
    # Try common names first
    common_names = ['email', 'e-mail', 'mail', 'email address', 'subscriber email']
    for col in df.columns:
        if str(col).lower() in common_names:
            return col
    
    # Fallback: find column with most email-like strings
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
        print("[!] Error: Could not find an Email column in the Excel file.")
        return

    print(f"[+] Found email data in column: '{email_col}'")
    
    # Clean up email strings (remove whitespace)
    df[email_col] = df[email_col].astype(str).str.strip()
    unique_emails = df[email_col].unique()
    
    # Create temp text file for Validol
    temp_txt = "temp_emails_for_validol.txt"
    with open(temp_txt, 'w', encoding='utf-8') as f:
        for email in unique_emails:
            if '@' in email:
                f.write(f"{email}\n")

    validator_path = os.path.join(os.path.dirname(__file__), "core", "validator.py")
    
    print("[*] Launching Validol...")
    print("[!] When prompted by the tool, press ENTER to start the validation.")
    
    try:
        # Run the tool. It produces temp_emails_for_validol_safe.txt and _dangerous.txt
        subprocess.run([sys.executable, validator_path, temp_txt], check=True)
        
        safe_file = "temp_emails_for_validol_safe.txt"
        dang_file = "temp_emails_for_validol_dangerous.txt"
        
        if os.path.exists(safe_file) and os.path.exists(dang_file):
            # Read back the results
            with open(safe_file, 'r', encoding='utf-8') as f:
                safe_emails = set(line.strip() for line in f if line.strip())
            
            with open(dang_file, 'r', encoding='utf-8') as f:
                # Dangerous file usually has "email | reason", we just want the email
                dang_emails = set(line.split('|')[0].strip() for line in f if line.strip())

            # Split the original DataFrame
            safe_df = df[df[email_col].isin(safe_emails)]
            dang_df = df[df[email_col].isin(dang_emails)]

            # Save back to Excel
            base_name = os.path.splitext(excel_path)[0]
            safe_output = f"{base_name}_SAFE.xlsx"
            dang_output = f"{base_name}_DANGEROUS.xlsx"
            
            safe_df.to_excel(safe_output, index=False)
            dang_df.to_excel(dang_output, index=False)
            
            print(f"\n[SUCCESS] Separation complete!")
            print(f"[+] Safe entries saved to: {safe_output}")
            print(f"[+] Dangerous entries saved to: {dang_output}")
            print(f"[i] Total Safe: {len(safe_df)} | Total Dangerous: {len(dang_df)}")
            
        else:
            print("[!] Error: Validol did not generate the expected result files.")

    except Exception as e:
        print(f"[!] An error occurred: {e}")
    finally:
        # Cleanup temp files
        for f in [temp_txt, "temp_emails_for_validol_safe.txt", "temp_emails_for_validol_dangerous.txt"]:
            if os.path.exists(f):
                os.remove(f)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python process_excel_pro.py <path_to_excel_file>")
    else:
        # Join all arguments in case the user forgot quotes for a path with spaces
        full_path = " ".join(sys.argv[1:])
        # Remove any stray quotes the user might have added manually
        full_path = full_path.strip('"').strip("'")
        run_pro_validation(full_path)
