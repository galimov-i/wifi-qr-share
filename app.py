import streamlit as st
from PIL import Image

import wifi_qr_generator
import print_template


def main():
    st.set_page_config(
        page_title="WiFi QR Share",
        page_icon="🌐",
        layout="centered"
    )

    # Custom CSS for minimalist UI
    st.markdown("""
        <style>
        .stApp {
            max-width: 800px;
            margin: 0 auto;
        }
        .main-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("<div class='main-header'><h1>🌐 WiFi QR Share</h1><p>Generate secure WiFi connection codes instantly</p></div>", unsafe_allow_html=True)

    # Input Form
    with st.container():
        ssid = st.text_input("Network Name (SSID)", placeholder="e.g., MyHomeWiFi", max_chars=32)
        password = st.text_input("Password", type="password", placeholder="Enter WiFi password")

        with st.expander("Advanced Settings"):
            col1, col2 = st.columns(2)
            with col1:
                security = st.selectbox(
                    "Security Type",
                    options=["WPA", "WEP", "nopass"],
                    index=0,
                    help="WPA/WPA2 is standard for most modern networks."
                )
            with col2:
                hidden = st.checkbox("Hidden Network", help="Check if your network doesn't broadcast its name.")

    # Generation Logic
    if ssid:
        try:
            # Generate QR Code
            qr = wifi_qr_generator.generate_wifi_qr(
                ssid=ssid,
                password=password if security != "nopass" else None,
                security=security,
                hidden=hidden
            )
            
            # Export to PNG for display
            png_buffer = wifi_qr_generator.export_to_png(qr)
            
            # Display
            st.markdown("---")
            col_display, col_actions = st.columns([1, 1])
            
            with col_display:
                image = Image.open(png_buffer)
                st.image(image, caption=f"Scan to join: {ssid}", width=300)

            with col_actions:
                st.markdown("### Actions")
                
                # Download PNG
                png_buffer.seek(0)
                st.download_button(
                    label="⬇️ Download PNG",
                    data=png_buffer,
                    file_name=f"wifi_qr_{ssid}.png",
                    mime="image/png",
                    use_container_width=True
                )

                # Download Print HTML
                html_content = print_template.get_printable_html(qr, ssid)
                st.download_button(
                    label="🖨️ Print Friendly HTML",
                    data=html_content,
                    file_name=f"wifi_qr_print_{ssid}.html",
                    mime="text/html",
                    use_container_width=True
                )

        except ValueError as e:
            st.error(f"Error: {str(e)}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 0.8em;'>"
        "Securely generated locally. No data leaves your device."
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
