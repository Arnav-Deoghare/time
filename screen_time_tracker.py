import time
import re
import ctypes
import pygetwindow as gw
import threading
import keyboard

class ScreenTimeTracker:
    def __init__(self):
        self.active_window = None
        self.start_time = None
        self.time_spent = {}
        self.total_time = 0
        self.idle_threshold = 60  # 1 minute of idle time threshold
        self.is_tracking = False
        self.tracker_thread = threading.Thread(target=self.track_time, daemon=True)

    def get_idle_time(self):
        class LASTINPUTINFO(ctypes.Structure):
            _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_int)]

        last_input_info = LASTINPUTINFO()
        last_input_info.cbSize = ctypes.sizeof(LASTINPUTINFO)
        ctypes.windll.user32.GetLastInputInfo(ctypes.byref(last_input_info))
        millis_since_last_input = ctypes.windll.kernel32.GetTickCount() - last_input_info.dwTime
        return millis_since_last_input / 1000

    def extract_domain(self, title):
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

    def track_time(self):
        print("Tracking started. Press 'q' to quit.\n")
        self.is_tracking = True
        while self.is_tracking:
            try:
                if self.get_idle_time() > self.idle_threshold:
                    time.sleep(1)
                    continue

                window = gw.getActiveWindow()
                if window:
                    current_window = window.title
                    domain = self.extract_domain(current_window)

                    if self.active_window != current_window:
                        if self.active_window and self.start_time:
                            self.update_time_spent(self.previous_domain)
                        self.active_window = current_window
                        self.previous_domain = domain
                        if domain not in self.time_spent:
                            self.time_spent[domain] = 0
                        self.start_time = time.time()

                    self.update_display_time()

                if keyboard.is_pressed("q"):
                    self.stop()
                    break

                time.sleep(1)
            except Exception as e:
                print(f"Error: {e}")
                break  # Exit the loop on exception

    def update_display_time(self):
        if self.start_time:
            elapsed_time = time.time() - self.start_time
            minutes, seconds = divmod(int(elapsed_time), 60)
            formatted_time = f"{minutes:02}:{seconds:02}"
            try:
                print(f"\rCurrent Window: {self.previous_domain} | Time Spent: {formatted_time}", end="")
            except Exception:
                pass  # Avoids errors during shutdown

    def update_time_spent(self, domain):
        if self.start_time:
            elapsed_time = time.time() - self.start_time
            self.time_spent[domain] += elapsed_time
            self.total_time += elapsed_time

    def print_summary(self):
        print("\n\n--- Screen Time Summary ---")
        for domain, time_spent in self.time_spent.items():
            minutes, seconds = divmod(int(time_spent), 60)
            print(f"'{domain}': {minutes:02}:{seconds:02}")

        total_minutes, total_seconds = divmod(int(self.total_time), 60)
        print(f"\nTotal Screen Time: {total_minutes:02}:{total_seconds:02}")

    def stop(self):
        """Signal the thread to stop and print the summary."""
        self.is_tracking = False
        print("\n\nTracking stopped.")
        self.print_summary()

    def start_tracking(self):
        """Start the tracking thread."""
        self.tracker_thread.start()
