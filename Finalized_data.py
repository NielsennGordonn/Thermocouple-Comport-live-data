import threading
import time
import os
import tkinter as tk
from tkinter import simpledialog
import RS232_Tmp as tmp
import RS232_Voltz as Voltz
import matplotlib.pyplot as plt

# Get the directory of the script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Function to get user input
def get_user_input():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Get user inputs
    user_name = simpledialog.askstring("Input", "Enter your name:")
    project_date = simpledialog.askstring("Input", "Enter the date (YYYY-MM-DD):")
    project_title = simpledialog.askstring("Input", "Enter the project/Test name:")

    root.destroy()
    return user_name, project_date, project_title

# Get user input
user_name, project_date, project_title = get_user_input()

# Replace spaces and special characters in the project title to create a valid filename
sanitized_project_title = project_title.replace(" ", "_").replace("/", "_").replace("\\", "_")

# Set the output file path based on the project title
output_file_path = os.path.join(script_dir, f'{sanitized_project_title}.txt')

# Initialize lists to store temperature and voltage data
temperatures = []
voltages = []

# Use a lock to prevent concurrent access to the serial ports
lock = threading.Lock()

###############################################################################  TXT ##########################################################################

def print_temperature_and_voltage(user_name, project_date, project_title):
    count = 1

    try:
        with open(output_file_path, 'w') as file:
            # Write the header information
            header = f'\n\nUser Name: {user_name}\n     Date: {project_date}\nTest Name: {project_title}\n'
            print(f"Writing header to file: {header.strip()}")  # Debug statement for header
            file.write(header)
            file.write(f'{"Count":<6} | {"Temp":<10}    | {"Voltage":<10}\n')
            file.flush()  # Ensure header is written to the file

            try:
                while True:
                    with lock:
                        temperature = tmp.read_adc_data()
                        voltage = Voltz.read_adc_data()

                    if temperature is not None and voltage is not None:
                        try:
                            voltage = float(voltage) / 10000  # Convert voltage to float and divide by 10000
                            data_line = f'{count:<6} | {temperature:<10}(°C) | {voltage:<10}(Inches) \n'
                            print(f"Writing data to file: {data_line.strip()}")  # Debug statement for data
                            file.write(data_line)
                            file.flush()
                            count += 1
                        except ValueError:
                            print("Received non-numeric voltage data.")
                    else:
                        print("Failed to read data from the COM port.")
                    time.sleep(0.005)
            except KeyboardInterrupt:
                print("\nScript interrupted by user.")
            finally:
                with lock:
                    tmp.ser.close()
                    Voltz.ser.close()
                print("Serial connections closed.")
    except IOError as e:
        print(f"Failed to open file {output_file_path}: {e}")


############################################################################### Graph ##########################################################################

def plot_temperature_and_voltage():
    try:
        plt.ion()
        fig, ax = plt.subplots()

        while True:
            with lock:
                temperature = tmp.read_adc_data()
                voltage = Voltz.read_adc_data()

            if temperature is not None and voltage is not None:
                temperatures.append(float(temperature))
                voltages.append(float(voltage) / 10000)

                ax.clear()
                ax.plot(temperatures[:-1], voltages[:-1], marker='o', color='b')  # Plot previous points in blue
                ax.plot(temperatures[-1:], voltages[-1:], marker='o', color='r', markersize=10)  # Plot the most recent point in red
                ax.set_xlabel('Temperature (°C)')
                ax.set_ylabel('Displacement (Inches)')
                ax.set_title(project_title)
                ax.grid(True)

                plt.draw()
                plt.pause(0.05)
            else:
                print("Failed to read data from the COM port.")
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\nScript interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        try:
            with open(output_file_path, 'a') as file:
                for temp, volt in zip(temperatures, voltages):
                    file.write(f'{temp}\t{volt}\n')

            with lock:
                tmp.ser.close()
                Voltz.ser.close()
            print("Serial connections closed.")
            print(f"Data appended to {output_file_path}.")
        except Exception as e:
            print(f"An error occurred while saving data: {e}")

###############################################################################  MAIN  ##########################################################################

# Start the temperature and voltage control loop in separate threads
data_thread = threading.Thread(target=print_temperature_and_voltage, args=(user_name, project_date, project_title), daemon=True)
plot_thread = threading.Thread(target=plot_temperature_and_voltage, daemon=True)

data_thread.start()
plot_thread.start()

# Wait for threads to start and run
try:
    while data_thread.is_alive() and plot_thread.is_alive():
        time.sleep(1)
except KeyboardInterrupt:
    print("Main script interrupted by user.")

print("Exiting main script.")
