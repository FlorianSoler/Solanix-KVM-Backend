# interfaces/__init__.py
from dotenv import load_dotenv

from .hid_interface import HIDInterface
from .ch9329_hid import CH9329HID

load_dotenv()