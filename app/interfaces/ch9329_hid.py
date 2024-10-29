# interfaces/ch9329_hid.py

import os
from serial import Serial
from .hid_interface import HIDInterface
from ch9329 import keyboard, mouse
from ch9329.config import get_manufacturer, get_product, get_serial_number

class CH9329HID(HIDInterface):
    def __init__(self):
        self.device = None
        # Get COM port and baud rate from environment variables, or use defaults
        self.serial_port = os.getenv("HID_SERIAL_PORT")
        self.baud_rate = int(os.getenv("HID_SERIAL_BAUD_RATE", 9600))
        self.ser = None  # Initialize the Serial object

    def init_connection(self):
        """Initialize the CH9329 HID device connection."""
        try:
            self.ser = Serial(self.serial_port, self.baud_rate, timeout=0.05)  # Open the serial connection
        except Exception as e:
            raise ConnectionError(f"Failed to initialize CH9329 device on port {self.serial_port}: {e}")

    def press_key(self, key: str):
        """Press a specified key on the HID device."""
        if not self.ser:
            raise ConnectionError("Device not initialized. Call init_connection first.")
        try:
            keyboard.press_and_release(self.ser, key)  # Press and release the key
        except Exception as e:
            raise IOError(f"Failed to press key '{key}' on device: {e}")

    def release_key(self, key: str):
        """Release a specified key on the HID device."""
        # This method can be defined for additional implementations if needed.

    def set_mouse_position(self, x: int, y: int, relative: bool = False):
        """Set the mouse position by moving x and y units."""
        if not self.ser:
            raise ConnectionError("Device not initialized. Call init_connection first.")
        try:
            if relative:
                mouse.move(self.ser, x=x, y=y, relative=True)  # Move mouse relatively
            else:
                mouse.move(self.ser, x=x, y=y)  # Move mouse to absolute position
        except Exception as e:
            raise IOError(f"Failed to move mouse to position x: {x}, y: {y}: {e}")

    def mouse_click(self, button: str):
        """Press mouse click button."""
        if not self.ser:
            raise ConnectionError("Device not initialized. Call init_connection first.")
        try:
            mouse.click(self.ser, button)
        except Exception as e:
            raise IOError(f"Failed to click mouse button '{button}': {e}")

    def disconnect(self):
        """Clean up and close the connection to the HID device."""
        if self.ser:
            try:
                self.ser.close()  # Close the serial connection
            except Exception as e:
                raise IOError(f"Error while disconnecting: {e}")
            finally:
                self.ser = None

    def set_baud_rate(self, baud_rate: int):
        """Set the baud rate for the CH9329 device."""
        valid_baud_rates = [9600, 19200, 38400, 57600, 115200]  # Common baud rates
        if baud_rate not in valid_baud_rates:
            raise ValueError(f"Invalid baud rate: {baud_rate}. Valid rates are: {valid_baud_rates}")

        self.baud_rate = baud_rate
        # Reinitialize the connection with the new baud rate
        self.disconnect()
        try:
            self.init_connection()
        except ConnectionError as e:
            raise ConnectionError(f"Failed to set new baud rate {baud_rate}: {e}")

    def get_device_info(self):
        """Get information about the HID device."""
        if not self.ser:
            raise ConnectionError("Device not initialized. Call init_connection first.")

        try:
            serial_number = get_serial_number(self.ser)
            product = get_product(self.ser)
            manufacturer = get_manufacturer(self.ser)
        except Exception as e:
            raise IOError(f"Failed to retrieve device information: {e}")

        return {
            "serial_number": serial_number,
            "product": product,
            "manufacturer": manufacturer,
        }
