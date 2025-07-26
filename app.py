from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import io
import tempfile
import os
from cryptography.fernet import Fernet
import base64
import hashlib
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def generate_key_from_password(password):
    """Generate a Fernet key from a password"""
    # Create a consistent key from password using SHA-256 and base64 encoding
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
    
    # Check for empty rows
    if df.empty:
        raise ValueError("Excel file contains no data rows")
    
    return True

def generate_mxtsessions_content(df, file_name):
    """Generate MobaXterm sessions file content"""
    
    # Header section
    content = "[Bookmarks]\n"
    content += f"SubRep={file_name}\n"
    content += f"ImgNum=41\n\n"
    
    # Sessions section
    for index, row in df.iterrows():
        hostname = str(row['Hostname']).strip()
        ip = str(row['IP']).strip()
        username = str(row['user']).strip()
        password = str(row['password']).strip()
        
        # Skip empty rows
        if not hostname or not ip:
            continue
            
        # Session entry format for MobaXterm
        session_name = f"{hostname}_{ip}"
        content += f"{session_name}=#109#0%{ip}%22%{username}%{password}%-1%-1%%%%%0%0%0%%1080%%0%0%1#MobaFont%10%0%0%-1%15%236,236,236%30,30,30%180,180,192%0%-1%0%%xterm%-1%-1%_Std_Colors_0_%80%24%0%1%-1%<none>%%0%1%-1#0# #-1\n"
    
    return content

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "MXTSessions Generator API",
        "version": "1.0",
        "endpoints": {
            "/generate": "POST - Generate MobaXterm sessions file",
            "/encrypt": "POST - Encrypt passwords in Excel file",
            "/health": "GET - Health check"
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/generate', methods=['POST'])
def generate_sessions():
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not file.filename.endswith('.xlsx'):
            return jsonify({"error": "Only .xlsx files are supported"}), 400
        
        # Get encryption key if provided
        encryption_key = request.form.get('encryptionKey', '')
        
        # Read Excel file
        try:
            df = pd.read_excel(file, engine='openpyxl')
        except Exception as e:
            return jsonify({"error": f"Failed to read Excel file: {str(e)}"}), 400
        
        # Validate structure
        try:
            validate_excel_structure(df)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        
        # Decrypt passwords if encryption key is provided
        if encryption_key:
            try:
                for index in df.index:
                    encrypted_password = str(df.at[index, 'password'])
                    if encrypted_password and encrypted_password != 'nan':
                        df.at[index, 'password'] = decrypt_password(encrypted_password, encryption_key)
            except Exception as e:
                return jsonify({"error": f"Password decryption failed: {str(e)}"}), 400
        
        # Generate file name from original filename
        base_filename = os.path.splitext(file.filename)[0]
        
        # Generate MobaXterm sessions content
        try:
            sessions_content = generate_mxtsessions_content(df, base_filename)
        except Exception as e:
            return jsonify({"error": f"Failed to generate sessions: {str(e)}"}), 500
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mxtsessions', delete=False) as tmp_file:
            tmp_file.write(sessions_content)
            tmp_file_path = tmp_file.name
        
        # Return file
        try:
            return send_file(
                tmp_file_path,
                as_attachment=True,
                download_name=f"{base_filename}.mxtsessions",
                mimetype='text/plain'
            )
        finally:
            # Clean up temporary file
            try:
                os.unlink(tmp_file_path)
            except:
                pass
                
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/encrypt', methods=['POST'])
def encrypt_passwords():
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not file.filename.endswith('.xlsx'):
            return jsonify({"error": "Only .xlsx files are supported"}), 400
        
        # Get encryption key
        encryption_key = request.form.get('encryptionKey', '')
        if not encryption_key:
            return jsonify({"error": "Encryption key is required"}), 400
        
        # Read Excel file
        try:
            df = pd.read_excel(file, engine='openpyxl')
        except Exception as e:
            return jsonify({"error": f"Failed to read Excel file: {str(e)}"}), 400
        
        # Validate structure
        try:
            validate_excel_structure(df)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        
        # Encrypt passwords
        try:
            for index in df.index:
                password = str(df.at[index, 'password'])
                if password and password != 'nan' and password.strip():
                    df.at[index, 'password'] = encrypt_password(password.strip(), encryption_key)
        except Exception as e:
            return jsonify({"error": f"Password encryption failed: {str(e)}"}), 400
        
        # Create temporary Excel file
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp_file:
            df.to_excel(tmp_file.name, index=False, engine='openpyxl')
            tmp_file_path = tmp_file.name
        
        # Generate output filename
        base_filename = os.path.splitext(file.filename)[0]
        output_filename = f"{base_filename}_encrypted.xlsx"
        
        # Return file
        try:
            return send_file(
                tmp_file_path,
                as_attachment=True,
                download_name=output_filename,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        finally:
            # Clean up temporary file
            try:
                os.unlink(tmp_file_path)
            except:
                pass
                
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
