"""This code defines a structure for rules that clinicians will make, and a class `UserSettings` to store and
manipulate these rules. The rules are represented as strings with specific formats (e.g., ">145" or "<=5.0") and
associated actions. this code assumes a specific format for the rules (e.g., ">145" or "<=5.0")

classes and methods:

1. `LabRule`: Represents a single rule and its associated action.
2. `UserSettings`:
        * Initializes with empty lists for each lab test.
        * `load_default_lab_rules`: Loads default rules from a JSON file.
        * `add_lab_rule`: Adds a new rule and action for a specific lab test.
        * `get_lab_rules`: Retrieves all rules for a specific lab test.
        * `show_all_lab_rules`: Prints all rules for each lab test.
        * `update_lab_rule`: Updates the rule or action of an existing lab rule identified by its current rule string.
        * `remove_lab_rule`: Removes a lab rule identified by its rule string.
        * `process_test_data_with_rules`: Iterates through test data and applies clinician's rules.
        * `are_test_results_normal`: Checks test results against built-in normal ranges.

The methods `parse_value_setting` and `apply_parsed_clinicians_rule_to_test_result` are used to parse and apply
the rules, respectively. The former method takes a rule string (e.g., ">100") and returns the corresponding
operator string and numeric value. The latter method applies the parsed rule to a test result and returns a
boolean indicating whether the rule is matched- the matched rule is what applies for the test result

The `compare_labtest_to_verify_normal_result` function compares a lab test result to its normal range and returns
a string to indicate whether the result is low, high, or within the normal range.

"""
# standard python library imports
import json
import os 

# Represents a single rule and its associated action.
class LabRule:

    def __init__(self, rule, action):
        self.rule = rule
        self.action = action

    def __repr__(self):
        return f"LabRule(rule='{self.rule}', action='{self.action}')"

# Class for storing and manipulating user settings, specific to a clinician.
# Using a dictionary where keys are lab names and values are lists of LabRule objects
# Initialize with empty lists, rules can be added later
# lists allow for the clinican to have any number of rules
class UserSettings:

    def __init__(self, clinician):
        self.clinician = clinician
        self.lab_rules = {\
            'sodium': [],
            'potassium': [],
            'chloride': [],
            'bicarb': [],
            'bun': [],
            'creatinine': [],
            'glucose': [],
            'calcium': [],
            'magnesium': [],
            'phosphorus': [],
            'whitecellcount': [],
            'hemoglobin': [],
            'hematocrit': [],
            'platelets': [],
            'a1c': [],
            "tsh":[]
        }
        # Load default rules on initialization
        # Assuming default_lab_rules.json is in the same directory or a known path
        default_rules_path = os.path.join(os.path.dirname(__file__), 'Example_default_lab_rules.json')
        if os.path.exists(default_rules_path):
             self.load_default_lab_rules(file_path=default_rules_path)
        else:
             print(f"Error: Default lab rules file not found at {default_rules_path}")


    def load_default_lab_rules(self, file_path):
        try:
            with open(file_path, 'r') as f:
                lab_rules_dictionary = json.load(f) # Use json.load directly

            for lab_name, rules_list in lab_rules_dictionary.items():
                # Ensure lab_name is in the predefined list or handle new labs
                if lab_name.lower() in self.lab_rules:
                    self.lab_rules[lab_name.lower()] = [\
                        LabRule(rule=rule["rule"], action=rule["action"])
                        for rule in rules_list
                    ]
                else:
                    print(f"Error: Lab '{lab_name}' from default rules not in predefined list.")

        except FileNotFoundError:
            print(f"Error: Default lab rules file not found at {file_path}")
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {file_path}")
        except Exception as e:
            print(f"An error occurred loading default rules: {e}")


    # Adds new rule and action for a specific lab.
    def add_lab_rule(self, lab_name, rule, action):
        lab_name_lower = lab_name.lower()
        if lab_name_lower not in self.lab_rules:
            print(f"Error: Invalid lab name '{lab_name}'.")
            return False
        new_rule = LabRule(rule=rule, action=action)
        self.lab_rules[lab_name_lower].append(new_rule)
        print(f"Rule added for {lab_name}: Rule='{rule}', Action='{action}'")
        return True

    # method to retrieve all rules for a specific lab test
    # return object is list of dictionary(rules:actions)
    # .get dictionary method returns None if key not found
    def get_lab_rules(self, lab_name):
        lab_name_lower = lab_name.lower()
        return self.lab_rules.get(lab_name_lower)
    
    # Updates the rule or action of an existing lab rule identified by its current rule string.
    #    Args:
    #       lab_name (str): The name of the lab (e.g., 'sodium').
    #       current_rule_str (str): The current rule string to find (e.g., '>145').
    #       new_rule_str (str, optional): The new rule string to set. Defaults to None.
    #       new_action_str (str, optional): The new action string to set. Defaults to None.\
    #    Returns:
    #       bool: True if the rule was found and updated, False otherwise.
    def update_lab_rule(self, lab_name, current_rule_str, new_rule_str=None, new_action_str=None):

        lab_name_lower = lab_name.lower()

        if lab_name_lower not in self.lab_rules:
            print(f"Error: Invalid lab name '{lab_name}'.")
            return False

        rules_list = self.lab_rules[lab_name_lower]
        found_rule = None

        # Find the rule by its current rule string
        for rule_obj in rules_list:
            if rule_obj.rule == current_rule_str:
                found_rule = rule_obj
                break

        if found_rule:
            if new_rule_str is not None:
                found_rule.rule = new_rule_str
                print(f"Updated rule string for '{lab_name}' rule '{current_rule_str}' to '{new_rule_str}'.")
            if new_action_str is not None:
                found_rule.action = new_action_str
                print(f"Updated action string for '{lab_name}' rule '{current_rule_str}' to '{new_action_str}'.")

            if new_rule_str is None and new_action_str is None:
                 print(f"No updates specified for '{lab_name}' rule '{current_rule_str}'.")

            return True
        else:
            print(f"Rule with string '{current_rule_str}' not found for lab '{lab_name}'.")
            return False

    # Removes a lab rule identified by its rule string.
    #   Args:
    #       lab_name (str): The name of the lab (e.g., 'sodium').
    #       rule_str_to_remove (str): The rule string to find and remove (e.g., '<135')
    #    Returns:
    #       bool: True if the rule was found and removed, False otherwise.
    def remove_lab_rule(self, lab_name, rule_str_to_remove):

        lab_name_lower = lab_name.lower()

        if lab_name_lower not in self.lab_rules:
            print(f"Error: Invalid lab name '{lab_name}'.")
            return False

        rules_list = self.lab_rules[lab_name_lower]
        initial_count = len(rules_list)

        # Create a new list excluding the rule to remove
        self.lab_rules[lab_name_lower] = [\
            rule_obj for rule_obj in rules_list if rule_obj.rule != rule_str_to_remove
        ]

        if len(self.lab_rules[lab_name_lower]) < initial_count:
            print(f"Removed rule with string '{rule_str_to_remove}' for lab '{lab_name}'.")
            return True
        else:
            print(f"Rule with string '{rule_str_to_remove}' not found for lab '{lab_name}'.")
            return False


    @staticmethod
    # Parses the rule that is written as a string (example format should be '>100', '<=5.0')
    # and returns the corresponding operator string and the numeric value.
    # the operator string will be parsed later again in the staticnmethod apply_parsed_clinician_rule_to_test_result
    def parse_value_setting(string_value):
        if not string_value:
            raise ValueError("Rule string is empty")

        string_value = string_value.strip()
        operator = None
        number_str = None

        if string_value.startswith('<='):
            operator = '<='
            number_str = string_value[2:].strip()
        elif string_value.startswith('<'):
            operator = '<'
            number_str = string_value[1:].strip()
        elif string_value.startswith('>='):
            operator = '>='
            number_str = string_value[2:].strip()
        elif string_value.startswith('>'):
            operator = '>'
            number_str = string_value[1:].strip()
        elif string_value.startswith('=='): # Added equality check
             operator = '=='
             number_str = string_value[2:].strip()
        else:
            raise ValueError(f'Invalid value format: "{string_value}". Expected format like ">100", "<=5.0", etc.')

        try:
            number = float(number_str)
        except ValueError:
            raise ValueError(f'Invalid number format in setting: "{string_value}"')

        return operator, number # Return operator as a string

    @staticmethod
    # evaluate operators with test result and return boolean
    # because operators were represented as strings, these strings need to be parsed here
    def apply_parsed_clinicians_rule_to_test_result(operator_string,number_float,test_result):

        try:
            # Apply if/elif checks to
            is_match = False
            if operator_string == '<':
                is_match = test_result < number_float
            elif operator_string == '<=':
                is_match = test_result <= number_float
            elif operator_string == '>':
                is_match = test_result > number_float
            elif operator_string == '>=':
                is_match = test_result >= number_float
            elif operator_string == '==':
                is_match = test_result == number_float

            # Removed print statement here
            # print(f"Is the test result {test_result} {operator_string} {number_float}? Therefore the boolean answer is : {is_match}")

        except ValueError as e:
            print(f"Parsing error: {e}") # Keep print for parsing errors
            is_match = False # Assume no match on error
        return is_match

    @staticmethod
    # --- static method for Normal Range Comparison ---
    # method self contains dictionary mapping to built in normal ranges for the tests being evaluated
    #  returns a string stating low normal or high to make further decisions with the lab reuslt
    def compare_labtest_to_verify_normal_result(labtest, value):

        # to have fun add as many more tests to this dictionary as you can find
        normal_ranges = {
        'sodium': (135.0, 145.0),
        'potassium': (3.5, 5.0),
        'chloride': (95.0, 110.0),
        'bicarbonate': (22.0, 29.0),
        'bun': (7.0, 24.0),
        'creatinine': (0.5, 1.2),
        'glucose': (70.0, 110.0),
        'calcium':( 8.5,10.5), 
        'magnesium':(1.7, 3.2),
        'phosphorus':( 2.5,4.5),
        'whitecellcount':(4.5, 11.0),
        'hemoglobin':(12.5, 17.5),
        'hematocrit':(37, 49),
        'platelets': (150,450),
        'tsh':(0.3,4.5),
        'a1c':(4.5,6.0),
        }

        # convert testname to lower case to avoid case sensitivty error
        labtest_lower = labtest.lower()
        # check if labtest normal range has been defined
        if labtest_lower not in normal_ranges:
            # print(f"Normal reference value for labtest = {labtest} needs to be defined") # Removed print
            return 'undefined_range'
        lower_bound, upper_bound = normal_ranges[labtest_lower]
        # check if labtest is below normal range
        if value < lower_bound:
            return 'low'
        # check if labtest is above normal range
        elif value > upper_bound:
            return 'high'
        else:
            return 'normal'


    # check if test sample lab results are normal and returns a boolean to answer the question to make a decision
    # whether the lab report is all normal or has abnormal results with further processing needed
    # Accepts test_data_dictionary as input
    # classification data counter tracks how many abnormal results and returns True if there are any
    # which means that that there are abnormal results found and furt




    def are_test_results_normal(self, test_data_dictionary):
        abnormal_high_count = 0
        abnormal_low_count = 0
        report_lines = [] #  list to contain the report

        if not test_data_dictionary:
            return False, "No test data provided."

        report_lines.append("--- Normal Range Check ---")

        for example_test, example_lab_value in test_data_dictionary.items():
            # Ensure value is numeric before comparison
            try:
                value = float(example_lab_value)
            except (ValueError, TypeError):
                report_lines.append(f"Error  {example_test}: Invalid value '{example_lab_value}'")

            test_classification = self.compare_labtest_to_verify_normal_result(labtest=example_test,value=value)
            report_lines.append(f"{example_test}: {example_lab_value}  Classification: {test_classification}")

            if test_classification == "high":
                abnormal_high_count += 1
            elif test_classification == "low":
                abnormal_low_count += 1

        is_all_normal = (abnormal_high_count == 0 and abnormal_low_count == 0)

        if is_all_normal:
            report_lines.append("Summary: All test results are within the normal range.")
        else:
            summary = f"Summary: Found {abnormal_high_count} high and {abnormal_low_count} low test results."
            report_lines.append(summary)
            
        # Join the lines to form the final report string
        report_string = "\n".join(report_lines)

        # Return boolean indicating if *any* abnormal results were found (True if abnormal, False if all normal)
        # This matches the logic in the original do_the_tests_need_further_processing
        needs_further_processing = not is_all_normal

        return needs_further_processing, report_string

    #  method to process test data using clinician's custom rules
    def process_test_data_with_rules(self, test_data_dictionary):
        report_lines = []
        report_summary_lines = []
        report_lines.append(f"--- {self.clinician}'s Custom Rule Check ---")

        if not self.clinician:
             report_lines.append("Clinician name not set. Cannot apply custom rules.")
             return "\n".join(report_lines)

        if not test_data_dictionary:
            report_lines.append("No test data provided to apply rules.")
            return "\n".join(report_lines)

        for lab_test, test_value in test_data_dictionary.items():
            lab_test_lower = lab_test.lower()
            report_lines.append(f"\nChecking rules for {lab_test}: {test_value}")

            # Ensure value is numeric before applying rules
            try:
                value = float(test_value)
            except (ValueError, TypeError):
                report_lines.append(f" rule check error : Invalid value '{test_value}'")
                 

            rules_for_lab = self.get_lab_rules(lab_test_lower)

            if rules_for_lab:
                found_match = False
                for rule_object in rules_for_lab:
                    try:
                        rule_operator_string, rule_num = self.parse_value_setting(rule_object.rule)
                        rule_matches = self.apply_parsed_clinicians_rule_to_test_result(
                            rule_operator_string, rule_num, value
                        )

                        if rule_matches:
                            report_lines.append(f"  Rule '{rule_object.rule}' matches.")
                            report_lines.append(f"  {self.clinician}'s Action: {rule_object.action}")
                            report_summary_lines.append(f"\n This labtest: {lab_test}:  has this lab value : {test_value}")
                            report_summary_lines.append(f"  Rule '{rule_object.rule}' matches.{self.clinician}'s Action: {rule_object.action}")
                            found_match = True

                    except ValueError as e:
                        report_lines.append(f"  Could not evaluate rule '{rule_object.rule}': {e}")

                if not found_match:
                    report_lines.append(f"  No custom rule matched for {lab_test} with value {test_value}.")
            else:
                report_lines.append(f"  No custom rules defined for {lab_test}.")
        # Return 2 separate reports for the GUI
        return "\n".join(report_lines),"\n".join(report_summary_lines)
