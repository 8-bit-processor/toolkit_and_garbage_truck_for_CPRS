import tkinter as tk
from tkinter import filedialog
import json
import clinical_logic
from rule_settings_popup import RuleSettingsPopup,messagebox

class TMTlabsGui:
    def __init__(self, master: tk.Tk):

        #Initialize the GUI application.
        # Args:master (tk.Tk): Root window of the application.
        self.master = master
        self.master.title("Multipurpose Development GUI")

        # title header and button bar at top
        self.header_and_button_bar = tk.Frame(self.master, bg="black", highlightbackground="white")
        tk.Label(self.header_and_button_bar, text="GUI Tool for Programming Logic Testing and Development of Customized View Alert Processing Capabilities for CPRS in 2025", font=("Arial", 14), bg="white").pack(fill="x")
        self.frame = tk.Frame(self.master, bg="black", highlightthickness=3, highlightbackground="white")
        
        self.header_and_button_bar.pack(side="top", fill="x", padx=5, pady=5)
        self.frame.pack(fill="both", expand=True)

        buttons_frame = tk.Frame(self.header_and_button_bar)
        buttons_frame.pack(fill="x")

        button1 = tk.Button(buttons_frame, text="Add,Update,Delete Logic Settings", font=("Arial", 10), command=self.open_rule_settings)
        button2 = tk.Button(buttons_frame, text="Delete Logic", font=("Arial", 10), command=lambda: print("Button 2 clicked"))
        button3 = tk.Button(buttons_frame, text="Update Logic", font=("Arial", 10), command=lambda: print("Button 3 clicked"))
        button4 = tk.Button(buttons_frame, text="Copy Outbox to Clipboard", font=("Arial", 10), command=lambda: print("Button 4 clicked"))
        button5 = tk.Button(buttons_frame, text="Paste Note to CPRS", font=("Arial", 10), command=lambda: print("Button 5 clicked"))
        button1.pack(side="left", padx=5,fill="x",expand=True)   
        button2.pack(side="left", padx=5,fill="x",expand=True)
        button3.pack(side="left", padx=5,fill="x",expand=True)
        button4.pack(side="left", padx=5,fill="x",expand=True)
        button5.pack(side="left", padx=5,fill="x",expand=True)

        # Create main frames
        self.main_frame = tk.Frame(self.frame, bg="black",highlightthickness=3,highlightbackground="white")
        self.main_frame.pack(fill="both", expand=True)

        self.left_frame = tk.Frame(self.main_frame, bg="black", highlightthickness=3,highlightbackground="white")
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.right_frame = tk.Frame(self.main_frame, bg="black",highlightthickness=3,highlightbackground="white")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Create input data frame
        self.input_frame = tk.Frame(self.left_frame, bg="black",highlightthickness=3,highlightbackground="white")
        self.input_frame.pack(fill="x", padx=5,pady=5)

        self.input_data_button = tk.Button(self.input_frame, text="Select JSON Test Data File",
                                        command=self.select_json_data_file, bg="grey",
                                        fg="white", font=("Arial", 12), relief="flat")
        self.input_data_button.pack(side="top",padx=5,pady=5 )

        self.data_file_label = tk.Label(self.input_frame, text="JSON Test Data File Path:",
                                     bg="black", fg="white", font=("Arial", 12))
        self.data_file_label.pack(side="top",padx=5,pady=5)

        # Create left text box frame
        self.left_text_frame = tk.Frame(self.left_frame, bg="black",highlightthickness=3,highlightbackground="white")
        self.left_text_frame.pack(fill="both", expand=True,padx=5, pady=5)

        self.text_box = tk.Text(self.left_text_frame, font=("Arial", 12),
                                bg="black", fg="white", relief="flat",
                                highlightthickness=3, highlightbackground="black")
        self.text_box.pack(side="left", fill="both", expand=True, padx=5,pady=5)

        self.text_scrollbar = tk.Scrollbar(self.left_text_frame)
        self.text_scrollbar.pack(side="right", fill="y")
        self.text_box.config(yscrollcommand=self.text_scrollbar.set)
        self.text_scrollbar.config(command=self.text_box.yview)

        # Create right side output box frame
        self.output_frame = tk.Frame(self.right_frame, bg="black",highlightthickness=3,highlightbackground="white")
        self.output_frame.pack(fill="x", padx=5, pady=5)

        self.output_button = tk.Button(self.output_frame, text="Enter The Clinician's Name In The Input Box And Press Here",
                                        command=self.set_clinician_button_pressed, bg="grey",
                                          fg="white", font=("Arial", 12), relief="flat")
        self.output_button.pack(side="top", padx=5,pady=5)

        self.output_label = tk.Label(self.output_frame, text="Output Textbox:",
                                     bg="black", fg="white", font=("Arial", 12))
        self.output_label.pack(side="top", padx=5,pady=5)

        # Create right side text box frame
        self.right_text_frame = tk.Frame(self.right_frame, bg="black",highlightthickness=3,highlightbackground="white")
        self.right_text_frame.pack(fill="both", expand=True, padx=5,pady=5)

        self.output_text_box = tk.Text(self.right_text_frame, font=("Arial", 12),
                                      bg="black", fg="white", relief="flat",
                                      highlightthickness=0, highlightbackground="black")
        self.output_text_box.pack(side="left", fill="both", expand=True, padx=5,pady=5)

        self.info_scrollbar = tk.Scrollbar(self.right_text_frame)
        self.info_scrollbar.pack(side="right", fill="y")
        self.output_text_box.config(yscrollcommand=self.info_scrollbar.set)
        self.info_scrollbar.config(command=self.output_text_box.yview)



        # Create chatbox frame
        self.tmtbot_frame = tk.Frame(self.frame, bg="black",highlightthickness=3,highlightbackground="white")
        self.tmtbot_frame.pack(fill="both",padx=0,pady=0)

        self.tmtbot_text_frame = tk.Frame(self.tmtbot_frame, bg="black",highlightthickness=3,highlightbackground="white")
        self.tmtbot_text_frame.pack(side="top", fill="both", expand=True, padx=5, pady=5)


        # Create chatbox
        self.chatbox_textbox = tk.Text(self.tmtbot_text_frame, font=("Arial", 12),
                               bg="black", fg="white",
                               relief="flat", height=5, highlightthickness=3,
                               highlightbackground="black")
        self.chatbox_textbox.pack(side="left", fill="both", expand=True, padx=5,pady=5)
        self.chatbot_scrollbar = tk.Scrollbar(self.tmtbot_text_frame)
        self.chatbot_scrollbar.pack(side="right", fill="y",padx=10,pady=5)
        self.chatbox_textbox.config(yscrollcommand=self.chatbot_scrollbar.set)
        self.chatbot_scrollbar.config(command=self.chatbox_textbox.yview)


        # create bottom frame for input box and send button
        self.bottom_frame = tk.Frame(self.tmtbot_frame, bg="black",highlightthickness=3,highlightbackground="white")
        self.bottom_frame.pack(fill="both", padx=5,pady=5)
        self.center_frame = tk.Frame(self.bottom_frame, bg="black")
        self.center_frame.pack(side="left", fill="both", expand=True ,padx=5,pady=5)

        # Set up input_box, set cursor to bright white
        self.input_box = tk.Text(self.center_frame, font=("Arial", 12), bg="black", fg="white",
                                  relief="flat", height=2, highlightthickness=0,
                                  insertbackground="white", insertwidth=3) # Set cursor color and width
        self.input_box.pack(fill="both", expand=True)


        self.send_button = tk.Button(self.bottom_frame, text="Send chat message",
                                     command=self.send_button_pressed,
                                      bg="grey", fg="white", font=("Arial",12), relief="flat")
        self.send_button.pack(side="right", fill="both", padx=5, pady=5)

        # Path for json test data file will be set by user
        self.json_data_file_path = ""
        # Variable to store the loaded JSON data
        # other variables will be added here to track processes
        self.sample_json_test_data = None

        # clinician object will be named by the user.
        # clinician initialized within GUI instance with empty string
        # The clinical_logic.UserSettings instance is created here
        # other class objects to be added later for more view alert functionality 
        self.clinical_settings = clinical_logic.UserSettings(clinician="")

        # This gui dictionary defines user inputs that will be mapped to the actions 
        # or outputs the user is asking for
        # later we will store these in a separate configuration file so that the 
        # user can add or change these if needed either thru the chatbot or a separate GUI popup
        self.map_user_response_to_the_desired_chatbot_response = {
            "hello": "Hello! How can I assist you today?",
            "what is your purpose": "My purpose is to demonstrate how users can create custom rules to automate and assist with the most tedious tasks of CPRS",
            "how are you": "I'm doing well, thank you for asking!",
            "show lab rules": "show_lab_rules():",
            "apply lab rules" : "process_json_data_file_with_lab_rules():",
        }
        self.master.bind('<Return>', self.send_button_pressed)

    # Select Json file and update the file label with the path of the test lab data
    # always use json format for the incoming test data  
    def select_json_data_file(self) -> None:
        self.json_data_file_path = filedialog.askopenfilename(title="Select JSON Data File", filetypes=[("JSON Files","*.json")])
        if self.json_data_file_path:
            self.data_file_label.config(text=f"Selected Data File: {self.json_data_file_path}")
            self.display_input_json_data()

    def display_input_json_data(self):
        if self.json_data_file_path:
            try:
                with open(self.json_data_file_path, 'r') as f:
                    # Load the data into the instance variable
                    self.sample_json_test_data = json.load(f)
                    self.text_box.delete('1.0', tk.END)
                    # Display the loaded data in the left textbox
                    for key, value in self.sample_json_test_data.items():
                        self.text_box.insert(tk.END, f"{key}: {value}\n\n")
            except Exception as e:
                self.text_box.delete('1.0', tk.END)
                self.text_box.insert(tk.END, f"Error loading JSON: {str(e)}")
                self.sample_json_test_data = None # Clear data if loading fails
        else:
            self.text_box.delete('1.0', tk.END)
            self.text_box.insert(tk.END, "Please select a JSON file.")
            self.sample_json_test_data = None # Clear data if no file selected

    def open_rule_settings(self):
        """Opens the rule settings popup window."""
        if self.clinical_settings:
            # Pass self (the main window) and the user_settings instance
            RuleSettingsPopup(self.master, self.clinical_settings)
        else:
            messagebox.showerror("Error", "User settings are not available.")

    # prompt user to enter the clinicians name with message to chatbox
    # render update into GUI instance
    def set_clinician_button_pressed(self):
        clinician_name = self.input_box.get('1.0', tk.END).strip() # Use strip() to remove leading/trailing whitespace and newline
        self.input_box.delete('1.0', tk.END)

        if not clinician_name: # Check if the stripped name is empty
            self.chatbox_textbox.insert(tk.END, "CPRS assistant bot: Please enter the clinician's name in the input box and press the button.\n\n")
        elif len(clinician_name) <= 1:
            self.chatbox_textbox.insert(tk.END, "CPRS assistant bot: Please enter a valid clinician name (more than one character).\n\n")
        elif len(clinician_name) > 25:
            self.chatbox_textbox.insert(tk.END, "CPRS assistant bot: Please enter a shorter clinician name (max 25 characters).\n\n")
        else:
            self.clinical_settings.clinician = clinician_name
            self.output_label.config(text=f"{self.clinical_settings.clinician}'s Outbox")
            self.chatbox_textbox.insert(tk.END, f"CPRS assistant bot: The clinician name is now set to {self.clinical_settings.clinician}.\n\n")

        self.chatbox_textbox.see(tk.END)

    def show_rules(self):
        # Clear the output textbox and clinician's lab rules header   
        self.output_text_box.delete('1.0', tk.END)
        self.output_text_box.insert(tk.END, f"--- {self.clinical_settings.clinician}'s Lab Rules ---\n\n")

        #  if no clinician defined prompt user
        if not self.clinical_settings.clinician:
             self.output_text_box.insert(tk.END, "Clinician name not set. Cannot display rules.\n")
             return
        
        # Access the dictionary from the object instance to get rules
        all_rules = self.clinical_settings.lab_rules 

        # if no rules handle with message
        # will later add suggested actions for user to select or choose 
        if not any(all_rules.values()):
             self.output_text_box.insert(tk.END, "No custom rules defined for this clinician.\n")
             return

        for lab, rules_list in all_rules.items():
            self.output_text_box.insert(tk.END, f"Rules for {lab.capitalize()}:\n")
            self.output_text_box.insert(tk.END, "-------------------------\n")
            if rules_list:
                for rule_obj in rules_list:
                    self.output_text_box.insert(tk.END, f"  Rule: {rule_obj.rule}, Action: {rule_obj.action}\n")
            else:
                 self.output_text_box.insert(tk.END, "  No rules defined for this lab.\n")
            self.output_text_box.insert(tk.END, "\n") # Adds a blank line between labs

        self.output_text_box.see(tk.END)


    def process_json_data_file_with_lab_rules(self):
        # Clear previous output
        self.output_text_box.delete('1.0', tk.END)
        self.chatbox_textbox.insert(tk.END, "CPRS assistant bot: Processing lab data...\n")
        self.chatbox_textbox.see(tk.END)

        # 1. Check against normal ranges
        needs_further_processing, normal_range_report = self.clinical_settings.are_test_results_normal(self.sample_json_test_data)

        # Display normal range report in outbox
        self.output_text_box.insert(tk.END, f"{normal_range_report}\n")

        if needs_further_processing:
            self.chatbox_textbox.insert(tk.END, "CPRS assistant bot: Out of normal range results were found. Applying clinician\'s rules...\n\n")

            # 2. Apply clinician\'s custom rules
            clinician_rules_report,final_summary_report = self.clinical_settings.process_test_data_with_rules(self.sample_json_test_data)

            # Display clinician\'s rule-based report in the output textbox
            self.output_text_box.insert(tk.END, clinician_rules_report)
            self.output_text_box.insert(tk.END, "\n\n\n*********** Summary of instructions ***************\n")
            self.output_text_box.insert(tk.END, final_summary_report)
            self.output_text_box.see(tk.END)

        else:
            self.chatbox_textbox.insert(tk.END, "CPRS assistant bot: All results are within the normal range. No further processing needed.\n\n")

        self.chatbox_textbox.see(tk.END)

    # rules based chatbot will add more advanced natural language processing later to handle user input 
    # which can be later fed into the methods accordingly 
    def send_button_pressed(self, event=None) -> None:
        # send a chat message and execute function
        user_input = self.input_box.get('1.0', tk.END).strip().lower() # Use strip() and lower()
        self.input_box.delete('1.0', tk.END) # Clear input box immediately
        
        # do nothing if clinician is trying to process empty input
        if not user_input: 
            return
        # prompt user if json test data file is not selected
        if not self.sample_json_test_data:
            self.chatbox_textbox.insert(tk.END, "CPRS assistant bot: Please select and load a JSON test data file first.\n\n")
            self.chatbox_textbox.see(tk.END)
            return
        # prompt user to identify clinician's name
        if not self.clinical_settings.clinician:
            self.chatbox_textbox.insert(tk.END, "CPRS assistant bot: Please set the clinician name first.\n\n")
            self.chatbox_textbox.see(tk.END)
            return

        # Display user input in chatbox
        self.chatbox_textbox.insert(tk.END, "You : " + user_input + "\n")
        self.chatbox_textbox.see(tk.END)

        # Default response
        chatbot_response = "I didn't quite understand that."

        # check if json data file is selected and loaded
        if user_input in self.map_user_response_to_the_desired_chatbot_response and not self.sample_json_test_data:
             chatbot_response = "To apply or show rules, please select and load a JSON test data file first."

        # check if clinician name has been set
        elif user_input in self.map_user_response_to_the_desired_chatbot_response and not self.clinical_settings.clinician:
             chatbot_response = "Please set the clinician name first. I need the clinician's name to load their rules."

        # check for user directed function responses as defined in the gui\'s dictionary
        # To direct user\'s text input to a reponse or instruction given back in plain english
        # that will be the clinician\'s desired action
        elif user_input in self.map_user_response_to_the_desired_chatbot_response:
            action = self.map_user_response_to_the_desired_chatbot_response[user_input]

            if action == "show_lab_rules():":
                self.show_rules()
                chatbot_response = "Displaying clinician's lab rules in the output box."
            elif action == "process_json_data_file_with_lab_rules():":
                # The processing method itself also adds to the chatbox and output box
                self.process_json_data_file_with_lab_rules()
                chatbot_response = "Processing complete. Check the chatbox and output box for results."
            else:
                # handle simple text responses from 'map_user_response_to_the_desired_chatbot_response'
                chatbot_response = action
            self.chatbox_textbox.insert(tk.END, "CPRS assistant bot: " + chatbot_response + "\n\n")
            self.chatbox_textbox.see(tk.END)

        else:
            chatbot_response = "I'm sorry I didn't understand. Try again"
            # Render chatbot response into GUI instance
            # Only insert the chatbot response if it\'s not handled by one of the specific function calls above
            # For actions that update other boxes, still provide a simple chat response
            self.chatbox_textbox.insert(tk.END, "CPRS assistant bot: " + chatbot_response + "\n\n")
            self.chatbox_textbox.see(tk.END)
            # if not using a user mapped function, option to use ollama to respond to the user input
            # from NLP_and_ollama_functions import ollama_response
            # response= ollama_response(user_input=user_input)
            # chatbot_response = response # Uncomment and use this if Ollama is integrated

def main() -> None:
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = int(screen_width * 0.9)
    height = int(screen_height * 0.9)
    x = (screen_width - width) // 2
    y = 0
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.focus_set()
    app = TMTlabsGui(root)
    root.mainloop()

if __name__ == "__main__":
    main()
