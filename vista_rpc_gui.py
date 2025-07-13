import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from vista_rpc_client import VistARPCClient

class VistARPCGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("VistA RPC Client")
        self.root.geometry("800x600")

        self.client = None

        # Style
        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')

        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Connection Frame
        self.conn_frame = ttk.LabelFrame(self.main_frame, text="Connection Details", padding="10")
        self.conn_frame.pack(fill=tk.X, pady=5)

        ttk.Label(self.conn_frame, text="Host:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.host_entry = ttk.Entry(self.conn_frame, width=20)
        self.host_entry.grid(row=0, column=1, padx=5, pady=5)
        self.host_entry.insert(0, "localhost")

        ttk.Label(self.conn_frame, text="Port:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.port_entry = ttk.Entry(self.conn_frame, width=10)
        self.port_entry.grid(row=0, column=3, padx=5, pady=5)
        self.port_entry.insert(0, "9297")

        ttk.Label(self.conn_frame, text="Access Code:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.access_code_entry = ttk.Entry(self.conn_frame, width=20)
        self.access_code_entry.grid(row=1, column=1, padx=5, pady=5)
        self.access_code_entry.insert(0, "gtmuser")

        ttk.Label(self.conn_frame, text="Verify Code:").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.verify_code_entry = ttk.Entry(self.conn_frame, width=20, show="*")
        self.verify_code_entry.grid(row=1, column=3, padx=5, pady=5)
        self.verify_code_entry.insert(0, "GT.M Rocks!")
        
        ttk.Label(self.conn_frame, text="Context:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.context_entry = ttk.Entry(self.conn_frame, width=20)
        self.context_entry.grid(row=2, column=1, padx=5, pady=5)
        self.context_entry.insert(0, "XWB BROKER EXAMPLE")

        self.connect_button = ttk.Button(self.conn_frame, text="Connect", command=self.toggle_connection)
        self.connect_button.grid(row=2, column=3, padx=5, pady=5, sticky=tk.E)

        # RPC and Parameters Frame
        self.rpc_frame = ttk.Frame(self.main_frame)
        self.rpc_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # RPC List
        self.rpc_list_frame = ttk.LabelFrame(self.rpc_frame, text="Available RPCs", padding="10")
        self.rpc_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.rpc_listbox = tk.Listbox(self.rpc_list_frame)
        self.rpc_listbox.pack(fill=tk.BOTH, expand=True)
        self.rpc_listbox.bind('<<ListboxSelect>>', self.on_rpc_select)

        # Parameters
        self.params_frame = ttk.LabelFrame(self.rpc_frame, text="Parameters", padding="10")
        self.params_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        self.params_text = scrolledtext.ScrolledText(self.params_frame, height=10, state='disabled')
        self.params_text.pack(fill=tk.BOTH, expand=True)

        # Results Frame
        self.results_frame = ttk.LabelFrame(self.main_frame, text="Results", padding="10")
        self.results_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.results_text = scrolledtext.ScrolledText(self.results_frame, height=10)
        self.results_text.pack(fill=tk.BOTH, expand=True)

    def toggle_connection(self):
        if not self.client or not self.client.connected:
            self.connect()
        else:
            self.disconnect()

    def connect(self):
        host = self.host_entry.get()
        port = int(self.port_entry.get())
        access_code = self.access_code_entry.get()
        verify_code = self.verify_code_entry.get()
        context = self.context_entry.get()

        self.client = VistARPCClient(host, port, access_code, verify_code, context)
        self.client.connect()

        if self.client.connected:
            if self.client.login():
                self.client.create_context()
                self.connect_button.config(text="Disconnect")
                self.load_rpc_list()
            else:
                messagebox.showerror("Login Failed", "Please check your credentials.")
                self.disconnect()
        else:
            messagebox.showerror("Connection Failed", "Could not connect to the VistA server.")

    def disconnect(self):
        if self.client:
            self.client.disconnect()
        self.connect_button.config(text="Connect")
        self.rpc_listbox.delete(0, tk.END)
        self.params_text.config(state='normal')
        self.params_text.delete(1.0, tk.END)
        self.params_text.config(state='disabled')
        self.results_text.delete(1.0, tk.END)

    def load_rpc_list(self):
        self.rpc_listbox.delete(0, tk.END)
        response = self.client.call_rpc("XWB LIST ALL RPCS")
        if response:
            rpcs = response.strip().split('\n')
            for rpc in rpcs:
                self.rpc_listbox.insert(tk.END, rpc)

    def on_rpc_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            rpc_name = event.widget.get(index)
            self.display_rpc_parameters(rpc_name)

    def display_rpc_parameters(self, rpc_name):
        self.params_text.config(state='normal')
        self.params_text.delete(1.0, tk.END)

        if not self.client or not self.client.connected:
            self.params_text.insert(tk.END, "Not connected.")
            self.params_text.config(state='disabled')
            return

        self.params_text.insert(tk.END, f"Fetching details for: {rpc_name}...\n\n")

        # Use 'XWB RPC LIST' to get details for the selected RPC
        params = [('literal', rpc_name)]
        response = self.client.call_rpc("XWB RPC LIST", params)

        self.params_text.delete(1.0, tk.END)  # Clear the "fetching" message

        if response:
            # The first line is often the RPC name itself, so we can optionally skip it
            details = response.strip().split('\n')[1:] 
            self.params_text.insert(tk.END, "\n".join(details) if details else "No details found.")
        else:
            self.params_text.insert(tk.END, f"Could not retrieve details for {rpc_name}.")

        self.params_text.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = VistARPCGUI(root)
    root.mainloop()
