import clinical_logic
import test_lab_data

def Main():

    def initialize_clinican_object(clinical_user):     
        # create a clinician_settings object to hold the rules we will use for clinical logic
        print(f"instantiating clinician settings for the clinician: {clinical_user}")
        clinician_settings = clinical_logic.UserSettings(clinical_user)
        return clinician_settings


    def demonstration_of_how_to_use__this_code():
        
        # show that the clinician_settings object has default rules automatically loaded 
        #  by the constructor during instantiation
        print("first let's see the default rules that have been loaded from JSON file during the instantiation")
        print("---------------------------------------------------------------------------------------------")
        clinician_settings.show_all_lab_rules()
        print()

        # demonstration how to add more rules to the default rules
        print(f"what if {clinician_settings.clinician} wants to add some more rules")
        print("---------------------------------------------------------------------")
        clinician_settings.add_lab_rule("sodium", ">145", "drink more water or use 1/2 normal saline")
        clinician_settings.add_lab_rule("sodium", "<135", "review medications and Suggest fluid restricion")
        clinician_settings.add_lab_rule("glucose", ">400", "reassess for an insulin dose adjustment")
        clinician_settings.add_lab_rule("sodium", ">149", "go to the ER")
        print()

        # show to verify that the rules were added 
        print(f"let's see {clinician_settings.clinician}'s updated rules for the specific test sodium")
        print("--------------------------------------------------------------------------------------------")
        clinician_settings.get_lab_rules("sodium")
        print()

        # show that the other rules are unchanged - because we only added rules to one test
        print(f"now lets check on all rules for clinician {clinician_settings.clinician} we will also see the one rule that was just added to the glucose test:")
        print("-------------------------------------------------------------------------")
        clinician_settings.show_all_lab_rules()
        print()

        #  First step is how to decide whether the lab result is abnormal or needs futher computation
        print("If a test result is normal then there is no need to further evaluate the test result")
        print("show a few examples how to check if lab values are high,low or within normal ranges:")
        print("----------------------------------------------------------------------------------------")
        example_lab_value_sodium = 140
        status_sodium = clinical_logic.compare_labtest_to_verify_normal_result("Sodium", example_lab_value_sodium)
        print(f"Sodium {example_lab_value_sodium}: {status_sodium}")
        lab_value_potassium = 3.0
        status_potassium = clinical_logic.compare_labtest_to_verify_normal_result("Potassium", lab_value_potassium)
        print(f"Potassium {lab_value_potassium}: {status_potassium}")
        lab_value_glucose = 250
        status_glucose = clinical_logic.compare_labtest_to_verify_normal_result("Glucose", lab_value_glucose)
        print(f"Glucose {lab_value_glucose}: {status_glucose}")
        print()

        # demo how the clinician's rules will be applied to the test result
        # parsing and applying a string data rule '{example_rule}' returns operator=string and value=float
        example_rule = ">=5.5"
        example_test_result = 6.6
        print(f"We are using example rule {example_rule} and an example test result {example_test_result} to see how rules are evaluated")
        print(f"let's see an Example of applying {example_rule} to the test result {example_test_result}")
        print("--------------------------------------------------------------------------------------------------------------------------")
        operator_string, number_float = clinical_logic.UserSettings.parse_value_setting(example_rule)
        clinician_settings.apply_parsed_clinicians_rule_to_test_result(test_result=example_test_result,operator_string=operator_string,number_float=number_float)
        print()


        # Example of evaluating rules that match a value (the rules that should apply to that value) 
        example_test= "sodium"
        test_value = 150
        print(f"We are using {example_test} as the example test and trying to figure out what the clinician {clinician_settings.clinician} wants to do with a test value {test_value}")
        print(f"Evaluating {clinician_settings.clinician}'s rules for {example_test} with a value of {test_value}:")
        evaluate_rules_for_test_value(clinician_settings=clinician_settings,labTest=example_test, test_value=test_value)
        print()


        # demonstrate methods that can update or remove rules
        print(f"what if {clinician_settings.clinician} is unhappy with his settings-now what can we do?")
        print(f"we will now demonstrate how to change existing rules for on test {example_test}")
        print(f"--- the {example_test} Rules for {clinician_settings.clinician} ---")
        clinician_settings.get_lab_rules(example_test)


        # demo how the clinician can change the rules if the clinician wants something changed 
        new_action = "call pt and tell him to drink more water"
        existing_rule = ">145"
        print(f"the clinician {clinician_settings.clinician} wants to change his {example_test} with exisiting rule {existing_rule} to replace the action with a new action {new_action}")
        print("\n--- Updating a Rule ---")
        print(f"we will show how to update the action for the {example_test} {existing_rule} rule")
        clinician_settings.update_lab_rule(lab_name=example_test, current_rule_str=existing_rule, new_action_str=new_action)
        print(f"here is the update {example_test} rules")
        clinician_settings.get_lab_rules(lab_name=example_test)
        print()

        # the clinician trys to update a rule that is not present 
        print(f"What happens if {clinician_settings.clinician} tries to update a non-existent rule")
        print("-------------------------------------")
        clinician_settings.update_lab_rule("Sodium", "==140", new_action_str="Should not find this")
        print()

        # the clinician is changing both rule and action
        example_test = "potassium"
        existing_rule ="<3.5"
        replacement_rule= "<=3.3"
        new_action_plan = "Suggest K+ supplement or dietary increase"
        print(f"the clinician {clinician_settings.clinician} now wants to change for test {example_test} both the existing rule {existing_rule} with a new rule {replacement_rule} and the action will be changed to {new_action_plan}")
        print("we can update both rule string and action to be done")
        print(f"we will demonstrate how to update both rule and action on the same test {example_test}")
        print("original potassium rules are:")
        print("--------------------------------")
        clinician_settings.get_lab_rules(lab_name=example_test)
        print("--------------------------------------")
        clinician_settings.update_lab_rule(lab_name=example_test, current_rule_str=existing_rule, new_rule_str=replacement_rule, new_action_str=new_action_plan)
        print(f"here is the updated {"potassium"} rule")
        print("--------------------------------------------")
        clinician_settings.get_lab_rules(lab_name="potassium")
        print()

        # demo foe the purpose of error handling 
        print(f"the clinician {clinician_settings.clinician} Tried to update an invalid lab")
        print("------------------------------------------------------------------------------")
        clinician_settings.update_lab_rule("UnknownLab", ">10", new_action_str="Should fail")

        # demo how to remore rules
        example_rule = "<135"
        example_test = "sodium"
        print(f"The clinician {clinician_settings.clinician} can also remove a rule that is no longer wanted")
        print(f"Let's see how a rule {example_rule} can be removed from the test {example_test}")
        print("\n--- Removing a Rule ---")
        print(f"Remove the {example_test} {example_rule} rule")
        print(f"before removal, let's see all the {example_test} rules again")
        print("----------------------------------------------------------------")
        clinician_settings.get_lab_rules(lab_name=example_test)
        print()
        print(f"proceed with removing the {example_rule} rule")
        clinician_settings.remove_lab_rule(lab_name=example_test, rule_str_to_remove=example_rule)
        print(f"now let's see the updated rules for {example_test}")
        clinician_settings.get_lab_rules(lab_name=example_test)
        print()

        # for user's error handling 
        print(f"for error handling purposes we will demonstrate what happens when the clinicain {clinician_settings.clinician} makes an error")
        print(f"{clinician_settings.clinician} Tries to remove a non-existent rule")
        print("----------------------------------------------------------------------")
        clinician_settings.remove_lab_rule("Sodium", "==140")
        print()
        print(f"{clinician_settings.clinician} tries to remove from an invalid lab")
        print("-------------------------------------------------------------------")
        clinician_settings.remove_lab_rule("UnknownLab", ">10")
        print()

        # conclusion
        print("This simple demo proides how a lab alert handler can manage and apply so many differenct custom rules and show that this code will obviously work")
        print("        This is only one automatable task what CPRS view alert booster could be doing- *** this is only the beginning ***")
        print("***********************************************************************************************************************************************")
        print("Object oriented programming provides a structure for storing, maniputlating and processing logical rules to automate our most tedious tasks" )
        print("***********************************************************************************************************************************************")
        return
    
    # check if lab results are normal and returns a boolean to answer the question to make a decision
    def are_test_results_normal(data_dictionary):
        abnormal_high_count = 0
        abnormal_low_count = 0
        for key, value in data_dictionary:
            example_test=key
            example_lab_value = value
            test_classification = clinical_logic.compare_labtest_to_verify_normal_result(labtest=example_test,value=example_lab_value)
            print(f"LabTest : {example_test}  Result : {example_lab_value}:  classification : {test_classification}")
            if test_classification == "high":
                abnormal_high_count += 1
            elif test_classification == "low":
                abnormal_low_count += 1
        print()
        if abnormal_high_count > 0 and abnormal_low_count > 0:
            print(f"**** {abnormal_high_count} high test results and {abnormal_low_count} low test results were found ***")
            return False
        elif abnormal_high_count > 0:
            print(f"****  {abnormal_high_count} High Test results found - ****")
            return False
        elif abnormal_low_count > 0:
            print(f"***** {abnormal_low_count} low test results were found *****")
            return False
        else:
            print("no abnormal tests were found- no further analysis needed")
            return True
        
    # funtion to decide on further action based on whether lab results were normal or contain abnoramal values 
    # returns a boolean - true more evaluation needed for abnoraml results
    def tests_need_further_processing(lab_data_dictionary):
        normal_lab_report = are_test_results_normal(data_dictionary=lab_data_dictionary)
        print()
        if normal_lab_report == True:
            print("****************************************************************************************************")
            print(f"Great- we are dealing with all normal labs- The lab report will be sent with {clinician_settings.clinician}'s messages")
            print("****************************************************************************************************")
            print()
            return False
        if normal_lab_report == False:
            print("****************************************************************************************************")
            print("Comparison with reference range determined more analysis is needed before the lab report can be sent")
            print("****************************************************************************************************")
            print()
            return True
            
    
    # takes the data dictionary and iterates each lab result 
    # abnoraml results are then evaluated with the clinician's settings 
    def applying_clinicians_rules(data_dictionary):
        for key, value in data_dictionary:
            example_test=key
            example_lab_value = value
            test_classification = clinical_logic.compare_labtest_to_verify_normal_result(labtest=example_test,value=example_lab_value)
            if test_classification =="high" or test_classification == "low":
                print("*******************************************************")
                print(f"LabTest : {example_test}  Result : {example_lab_value}:  classification : {test_classification}")
                print("*******************************************************")
                evaluate_rules_for_test_value(clinician_settings=clinician_settings,labTest=example_test,test_value=example_lab_value)    
                print()
        return print("  please note rules can be added or changed to best suit that clinician ")
        
    # funtion to implement the clinician's rules on the test value that is being evaluated
    def evaluate_rules_for_test_value(clinician_settings,labTest,test_value):
        # get lab rules
        print(f"First we get all of {clinician_settings.clinician}'s rules that apply to the test {labTest}")
        print("------------------------------------------------------------------------------------------------")
        test_rules = clinician_settings.get_lab_rules(lab_name=labTest)
        print()
        print(f"Now let's see tHe {labTest} rules that match based on the rules and test result {test_value}")
        print("-------------------------------------------------------------------------------------------------")
        if test_rules:
            found_match = False
            for rule_object in test_rules:
                try:
                    # parse_value_setting now returns operator as a string
                    rule_operator_string, rule_num = clinical_logic.UserSettings.parse_value_setting(rule_object.rule)

                    # Use if/elif to perform the comparison based on the operator string        
                    rule_matches = False
                    if rule_operator_string == '<':
                        rule_matches = test_value < rule_num
                    elif rule_operator_string == '<=':
                        rule_matches = test_value <= rule_num
                    elif rule_operator_string == '>':
                        rule_matches = test_value > rule_num
                    elif rule_operator_string == '>=':
                        rule_matches = test_value >= rule_num
                    elif rule_operator_string == '==':
                        rule_matches = test_value == rule_num

                    if rule_matches:
                        print(f"Rule '{rule_object.rule}' matches. This is {clinician_settings.clinician}'s desired action: {rule_object.action}")
                        instruction = [rule_object.rule, rule_object.action]
                        found_match = True
                        return instruction
                except ValueError as e:
                    print(f"  Could not evaluate rule '{rule_object.rule}': {e}")
            if found_match == False:
                print(f"the clinician {clinician_settings.clinician} does not have a rule that matches this test result value")


    # instantiate clinical object
    print("*************  Hello World *********************")
    print("we first create a clinician who has a particular way of handling labs")
    print()
    clinical_user = input("What is the clinical user's name?")
    clinician_settings= initialize_clinican_object(clinical_user=clinical_user)
    print()

    # Main Loop
    should_finish = False
    while not should_finish:
        print("********************************************************")
        print("      Enter the number for your selection:")
        print("********************************************************")
        print("1. Dataset 1: process labork with noemal results")
        print("2. Dataset 2: process labwotk with some abnormal results")
        print("3. Dataset 3: process labwork with critical results")
        print("4. Show demonstration of the code")
        print("********************************************************")
        choice = input("Enter a number (or 'q' to quit): ")

        if choice.lower() == 'q':
            should_finish = True
        elif not choice.isdigit():
            print("Please enter a number.") 
        else:
                choice = int(choice)
                if 1 <= choice <= 4:
                    if choice == 1:
                        print()
                        print("CASE 1 sernerio- patient has normal health and normal lab results")
                        print("First the example lab tests are evaluated in comparison to normal valuse")
                        print("************************************************************************")
                        sample_data_dictionary = test_lab_data.Input_lab_results_set1_all_normal_results.items()
                        decision = tests_need_further_processing(lab_data_dictionary=sample_data_dictionary)
                        if decision==False:
                            print("The job is complete- choose another selection")
                            print()
                        elif decision == True:
                            applying_clinicians_rules(data_dictionary=sample_data_dictionary)


                    elif choice == 2:
                        print()
                        print("CASE 2 sernerio- patient has a a few non-clitical lab results")
                        print("First the example lab tests are evaluated in comparison to normal valuse")
                        print("************************************************************************")
                        sample_data_dictionary = test_lab_data.Input_lab_results_set2_some_abnormal_results.items()
                        decision = tests_need_further_processing(lab_data_dictionary=sample_data_dictionary)
                        if decision==False:
                            print("the job is complete")
                        elif decision == True:
                            applying_clinicians_rules(data_dictionary=sample_data_dictionary)
                        

                    elif choice == 3:
                        print()
                        print("CASE 3 sernerio- patient has critical abnormal results ")
                        print("First the example lab tests are evaluated in comparison to normal valuse")
                        print("************************************************************************")
                        sample_data_dictionary = test_lab_data.Input_lab_results_set3_critical_results.items()
                        decision = tests_need_further_processing(lab_data_dictionary=sample_data_dictionary)
                        if decision==False:
                            print("*****  End of analysis ****** ")
                        elif decision == True:
                            applying_clinicians_rules(data_dictionary=sample_data_dictionary)

                    elif choice == 4:
                        print()
                        demonstration_of_how_to_use__this_code()
                else:
                    print("Number must be between 1 and 4.")
 
if __name__ == "__main__":
    Main()






