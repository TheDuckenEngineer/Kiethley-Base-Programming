# Introduction
In order to speed up data collection within the lab, a set of python scripts have been developed to access the Keithley buffer and store its results in a csv. This permits faster data collection without data overwriting as a result of starting a new scan before saving the previous buffer. Additionally, these scripts automatically adjust the Keithley channels to the appropriate scan settings. 
The purpose of this guide is to enable any lab user the ability to connect and collect data from a Keithley DAQ6510 with any computer for data collection using an ethernet cable. 
There are three programs that need to be downloaded before using the Keithley scripts. First is VSCode. This is a versatile and powerful programming environment with many open-source extensions to make programing easier. It can be used with any coding language so long as the language is installed on the device. Second is git. Git is a version control system that facilitates communication between GitHub, the location of our code, and VSCode. Note, unless you want to make meaningful improvements to the code, you don’t need a GitHub account. As new updates come about, git will automatically install these on your device. It will override any adjustments you’ve made so make sure to document these changes. The final program is uv-sync. This revolutionary program will find the necessary library dependencies the Keithley scripts use and download them onto your system. This makes the Keithley scripts immediately usable. 


# Program Installation Links
Begin by downloading VSCode and git.
https://code.visualstudio.com/
https://git-scm.com/downloads/win

Finally, install uv-sync. Open the PowerShell or command terminal and paste the following code. Restart the computer after installation.
'''
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
'''	

# Keithley Scripts Installation 
Go to TheDuckenEngineers GitHub and click on the Keithley-Base-Programming repository. Move to the green code drop down and press copy link.
https://github.com/TheDuckenEngineer/Kiethley-Base-Programming
![image](https://github.com/user-attachments/assets/406f9bb3-6a5c-4ffb-85b6-df844e55781e)

Open a new window in VSCode. If it’s prepopulated, it means the current window is working in a directory in your computer. Opening a new window creates an unlinked directory that the Keithley scripts can be saved, unaffecting other directories and scripts.
 ![image](https://github.com/user-attachments/assets/4486cd54-f73a-4313-a08e-5702815469c7)

Select the folder location and hit enter. A prompt will ask to open the new folder to which you say yes. When it opens, head to the Laser Displacement and open. The top imports should have a yellow underscore. This is fine and we should proceed to the next step. 

Open the folder containing the Keithley scripts.
![image](https://github.com/user-attachments/assets/e946c14f-7e99-43e4-83ed-78c75205450b)

Right click and scroll down to the terminal option. This will produce a black (or blue) terminal window for that directory. Copy and paste the following command. It will automatically begin downloading all necessary libraries, the python virtual environment, and establish communication to the source (src) folder. 
'''
uv run --script Test.py --with .
'''
Restart VSCode. The top import lines won’t have the yellow underscore showing the setup is complete. 

Finish by making a Data folder for your dated to be automatically stored into. 

Updates will manifest at the bottom left of the program. Updates will show as a number attributed to the downwards arrow. Be sure to check this occasionally. 
![image](https://github.com/user-attachments/assets/24897d88-4c89-45d3-ba98-97b3ec5fa97f)


# Description of Code
Each code block is separated by headers indicating what the following body of code performs. Since python is a high-level programming language it’s easy to read each line and understand what each does. A small description of important features will be listed here. 

## Device Connection
Using the ethernet cable means we will communicate with the LAN socket on the Keithley. The IP address is of the Keithley device. It can be found on the Keithley’s home screen under a tab located at the upper left corner. I’ve set Keithley 1 and Keithley 2 manually to the scripts IP address. Afterwards, a subroutine will automatically connect to the Keithley. 

## Try-Exception Handling
The control script is nested in a try-exception handling format. This allows the Keithley to be set up and data to begin being collected. When we want to finish, click into the terminal and press CTRL+C. This is the key binding for the KEYBOARD exception. The data then be read from the Keithley’s buffer and placed into a pandas data frame to be saved as a csv. If we don’t assert the KEYBOARD exception, the script will run for 10 minutes. 

## SRC\Keithley_Base
This folder contains functions that run as subroutines for the Keithley. The __init__.py shouldn’t be moves as it serves as a placeholder for uv-sync to connect these files, in a subdirectory, to the primary directory. Functions contains misc. functions that simplify the main Keithley scripts. Keithley_connect operates all the writing, querying, and reading of the Keithley.  Finally, Keithely_setup sets up all the channels. Keithley can communicate using the SCPI or TSP communication protocols. We use SCPI. A pdf manual of the DAQ 6510 is provided within the GitHub download so we can search for the desired command for each channel setup. Generally, these shouldn’t be messed with unless you understand the commands or wish to have a specific setting enabled. 
