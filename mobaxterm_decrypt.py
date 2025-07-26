#!/usr/bin/env python3
"""
MobaXterm Sessions Password Decryption Tool
Decrypts passwords from .mxtsessions files generated with encrypted passwords

Usage:
    python mobaxterm_decrypt.py sessions.mxtsessions master_password
    python mobaxterm_decrypt.py sessions.mxtsessions master_password --output decrypted.mxtsessions
    python mobaxterm_decrypt.py sessions.mxtsessions master_password --show-passwords
"""

from cryptography.fernet import Fernet
import base64
import hashlib
import argparse
import sys
import re
import os

def generate_key_from_password(password):
    """Generate a Fernet key from a password"""
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

def decrypt_mobaxterm_password(encrypted_password, master_password):
    """Decrypt a MobaXterm encrypted password"""
    try:
        # Remove ENC: prefix if present
        if encrypted_password.startswith('ENC:'):
            encrypted_password = encrypted_password[4:]
        
        key = generate_key_from_password(master_password)
        fernet = Fernet(key)
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_password.encode())
        decrypted = fernet.decrypt(encrypted_bytes)
        return decrypted.decode()
    except Exception as e:
        raise Exception(f"Decryption failed: {str(e)}")

def parse_mxtsessions_file(file_path):
    """Parse .mxtsessions file and extract session information"""
    sessions = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find session entries (lines that contain session data)
        session_pattern = r'^([^=]+)=#109#0%([^%]+)%22%([^%]+)%([^%]+)%-1%-1.*
        
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('[') and '=' in line and '#109#0%' in line:
                match = re.match(session_pattern, line)
                if match:
                    session_name = match.group(1)
                    ip = match.group(2)
                    username = match.group(3)
                    password = match.group(4)
                    
                    sessions.append({
                        'session_name': session_name,
                        'ip': ip,
                        'username': username,
                        'password': password,
                        'original_line': line
                    })
        
        return sessions
    except Exception as e:
        raise Exception(f"Failed to parse sessions file: {str(e)}")

def decrypt_sessions(sessions, master_password):
    """Decrypt passwords in sessions list"""
    decrypted_sessions = []
    
    for session in sessions:
        try:
            password = session['password']
            
            # Check if password is encrypted
            if password.startswith('ENC:') or password.startswith('ENCRYPT_FAILED_'):
                if password.startswith('ENCRYPT_FAILED_'):
                    # Handle failed encryption case
                    decrypted_password = password.replace('ENCRYPT_FAILED_', '')
                    print(f"⚠️  Warning: {session['session_name']} had encryption failure, using original password")
                else:
                    # Decrypt the password
                    decrypted_password = decrypt_mobaxterm_password(password, master_password)
                
                # Create new session with decrypted password
                new_session = session.copy()
                new_session['password'] = decrypted_password
                new_session['decrypted'] = True
                decrypted_sessions.append(new_session)
            else:
                # Password is already plain text
                new_session = session.copy()
                new_session['decrypted'] = False
                decrypted_sessions.append(new_session)
                
        except Exception as e:
            print(f"❌ Failed to decrypt {session['session_name']}: {e}")
            # Keep original session with failed decryption note
            failed_session = session.copy()
            failed_session['decryption_error'] = str(e)
            decrypted_sessions.append(failed_session)
    
    return decrypted_sessions

def generate_decrypted_mxtsessions(original_file, decrypted_sessions):
    """Generate new .mxtsessions file with decrypted passwords"""
    try:
        with open(original_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace encrypted passwords with decrypted ones
        new_content = content
        
        for session in decrypted_sessions:
            if 'decrypted' in session and session['decrypted']:
                # Replace the password in the original line
                original_line = session['original_line']
                
                # Create new line with decrypted password
                session_pattern = r'^([^=]+)=#109#0%([^%]+)%22%([^%]+)%([^%]+)(%-1%-1.*)
                match = re.match(session_pattern, original_line)
                
                if match:
                    session_name = match.group(1)
                    ip = match.group(2)
                    username = match.group(3)
                    old_password = match.group(4)
                    suffix = match.group(5)
                    
                    new_line = f"{session_name}=#109#0%{ip}%22%{username}%{session['password']}{suffix}"
                    new_content = new_content.replace(original_line, new_line)
        
        return new_content
        
    except Exception as e:
        raise Exception(f"Failed to generate decrypted file: {str(e)}")

def main():
    parser = argparse.ArgumentParser(
        description='MobaXterm Sessions Password Decryption Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s sessions.mxtsessions "my_master_password"
  %(prog)s sessions.mxtsessions "my_master_password" --output decrypted.mxtsessions
  %(prog)s sessions.mxtsessions "my_master_password" --show-passwords
  %(prog)s sessions.mxtsessions "my_master_password" --output decrypted.mxtsessions --show-passwords
        """
    )
    
    parser.add_argument('sessions_file', help='Path to .mxtsessions file')
    parser.add_argument('master_password', help='Master password used for encryption')
    parser.add_argument('--output', '-o', help='Output file path for decrypted sessions')
    parser.add_argument('--show-passwords', '-s', action='store_true', 
                       help='Display decrypted passwords in terminal (use with caution)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.exists(args.sessions_file):
        print(f"❌ Error: Sessions file '{args.sessions_file}' not found", file=sys.stderr)
        sys.exit(1)
    
    print(f"🔍 Parsing sessions file: {args.sessions_file}")
    
    try:
        # Parse the sessions file
        sessions = parse_mxtsessions_file(args.sessions_file)
        print(f"✅ Found {len(sessions)} sessions")
        
        if len(sessions) == 0:
            print("⚠️  No sessions found in file")
            sys.exit(0)
        
        # Decrypt sessions
        print(f"🔓 Decrypting passwords with master password...")
        decrypted_sessions = decrypt_sessions(sessions, args.master_password)
        
        # Count results
        encrypted_count = sum(1 for s in decrypted_sessions if s.get('decrypted', False))
        plain_count = sum(1 for s in decrypted_sessions if not s.get('decrypted', True) and 'decryption_error' not in s)
        failed_count = sum(1 for s in decrypted_sessions if 'decryption_error' in s)
        
        print(f"📊 Results:")
        print(f"   🔓 Decrypted: {encrypted_count}")
        print(f"   📝 Already plain: {plain_count}")
        print(f"   ❌ Failed: {failed_count}")
        
        # Show passwords if requested
        if args.show_passwords:
            print(f"\n🔐 Session Details:")
            print("-" * 80)
            for session in decrypted_sessions:
                status = "🔓 DECRYPTED" if session.get('decrypted') else "📝 PLAIN"
                if 'decryption_error' in session:
                    status = "❌ FAILED"
                
                print(f"{status} | {session['session_name']}")
                print(f"       IP: {session['ip']}")
                print(f"       User: {session['username']}")
                
                if 'decryption_error' in session:
                    print(f"       Error: {session['decryption_error']}")
                else:
                    print(f"       Password: {session['password']}")
                print()
        
        # Generate output file if requested
        if args.output:
            print(f"💾 Generating decrypted sessions file: {args.output}")
            try:
                decrypted_content = generate_decrypted_mxtsessions(args.sessions_file, decrypted_sessions)
                
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(decrypted_content)
                
                print(f"✅ Decrypted sessions saved to: {args.output}")
            except Exception as e:
                print(f"❌ Failed to save output file: {e}", file=sys.stderr)
                sys.exit(1)
        
        if not args.show_passwords and not args.output:
            print("\n💡 Use --show-passwords to display passwords or --output to save decrypted file")
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()