# Transmitter from VScode to GitHub

version 1

with run setup.py in your VScode , you can Uploade your current project in your GitHub repositiry.
_________________________________________________________________________________________________________

Usage Instructions :

1. move objects.py and Setup.py in your project folder (you must move to just project folder , not any folder ).
2. install tkinter library , if tkinter library is not installed in your vscode.
3. run setup.py in your vscode.
4. enter your repository address in first text box entry.
5. enter the branch that you want to move project in that at second text box entry.
6. enter a message commit in third text box entry.
7. Click from the 'git init' button in order to the 'git push' button.
8. If the push operation is successful, you will see the message 'Push to "{branch}" branch operation was successful' at the end of the terminal and the textbox program messages. :)

_________________________________________________________________________________________________________

Good luck 🎉🚀 ;)

# Version 2
In version 2 :
1) added project size button
2) added some text in entries to better guidance
3) added a combobox for write some need to enter in commit text entry (like repository name , branch name , etc)
4) added a cammand to delete git folder after push project in the code script (objects.py) --> run_command ('Remove-Item -Recurse -Force .git')
