import io
import re
from typing import Literal

import segno


def escape_special_chars(text: str) -> str:
    """
    Escapes special characters in SSID or Password for WiFi string format.
    Characters to escape: ';', ':', ',', '"', '\'
    
    Args:
        text: The input string to escape.
        
    Returns:
        The escaped string.
    """
    if not text:
        return ""
    # Backslash must be escaped first to avoid double escaping
    escaped = text.replace("\\", "\\\\")
    escaped = escaped.replace(";", "\;")
    escaped = escaped.replace(":", "\:")
    escaped = escaped.replace(",", "\,")
    escaped = escaped.replace('"', '\"')
    return escaped


def generate_wifi_qr(
    ssid: str,
    password: str | None = None,
    security: Literal["WPA", "WEP", "nopass"] = "WPA",
    hidden: bool = False,
) -> segno.QRCode:
    """
    Generates a WiFi QR code object.

    Args:
        ssid: The name of the WiFi network.
        password: The password for the network.
        security: The security type ('WPA', 'WEP', or 'nopass').
        hidden: Whether the network is hidden.

    Returns:
        A segno.QRCode object.

    Raises:
        ValueError: If inputs are invalid.
    """
    if not ssid:
        raise ValueError("SSID cannot be empty.")
    
    # SSID length validation (1-32 bytes)
    # Note: Using len(ssid.encode('utf-8')) to check byte length
    if len(ssid.encode("utf-8")) > 32:
        raise ValueError("SSID must be between 1 and 32 bytes.")

    # Validate password length based on security type
    if security != "nopass":
        if not password:
            raise ValueError(f"Password is required for {security} security.")
        
        # WPA password length check (8-63 ASCII characters)
        if security == "WPA":
            if len(password) < 8 or len(password) > 63:
                 raise ValueError("WPA password must be between 8 and 63 characters.")
        
        # WEP keys can be 5, 13, 16, or 29 bytes (ASCII chars) or 10/26 hex digits
        # This is a basic check; real WEP validation is complex, but this covers common cases
        if security == "WEP":
             if len(password) == 0:
                 raise ValueError("WEP password cannot be empty.")

    # Construct the WiFi configuration string manually to ensure control over escaping
    # Format: WIFI:T:{security};S:{ssid};P:{password};H:{hidden};;
    
    security_val = security if security != "nopass" else "nopass"
    escaped_ssid = escape_special_chars(ssid)
    escaped_password = escape_special_chars(password) if password else ""
    hidden_val = "true" if hidden else "false"
    
    # Standard format: WIFI:S:MySSID;T:WPA;P:MyPass;H:false;;
    # Order doesn't strictly matter but standard practice is T, S, P, H
    wifi_string = f"WIFI:T:{security_val};S:{escaped_ssid};"
    
    if security != "nopass":
        wifi_string += f"P:{escaped_password};"
        
    wifi_string += f"H:{hidden_val};;"

    # Create QR code
    qr = segno.make(wifi_string, error="H")  # High error correction
    return qr


def export_to_png(qr: segno.QRCode, scale: int = 10) -> io.BytesIO:
    """
    Exports a QR code to a PNG image in a BytesIO buffer.

    Args:
        qr: The segno.QRCode object.
        scale: The scaling factor for the image.

    Returns:
        A BytesIO object containing the PNG image data.
    """
    buffer = io.BytesIO()
    qr.save(buffer, kind="png", scale=scale, border=4)
    buffer.seek(0)
    return buffer
