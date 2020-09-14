"""My first program."""
# Save the user input to the variable "username"
username = input("Hello, my name is Python! Please type your name to continue our conversation.")
# Save the user input to the variable "has_programmed before"
has_programmed_before = input("Have you programmed before?")
# Check if the user has programmed before
if has_programmed_before == "Yes":  # User typed Yes
    print("Congratulations, " + username + "! It will be a little bit easier for you.")
elif has_programmed_before == "No":  # User typed "No"
    print("Don`t worry, " + username + "! You will learn everything you need.")
else:  # The user didn't insert "Yes" or "No"
    print("Your input is incorrect!")
