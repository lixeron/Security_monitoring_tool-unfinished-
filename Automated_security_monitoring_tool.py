import time
import re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class LogMonitor(FileSystemEventHandler):
    def on_modified(self, event):
        # Check if the modified file is not a directory and ends with .log
        if not event.is_directory and event.src_path.endswith(".log"):
            self.process_log(event.src_path)

    def process_log(self, filepath):
        # Open and read the file to check for specific log patterns
        with open(filepath, "r") as file:
            lines = file.readlines()
            for line in lines:
                if "Failed login" in line:
                    if self.detect_brute_force(line):
                        self.send_alert(line)

    def detect_brute_force(self, log_entry):
        # Regular expression to find failed login attempts
        pattern = r"Failed login for user (\S+) from IP (\S+)"
        matches = re.findall(pattern, log_entry)
        if matches:
            user, ip = matches[0]
            print(f"Brute force attempt detected from {ip} for user {user}")
            return True
        return False

    def send_alert(self, message):
        # Placeholder for alert logic; replace with actual email sending code
        print(f"Alert: {message}")
        # Example: Use smtplib to send an email alert here

def main():
    # Specify the path to the directory containing log files
    path = r"C:\Users\puffy\Downloads"  # Ensure this is the correct path
    event_handler = LogMonitor()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        # Keep the script running until manually interrupted
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Stop the observer if interrupted
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
