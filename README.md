# LEARN Quiz Maker
Problem Statement: Lots of teaching organizations use the LEARN learning management system to create and manage courses online. Quizzes are a major component of any instructional course, but everyone hates making them as they take too much time (often hours) to fill in and create questions.

Solution: I built an automation bot that automates the building of quizzes given a set of quiz/section data in the form of CSV (comma separated values) files.

## Setup
First download the .zip and extract my project by going to my project source code on my [GitHub profile](https://github.com/lekangwang/learn-quiz-maker).\
Click "Code" -> "Download ZIP" and extract my project. Make sure to change the title of the project folder from "learn-quiz-maker-main" to just "learn-quiz-maker".

This project requires use of the command line and a code text-editor.\
Code text editor suggested: [Visual Studio Code](https://code.visualstudio.com/docs/setup/setup-overview) (by Microsoft)
Click on the VSCode installer file and follow the instructions to install VSCode for both macOS and Windows 10. 

Download Python3 [here](https://www.python.org/downloads/).\
Once you've reached the Python downloads page, hover over the "Downloads" tab in the navigation bar. It should automatically suggest the latest version download for your OS. Make sure to click on Python 3.X NOT 2.X.

### THIS IS IMPORTANT
For Windows 10 users, once the Python3 download file is clicked and an installation panel opens, please check off the option called "Add Python 3.X to PATH" before you finish the installation. 

To check if Python3 was successfully installed: 

### For Windows 10:
1. Find and open the Command Prompt (Powershell) application
2. Type the following and press ENTER
```bash 
py --version or python --version (whichever one works)
```

3. Type the following and press ENTER
```bash
pip --version
```
If no error message(s) appear then Python 3 was installed successfully.

### For macOS
1. Find and open the Terminal application
2. Type the following and press ENTER
```bash 
python3 --version
```

3. Type the following and press ENTER
```bash
pip --version
```
If no error message(s) appear then Python 3 was installed successfully.

### Open VSCode Integrated Terminal
Open VSCode and select this project folder to be opened. Click on "View" in the actions bar on the top and click "Terminal". A terminal prompt should open up at the bottom in the VSCode window. This is where you will type further commands to configure/run this project.

**Note: Windows 10 and VSCode Integrated Terminal Issues** 
In Windows 10, current Python installations might have trouble providing commands you can use in the VSCode integrated terminal. If you find that an error occurs when running installation commands in the integrated terminal, try executing the following installation commands inside the Command Prompt you already have open where you checked your Python install version.

### Install Selenium 4, pyshadow, webdriver-manager
Now that we have Python 3 installed, we must now install some programs written by other developers for this project to work.

Selenium is an automation framework that helps developers write code to automate QA tasks on websites. \
Install Selenium (type and ENTER):
```bash
pip install selenium
```

pyshadow is a code package that helps with working with LEARN's quirky HTML structure. \
Install pyshadow (type and ENTER):
```bash
pip install pyshadow
```

webdriver-manager is a code package that will automatically download the appropriate drivers needed for your Chrome browser version to work with Selenium. \
Install webdriver-manager (type and ENTER):
```bash
pip install webdriver-manager
```

Type and ENTER:
```bash 
pip list
```
Check if Selenium, pyshadow and webdriver-manager are listed. 

## Usage
There are 3 CSV files in this project and 1 errors.txt file:
1. settings.csv inside the folder "navigation"
    - This file you will need to enter your UWaterloo email or your username that you use to login to your LEARN profile
    - You will also need to the enter the **EXACT** name of the course you want quizzes to be made for. Specifically I mean the larger text inside the course cards on your LEARN homepage
    - Make sure to pin your desired course at the very top of your course card list in order for my program to find it
2. sections.csv inside the folder "quiz_library"
    - This to make several sections if the quiz requires it. My program will not create the overarching quiz folder, it will only create the section folders inside with quiz questions separated into the appropriate section folder. 
    - Each row of this file is the data for 1 section folder. Please enter the information as I've done in the file already as an example.
3. learn-quiz-template.csv inside the folder "quiz_library"
    - This csv file will hold ALL of the quiz question information for 1 quiz. All of your quiz content/settings will be written in an Excel file template that I have provided. Once filled in, please export the file as a plain CSV file (with the same name learn-quiz-template.csv) and replace that file into the "quiz_library" folder.
    - Read more about specific instructions about how to fill in the LEARN quiz template Excel sheet in the template-instructions.txt file inside the folder "docs". 
3. errors.txt inside the folder "quiz_library"
    - File where you will find all the unsuccessfully made quiz questions and their associated error messages
    - My program will automatically skip to the next question if an error is encountered so execution will always complete

To run the program after configuring/adding all 3 of the necessary CSV files in the correct folders, run the following command inside the integrated terminal inside VSCode to execute the build process. 

**For Windows 10**
Type and ENTER:
```bash
py -m learn_quiz_maker
```

**For macOS**
Type and ENTER:
```bash
python3 -m learn_quiz_maker
```

You will be required to enter your password manually (for security reasons) and perform the DUO two-authentication process within 2 minutes so please have those things ready. After logging in, the program will perform the rest of the actions automatically without further intervention. 

**IMPORTANT**
If you need to end the Quiz Maker script at any time, type **Ctrl (or CMD) + C** in the VS Code Terminal. 

## License
[MIT](https://choosealicense.com/licenses/mit/)
