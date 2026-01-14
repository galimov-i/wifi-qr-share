import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import io
from typing import Literal

import wifi_qr_generator
import print_template


class WiFiQRApp:
    """Main application window for WiFi QR Share utility."""

    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize the application window.

        Args:
            root: The root Tkinter window.
        """
        self.root = root
        self.root.title("WiFi QR Share")
        self.root.geometry("700x600")
        self.root.resizable(False, False)

        # Variables
        self.ssid_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.security_var = tk.StringVar(value="WPA")
        self.hidden_var = tk.BooleanVar(value=False)
        self.current_qr = None
        self.current_ssid = ""

        self._create_ui()

    def _create_ui(self) -> None:
        """Create the user interface components."""
        # Header
        header_frame = tk.Frame(self.root, bg="#f0f0f0", pady=20)
        header_frame.pack(fill=tk.X)

        title_label = tk.Label(
            header_frame,
            text="🌐 WiFi QR Share",
            font=("Helvetica", 24, "bold"),
            bg="#f0f0f0"
        )
        title_label.pack()

        subtitle_label = tk.Label(
            header_frame,
            text="Generate secure WiFi connection codes instantly",
            font=("Helvetica", 10),
            bg="#f0f0f0",
            fg="#666"
        )
        subtitle_label.pack(pady=(5, 0))

        # Main content frame
        main_frame = tk.Frame(self.root, padx=30, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Input form
        form_frame = tk.Frame(main_frame)
        form_frame.pack(fill=tk.X, pady=(0, 20))

        # SSID input
        ssid_label = tk.Label(form_frame, text="Network Name (SSID):", anchor="w")
        ssid_label.pack(fill=tk.X, pady=(0, 5))
        ssid_entry = tk.Entry(form_frame, textvariable=self.ssid_var, width=40)
        ssid_entry.pack(fill=tk.X, pady=(0, 10))
        ssid_entry.bind("<FocusOut>", self._on_input_change)
        ssid_entry.bind("<Return>", self._on_input_change)

        # Password input
        password_label = tk.Label(form_frame, text="Password:", anchor="w")
        password_label.pack(fill=tk.X, pady=(0, 5))
        password_entry = tk.Entry(
            form_frame,
            textvariable=self.password_var,
            show="*",
            width=40
        )
        password_entry.pack(fill=tk.X, pady=(0, 10))
        password_entry.bind("<FocusOut>", self._on_input_change)
        password_entry.bind("<Return>", self._on_input_change)

        # Advanced settings frame
        advanced_frame = tk.LabelFrame(
            form_frame,
            text="Advanced Settings",
            padx=10,
            pady=10
        )
        advanced_frame.pack(fill=tk.X, pady=(0, 10))

        # Security type
        security_label = tk.Label(advanced_frame, text="Security Type:", anchor="w")
        security_label.pack(fill=tk.X, pady=(0, 5))
        security_combo = ttk.Combobox(
            advanced_frame,
            textvariable=self.security_var,
            values=["WPA", "WEP", "nopass"],
            state="readonly",
            width=37
        )
        security_combo.pack(fill=tk.X, pady=(0, 10))
        security_combo.bind("<<ComboboxSelected>>", self._on_input_change)

        # Hidden network checkbox
        hidden_check = tk.Checkbutton(
            advanced_frame,
            text="Hidden Network",
            variable=self.hidden_var,
            anchor="w",
            command=self._on_input_change
        )
        hidden_check.pack(fill=tk.X)

        # Generate button
        generate_btn = tk.Button(
            form_frame,
            text="Generate QR Code",
            command=self._on_input_change,
            width=20,
            pady=8,
            bg="#4CAF50",
            fg="white",
            font=("Helvetica", 10, "bold")
        )
        generate_btn.pack(pady=(10, 0))

        # Separator
        separator = ttk.Separator(main_frame, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, pady=20)

        # QR Code display area
        self.qr_frame = tk.Frame(main_frame)
        self.qr_frame.pack(fill=tk.BOTH, expand=True)

        self.qr_label = tk.Label(
            self.qr_frame,
            text="Enter network name to generate QR code",
            font=("Helvetica", 10),
            fg="#999"
        )
        self.qr_label.pack(expand=True)

        # Action buttons frame
        self.actions_frame = tk.Frame(main_frame)
        self.actions_frame.pack(fill=tk.X, pady=(10, 0))

        # Footer
        footer_label = tk.Label(
            self.root,
            text="Securely generated locally. No data leaves your device.",
            font=("Helvetica", 8),
            fg="#666",
            bg="#f0f0f0"
        )
        footer_label.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

    def _on_input_change(self, event=None) -> None:
        """Handle input changes and regenerate QR code."""
        ssid = self.ssid_var.get().strip()
        if not ssid:
            self._clear_qr_display()
            return

        try:
            self._generate_and_display_qr()
        except ValueError as e:
            # Don't show error popup, just clear the display
            # Errors will be visible when user tries to generate with invalid data
            self._clear_qr_display()
        except Exception as e:
            # Only show unexpected errors
            self._show_error(f"An unexpected error occurred: {str(e)}")

    def _generate_and_display_qr(self) -> None:
        """Generate QR code and display it in the UI."""
        ssid = self.ssid_var.get().strip()
        password = self.password_var.get() if self.security_var.get() != "nopass" else None
        security: Literal["WPA", "WEP", "nopass"] = self.security_var.get()
        hidden = self.hidden_var.get()

        # Generate QR code
        qr = wifi_qr_generator.generate_wifi_qr(
            ssid=ssid,
            password=password,
            security=security,
            hidden=hidden
        )

        self.current_qr = qr
        self.current_ssid = ssid

        # Export to PNG
        png_buffer = wifi_qr_generator.export_to_png(qr, scale=8)
        image = Image.open(png_buffer)
        photo = ImageTk.PhotoImage(image)

        # Update display
        self.qr_label.config(image=photo, text="")
        self.qr_label.image = photo  # Keep a reference

        # Update action buttons
        self._update_action_buttons()

    def _clear_qr_display(self) -> None:
        """Clear the QR code display."""
        self.qr_label.config(image="", text="Enter network name to generate QR code")
        self.qr_label.image = None
        self.current_qr = None
        self.current_ssid = ""

        # Clear action buttons
        for widget in self.actions_frame.winfo_children():
            widget.destroy()

    def _update_action_buttons(self) -> None:
        """Update the action buttons frame."""
        # Clear existing buttons
        for widget in self.actions_frame.winfo_children():
            widget.destroy()

        if not self.current_qr:
            return

        # Download PNG button
        download_png_btn = tk.Button(
            self.actions_frame,
            text="⬇️ Download PNG",
            command=self._download_png,
            width=20,
            pady=5
        )
        download_png_btn.pack(side=tk.LEFT, padx=5)

        # Download HTML button
        download_html_btn = tk.Button(
            self.actions_frame,
            text="🖨️ Print Friendly HTML",
            command=self._download_html,
            width=20,
            pady=5
        )
        download_html_btn.pack(side=tk.LEFT, padx=5)

    def _download_png(self) -> None:
        """Save QR code as PNG file."""
        if not self.current_qr:
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            initialfile=f"wifi_qr_{self.current_ssid}.png"
        )

        if filename:
            try:
                png_buffer = wifi_qr_generator.export_to_png(self.current_qr, scale=10)
                with open(filename, "wb") as f:
                    f.write(png_buffer.getvalue())
                messagebox.showinfo("Success", f"QR code saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")

    def _download_html(self) -> None:
        """Save QR code as printable HTML file."""
        if not self.current_qr:
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")],
            initialfile=f"wifi_qr_print_{self.current_ssid}.html"
        )

        if filename:
            try:
                html_content = print_template.get_printable_html(
                    self.current_qr,
                    self.current_ssid
                )
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(html_content)
                messagebox.showinfo("Success", f"HTML file saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")

    def _show_error(self, message: str) -> None:
        """Display an error message."""
        messagebox.showerror("Error", message)


def main() -> None:
    """Main entry point for the application."""
    root = tk.Tk()
    app = WiFiQRApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
