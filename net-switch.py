import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import time
import re
import html
import string

# ----------------------
# Input Sanitization Functions
# ----------------------

def sanitize_string(text, max_length=255):
    """Sanitize string input to prevent injection attacks and ensure safe processing"""
    if not isinstance(text, str):
        return ""
    
    # Remove null bytes and control characters except newline and tab
    sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]', '', text)
    
    # Truncate to max length
    sanitized = sanitized[:max_length]
    
    # Strip leading/trailing whitespace
    sanitized = sanitized.strip()
    
    return sanitized

def sanitize_network_adapter_name(adapter_name):
    """Sanitize network adapter name for netsh commands"""
    if not isinstance(adapter_name, str):
        return "Wi-Fi"
    
    # Only allow alphanumeric, spaces, hyphens, underscores, and parentheses
    sanitized = re.sub(r'[^a-zA-Z0-9\s\-_()]', '', adapter_name)
    sanitized = sanitized.strip()
    
    # If empty or too long, default to Wi-Fi
    if not sanitized or len(sanitized) > 100:
        return "Wi-Fi"
    
    return sanitized

def validate_dns_server_name(dns_name):
    """Validate DNS server selection name"""
    allowed_dns_names = [
        "AU - Cloudflare (1.1.1.1, 1.0.0.1)",
        "Google (8.8.8.8, 8.8.4.4)", 
        "Quad9 (9.9.9.9, 149.112.112.112)",
        "Custom..."
    ]
    return dns_name in allowed_dns_names

def sanitize_command_args(args):
    """Sanitize command line arguments to prevent injection"""
    if not isinstance(args, list):
        return []
    
    sanitized_args = []
    for arg in args:
        if isinstance(arg, str):
            # Remove dangerous characters and limit length
            sanitized = re.sub(r'[;&|`$()<>]', '', arg)
            sanitized = sanitized[:100]  # Limit argument length
            sanitized_args.append(sanitized)
        else:
            sanitized_args.append(str(arg)[:100])
    
    return sanitized_args

# ----------------------
# Core DNS Functions
# ----------------------

def is_valid_ip(ip):
    """Enhanced IPv4 validation with sanitization"""
    if not isinstance(ip, str):
        return False
    
    # Sanitize input
    ip = sanitize_string(ip, 15)  # Max IPv4 length is 15 chars
    
    # Basic format check
    pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    if not re.match(pattern, ip):
        return False
    
    # Validate each octet
    try:
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        
        for part in parts:
            num = int(part)
            if not (0 <= num <= 255):
                return False
            # No leading zeros (except for 0 itself)
            if len(part) > 1 and part[0] == '0':
                return False
        return True
    except (ValueError, IndexError):
        return False

def is_valid_ipv6(ip):
    """Validate IPv6 addresses"""
    if not isinstance(ip, str):
        return False
    
    # Sanitize input
    ip = sanitize_string(ip, 45)  # Max IPv6 length
    
    # Basic IPv6 pattern (simplified)
    pattern = r'^([0-9a-fA-F]{0,4}:){1,7}[0-9a-fA-F]{0,4}$|^::1$|^::$'
    return bool(re.match(pattern, ip))

def apply_dns(dns1, dns2, adapter_name="Wi-Fi"):
    """Apply DNS with enhanced validation and sanitization"""
    # Sanitize and validate inputs
    dns1 = sanitize_string(dns1, 45)  # Support both IPv4 and IPv6
    dns2 = sanitize_string(dns2, 45)
    adapter_name = sanitize_network_adapter_name(adapter_name)
    
    # Validate DNS addresses
    if not (is_valid_ip(dns1) and is_valid_ip(dns2)):
        if not (is_valid_ipv6(dns1) and is_valid_ipv6(dns2)):
            messagebox.showerror("Invalid Input", "Please enter valid IPv4 or IPv6 addresses for DNS.")
            return False
    
    try:
        # Use sanitized arguments for subprocess
        cmd1 = ["netsh", "interface", "ip", "set", "dns", f"name={adapter_name}", "static", dns1]
        cmd2 = ["netsh", "interface", "ip", "add", "dns", f"name={adapter_name}", dns2, "index=2"]
        
        # Sanitize command arguments
        cmd1 = sanitize_command_args(cmd1)
        cmd2 = sanitize_command_args(cmd2)
        
        subprocess.run(cmd1, check=True, timeout=30)
        subprocess.run(cmd2, check=True, timeout=30)
        
        messagebox.showinfo("Success", f"DNS applied: {html.escape(dns1)}, {html.escape(dns2)}")
        return True
    except subprocess.TimeoutExpired:
        messagebox.showerror("Error", "Command timed out. Please try again.")
        return False
    except Exception as e:
        error_msg = sanitize_string(str(e), 200)
        messagebox.showerror("Error", f"Failed to apply DNS: {html.escape(error_msg)}")
        return False

def flush_dns():
    """Flush DNS cache with enhanced security"""
    try:
        # Use fixed command arguments to prevent injection
        cmd = ["ipconfig", "/flushdns"]
        result = subprocess.run(cmd, check=True, timeout=30, capture_output=True, text=True)
        messagebox.showinfo("Success", "DNS cache flushed successfully!")
        return True
    except subprocess.TimeoutExpired:
        messagebox.showerror("Error", "Command timed out. Please try again.")
        return False
    except Exception as e:
        error_msg = sanitize_string(str(e), 200)
        messagebox.showerror("Error", f"Failed to flush DNS: {html.escape(error_msg)}")
        return False

def test_dns(dns):
    """Test DNS with enhanced validation and sanitization"""
    # Sanitize and validate DNS address
    dns = sanitize_string(dns, 45)
    if not (is_valid_ip(dns) or is_valid_ipv6(dns)):
        return None
    
    start = time.time()
    try:
        # Use sanitized arguments and timeout
        cmd = ["ping", "-n", "1", dns]
        cmd = sanitize_command_args(cmd)
        
        result = subprocess.run(
            cmd, 
            check=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            timeout=10,
            text=True
        )
        end = time.time()
        return round((end - start) * 1000, 2)  # ms
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, Exception):
        return None

def find_fastest_dns():
    """Find fastest DNS with predefined safe list"""
    # Use only trusted, hardcoded DNS servers
    dns_list = ["1.1.1.1", "8.8.8.8", "9.9.9.9", "208.67.222.222"]
    fastest = None
    best_time = float("inf")
    
    for dns in dns_list:
        if not is_valid_ip(dns):  # Extra validation
            continue
            
        response_time = test_dns(dns)
        if response_time and response_time < best_time:
            best_time = response_time
            fastest = dns
    
    return fastest, best_time if fastest else (None, None)

# ----------------------
# GUI
# ----------------------


class NetSwitchApp:
    def get_adapters(self):
        """Get network adapters with enhanced security and validation"""
        try:
            # Use fixed command to prevent injection
            cmd = ["netsh", "interface", "show", "interface"]
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=15,
                check=True
            )
            
            adapters = ["All Network Adapters"]
            
            for line in result.stdout.splitlines():
                line = sanitize_string(line, 200)  # Sanitize each line
                
                if "Enabled" in line or "Disabled" in line:
                    parts = line.split()
                    if len(parts) > 3:
                        adapter_name = parts[-1]
                        # Validate adapter name
                        adapter_name = sanitize_network_adapter_name(adapter_name)
                        if adapter_name and adapter_name != "Wi-Fi":  # Avoid duplicates
                            adapters.append(adapter_name)
            
            # Ensure we always have at least the default options
            if len(adapters) == 1:
                adapters.extend(["Wi-Fi", "Ethernet", "Local Area Connection"])
                
            return adapters[:20]  # Limit to prevent UI overflow
            
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, Exception):
            # Fallback to safe defaults if command fails
            return ["All Network Adapters", "Wi-Fi", "Ethernet", "Local Area Connection"]


    def __init__(self, root):
            self.root = root
            
            # Sanitize and validate window title
            title = sanitize_string("NetSwitch v1.0", 50)
            self.root.title(title)
            self.root.geometry("620x550")
            self.root.resizable(False, False)
            self.root.configure(fg_color="#f0f0f0")  # Light grey background
            ctk.set_appearance_mode("light")
            ctk.set_default_color_theme("blue")

            # Initialize sanitized theme and status variables
            self.theme = "Light"
            self.show_status = True

            # Top menu bar
            menu_bar = ctk.CTkFrame(self.root, height=36)
            menu_bar.pack(fill='x', side='top')
            menu_label = ctk.CTkLabel(
                menu_bar, text="NetSwitch", font=("Segoe UI", 16, "bold"),
                text_color=("#9370db", "#dda0dd")
            )
            menu_label.pack(side='left', padx=12, pady=4)
            exit_btn = ctk.CTkButton(menu_bar, text="Exit", width=60, command=self.safe_exit,
                                   fg_color=("#dc3545", "#c82333"), hover_color=("#c82333", "#dc3545"))
            exit_btn.pack(side='right', padx=12, pady=4)

            # Logo/Icon (sanitized text)
            logo_text = sanitize_string("🌐 NetSwitch", 30)
            logo_label = ctk.CTkLabel(self.root, text=logo_text, font=("Segoe UI", 18, "bold"),
                                    text_color=("#9370db", "#dda0dd"))
            logo_label.pack(pady=(10, 0))

            # Main Frame
            main_frame = ctk.CTkFrame(self.root)
            main_frame.pack(fill='both', expand=True, padx=10, pady=5)

            # Section: Network Adapter
            adapter_label = ctk.CTkLabel(main_frame, text="Select Network Adapter", font=("Segoe UI", 10, "bold"))
            adapter_label.grid(row=0, column=0, sticky='w', pady=(0, 2))
            self.adapter_choice = ctk.CTkComboBox(main_frame, values=self.get_adapters(), width=260)
            self.adapter_choice.set(self.get_adapters()[0])
            self.adapter_choice.grid(row=1, column=0, sticky='w', pady=(0, 10))

            # Section: Preset DNS
            preset_label = ctk.CTkLabel(main_frame, text="Choose a DNS Server", font=("Segoe UI", 10, "bold"))
            preset_label.grid(row=2, column=0, sticky='w', pady=(0, 2))
            
            # Validate DNS choices
            dns_options = [
                "AU - Cloudflare (1.1.1.1, 1.0.0.1)",
                "Google (8.8.8.8, 8.8.4.4)",
                "Quad9 (9.9.9.9, 149.112.112.112)",
                "Custom..."
            ]
            self.dns_choice = ctk.CTkComboBox(main_frame, values=dns_options, width=260)
            self.dns_choice.set(dns_options[0])
            self.dns_choice.grid(row=3, column=0, sticky='w', pady=(0, 10))
            self.dns_choice.bind("<<ComboboxSelected>>", self.on_dns_choice)

            # Section: Custom DNS
            self.custom_frame = ctk.CTkFrame(main_frame)
            self.custom_frame.grid(row=4, column=0, sticky='ew', pady=(0, 10))
            self.custom_frame.grid_remove()
            ctk.CTkLabel(self.custom_frame, text="Primary DNS:").grid(row=0, column=0, sticky='w')
            self.custom_dns1 = ctk.CTkEntry(self.custom_frame, width=120, placeholder_text="e.g. 8.8.8.8")
            self.custom_dns1.grid(row=0, column=1, padx=(5, 0))
            ctk.CTkLabel(self.custom_frame, text="Secondary DNS:").grid(row=1, column=0, sticky='w')
            self.custom_dns2 = ctk.CTkEntry(self.custom_frame, width=120, placeholder_text="e.g. 8.8.4.4")
            self.custom_dns2.grid(row=1, column=1, padx=(5, 0))

            # IPv6 Option
            self.use_ipv6 = tk.BooleanVar()
            self.ipv6_check = ctk.CTkCheckBox(self.custom_frame, text="Use IPv6 DNS", variable=self.use_ipv6, command=self.toggle_ipv6)
            self.ipv6_check.grid(row=2, column=0, sticky='w', pady=(5, 0))
            self.custom_dns1_v6 = ctk.CTkEntry(self.custom_frame, width=120, placeholder_text="e.g. 2001:4860:4860::8888")
            self.custom_dns2_v6 = ctk.CTkEntry(self.custom_frame, width=120, placeholder_text="e.g. 2001:4860:4860::8844")

            # Section: Buttons (with icons and color)
            btn_frame = ctk.CTkFrame(main_frame)
            btn_frame.grid(row=5, column=0, pady=(5, 10), sticky='ew')
            self.apply_btn = ctk.CTkButton(
                btn_frame, text="💾 Apply DNS", command=self.apply_dns_action,
                fg_color=("#1976d2", "#1565c0"), hover_color=("#1565c0", "#1976d2")
            )
            self.apply_btn.grid(row=0, column=0, padx=5)
            self.fastest_btn = ctk.CTkButton(
                btn_frame, text="⚡ Fastest DNS", command=self.fastest_dns_action,
                fg_color=("#43a047", "#2e7d32"), hover_color=("#2e7d32", "#43a047")
            )
            self.fastest_btn.grid(row=0, column=1, padx=5)
            self.flush_btn = ctk.CTkButton(
                btn_frame, text="🧹 Flush DNS", command=self.flush_dns_action,
                fg_color=("#ac841f", "#f9a825"), hover_color=("#ac841f", "#ac841f")
            )
            self.flush_btn.grid(row=0, column=2, padx=5)
            self.options_btn = ctk.CTkButton(
                btn_frame, text="⚙️ Options", command=self.show_options,
                fg_color=("#607d8b", "#37474f"), hover_color=("#37474f", "#607d8b")
            )
            self.options_btn.grid(row=0, column=3, padx=5)

            # Section: Status Bar
            self.status = tk.StringVar()
            self.status.set("Ready.")
            self.status_bar = ctk.CTkLabel(self.root, textvariable=self.status, height=28, anchor='w', font=("Segoe UI", 10))
            self.status_bar.pack(side='bottom', fill='x')
    
    def safe_exit(self):
        """Safely exit the application"""
        try:
            self.root.destroy()
        except Exception:
            import sys
            sys.exit(0)
    def toggle_ipv6(self):
        if self.use_ipv6.get():
            ctk.CTkLabel(self.custom_frame, text="Primary IPv6 DNS:").grid(row=3, column=0, sticky='w')
            self.custom_dns1_v6.grid(row=3, column=1, padx=(5, 0))
            ctk.CTkLabel(self.custom_frame, text="Secondary IPv6 DNS:").grid(row=4, column=0, sticky='w')
            self.custom_dns2_v6.grid(row=4, column=1, padx=(5, 0))
        else:
            self.custom_dns1_v6.grid_remove()
            self.custom_dns2_v6.grid_remove()


    def show_options(self):
        """Options dialog with enhanced input validation"""
        try:
            options_win = ctk.CTkToplevel(self.root)
            options_win.title("Options")
            options_win.geometry("340x280")
            options_win.resizable(False, False)
            options_win.grab_set()

            # Theme selection with validation
            ctk.CTkLabel(options_win, text="Theme:", font=("Segoe UI", 10, "bold")).pack(pady=(15, 5), anchor='w', padx=20)
            
            # Validate current theme
            current_theme = getattr(self, 'theme', 'Light')
            if current_theme not in ['Light', 'Dark']:
                current_theme = 'Light'
                
            theme_var = tk.StringVar(value=current_theme)
            theme_frame = ctk.CTkFrame(options_win, fg_color="transparent")
            theme_frame.pack(anchor='w', padx=20)
            ctk.CTkRadioButton(theme_frame, text="Light", variable=theme_var, value="Light").pack(side='left', padx=5)
            ctk.CTkRadioButton(theme_frame, text="Dark", variable=theme_var, value="Dark").pack(side='left', padx=5)

            # Status bar toggle with validation
            current_status = getattr(self, 'show_status', True)
            if not isinstance(current_status, bool):
                current_status = True
                
            status_var = tk.BooleanVar(value=current_status)
            status_frame = ctk.CTkFrame(options_win, fg_color="transparent")
            status_frame.pack(anchor='w', padx=20, pady=(15, 0))
            ctk.CTkCheckBox(status_frame, text="Show Status Bar", variable=status_var).pack(side='left')

            def save_options():
                try:
                    # Validate and sanitize theme selection
                    theme = theme_var.get()
                    if theme not in ['Light', 'Dark']:
                        theme = 'Light'
                    
                    # Validate status bar setting
                    show_status = bool(status_var.get())
                    
                    # Apply validated settings
                    self.theme = theme
                    self.show_status = show_status
                    self.apply_theme(self.theme)
                    self.toggle_status_bar(self.show_status)
                    options_win.destroy()
                    
                except Exception as e:
                    error_msg = sanitize_string(str(e), 100)
                    messagebox.showerror("Error", f"Failed to save options: {html.escape(error_msg)}")

            ctk.CTkButton(options_win, text="Save", command=save_options).pack(pady=20)
            
        except Exception as e:
            error_msg = sanitize_string(str(e), 100)
            messagebox.showerror("Error", f"Failed to open options: {html.escape(error_msg)}")

    def toggle_status_bar(self, show):
        """Toggle status bar with validation"""
        try:
            # Validate input
            if not isinstance(show, bool):
                show = True
                
            # Show or hide the status bar
            if show:
                self.status_bar.pack(side='bottom', fill='x')
            else:
                self.status_bar.pack_forget()
                
        except Exception:
            # Ensure status bar is shown on error
            try:
                self.status_bar.pack(side='bottom', fill='x')
            except:
                pass

    def apply_theme(self, theme):
        """Apply theme with validation"""
        try:
            # Sanitize and validate theme
            theme = sanitize_string(str(theme), 20)
            if theme.lower() not in ['light', 'dark']:
                theme = 'light'
            
            # Use customtkinter's appearance mode for light/dark
            ctk.set_appearance_mode(theme.lower())
            
        except Exception:
            # Fallback to light theme if error
            ctk.set_appearance_mode("light")

    def on_dns_choice(self, event=None):
        """Handle DNS choice selection with validation"""
        try:
            choice = self.dns_choice.get()
            choice = sanitize_string(choice, 100)
            
            # Validate the choice is from our allowed list
            if validate_dns_server_name(choice):
                if choice == "Custom...":
                    self.custom_frame.grid()
                else:
                    self.custom_frame.grid_remove()
            else:
                # Reset to safe default if invalid choice
                self.dns_choice.set("AU - Cloudflare (1.1.1.1, 1.0.0.1)")
                self.custom_frame.grid_remove()
        except Exception:
            # Fallback to safe state
            self.dns_choice.set("AU - Cloudflare (1.1.1.1, 1.0.0.1)")
            self.custom_frame.grid_remove()

    def set_status(self, msg):
        """Set status message with sanitization"""
        try:
            sanitized_msg = sanitize_string(str(msg), 200)
            sanitized_msg = html.escape(sanitized_msg)
            self.status.set(sanitized_msg)
            self.root.update_idletasks()
        except Exception:
            self.status.set("Ready.")

    def get_custom_dns_input(self):
        """Get and validate custom DNS input"""
        try:
            dns1 = sanitize_string(self.custom_dns1.get().strip(), 45)
            dns2 = sanitize_string(self.custom_dns2.get().strip(), 45)
            
            # Validate both addresses
            if self.use_ipv6.get():
                dns1_v6 = sanitize_string(self.custom_dns1_v6.get().strip(), 45)
                dns2_v6 = sanitize_string(self.custom_dns2_v6.get().strip(), 45)
                
                if dns1_v6 and dns2_v6:
                    if is_valid_ipv6(dns1_v6) and is_valid_ipv6(dns2_v6):
                        return dns1_v6, dns2_v6
                    else:
                        messagebox.showerror("Invalid Input", "Please enter valid IPv6 addresses.")
                        return None, None
            
            if is_valid_ip(dns1) and is_valid_ip(dns2):
                return dns1, dns2
            else:
                messagebox.showerror("Invalid Input", "Please enter valid IP addresses.")
                return None, None
                
        except Exception:
            messagebox.showerror("Error", "Invalid DNS input format.")
            return None, None

    def apply_dns_action(self):
        self.set_status("Applying DNS...")
        self.apply_btn.configure(state='disabled')
        self.root.after(100, self._apply_dns_action)

    def _apply_dns_action(self):
        """Apply DNS with enhanced validation and sanitization"""
        try:
            choice = sanitize_string(self.dns_choice.get(), 100)
            adapter = sanitize_network_adapter_name(self.adapter_choice.get())
            
            # Validate DNS choice
            if not validate_dns_server_name(choice):
                self.set_status("Invalid DNS server selection.")
                self.apply_btn.configure(state='normal')
                return
            
            # Get DNS addresses based on choice
            if "Cloudflare" in choice:
                dns1, dns2 = "1.1.1.1", "1.0.0.1"
            elif "Google" in choice:
                dns1, dns2 = "8.8.8.8", "8.8.4.4"
            elif "Quad9" in choice:
                dns1, dns2 = "9.9.9.9", "149.112.112.112"
            else:  # Custom
                dns1, dns2 = self.get_custom_dns_input()
                if not dns1 or not dns2:
                    self.apply_btn.configure(state='normal')
                    return
            
            # Use selected adapter, default to Wi-Fi if invalid
            adapter_name = adapter if adapter != "All Network Adapters" else "Wi-Fi"
            
            # Apply DNS with enhanced security
            success = apply_dns(dns1, dns2, adapter_name)
            
            if success:
                self.set_status(f"DNS applied: {dns1}, {dns2}")
            else:
                self.set_status("Failed to apply DNS.")
                
        except Exception as e:
            error_msg = sanitize_string(str(e), 100)
            self.set_status(f"Error: {error_msg}")
        finally:
            self.apply_btn.configure(state='normal')

    def flush_dns_action(self):
        """Flush DNS cache with enhanced security"""
        self.set_status("Flushing DNS cache...")
        self.flush_btn.configure(state='disabled')
        
        def run():
            try:
                success = flush_dns()
                if success:
                    self.set_status("DNS cache flushed successfully.")
                else:
                    self.set_status("Failed to flush DNS cache.")
            except Exception as e:
                error_msg = sanitize_string(str(e), 100)
                self.set_status(f"Error flushing DNS: {error_msg}")
            finally:
                self.flush_btn.configure(state='normal')
                
        threading.Thread(target=run, daemon=True).start()

    def fastest_dns_action(self):
        """Find fastest DNS with enhanced security"""
        self.set_status("Testing fastest DNS...")
        self.fastest_btn.configure(state='disabled')
        
        def run():
            try:
                dns, time_ms = find_fastest_dns()
                if dns and time_ms:
                    safe_dns = html.escape(dns)
                    safe_time = html.escape(str(time_ms))
                    messagebox.showinfo("Fastest DNS", f"{safe_dns} ({safe_time} ms)")
                    self.set_status(f"Fastest DNS: {safe_dns} ({safe_time} ms)")
                else:
                    messagebox.showerror("Error", "No DNS servers reachable.")
                    self.set_status("No DNS servers reachable.")
            except Exception as e:
                error_msg = sanitize_string(str(e), 100)
                self.set_status(f"Error testing DNS: {error_msg}")
            finally:
                self.fastest_btn.configure(state='normal')
                
        threading.Thread(target=run, daemon=True).start()

# ----------------------
# Run Program
# ----------------------
if __name__ == "__main__":
    root = ctk.CTk()
    app = NetSwitchApp(root)
    root.mainloop()
