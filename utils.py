import ctypes
import re

def get_idle_time():
    """Returns the system idle time in seconds."""
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_int)]

    last_input_info = LASTINPUTINFO()
    last_input_info.cbSize = ctypes.sizeof(LASTINPUTINFO)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(last_input_info))
    millis_since_last_input = ctypes.windll.kernel32.GetTickCount() - last_input_info.dwTime
    return millis_since_last_input / 1000

def extract_domain(title):
    """Extracts the domain name from the window title if it's a browser window."""
    if "YouTube" in title:
        return "youtube.com"
    elif "Instagram" in title:
        return "instagram.com"
    elif "Twitter" in title:
        return "twitter.com"
    elif "Facebook" in title:
        return "facebook.com"

    domain_match = re.search(r"(?:www\.)?([a-zA-Z0-9-]+)\.(com|org|net|edu|gov|io|co|us|in)", title)
    if domain_match:
        return domain_match.group(1)
    return title
