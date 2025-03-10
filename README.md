Shape Memory Alloy Expansion Measurement

Project Overview

This project is designed to measure and visualize the expansion of Shape Memory Alloys (SMA) by capturing temperature and displacement data from a thermocouple and a displacement sensor. The data is read through RS232 communication and displayed graphically in real-time.


How It Works


The system consists of three Python scripts:

datat.py: The main script that collects data, logs it to a file, and generates real-time graphs.

temp.py: Reads temperature data from the thermocouple via a serial COM port.

voltz.py: Reads displacement voltage data from a sensor via another serial COM port.


Steps:


The user inputs their name, date, and project name via a Tkinter prompt.

The user is then prompted to enter the COM ports for the temperature and voltage sensors.

The temp.py and voltz.py scripts communicate with the respective sensors over RS232.

Data is continuously logged into a .txt file and displayed in real-time using Matplotlib.

The program plots temperature vs. displacement (converted from voltage readings).

The script allows for user interruption and safely closes serial connections upon termination.


COM Ports Configuration


Since the sensors communicate via RS232, each sensor must be assigned to a COM port. The user is prompted to enter the COM port numbers when running the script. Ensure that:

The thermocouple is connected to the correct COM port (e.g., COM10).

The displacement sensor is connected to another COM port (e.g., COM9).

The correct baud rate (300) and serial settings are configured for both devices.

If using USB-to-RS232 adapters, verify their port assignments in the device manager.


Hardware Requirements


Thermocouple for temperature measurement

Displacement sensor with RS232 output

Computer with Python installed

RS232-to-USB adapters (if needed)

Software Requirements

Python 3.x


Required Python Libraries:


serial (for RS232 communication)

tkinter (for user input dialogs)

matplotlib (for real-time graphing)

threading (for parallel data acquisition)


Running the Project


Ensure all required hardware is connected to the appropriate COM ports.

Run datat.py:

python datat.py

Follow the on-screen prompts to enter project details and COM ports.

Observe real-time graphing of temperature vs. displacement.

Stop the script using Ctrl + C when finished.

The logged data can be found in the generated .txt file.


Applications


This project is particularly useful for research and industrial applications involving Shape Memory Alloys, where precise measurement of expansion due to temperature changes is required. It can be modified for various materials and different experimental setups.

Future Improvements

Implement GUI-based control for easier configuration.

Automate COM port detection.

Improve data smoothing and filtering for more accurate plots.

Add export options for CSV or Excel formats.
  This project is particularly useful for research and industrial applications involving Shape Memory Alloys, where precise measurement of expansion due to temperature changes is required. It can be modified for various materials and different experimental setups.
![Screenshot 2024-10-16 165549](https://github.com/user-attachments/assets/46bb7b1d-3a4d-44b3-b051-707a8277172e)

