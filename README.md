# 🌐 WiFi QR Share

A minimalist, secure, and offline-capable Python utility to generate WiFi connection QR codes. Built with Streamlit, Segno, and Pillow.

## 🚀 Features

- **Instant Generation**: Create QR codes for WPA/WPA2, WEP, and Open networks.
- **Privacy First**: Runs 100% locally. No data is sent to the cloud. Passwords are never logged.
- **Print Friendly**: Generate A4-formatted HTML pages with "Scan to Connect" instructions.
- **Secure**: Handles special characters in SSIDs and passwords correctly using standard escaping rules.
- **Masked Input**: Password input is masked for security during presentation.
- **Hidden Networks**: Supports configuration for hidden WiFi networks.

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit**: For the minimalist web interface.
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

## 🖥️ Usage

1. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. Open your browser at `http://localhost:8501`.

3. Enter your WiFi details:
   - **SSID**: Network name.
   - **Password**: Network password (optional for open networks).
   - **Security**: Select WPA, WEP, or nopass (Open).
   - **Hidden**: Check if the network is hidden.

4. **Actions**:
   - **Download PNG**: Save the QR code image.
   - **Print Friendly HTML**: Download a ready-to-print A4 page.

## 🔒 Security Note

This tool operates entirely on your local machine. It does not store, log, or transmit your WiFi credentials. The QR code generation happens in memory.

## 📝 License

[MIT](LICENSE)
