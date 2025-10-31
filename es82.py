import serial.tools.list_ports
import serial

def find_esp_port():
    """
    Searches for the ESP8266 device by scanning all available serial ports.
    Returns the port name if found; otherwise, None.
    """
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(port.description)
        if "USB" in port.description or "UART" in port.description or "CH340" in port.description:
            return port.device
    return None

def check_esp_connection(port):
    """
    Tests the connection to the ESP8266 by sending a newline and checking for a response.
    Returns True if the device responds; otherwise, False.
    """
    try:
        with serial.Serial(port, baudrate=115200, timeout=2) as ser:
            ser.write(b'\r\n')  # Send a newline to wake up the ESP8266
            response = ser.read(10)  # Read a small response from the device
            if response:
                return True
    except Exception as e:
        print(f"Error: {e}")
    return False

def main():
    """
    Main function to detect and test the connection to an ESP8266.
    """
    esp_port = find_esp_port()
    if esp_port:
        print(f"ESP8266 detected on port: {esp_port}")
        if check_esp_connection(esp_port):
            print("Connection to ESP8266 successful!")
        else:
            print("ESP8266 found but not responding. Check the baud rate or connection.")
    else:
        print("No ESP8266 device detected. Ensure it's connected and powered on.")

main()