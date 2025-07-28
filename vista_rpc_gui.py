import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
import os

# Add the directory containing the vavista package to the Python path
sys.path.append(os.path.dirname(__file__))

from vavista.rpc import connect, PLiteral, PList, PReference, PEncoded

important_rpcs = [
    "ORQQAL LIST",
    "TIU SUMMARIES",
    "TIU DOCUMENTS BY CONTEXT",
    "TIU GET RECORD TEXT",
    "ORQQPL SELECTION LIST",
    "ORWU USERINFO",
    "ORQPT PROVIDER PATIENTS",
    "TIU LONG LIST OF TITLES",
    "ORWPT ENHANCED PATLOOKUP",
        "ORWPT LIST ALL",
        "ORWPT SELECT"
    ]

class VistARPCGUI(tk.Tk):

    def _select_patient(self, dfn):
        if not self.connection:
            messagebox.showwarning("RPC Error", "Not connected to VistA. Please connect first.")
            return

        self._log_status(f"Selecting patient with DFN: {dfn}")
        try:
            reply = self.connection.invoke("ORWPT SELECT", PLiteral(dfn))
            self._log_status(f"ORWPT SELECT Raw Reply: {reply!r}")
            # Optionally, you can parse the reply to confirm selection
            self._log_status(f"Successfully selected patient with DFN: {dfn}")
        except Exception as e:
            self._log_status(f"Failed to select patient: {e}")
            messagebox.showerror("RPC Error", f"Failed to select patient: {e}")

    def _search_patient(self):
        if not self.connection:
            messagebox.showwarning("RPC Error", "Not connected to VistA. Please connect first.")
            return

        search_term = self.search_patient_entry.get()
        if not search_term:
            messagebox.showwarning("Search Error", "Please enter a patient name to search.")
            return

        self._log_status(f"Searching for patient: {search_term}")
        try:
            # Using ORWPT LIST ALL for searching, as ENHANCED PATLOOKUP may not be available
            patients_reply = self.connection.invoke("ORWPT LIST ALL", PLiteral(search_term), PLiteral("1"))
            self._log_status(f"ORWPT LIST ALL Raw Reply: {patients_reply!r}")

            if patients_reply and patients_reply.strip():
                patients_list = patients_reply.split('\r\n')
                self.patients_data = []
                for patient_info in patients_list:
                    if patient_info.strip():
                        parts = patient_info.split('^')
                        if len(parts) >= 2:
                            dfn = parts[0]
                            name = parts[1]
                            self.patients_data.append({"DFN": dfn, "Name": name})
                
                if self.patients_data:
                    self._open_patient_selection()
                else:
                    messagebox.showinfo("Search Results", "No patients found matching the search criteria.")
            else:
                messagebox.showinfo("Search Results", "No patients found matching the search criteria or empty response.")

        except Exception as e:
            self._log_status(f"Failed to search for patients: {e}")
            messagebox.showerror("RPC Error", f"Failed to search for patients: {e}")

    def __init__(self, rpc_list, rpc_info):
        super().__init__()
        self.title("VistA RPC Client")
        self.geometry("1000x700")

        self.rpc_list = rpc_list
        self.rpc_info = rpc_info
        self.connection = None

        self._create_widgets()

    def _create_widgets(self):
        # Connection Frame
        conn_frame = ttk.LabelFrame(self, text="VistA Connection", padding="10")
        conn_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        ttk.Label(conn_frame, text="Host:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.host_entry = ttk.Entry(conn_frame, width=20)
        self.host_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        self.host_entry.insert(0, "127.0.0.1")

        ttk.Label(conn_frame, text="Port:").grid(row=0, column=2, padx=5, pady=2, sticky="w")
        self.port_entry = ttk.Entry(conn_frame, width=10)
        self.port_entry.grid(row=0, column=3, padx=5, pady=2, sticky="ew")
        self.port_entry.insert(0, "9297")

        ttk.Label(conn_frame, text="Access Code:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.access_entry = ttk.Entry(conn_frame, width=20, show="*")
        self.access_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        self.access_entry.insert(0, "DOCTOR1")

        ttk.Label(conn_frame, text="Verify Code:").grid(row=1, column=2, padx=5, pady=2, sticky="w")
        self.verify_entry = ttk.Entry(conn_frame, width=20, show="*")
        self.verify_entry.grid(row=1, column=3, padx=5, pady=2, sticky="ew")
        self.verify_entry.insert(0, "DOCTOR1.")

        ttk.Label(conn_frame, text="App Context:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.context_entry = ttk.Entry(conn_frame, width=30)
        self.context_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=2, sticky="ew")
        self.context_entry.insert(0, "OR CPRS GUI CHART")

        ttk.Label(conn_frame, text="Patient DFN:").grid(row=3, column=0, padx=5, pady=2, sticky="w")
        self.dfn_entry = ttk.Entry(conn_frame, width=20)
        self.dfn_entry.grid(row=3, column=1, padx=5, pady=2, sticky="ew")
        self.dfn_entry.insert(0, "100001") # Default DFN for testing

        self.connect_button = ttk.Button(conn_frame, text="Connect", command=self._connect_to_vista)
        self.connect_button.grid(row=3, column=3, padx=5, pady=2, sticky="ew")

        conn_frame.columnconfigure(1, weight=1)
        conn_frame.columnconfigure(3, weight=1)
        conn_frame.rowconfigure(3, weight=1) # Add weight to the DFN row

        # RPC Call Frame
        rpc_frame = ttk.LabelFrame(self, text="RPC Call", padding="10")
        rpc_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        ttk.Label(rpc_frame, text="Select RPC:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.rpc_combobox = ttk.Combobox(rpc_frame, values=self.rpc_list, state="readonly")
        self.rpc_combobox.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        self.rpc_combobox.set("ORWPT ID INFO") # Default RPC
        self.rpc_combobox.bind("<<ComboboxSelected>>", self._on_rpc_selected)

        ttk.Label(rpc_frame, text="Parameters (comma-separated):").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.params_entry = ttk.Entry(rpc_frame, width=50)
        self.params_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        self.params_entry.insert(0, "2") # Default parameter for ORWPT ID INFO

        ttk.Label(rpc_frame, text="RPC Description:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.rpc_description_text = scrolledtext.ScrolledText(rpc_frame, wrap=tk.WORD, height=3, width=50)
        self.rpc_description_text.grid(row=3, column=0, columnspan=2, padx=5, pady=2, sticky="ew")

        ttk.Label(rpc_frame, text="Expected Parameters:").grid(row=4, column=0, padx=5, pady=2, sticky="w")
        self.rpc_expected_params_text = scrolledtext.ScrolledText(rpc_frame, wrap=tk.WORD, height=3, width=50)
        self.rpc_expected_params_text.grid(row=5, column=0, columnspan=2, padx=5, pady=2, sticky="ew")

        self.invoke_button = ttk.Button(rpc_frame, text="Invoke RPC", command=self._invoke_rpc, state=tk.DISABLED)
        self.invoke_button.grid(row=6, column=0, padx=5, pady=5, sticky="ew")

        self.get_patients_button = ttk.Button(rpc_frame, text="Get Doctor's Patients", command=self._get_doctor_patients, state=tk.DISABLED)
        self.get_patients_button.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

        self.search_patient_entry = ttk.Entry(rpc_frame, width=50)
        self.search_patient_entry.grid(row=7, column=0, padx=5, pady=5, sticky="ew")
        self.search_patient_button = ttk.Button(rpc_frame, text="Search Patient", command=self._search_patient, state=tk.DISABLED)
        self.search_patient_button.grid(row=7, column=1, padx=5, pady=5, sticky="ew")

        self.select_patient_button = ttk.Button(rpc_frame, text="Select Patient", command=self._open_patient_selection, state=tk.DISABLED)
        self.select_patient_button.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        rpc_frame.columnconfigure(1, weight=1)
        rpc_frame.rowconfigure(3, weight=1)
        rpc_frame.rowconfigure(5, weight=1)

        # Informative Displays
        display_frame = ttk.LabelFrame(self, text="RPC Response & Status", padding="10")
        display_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        ttk.Label(display_frame, text="Raw RPC Response:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.raw_response_text = scrolledtext.ScrolledText(display_frame, wrap=tk.WORD, height=10)
        self.raw_response_text.grid(row=1, column=0, columnspan=2, padx=5, pady=2, sticky="nsew")

        ttk.Label(display_frame, text="Status Messages:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.status_text = scrolledtext.ScrolledText(display_frame, wrap=tk.WORD, height=5)
        self.status_text.grid(row=3, column=0, columnspan=2, padx=5, pady=2, sticky="nsew")

        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(1, weight=1)
        display_frame.rowconfigure(3, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

    def _on_rpc_selected(self, event=None):
        selected_rpc = self.rpc_combobox.get()
        info = self.rpc_info.get(selected_rpc, {})
        
        description = info.get("description", "No description available.")
        parameters = info.get("parameters", "No parameters found.")

        self.rpc_description_text.delete(1.0, tk.END)
        self.rpc_description_text.insert(tk.END, description)

        self.rpc_expected_params_text.delete(1.0, tk.END)
        self.rpc_expected_params_text.insert(tk.END, parameters)

        self.params_entry.delete(0, tk.END)

        if selected_rpc == "ORQQAL LIST" or selected_rpc == "TIU SUMMARIES":
            dfn = self.dfn_entry.get()
            if dfn:
                self.params_entry.insert(0, f"literal:{dfn}")
            else:
                self._log_status("Please enter a Patient DFN for this RPC.")
        elif selected_rpc == "TIU DOCUMENTS BY CONTEXT":
            self.rpc_expected_params_text.configure(state="normal")
            self.rpc_expected_params_text.delete(1.0, tk.END)
            self.rpc_expected_params_text.insert(tk.END, "Parameters: Context (e.g., 3), Patient.DFN, EarlyDate (optional), LateDate (optional), Person (optional), OccLimit (optional), SortSeq (optional), SHOW_ADDENDA (optional). Example: 3;literal:100001;literal:2023-01-01;literal:2023-12-31")
            self.rpc_expected_params_text.configure(state="disabled")
        elif selected_rpc == "TIU GET RECORD TEXT":
            self.rpc_expected_params_text.configure(state="normal")
            self.rpc_expected_params_text.delete(1.0, tk.END)
            self.rpc_expected_params_text.insert(tk.END, "Parameters: IEN (Internal Entry Number) of the note. Example: literal:1234567")
            self.rpc_expected_params_text.configure(state="disabled")
        elif selected_rpc == "ORQQPL SELECTION LIST":
            self.rpc_expected_params_text.configure(state="normal")
            self.rpc_expected_params_text.delete(1.0, tk.END)
            self.rpc_expected_params_text.insert(tk.END, "Parameters: (Optional) May take no parameters or a simple literal like 'ALL' or 'ACTIVE'. Check VistA documentation for specifics.")
            self.rpc_expected_params_text.configure(state="disabled")
            self.params_entry.insert(0, "") # Start with no parameters
        elif selected_rpc == "TIU LONG LIST OF TITLES":
            self.rpc_expected_params_text.configure(state="normal")
            self.rpc_expected_params_text.delete(1.0, tk.END)
            self.rpc_expected_params_text.insert(tk.END, "Parameters: DocumentClass (e.g., CLS_PROGRESS_NOTES, CLS_DC_SUMM), StartFrom, Direction (optional), IDNotesOnly (optional). Example: literal:CLS_PROGRESS_NOTES,literal:")
            self.rpc_expected_params_text.configure(state="disabled")
            self.params_entry.insert(0, "literal:CLS_PROGRESS_NOTES,literal:") # Default to progress notes, starting from beginning

    def _log_status(self, message):
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)

    def _connect_to_vista(self):
        host = self.host_entry.get()
        port = self.port_entry.get()
        access = self.access_entry.get()
        verify = self.verify_entry.get()
        context = self.context_entry.get()

        if not all([host, port, access, verify, context]):
            messagebox.showerror("Connection Error", "All connection fields must be filled.")
            return

        try:
            self._log_status("Attempting to connect to VistA...")
            self.connection = connect(host, int(port), access, verify, context)
            self._log_status("Connection successful!")
            self.invoke_button.config(state=tk.NORMAL)
            self.get_patients_button.config(state=tk.NORMAL)
            self.select_patient_button.config(state=tk.NORMAL)
            self.search_patient_button.config(state=tk.NORMAL)
            self.connect_button.config(text="Connected", state=tk.DISABLED)
        except Exception as e:
            self._log_status(f"Connection failed: {e}")
            messagebox.showerror("Connection Error", f"Failed to connect: {e}")
            self.connection = None
            self.invoke_button.config(state=tk.DISABLED)
            self.connect_button.config(text="Connect", state=tk.NORMAL)

    def _invoke_rpc(self, event=None):
        if not self.connection:
            messagebox.showwarning("RPC Error", "Not connected to VistA. Please connect first.")
            return

        rpc_name = self.rpc_combobox.get()
        params_str = self.params_entry.get()

        if not rpc_name:
            messagebox.showwarning("RPC Error", "Please select an RPC.")
            return

        # Simple parsing for parameters: assumes comma-separated literals
        # For more complex parameter types (PList, PReference, PEncoded), 
        # the user would need to manually construct them in the input or 
        # we'd need a more sophisticated parameter input UI.
        params = [PLiteral(p.strip()) for p in params_str.split(',') if p.strip()]

        self._log_status(f"Invoking RPC '{rpc_name}' with parameters: {params_str}")
        self.raw_response_text.config(state=tk.NORMAL)
        self.raw_response_text.delete(1.0, tk.END)

        try:
            # The invoke method in vavista.rpc.Connection expects *args for params
            print(f"DEBUG: Attempting to invoke RPC: {rpc_name} with parsed params: {[p.value for p in params]}")
            reply = self.connection.invoke(rpc_name, *params)
            
            if rpc_name == "ORQQAL LIST":
                # Clean up the response for ORQQAL LIST
                cleaned_reply = reply.replace("^", "").replace("\r\n", "").strip()
                self.raw_response_text.insert(tk.END, cleaned_reply)
            else:
                self.raw_response_text.insert(tk.END, reply)
            self.raw_response_text.config(state=tk.DISABLED)
            self._log_status(f"RPC '{rpc_name}' invoked successfully. Response length: {len(reply) if reply else 0}")
            print(f"DEBUG: Raw RPC reply: {reply!r}")
        except Exception as e:
            self.raw_response_text.insert(tk.END, f"Error: {e}")
            self.raw_response_text.config(state=tk.DISABLED)
            self._log_status(f"RPC '{rpc_name}' invocation failed: {e}")
            messagebox.showerror("RPC Error", f"RPC invocation failed: {e}")

    def _get_doctor_patients(self):
        if not self.connection:
            messagebox.showwarning("RPC Error", "Not connected to VistA. Please connect first.")
            return

        self._log_status("Attempting to retrieve DOCTOR1's IEN...")
        try:
            user_info_reply = self.connection.invoke("ORWU USERINFO")
            self._log_status(f"ORWU USERINFO Raw Reply: {user_info_reply!r}")
            
            # Parse the user info reply to get the IEN
            # The format is typically "DUZ^Name^...^IEN"
            user_info_parts = user_info_reply.split('^')
            if len(user_info_parts) > 0:
                provider_ien = user_info_parts[0] # Assuming IEN is the first part
                self._log_status(f"Retrieved Provider IEN: {provider_ien}")

                self._log_status(f"Invoking ORQPT PROVIDER PATIENTS with IEN: {provider_ien}")
                patients_reply = self.connection.invoke("ORQPT PROVIDER PATIENTS", PLiteral(provider_ien))
                self._log_status(f"ORQPT PROVIDER PATIENTS Raw Reply: {patients_reply!r}")

                self.raw_response_text.config(state=tk.NORMAL)
                self.raw_response_text.delete(1.0, tk.END)
                
                if patients_reply:
                    patients_list = patients_reply.split('\r\n')
                    formatted_output = "Patients for DOCTOR1 (IEN: " + provider_ien + "):\n"
                    for patient_info in patients_list:
                        if patient_info.strip():
                            # Assuming format is DFN^PatientName
                            parts = patient_info.split('^')
                            if len(parts) >= 2:
                                dfn = parts[0]
                                name = parts[1]
                                formatted_output += f"DFN: {dfn}, Name: {name}\n"
                            else:
                                formatted_output += f"Raw: {patient_info}\n"
                    self.raw_response_text.insert(tk.END, formatted_output)
                self.patients_data = []
                for patient_info in patients_list:
                    if patient_info.strip():
                        parts = patient_info.split('^')
                        if len(parts) >= 2:
                            dfn = parts[0]
                            name = parts[1]
                            self.patients_data.append({"DFN": dfn, "Name": name})
                else:
                    self.raw_response_text.insert(tk.END, "No patients found for this provider or empty response.")
                self.raw_response_text.config(state=tk.DISABLED)
                self._log_status("Successfully retrieved and displayed patients.")

            else:
                self._log_status("Could not parse provider IEN from ORWU USERINFO response.")
                messagebox.showerror("RPC Error", "Could not retrieve provider IEN.")

        except Exception as e:
            self._log_status(f"Failed to get doctor's patients: {e}")
            messagebox.showerror("RPC Error", f"Failed to get doctor's patients: {e}")

    def _open_patient_selection(self):
        if not hasattr(self, 'patients_data') or not self.patients_data:
            messagebox.showwarning("Patient Selection", "Please click 'Get Doctor's Patients' first to load patient data.")
            return
        
        PatientSelectionWindow(self, self.patients_data)


class PatientSelectionWindow(tk.Toplevel):
    def __init__(self, master, patients_data):
            super().__init__(master)
            self.master = master
            self.title("Select Patient")
            self.geometry("400x300")
            self.patients_data = patients_data
            self.selected_dfn = None

            self._create_widgets()

    def _create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("DFN", "Name"), show="headings")
        self.tree.heading("DFN", text="DFN")
        self.tree.heading("Name", text="Patient Name")
        self.tree.column("DFN", width=100)
        self.tree.column("Name", width=250)
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        for patient in self.patients_data:
            self.tree.insert("", "end", values=(patient["DFN"], patient["Name"]))

        self.tree.bind("<Double-1>", self._on_double_click)

        select_button = ttk.Button(self, text="Select Patient", command=self._on_select_button_click)
        select_button.pack(pady=5)

    def _on_double_click(self, event):
        item = self.tree.selection()[0]
        self.selected_dfn = self.tree.item(item, "values")[0]
        self.master.dfn_entry.delete(0, tk.END)
        self.master.dfn_entry.insert(0, self.selected_dfn)
        self.master._select_patient(self.selected_dfn)
        self.destroy()

    def _on_select_button_click(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a patient from the list.")
            return
        self.selected_dfn = self.tree.item(selected_item[0], "values")[0]
        self.master.dfn_entry.delete(0, tk.END)
        self.master.dfn_entry.insert(0, self.selected_dfn)
        self.master._select_patient(self.selected_dfn)
        self.destroy()

if __name__ == "__main__":
    # Read RPC list from file
    rpc_file_path = r"C:\Users\guest_user\Desktop\CPRS and VIsta - Copy\cprs code\cprs_rpc_list.txt"
    all_rpc_names = []
    try:
        with open(rpc_file_path, 'r') as f:
            all_rpc_names = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
            messagebox.showerror("File Error", f"RPC list file not found: {rpc_file_path}")

    # Filter rpc_names to include only important ones
    rpc_names = [rpc for rpc in all_rpc_names if rpc in important_rpcs]

    # Parse rpc_details.txt
    all_rpc_info = {}
    rpc_details_file_path = r"C:\Users\guest_user\Desktop\CPRS and VIsta - Copy\cprs code\rpc_details.txt"
    try:
        with open(rpc_details_file_path, 'r') as f:
            rpc_details_content = f.read()

        current_category = ""
        for line in rpc_details_content.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.endswith("RPCs:"):
                current_category = line[:-5].strip()
                if current_category.endswith(" (None found)"):
                    current_category = current_category[:-13]
                continue
            if line.startswith("*"):
                rpc_entry = line[1:].strip()
                if ":" in rpc_entry:
                    rpc_name, params_str = rpc_entry.split(":", 1)
                    rpc_name = rpc_name.strip()
                    params_str = params_str.strip()
                    all_rpc_info[rpc_name] = {
                        "category": current_category,
                        "parameters": params_str,
                        "description": params_str # Use parameters as description for now
                    }
                else:
                    rpc_name = rpc_entry.strip()
                    all_rpc_info[rpc_name] = {
                        "category": current_category,
                        "parameters": "No parameters found.",
                        "description": "No parameters found." # Use this as description if no parameters
                    }
    except FileNotFoundError:
        messagebox.showwarning("File Warning", f"rpc_details.txt not found: {rpc_details_file_path}. RPC descriptions will be limited.")
    
    # Filter rpc_info to include only important ones and provide defaults if not found
    rpc_info = {}
    for rpc_name in important_rpcs:
        rpc_info[rpc_name] = all_rpc_info.get(rpc_name, {
            "category": "Important RPC",
            "parameters": "No specific parameters found in rpc_details.txt.",
            "description": "No specific description found in rpc_details.txt."
        })

    app = VistARPCGUI(rpc_names, rpc_info)
    app.mainloop()