import serial
import time
import threading
import tkinter as tk
from tkinter import simpledialog

def get_com_port():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    com_port = simpledialog.askstring("COM Port Input", "Enter the COM port fo voltz (e.g., COM9):")
    root.destroy()
    return com_port

# Get COM port from the user
com_port = get_com_port()


# Setup serial connection
ser = serial.Serial(
    port= com_port,
    baudrate=300,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

pause = False  # Global variable to control pausing

def read_adc_data():
    try:
        command = b'$1RD'  # Command to request ADC data

        # Clear the input buffer to ensure fresh data
        ser.reset_input_buffer()

        ser.write(command + b'\r')  # Send command with carriage return
        time.sleep(0.1)  # Short delay to allow the device to process the command

        response = ser.readline().decode('utf-8').strip()  # Read and decode response
        voltage = response.split('*')[1][1:]
        return voltage

    except serial.SerialException as e:
        print(f"Error: {e}")
        return None

def control_loop():
    global pause
    try:
        while True:
            if not pause:
                adc_value = read_adc_data()

                if adc_value:
                    print(f"{adc_value}")
                else:
                    print("Failed to read from the COM port.")
            time.sleep(.005)  # Wait for 1 second before the next read
    except KeyboardInterrupt:
        print("\nScript interrupted by user.")
    finally:
        ser.close()
        print("Serial connection closed.")




# Start the control loop in a separate thread
control_thread = threading.Thread(target=control_loop)
#control_thread.start()


