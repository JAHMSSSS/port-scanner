import socket
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk
from tkinter import scrolledtext, messagebox
import pyfiglet

def scan_port(host, port):
    """Scans a single port on the given host."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)  # Set timeout to 1 second
        try:
            s.connect((host, port))
            protocol_name = socket.getservbyport(port)
            return port, True, protocol_name
        except:
            return port, False, None

def scan_ports(host, ports):
    """Scans multiple ports on the given host."""
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(lambda port: scan_port(host, port), ports)
        return list(results)

def start_scan():
    host = host_entry.get()
    port_range = ports_entry.get()
    
    if not host:
        messagebox.showerror("Input Error", "Please enter a host.")
        return
    
    if not port_range:
        messagebox.showerror("Input Error", "Please enter a port range.")
        return
    
    try:
        start_port, end_port = map(int, port_range.split('-'))
    except ValueError:
        messagebox.showerror("Input Error", "Invalid port range format. Use 'start-end'.")
        return

    ports = range(start_port, end_port + 1)
    open_ports = scan_ports(host, ports)
    
    result_text.delete(1.0, tk.END)
    for port, is_open, protocol in open_ports:
        if is_open:
            result_text.insert(tk.END, f"Port {port} is open (Protocol: {protocol if protocol else 'Unknown'}).\n")
    
    result_text.insert(tk.END, "\nScan Complete.\n")

def show_scanner():
    run_button.grid_remove()
    ascii_art_label.grid_remove()
    
    host_label.grid(row=0, column=0, padx=5, pady=5)
    host_entry.grid(row=0, column=1, padx=5, pady=5)
    ports_label.grid(row=1, column=0, padx=5, pady=5)
    ports_entry.grid(row=1, column=1, padx=5, pady=5)
    start_button.grid(row=2, column=0, columnspan=2, pady=10)
    result_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Create the main window
root = tk.Tk()
root.title("PORT SCANNER")

# Set background color for the window
root.configure(bg="#282c34")

# Create initial interface with pyfiglet ASCII art
ascii_art = pyfiglet.figlet_format("OCEANNE")
ascii_art_label = tk.Label(root, text=ascii_art, font=("Courier", 12), justify=tk.LEFT, fg="#61dafb", bg="#282c34")
ascii_art_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Create "Run" button
run_button = tk.Button(root, text="Run", command=show_scanner, bg="#61dafb", fg="#282c34")
run_button.grid(row=1, column=0, columnspan=2, pady=10)

# Create scanner interface widgets but don't show them initially
host_label = tk.Label(root, text="Host:", fg="#61dafb", bg="#282c34")
host_entry = tk.Entry(root, width=40, bg="#abb2bf", fg="#282c34")

ports_label = tk.Label(root, text="Ports (start-end):", fg="#61dafb", bg="#282c34")
ports_entry = tk.Entry(root, width=40, bg="#abb2bf", fg="#282c34")

start_button = tk.Button(root, text="Start Scan", command=start_scan, bg="#61dafb", fg="#282c34")

result_text = scrolledtext.ScrolledText(root, width=60, height=20, bg="#abb2bf", fg="#282c34")

# Run the GUI event loop
root.mainloop()
