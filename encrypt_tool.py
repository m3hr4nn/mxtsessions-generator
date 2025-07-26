#!/usr/bin/env python3
"""
MXTSessions Password Encryption Tool
Compatible with the web application's encryption method

Usage:
    python encrypt_tool.py encrypt "password123" "my_secret_key"
    python encrypt_tool.py decrypt "gAAAAABh..." "my_secret_key"
    
    # For batch processing Excel files:
    python encrypt_tool.py batch-encrypt input.xlsx output.xlsx "my_secret_key"
    python encrypt_tool.py batch-decrypt encrypted.xlsx decrypted.xlsx "my_secret_key"
"""

from cryptography.fernet import Fernet
import base64
import hashlib
import argparse
import sys
import pandas as pd
import os

def generate_key_from_password(password):
    """Generate a Fernet key from a password"""
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

def encrypt_password(password, encryption_key):
    """Encrypt a password using Fernet encryption"""
    try:
        key = generate_key_from_password(encryption_key)
        fernet = Fernet(key)
        encrypted = fernet.encrypt(password.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    except Exception as e:
        raise Exception(f"Encryption failed: {str(e)}")

def decrypt_password(encrypted_password, encryption_key):
    """Decrypt a password using Fernet encryption"""
    try:
        key = generate_key_from_password(encryption_key)
        fernet = Fernet(key)
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_password.encode())
        decrypted = fernet.decrypt(encrypted_bytes)
        return decrypted.decode()
    except Exception as e:
        raise Exception(f"Decryption failed: {str(e)}")

def validate_excel_structure(df):
    """Validate that the Excel file has the required columns"""
    required_columns = ['Hostname', 'IP', 'user', 'password']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
    
    if df.empty:
        raise ValueError("Excel file contains no data rows")
    
    return True

def batch_encrypt_excel(input_file, output_file, encryption_key):
    """Encrypt passwords in an Excel file"""
    try:
        # Read Excel file
        df = pd.read_excel(input_file, engine='openpyxl')
        
        # Validate structure
        validate_excel_structure(df)
        
        # Encrypt passwords
        for index in df.index:
            password = str(df.at[index, 'password'])
            if password and password != 'nan' and password.strip():
                df.at[index, 'password'] = encrypt_password(password.strip(), encryption_key)
        
        # Save encrypted file
        df.to_excel(output_file, index=False, engine='openpyxl')
        print(f"✅ Successfully encrypted passwords in '{output_file}'")
        
    except Exception as e:
        print(f"❌ Error processing Excel file: {e}", file=sys.stderr)
        sys.exit(1)

def batch_decrypt_excel(input_file, output_file, encryption_key):
    """Decrypt passwords in an Excel file"""
    try:
        # Read Excel file
        df = pd.read_excel(input_file, engine='openpyxl')
        
        # Validate structure
        validate_excel_structure(df)
        
        # Decrypt passwords
        for index in df.index:
            encrypted_password = str(df.at[index, 'password'])
            if encrypted_password and encrypted_password != 'nan' and encrypted_password.strip():
                df.at[index, 'password'] = decrypt_password(encrypted_password.strip(), encryption_key)
        
        # Save decrypted file
        df.to_excel(output_file, index=False, engine='openpyxl')
        print(f"✅ Successfully decrypted passwords in '{output_file}'")
        
    except Exception as e:
        print(f"❌ Error processing Excel file: {e}", file=sys.stderr)
        sys.exit(1)

def test_encryption(encryption_key):
    """Test encryption/decryption with sample data"""
    test_passwords = ["password123", "admin@2024", "secure_pass_456"]
    
    print("🔧 Testing encryption/decryption...")
    print("-" * 50)
    
    for password in test_passwords:
        try:
            # Encrypt
            encrypted = encrypt_password(password, encryption_key)
            # Decrypt
            decrypted = decrypt_password(encrypted, encryption_key)
            
            status = "✅ PASS" if password == decrypted else "❌ FAIL"
            print(f"{status} '{password}' -> '{encrypted[:20]}...' -> '{decrypted}'")
            
        except Exception as e:
            print(f"❌ FAIL '{password}' -> Error: {e}")
    
    print("-" * 50)
    print("🔧 Test completed!")

def main():
    parser = argparse.ArgumentParser(
        description='MXTSessions Password Encryption Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s encrypt "password123" "my_secret_key"
  %(prog)s decrypt "gAAAAABh..." "my_secret_key"
  %(prog)s batch-encrypt input.xlsx output.xlsx "my_secret_key"
  %(prog)s batch-decrypt encrypted.xlsx decrypted.xlsx "my_secret_key"
  %(prog)s test "my_secret_key"
        """
    )
    
    parser.add_argument(
        'action', 
        choices=['encrypt', 'decrypt', 'batch-encrypt', 'batch-decrypt', 'test'],
        help='Action to perform'
    )
    
    parser.add_argument('args', nargs='+', help='Arguments for the action')
    
    args = parser.parse_args()
    
    try:
        if args.action == 'encrypt':
            if len(args.args) != 2:
                print("❌ Error: encrypt requires <password> <encryption_key>", file=sys.stderr)
                sys.exit(1)
            
            password, key = args.args
            result = encrypt_password(password, key)
            print(f"🔒 Encrypted: {result}")
            
        elif args.action == 'decrypt':
            if len(args.args) != 2:
                print("❌ Error: decrypt requires <encrypted_password> <encryption_key>", file=sys.stderr)
                sys.exit(1)
            
            encrypted_password, key = args.args
            result = decrypt_password(encrypted_password, key)
            print(f"🔓 Decrypted: {result}")
            
        elif args.action == 'batch-encrypt':
            if len(args.args) != 3:
                print("❌ Error: batch-encrypt requires <input.xlsx> <output.xlsx> <encryption_key>", file=sys.stderr)
                sys.exit(1)
            
            input_file, output_file, key = args.args
            
            if not os.path.exists(input_file):
                print(f"❌ Error: Input file '{input_file}' not found", file=sys.stderr)
                sys.exit(1)
            
            batch_encrypt_excel(input_file, output_file, key)
            
        elif args.action == 'batch-decrypt':
            if len(args.args) != 3:
                print("❌ Error: batch-decrypt requires <input.xlsx> <output.xlsx> <encryption_key>", file=sys.stderr)
                sys.exit(1)
            
            input_file, output_file, key = args.args
            
            if not os.path.exists(input_file):
                print(f"❌ Error: Input file '{input_file}' not found", file=sys.stderr)
                sys.exit(1)
            
            batch_decrypt_excel(input_file, output_file, key)
            
        elif args.action == 'test':
            if len(args.args) != 1:
                print("❌ Error: test requires <encryption_key>", file=sys.stderr)
                sys.exit(1)
            
            key = args.args[0]
            test_encryption(key)
            
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
