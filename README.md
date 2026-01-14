# 🌐 WiFi QR Share

A minimalist, secure, and offline-capable Python utility to generate WiFi connection QR codes. Built with Python's standard library (tkinter) and Segno.

## 🚀 Features

- **Instant Generation**: Create QR codes for WPA/WPA2, WEP, and Open networks.
- **Privacy First**: Runs 100% locally. No data is sent to the cloud. Passwords are never logged.
- **Print Friendly**: Generate A4-formatted HTML pages with "Scan to Connect" instructions.
- **Secure**: Handles special characters in SSIDs and passwords correctly using standard escaping rules.
- **Masked Input**: Password input is masked for security during presentation.
- **Hidden Networks**: Supports configuration for hidden WiFi networks.
- **Desktop GUI**: Native desktop application using Python's built-in tkinter library.

## 🛠️ Tech Stack

- **Python 3.10+**
- **tkinter**: Built-in GUI framework (no additional installation needed).
- **Segno**: For standard-compliant QR code generation.
- **Pillow**: For image processing.

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/galimov-i/wifi-qr-share.git
   cd wifi-qr-share
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Note: `tkinter` is included with Python by default on most systems. If it's missing, install it via your system package manager:
   - **Ubuntu/Debian**: `sudo apt-get install python3-tk`
   - **macOS**: Usually pre-installed with Python
   - **Windows**: Included with standard Python installation

## 🖥️ Usage

1. Run the application:
   ```bash
   python app.py
   ```

2. Enter your WiFi details in the GUI:
   - **Network Name (SSID)**: Enter your WiFi network name.
   - **Password**: Enter your network password (optional for open networks).
   - **Security Type**: Select WPA, WEP, or nopass (Open) from the dropdown.
   - **Hidden Network**: Check the box if your network doesn't broadcast its name.

3. The QR code will be generated automatically as you type.

4. **Actions**:
   - **Download PNG**: Save the QR code as a PNG image file.
   - **Print Friendly HTML**: Save a ready-to-print A4 HTML page.

## 🔒 Security Note

This tool operates entirely on your local machine. It does not store, log, or transmit your WiFi credentials. The QR code generation happens in memory.

## 📝 License

[MIT](LICENSE)
