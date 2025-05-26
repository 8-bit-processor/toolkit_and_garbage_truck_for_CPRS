import tkinter as tk
from tkinter import ttk, messagebox

# RuleSettingsPopup Class:
# inherits from TK.Toplevel to create a new top level window  (a popup window)
# __init__ takes parent window and user_settings_instance as arguments and 
# stores the instance and sets up the basic window properties title 
# and size modalites
class RuleSettingsPopup(tk.Toplevel):
    """
    A popup window to manage lab rules for a UserSettings instance.
    Allows adding, updating, and deleting lab rules.
    """
    def __init__(self, parent, user_settings_instance):
        """
        Initializes the RuleSettingsPopup window.

        Args:
            parent: The parent Tkinter window (e.g., the main GUI window).
            user_settings_instance: The active instance of the UserSettings class.
        """
        super().__init__(parent)
        self.user_settings = user_settings_instance
        self.title("Manage Lab Rules")
        self.geometry("600x600") # Adjust size as needed
        self.transient(parent) # Keep popup on top of parent
        self.grab_set() # Modal window - prevents interaction with parent

        # Get available lab names from the UserSettings instance
        self.available_labs = list(self.user_settings.lab_rules.keys())

        self._create_widgets()

    def _create_widgets(self):
        """Creates and places the GUI widgets."""
        padding = {'padx': 5, 'pady': 5}
        entry_width = 50

        # --- Lab Selection ---
        ttk.Label(self, text="Select Lab Test:").grid(row=0, column=0, sticky='w', **padding)
        self.lab_combobox = ttk.Combobox(self, values=self.available_labs, state='readonly', width=entry_width - 3)
        self.lab_combobox.grid(row=0, column=1, sticky='ew', **padding)
        if self.available_labs:
            self.lab_combobox.current(0) # Select the first lab by default

        # --- Add/Update Rule and Action ---
        ttk.Label(self, text="New Rule String (e.g., >145):").grid(row=1, column=0, sticky='w', **padding)
        self.new_rule_entry = ttk.Entry(self, width=entry_width)
        self.new_rule_entry.grid(row=1, column=1, sticky='ew', **padding)

        ttk.Label(self, text="New Action String:").grid(row=2, column=0, sticky='w', **padding)
        self.new_action_entry = ttk.Entry(self, width=entry_width)
        self.new_action_entry.grid(row=2, column=1, sticky='ew', **padding)

        # --- Update/Delete - Identify Rule ---
        ttk.Label(self, text="Current Rule String (for Update/Delete):").grid(row=3, column=0, sticky='w', **padding)
        self.current_rule_entry = ttk.Entry(self, width=entry_width)
        self.current_rule_entry.grid(row=3, column=1, sticky='ew', **padding)

        # --- Action Buttons ---
        button_frame = ttk.Frame(self)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Add Rule", command=self._add_rule).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Update Rule", command=self._update_rule).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Delete Rule", command=self._delete_rule).grid(row=0, column=2, padx=5)

        # --- Feedback Label ---
        self.feedback_label = ttk.Label(self, text="", foreground="blue")
        self.feedback_label.grid(row=5, column=0, columnspan=2, sticky='ew', **padding)

        # Configure grid weights to make the second column expandable
        self.grid_columnconfigure(1, weight=1)

    def _get_selected_lab(self):
        """Gets the currently selected lab test from the combobox."""
        return self.lab_combobox.get()

    def _add_rule(self):
        """Handles the 'Add Rule' button click."""
        lab_name = self._get_selected_lab()
        rule_str = self.new_rule_entry.get().strip()
        action_str = self.new_action_entry.get().strip()

        if not lab_name:
            self._show_feedback("Please select a lab test.", "red")
            return
        if not rule_str or not action_str:
            self._show_feedback("Rule and Action strings cannot be empty for adding.", "red")
            return

        #  validation for rule format 
        try:
            # Use the UserSettings' own parser to validate the rule format
            self.user_settings.parse_value_setting(rule_str)
        except ValueError as e:
            self._show_feedback(f"Invalid rule format: {e}", "red")
            return

        success = self.user_settings.add_lab_rule(lab_name, rule_str, action_str)

        if success:
            self._show_feedback(f"Rule added for {lab_name}: '{rule_str}' -> '{action_str}'", "green")
            # Clear input fields after successful add
            self.new_rule_entry.delete(0, tk.END)
            self.new_action_entry.delete(0, tk.END)
        else:
            # UserSettings prints an error, but we'll show a generic one here
            self._show_feedback(f"Failed to add rule for {lab_name}.", "red")

    def _update_rule(self):
        """Handles the 'Update Rule' button click."""
        lab_name = self._get_selected_lab()
        current_rule_str = self.current_rule_entry.get().strip()
        new_rule_str = self.new_rule_entry.get().strip()
        new_action_str = self.new_action_entry.get().strip()

        if not lab_name:
            self._show_feedback("Please select a lab test.", "red")
            return
        if not current_rule_str:
            self._show_feedback("Current Rule String cannot be empty for updating.", "red")
            return
        if not new_rule_str and not new_action_str:
             self._show_feedback("Provide either a New Rule String or a New Action String to update.", "red")
             return

        # Validate new rule format if provided
        if new_rule_str:
            try:
                self.user_settings.parse_value_setting(new_rule_str)
            except ValueError as e:
                self._show_feedback(f"Invalid new rule format: {e}", "red")
                return

        # Pass None if the entry is empty, as per update_lab_rule signature
        new_rule_arg = new_rule_str if new_rule_str else None
        new_action_arg = new_action_str if new_action_str else None

        success = self.user_settings.update_lab_rule(
            lab_name,
            current_rule_str,
            new_rule_str=new_rule_arg,
            new_action_str=new_action_arg
        )

        if success:
            msg = f"Rule '{current_rule_str}' updated for {lab_name}."
            if new_rule_arg: msg += f" New rule: '{new_rule_arg}'."
            if new_action_arg: msg += f" New action: '{new_action_arg}'."
            self._show_feedback(msg, "green")
            # Optionally clear fields or just the current rule field
            # self.current_rule_entry.delete(0, tk.END)
            # self.new_rule_entry.delete(0, tk.END)
            # self.new_action_entry.delete(0, tk.END)
        else:
            self._show_feedback(f"Rule '{current_rule_str}' not found for {lab_name}.", "red")


    def _delete_rule(self):
        """Handles the 'Delete Rule' button click."""
        lab_name = self._get_selected_lab()
        rule_str_to_remove = self.current_rule_entry.get().strip()

        if not lab_name:
            self._show_feedback("Please select a lab test.", "red")
            return
        if not rule_str_to_remove:
            self._show_feedback("Current Rule String cannot be empty for deleting.", "red")
            return

        # Optional: Add a confirmation dialog
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the rule '{rule_str_to_remove}' for {lab_name}?"):
            return

        success = self.user_settings.remove_lab_rule(lab_name, rule_str_to_remove)

        if success:
            self._show_feedback(f"Rule '{rule_str_to_remove}' deleted for {lab_name}.", "green")
            # Clear the current rule field after successful delete
            self.current_rule_entry.delete(0, tk.END)
        else:
            self._show_feedback(f"Rule '{rule_str_to_remove}' not found for {lab_name}.", "red")

    def _show_feedback(self, message, color="blue"):
        """Displays a message in the feedback label."""
        self.feedback_label.config(text=message, foreground=color)
