# cintel-06-custom

**Continuous Intelligence App**
* Repository: https://github.com/Priyankanaskar/cintel-06-custom

* Website: (https://github.com/Priyankanaskar/cintel-06-custom)
* Author: Priyanka Naskar
* Date : 4/11/2024

Customize Your Web App
Get the Code to your Local Machine
Open VS Code and from the menu, select View / Command Palette.
Type "Git: Clone" in the command palette and select it.
Enter the URL (web address) of your forked GitHub repository (make sure it contains your GitHub username - not denisecase).
Choose a directory on your local machine (e.g., Documents folder) to store the project.
Avoid spaces in your directory and file names. If you have spaces, you'll need to use double quotes to keep the entire path recognized as a single string.
If prompted, sign in to GitHub from VS Code.
Make Changes in VS Code
With your respository folder open in VS Code:

Click on this README.md file for editing.
Update the README.md file by changing your name in the author link above.
Update the links in the README.md file to your username instead of denisecase.
Save Your Changes
After making changes, you want to send them back to GitHub.
In VS Code, find the "Source Control" icon and click it.
Important: Enter a brief commit message describing your changes.
Change the "Commit" button dropdown to "Commit and Push" to send your changes back to GitHub.
Create a Local Virtual Environment
Open a PowerShell terminal in this cintel-05-live-updates folder on your machine. Create a virtual environment named .venv in the current directory. Verify that a .venv folder was created after running the command.

python -m venv .venv
If VS Code asks to use it as the workspace folder, select Yes.

Activate the Environment
Run the following command to activate the virtual environment we just created. Verify that the PowerShell prompt now shows (.venv) at the beginning of the line.

.venv\Scripts\activate
Prepare the Environment
Run the following commands to upgrade pip and install required packages. Rerun as needed until everything is successfully installed.

python -m pip install --upgrade pip wheel pyodide-py
python -m pip install --upgrade -r requirements.txt
Read the requirements.txt file to see the packages we are installing.

Additional information can be found in our first Shiny repo: cintel-02-app/SHINY.md

Run the App
Verify your virtual environment is activated and packages have been installed. Run the following PowerShell command to start the app.

shiny run app.py
You may use shiny run app.py --reload but it can be harder to stop the app during development. Open the app by following the instructions provided in the terminal. For example, try CTRL CLICK (at the same time) on the URL displayed (http://127.0.0.1:8000).

Hit CTRL c (at the same time) to quit the app. If it won't stop, close the terminal window. Reopen the terminal window and be sure the virtual environment is activated before running the app again.

Deploy the App
Add and customize .github/workflows/deploy.yml. Login to shinyapps.io then Account / Tokens and add 3 repo secrets. See the earlier SHINYAPPS.md for details.

Name: SHINYAPPS_ACCOUNT, Secret: Paste shinyapps.io account name
Name: SHINYAPPS_TOKEN, Secret: (paste token )
Name: SHINYAPPS_SECRET, Secret: (paste secret)
⚠️ Delete Hosted App Before Pushing to GitHub
Reminder: The GitHub action deploy.yml may not automatically delete an existing app from shinyapps.io so we can redeploy.

Before pushing to GitHub, login to shinyapps.io and view the list of applications.

First archive the app.
Then delete the archived app.