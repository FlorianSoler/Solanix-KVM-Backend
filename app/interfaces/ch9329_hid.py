import os
from hid_interface import HIDInterface
from ch9329 import CH9329, KeyboardKey, MouseMove  # Import necessary components

class CH9329HID(HIDInterface):
    def __init__(self):
        self.device = None
        # Get COM port and baud rate from environment variables, or use defaults
        self.serial_port = os.getenv("HID_SERIAL_PORT", "COM3")
        self.baud_rate = int(os.getenv("HID_SERIAL_BAUD_RATE", 9600))  # Default baud rate is 9600

    def init_connection(self):
        """Initialize the CH9329 HID device connection."""
        try:
            # Use the serial port and baud rate during initialization
            self.device = CH9329(port=self.serial_port, baudrate=self.baud_rate)  # Create an instance of the CH9329 device
            print(f"CH9329 HID initialized on {self.serial_port} at {self.baud_rate} baud rate.")
        except Exception as e:
            raise ConnectionError(f"Failed to initialize CH9329 device: {e}")

    def press_key(self, key: str):
        """Press a specified key on the HID device."""
        if not self.device:
            raise ConnectionError("Device not initialized. Call init_connection first.")
        
        key_enum = getattr(KeyboardKey, key.upper(), None)
        if key_enum is None:
            raise ValueError(f"Invalid key '{key}'")
        
        self.device.press_key(key_enum)
        print(f"Key '{key}' pressed on device.")

    def release_key(self, key: str):
        """Release a specified key on the HID device."""
        if not self.device:
            raise ConnectionError("Device not initialized. Call init_connection first.")
        
        key_enum = getattr(KeyboardKey, key.upper(), None)
        if key_enum is None:
            raise ValueError(f"Invalid key '{key}'")
        
        self.device.release_key(key_enum)
        print(f"Key '{key}' released on device.")

    def set_mouse_position(self, x: int, y: int):
        """Set the mouse position by moving x and y units."""
        if not self.device:
            raise ConnectionError("Device not initialized. Call init_connection first.")
        
        self.device.move_mouse(MouseMove(x=x, y=y))  # Move mouse to specified position
        print(f"Mouse moved to position x: {x}, y: {y}.")

    def disconnect(self):
        """Clean up and close the connection to the HID device."""
        if self.device:
            self.device.disconnect()  # Assuming the device has a disconnect method
            self.device = None
            print("Disconnected from CH9329 device.")
        else:
            print("No device to disconnect.")

    def set_baud_rate(self, baud_rate: int):
        """Set the baud rate for the CH9329 device."""
        valid_baud_rates = [9600, 19200, 38400, 57600, 115200]  # Common baud rates
        if baud_rate not in valid_baud_rates:
            raise ValueError(f"Invalid baud rate: {baud_rate}. Valid rates are: {valid_baud_rates}")

        self.baud_rate = baud_rate
        # Assuming the library has a way to set the baud rate
        self.device.set_baud_rate(baud_rate)  # Check if set_baud_rate method exists in the library
        print(f"Baud rate set to {self.baud_rate} for the CH9329 device.")
