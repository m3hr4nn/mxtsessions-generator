# MXTSessions Generator
[![View Demo](https://img.shields.io/badge/Demo-View%20Live-blue?style=for-the-badge)](https://m3hr4nn.github.io/mxtsessions-generator/)
[![License](https://img.shields.io/github/license/m3hr4nn/wsdl-to-xlsx-converter?style=for-the-badge)](LICENSE)
A web application that converts Excel files containing server information into MobaXterm session files (.mxtsessions) with **integrated password encryption options**.

## 🚀 Enhanced Features

- **Excel to MobaXterm Conversion**: Convert .xlsx files with server credentials to .mxtsessions format
- **🆕 Integrated Password Formats**: Choose between plain text or encrypted passwords directly in the output
- **🔐 MobaXterm-Compatible Encryption**: Passwords encrypted using industry-standard AES encryption
- **Drag & Drop Interface**: Modern, responsive web interface with MobaXterm dark theme
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
- Passwords should be in plain text (encryption happens during conversion)

## 🔐 Password Format Options

### 📝 Plain Text Passwords (Default)
- Passwords stored as plain text in the .mxtsessions file
- Directly readable in MobaXterm
- Best for: Personal use or secure environments

### 🔒 Encrypted Passwords (Recommended)
- Passwords encrypted using AES-128 with Fernet
- Requires master password for encryption/decryption
- More secure storage in session files
- Best for: Shared computers or sensitive environments

## 🎯 How to Use

### **Step 1: Choose Password Format**
- **Plain Text**: Select "Plain Text Passwords" (default)
- **Encrypted**: Select "Encrypted Passwords" and enter a strong master password

### **Step 2: Upload Excel File**
- Drag and drop your .xlsx file or click to browse
- File validation happens automatically

### **Step 3: Generate Sessions**
- Click "Generate MXTSessions File"
- Download your formatted .mxtsessions file

### **Step 4: Import to MobaXterm**
- Open MobaXterm
- Go to Sessions → Import Sessions
- Select your downloaded .mxtsessions file
- Sessions will appear in your bookmarks

## 🔧 Output Formats

### Plain Text Output (`servers.mxtsessions`)
```ini
[Bookmarks]
SubRep=servers
ImgNum=41

server1_192.168.1.10=#109#0%192.168.1.10%22%admin%mypassword123%-1%-1%%%%%0%0%0%%1080%%0%0%1#MobaFont%10%0%0%-1%15%236,236,236%30,30,30%180,180,192%0%-1%0%%xterm%-1%-1%_Std_Colors_0_%80%24%0%1%-1%<none>%%0%1%-1#0# #-1
```

### Encrypted Output (`servers_encrypted.mxtsessions`)
```ini
[Bookmarks]
SubRep=servers
ImgNum=41

server1_192.168.1.10=#109#0%192.168.1.10%22%admin%ENC:gAAAAABh...encrypted_data...%-1%-1%%%%%0%0%0%%1080%%0%0%1#MobaFont%10%0%0%-1%15%236,236,236%30,30,30%180,180,192%0%-1%0%%xterm%-1%-1%_Std_Colors_0_%80%24%0%1%-1%<none>%%0%1%-1#0# #-1
```

## 🏗️ Architecture

```
┌─────────────────┐    HTTPS     ┌─────────────────────┐
│   GitHub Pages  │──────────────▶│   Render.com API    │
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



## 🔧 Configuration

### Backend Configuration (Render.com)

1. **app.py** - Main Flask application
2. **requirements.txt** - Python dependencies
3. **Optional: .env file** for environment variables

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
Generate MobaXterm sessions file with password format options

**Request:**
- Form data with `file` (Excel file)
- `passwordFormat`: `"plain"` or `"encrypted"`
- `encryptionKey`: Required if passwordFormat is `"encrypted"`

**Response:**
- Success: `.mxtsessions` file download
- Error: JSON with error message

**Example:**
```bash
curl -X POST \
  -F "file=@servers.xlsx" \
  -F "passwordFormat=encrypted" \
  -F "encryptionKey=my_master_password" \
  https://your-api.onrender.com/generate
```

### GET /health
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-26T10:30:00"
}
```

### GET /
API information and version

**Response:**
```json
{
  "message": "MXTSessions Generator API - Enhanced Version",
  "version": "2.0.0",
  "features": [
    "Generate MobaXterm sessions with plain text passwords",
    "Generate MobaXterm sessions with encrypted passwords",
    "MobaXterm-compatible password encryption",
    "Lightweight processing without pandas"
  ]
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

## 🛠️ Password Decryption Tool

For advanced users who need to decrypt passwords from encrypted .mxtsessions files, use the included decryption tool:

### Installation
```bash
# Install required dependency
pip install cryptography

# Make the tool executable
chmod +x mobaxterm_decrypt.py
```

### Usage Examples
```bash
# View session info without showing passwords
python mobaxterm_decrypt.py servers_encrypted.mxtsessions "my_master_password"

# Show decrypted passwords in terminal (use with caution)
python mobaxterm_decrypt.py servers_encrypted.mxtsessions "my_master_password" --show-passwords

# Generate a new file with decrypted passwords
python mobaxterm_decrypt.py servers_encrypted.mxtsessions "my_master_password" --output servers_plain.mxtsessions

# Verbose output with password display
python mobaxterm_decrypt.py servers_encrypted.mxtsessions "my_master_password" -o decrypted.mxtsessions -s -v
```

### Sample Output
```
🔍 Parsing sessions file: servers_encrypted.mxtsessions
✅ Found 3 sessions
🔓 Decrypting passwords with master password...
📊 Results:
   🔓 Decrypted: 3
   📝 Already plain: 0
   ❌ Failed: 0
💾 Generating decrypted sessions file: servers_plain.mxtsessions
✅ Decrypted sessions saved to: servers_plain.mxtsessions
```

## 🎨 MobaXterm Dark Theme

The application features an authentic MobaXterm-inspired dark theme:

### Design Features
- **Terminal-inspired color scheme**: Dark backgrounds with cyan/blue accents matching MobaXterm
- **Monospace fonts**: Consolas/Monaco for authentic terminal look
- **Glowing effects**: Subtle animations and shadows
- **Responsive design**: Works perfectly on desktop, tablet, and mobile
- **Modern UI elements**: Radio buttons, progress bars, and status indicators
- **Accessibility**: High contrast and keyboard navigation support

### Color Palette
```css
--moba-bg-primary: #1e1e1e      /* Main background */
--moba-bg-secondary: #2d2d30    /* Container background */
--moba-accent-blue: #007acc     /* Primary accent */
--moba-accent-cyan: #00d4aa     /* Success/highlight */
--moba-accent-orange: #ff8c00   /* Warning/encryption */
--moba-text-primary: #cccccc    /* Main text */
--moba-success: #4ec9b0         /* Success messages */
--moba-error: #f44747           /* Error messages */
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
