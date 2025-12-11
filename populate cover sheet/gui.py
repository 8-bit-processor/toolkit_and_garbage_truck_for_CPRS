import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
from populate_pdf import populate_pdf

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class PdfPopulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Populator")

        self.output_folder = tk.StringVar()
        self.output_folder.set(os.getcwd())  # Default to current directory

        # The fields from the PDF
        self.fields = [
            "Last 4 of SSN", "Patient Name", "Patient Date of Birth",
            "Date Of OCC Consult", "Consult Number", "Multiple Visit End Date",
            "Multiple Visit Start Date", "Single Visit Date", "Reviewer Initials",
            "Status", "Location Where Care was conducted", "TOTAL PAGES"
        ]
        self.entries = {}

        self.create_widgets()

    def create_widgets(self):
        # Frame for input fields
        fields_frame = ttk.LabelFrame(self.root, text="PDF Data Fields", padding=(20, 10))
        fields_frame.pack(padx=10, pady=10, fill="x")

        # Create entry for each field
        for i, field in enumerate(self.fields):
            label = ttk.Label(fields_frame, text=field)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = ttk.Entry(fields_frame, width=40)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.entries[field] = entry

        # Frame for output settings
        output_frame = ttk.LabelFrame(self.root, text="Output Settings", padding=(20, 10))
        output_frame.pack(padx=10, pady=10, fill="x")

        # Output filename
        filename_label = ttk.Label(output_frame, text="Output Filename:")
        filename_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.filename_entry = ttk.Entry(output_frame, width=40)
        self.filename_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.filename_entry.insert(0, "populated_cover_sheet.pdf")

        # Output folder
        folder_label = ttk.Label(output_frame, text="Output Folder:")
        folder_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        folder_entry = ttk.Entry(output_frame, textvariable=self.output_folder, width=40, state="readonly")
        folder_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        browse_button = ttk.Button(output_frame, text="Browse...", command=self.select_folder)
        browse_button.grid(row=1, column=2, padx=5, pady=5)

        # Generate button
        generate_button = ttk.Button(self.root, text="Generate PDF", command=self.generate_pdf)
        generate_button.pack(pady=20)

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.output_folder.set(folder_selected)

    def generate_pdf(self):
        # Collect data from entries
        data_to_fill = {field: self.entries[field].get() for field in self.fields}

        # Get output path
        output_filename = self.filename_entry.get()
        if not output_filename:
            messagebox.showerror("Error", "Output filename cannot be empty.")
            return

        if not output_filename.lower().endswith(".pdf"):
            output_filename += ".pdf"
        
        output_path = os.path.join(self.output_folder.get(), output_filename)
        
        input_pdf = resource_path("cover sheet template.pdf")

        try:
            populate_pdf(input_pdf, output_path, data_to_fill)
            messagebox.showinfo("Success", f"PDF successfully created at:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PdfPopulatorApp(root)
    root.mainloop()
