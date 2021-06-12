# Shoping cart project

## Tasks accomplished
- [x] Base requirements
- [x] Configuring Sales Tax Rate
- [x] Handling Pricing per Pound
- [x] Writing Receipts to File
- [x] Sending Receipts via Email
- [x] Integrating with a CSV File Datastore


##Princeple of operation

An app is buit around the main "while" loop which keep asking for the user to enter a  product id until he enters the word DONE. Within the loop the app checks if user is entering a valid id and propmts the user if id entered does not exist. The list of products is pulled from the csv file using pandas package and converted to dataframe for convenient search by utilizing .loc functionaility of the dataframe class. 

There are 3 main function in the app
 - **save_to_file** 
 - **email** 
 - **print_receipt** 
 
### save_to_file


Here the function takes in the string and saves it to the txt file in a specified folder. The string is passed from the email function.

### email

This function takes in the string from the print_receipt function and sends it to an email via SendGridAPIClient. All of the API keys and parameters are pulled from .env file

### print_receipt
 This function takes in the list of products and compiles a receipt string which is first printed and then sent to email function.
 
 ## Things to note
 
 For Handling Pricing per Pound task the original csv file was added with additional product and all of the items received an additional attribute named "price_per" with item and pound values. Since the csv file was excluded from git commits, these attributes would need to be recreated for the proper operation of the app. 
 
 