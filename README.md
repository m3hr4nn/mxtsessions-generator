# MXTSessions Generator

A web application that converts Excel files containing server information into MobaXterm session files (.mxtsessions) with optional password encryption support.

## 🚀 Features

- **Excel to MobaXterm Conversion**: Convert .xlsx files with server credentials to .mxtsessions format
- **Password Encryption**: Secure password encryption using Fernet (AES-128) encryption
- **Drag & Drop Interface**: Modern, responsive web interface with drag-and-drop file upload
- **Real-time Processing**: Instant file processing with progress indicators
- **Cross-Platform**: Works on any device with a web browser
- **Free Hosting**: Static frontend on GitHub Pages + dynamic backend on Render.com

## 📋 Input Format

Your Excel file (.xlsx) must contain exactly 4 columns with these headers:

| Hostname | IP | user | password |
|----------|-------|------|----------|
| server1 | 192.168.1.10 | admin | mypassword123 |
| web-server | 10.0.0.5 | root | securepass456 |
| db-server | 172.16.0.20 | database | dbpass789 |

**Important Requirements:**
- File must be in .xlsx format (Excel 2007+)
- Column headers must match exactly: `Hostname`, `IP`, `user`, `password`
- All rows with data will be processed (empty rows are skipped)
- Passwords can be plain text or encrypted (if using encryption feature)

## 🔐 Password Encryption

The application includes a robust password encryption system:

### Encryption Method
- **Algorithm**: Fernet (AES-128 in CBC mode with HMAC authentication)
- **Key Derivation**: SHA-256 hash of your passphrase
- **Encoding**: Base64 URL-safe encoding

### How to Use Encryption

1. **Encrypt Passwords First** (Optional):
   - Upload your Excel file with plain text passwords
   - Check "Enable password encryption"
   - Enter your encryption key
   - Click "Encrypt Passwords Only"
   - Download the encrypted Excel file

2. **Generate Sessions with Encrypted Passwords**:
   - Upload Excel file (with encrypted or plain passwords)
   - If passwords are encrypted, check "Enable password encryption" and enter the same key
   - Click "Generate MXTSessions File"

### Encryption Tool Usage Example

```python
# If you want to encrypt/decrypt manually using Python
from cryptography.fernet import Fernet
import base64
import hashlib

def generate_key_from_password(password):
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

def encrypt_password(password, encryption_key):
    key = generate_key_from_password(encryption_key)
    fernet = Fernet(key)
    encrypted = fernet.encrypt(password.encode())
    return base64.urlsafe_b64encode(encrypted).decode()

# Example usage
encrypted_pass = encrypt_password("mypassword123", "my_secret_key")
print(encrypted_pass)
```

## 🏗️ Architecture

```
┌─────────────────┐    HTTPS      ┌─────────────────────┐
│   GitHub Pages  │──────────────▶/   Render.com API   /
│  (Static Site)  │               │  (Flask Backend)    │
│                 │               │                     │
│  - HTML/CSS/JS  │               │  - File Processing  │
│  - File Upload  │               │  - Encryption       │
│  - UI/UX        │               │  - MXT Generation   │
└─────────────────┘               └─────────────────────┘
```

## 📁 Project Structure

```
mxtsessions-generator/
├── index.html              # Frontend application
├── app.py                  # Flask backend server
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── .github/
    └── workflows/
        └── deploy.yml     # GitHub Actions for deployment
```

## 🚀 Deployment Guide

### Part 1: Deploy Backend on Render.com

1. **Create Render Account**:
   - Go to [render.com](https://render.com)
   - Sign up for a free account

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Choose "Build and deploy from a Git repository"
   - Connect your GitHub account if not already connected

3. **Configure the Service**:
   ```
   Name: mxtsessions-api (or any name you prefer)
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python app.py
   ```

4. **Environment Variables** (Optional):
   - Add any environment variables if needed
   - The app will automatically use PORT from Render

5. **Deploy**:
   - Click "Create Web Service"
   - Wait for deployment (usually 2-3 minutes)
   - Note your service URL (e.g., `https://your-app-name.onrender.com`)

### Part 2: Deploy Frontend on GitHub Pages

1. **Prepare Repository**:
   ```bash
   git clone https://github.com/m3hr4nn/mxtsessions-generator.git
   cd mxtsessions-generator
   
   # Add your files
   git add .
   git commit -m "Initial commit with MobaXterm theme"
   git push origin main
   ```

2. **Update API URL**:
   - Open `index.html`
   - Replace `https://your-render-app.onrender.com` with your actual Render URL
   - Commit and push changes

3. **Enable GitHub Pages**:
   - Go to repository Settings
   - Scroll to "Pages" section
   - Source: "Deploy from a branch"
   - Branch: `main` / `(root)`
   - Click "Save"

4. **Access Your Application**:
   - Your app will be available at: `https://m3hr4nn.github.io/mxtsessions-generator`
   - Wait 5-10 minutes for initial deployment

## 🔧 Configuration

### Backend Configuration (Render.com)

The Flask backend requires these files in your repository:

1. **app.py** - Main Flask application
2. **requirements.txt** - Python dependencies
3. **Optional: .env file** for environment variables

### Frontend Configuration (GitHub Pages)

Update the API URL in `index.html`:

```javascript
const API_BASE_URL = 'https://your-actual-render-url.onrender.com';
```

## 📝 Step-by-Step Integration Guide

### Step 1: Create Repository Structure

```bash
# Create the repository structure
mkdir mxtsessions-generator
cd mxtsessions-generator

# Create files (copy content from artifacts above)
touch index.html
touch styles.css
touch app.py
touch requirements.txt
touch README.md

# Initialize git
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/m3hr4nn/mxtsessions-generator.git
git push -u origin main
```

### Step 2: Deploy Backend First

1. Fork or create repository with backend files
2. Go to Render.com → New Web Service
3. Connect your GitHub repository
4. Configure as Python app with:
   - Build: `pip install -r requirements.txt`
   - Start: `python app.py`
5. Deploy and note the URL

### Step 3: Update Frontend

1. Edit `index.html`
2. Replace API_BASE_URL with your Render URL
3. Commit and push to GitHub

### Step 4: Enable GitHub Pages

1. Repository Settings → Pages
2. Source: Deploy from branch `main`
3. Wait for deployment

### Step 5: Test the Application

1. Visit your GitHub Pages URL
2. Upload a test Excel file
3. Verify file generation works

## 🛠️ File Structure Details

### Frontend Files (GitHub Pages)
```
├── index.html          # Main web application
├── styles.css          # MobaXterm dark theme
└── README.md          # Documentation
```

### Backend Files (Render.com)
```
├── app.py             # Flask API server
├── requirements.txt   # Python dependencies
└── runtime.txt        # Python version (optional)
```

## 🎨 MobaXterm Theme Features

The new dark theme includes:

- **Terminal-inspired color scheme**: Dark backgrounds with cyan/blue accents
- **Monospace fonts**: Consolas/Monaco for authentic terminal look
- **Glowing effects**: Subtle animations and shadows
- **MobaXterm color palette**: Authentic colors matching the application
- **Responsive design**: Works on all device sizes
- **Terminal scrollbars**: Custom styled scrollbars
- **Progress animations**: Smooth loading indicators

## 🔍 API Endpoints

### POST /generate
Generate MobaXterm sessions file from Excel

**Request:**
- Form data with `file` (Excel file)
- Optional: `encryptionKey` for password decryption

**Response:**
- Success: `.mxtsessions` file download
- Error: JSON with error message

### POST /encrypt  
Encrypt passwords in Excel file

**Request:**
- Form data with `file` (Excel file)
- Required: `encryptionKey` for encryption

**Response:**
- Success: Encrypted Excel file download
- Error: JSON with error message

### GET /health
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00"
}
```

## 🚨 Troubleshooting

### Common Issues

1. **CORS Errors**:
   - Ensure Flask-CORS is installed and configured
   - Check if Render service is running

2. **File Upload Fails**:
   - Verify Excel file has correct column headers
   - Check file size (Render free tier has limits)

3. **Encryption Errors**:
   - Ensure encryption key is provided when needed
   - Verify password format in Excel file

4. **GitHub Pages Not Updating**:
   - Check Actions tab for deployment status
   - Clear browser cache
   - Wait up to 10 minutes for changes

### Debug Mode

Enable debug mode in development:

```python
# In app.py, change last line to:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)  # Enable debug
```

## 📊 Output Format

The generated `.mxtsessions` file follows MobaXterm's format:

```ini
[Bookmarks]
SubRep=your_filename
ImgNum=41

server1_192.168.1.10=#109#0%192.168.1.10%22%admin%password123%-1%-1%%%%%0%0%0%%1080%%0%0%1#MobaFont%10%0%0%-1%15%236,236,236%30,30,30%180,180,192%0%-1%0%%xterm%-1%-1%_Std_Colors_0_%80%24%0%1%-1%<none>%%0%1%-1#0# #-1
web-server_10.0.0.5=#109#0%10.0.0.5%22%root%securepass456%-1%-1%%%%%0%0%0%%1080%%0%0%1#MobaFont%10%0%0%-1%15%236,236,236%30,30,30%180,180,192%0%-1%0%%xterm%-1%-1%_Std_Colors_0_%80%24%0%1%-1%<none>%%0%1%-1#0# #-1
```

## 🔐 Advanced Encryption Tool

For manual encryption/decryption outside the web app, use this Python script:

```python
#!/usr/bin/env python3
"""
MXTSessions Password Encryption Tool
Compatible with the web application's encryption method
"""

from cryptography.fernet import Fernet
import base64
import hashlib
import argparse
import sys

def generate_key_from_password(password):
    """Generate a Fernet key from a password"""
    key = hashlib.SHA256(password.encode()).digest()
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

def main():
    parser = argparse.ArgumentParser(description='MXTSessions Password Encryption Tool')
    parser.add_argument('action', choices=['encrypt', 'decrypt'], help='Action to perform')
    parser.add_argument('password', help='Password to encrypt/decrypt')
    parser.add_argument('key', help='Encryption key')
    
    args = parser.parse_args()
    
    try:
        if args.action == 'encrypt':
            result = encrypt_password(args.password, args.key)
            print(f"Encrypted: {result}")
        else:
            result = decrypt_password(args.password, args.key)
            print(f"Decrypted: {result}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
```

**Usage:**
```bash
# Install required package
pip install cryptography

# Encrypt a password
python encrypt_tool.py encrypt "mypassword123" "my_secret_key"

# Decrypt a password
python encrypt_tool.py decrypt "gAAAAABh..." "my_secret_key"
```

## 🎯 Performance Optimization

### Frontend Optimizations
- **Lazy Loading**: Scripts loaded only when needed
- **CSS Minification**: Compress CSS for faster loading
- **Image Optimization**: Use WebP format for icons
- **Caching**: Browser caching for static assets

### Backend Optimizations
- **File Streaming**: Handle large files efficiently
- **Memory Management**: Clean up temporary files
- **Error Handling**: Comprehensive error responses
- **Request Validation**: Input sanitization

## 🔒 Security Considerations

### Password Security
- **Client-side encryption**: Passwords never sent in plain text
- **Secure key derivation**: SHA-256 hashing for key generation
- **Memory cleanup**: Temporary files are automatically deleted
- **HTTPS enforcement**: All communication encrypted in transit

### Best Practices
1. **Use strong encryption keys**: At least 12 characters with mixed case, numbers, symbols
2. **Keep keys secure**: Never share encryption keys via email or chat
3. **Regular key rotation**: Change encryption keys periodically
4. **Audit access**: Monitor who has access to encrypted files

## 📱 Mobile Support

The application is fully responsive and works on:
- **Desktop**: Full features with drag-and-drop
- **Tablet**: Touch-friendly interface
- **Mobile**: Optimized layout and controls

### Mobile-Specific Features
- Touch-friendly buttons and inputs
- Responsive file upload area
- Optimized progress indicators
- Swipe-friendly navigation

## 🌐 Browser Compatibility

| Browser | Version | Status |
|---------|---------|---------|
| Chrome | 70+ | ✅ Full Support |
| Firefox | 65+ | ✅ Full Support |
| Safari | 12+ | ✅ Full Support |
| Edge | 79+ | ✅ Full Support |
| Opera | 57+ | ✅ Full Support |

## 🛡️ Error Handling

### Frontend Error Handling
- **File validation**: Check file type and size
- **Network errors**: Graceful handling of connection issues
- **User feedback**: Clear error messages and solutions

### Backend Error Handling
- **Input validation**: Comprehensive data validation
- **Exception logging**: Detailed error logging for debugging
- **Graceful degradation**: Fallback options for failed operations

## 📈 Monitoring and Analytics

### Health Monitoring
The backend includes health check endpoints for monitoring:

```bash
# Check if service is running
curl https://your-render-app.onrender.com/health

# Expected response
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00"
}
```

### Usage Analytics (Optional)
Add Google Analytics or similar service to track:
- File upload frequency
- Success/error rates
- Popular features
- User geography

## 🔄 Continuous Integration

### GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Install dependencies
      run: npm install -g html-minifier clean-css-cli
    
    - name: Minify HTML
      run: html-minifier --collapse-whitespace --remove-comments --minify-css --minify-js index.html -o index.min.html
    
    - name: Minify CSS
      run: cleancss -o styles.min.css styles.css
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      if: github.ref == 'refs/heads/main'
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./
```

## 🚀 Advanced Features

### Batch Processing
The application supports batch processing of multiple Excel files through the API:

```python
# Example batch processing endpoint (add to app.py)
@app.route('/batch', methods=['POST'])
def batch_process():
    files = request.files.getlist('files')
    results = []
    
    for file in files:
        # Process each file
        # Add to results
        pass
    
    return jsonify({"results": results})
```

### Custom Session Templates
Support for custom MobaXterm session templates:

```python
# Template system for different connection types
TEMPLATES = {
    'ssh': "#109#0%{ip}%22%{username}%{password}%-1%-1%%%%%0%0%0%%1080%%0%0%1#MobaFont%10%0%0%-1%15%236,236,236%30,30,30%180,180,192%0%-1%0%%xterm%-1%-1%_Std_Colors_0_%80%24%0%1%-1%<none>%%0%1%-1#0# #-1",
    'telnet': "#98#1%{ip}%23%{username}%{password}%-1%-1%%%%%0%0%0%%1080%%0%0%1#MobaFont%10%0%0%-1%15%236,236,236%30,30,30%180,180,192%0%-1%0%%xterm%-1%-1%_Std_Colors_0_%80%24%0%1%-1%<none>%%0%1%-1#0# #-1",
    'ftp': "#130#2%{ip}%21%{username}%{password}%-1%-1%%%%%0%0%0%%1080%%0%0%1#MobaFont%10%0%0%-1%15%236,236,236%30,30,30%180,180,192%0%-1%0%%xterm%-1%-1%_Std_Colors_0_%80%24%0%1%-1%<none>%%0%1%-1#0# #-1"
}
```

## 🎨 Theme Customization

### Creating Custom Themes
The CSS uses CSS custom properties for easy theming:

```css
/* Custom theme example */
:root {
    --moba-bg-primary: #0d1117;        /* GitHub dark background */
    --moba-bg-secondary: #161b22;      /* GitHub secondary */
    --moba-accent-blue: #58a6ff;       /* GitHub blue */
    --moba-accent-cyan: #56d364;       /* GitHub green */
    --moba-accent-orange: #ffa657;     /* GitHub orange */
}
```

### Dark/Light Mode Toggle
Add theme switching functionality:

```javascript
// Theme switcher (add to index.html)
function toggleTheme() {
    const root = document.documentElement;
    const isDark = root.classList.contains('light-theme');
    
    root.classList.toggle('light-theme', !isDark);
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
}

// Load saved theme
const savedTheme = localStorage.getItem('theme');
if (savedTheme === 'light') {
    document.documentElement.classList.add('light-theme');
}
```

## 📚 Additional Resources

### Documentation Links
- [MobaXterm Documentation](https://mobaxterm.mobatek.net/documentation.html)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [GitHub Pages Guide](https://docs.github.com/en/pages)
- [Render.com Documentation](https://render.com/docs)

### Community
- [GitHub Issues](https://github.com/m3hr4nn/mxtsessions-generator/issues)
- [Discussions](https://github.com/m3hr4nn/mxtsessions-generator/discussions)

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **MobaXterm**: For the excellent terminal application
- **Flask**: For the lightweight web framework
- **GitHub**: For free hosting and version control
- **Render.com**: For free backend hosting
- **Cryptography**: For secure password encryption

---

**Version**: 1.0.0  
**Last Updated**: January 2025  
**Author**: m3hr4nn  
**Repository**: https://github.com/m3hr4nn/mxtsessions-generator

For support or questions, please open an issue on GitHub or visit the discussions section.
