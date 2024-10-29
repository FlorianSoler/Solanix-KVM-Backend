from abc import ABC, abstractmethod

class HIDInterface(ABC):
    @abstractmethod
    def init_connection(self):
        """Initialize the HID device connection."""
        pass

    @abstractmethod
    def press_key(self, key: str):
        """Press a specified key on the HID device."""
        pass

    @abstractmethod
    def release_key(self, key: str):
        """Release a specified key on the HID device."""
        pass

    @abstractmethod
    def set_mouse_position(self, x: int, y: int):
        """Set the mouse position by moving x and y units."""
        pass

    @abstractmethod
    def mouse_click(self, button: str):
        """Press mouse click button"""
        pass


    @abstractmethod
    def disconnect(self):
        """Clean up and close the connection to the HID device."""
        pass

    @abstractmethod
    def set_baud_rate(self, baud_rate: int):
        """
        Set the communication baud rate for the HID device.
        This allows configuration of the device's serial communication speed.
        """
        pass
