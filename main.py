import tkinter as tk
from tkinter import ttk
from ctypes import windll
import sched
import time
import threading

class TaskReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Reminder")
        self.root.geometry("400x250")
        self.root.configure(bg="#2e2e2e")

        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.event = None
        self.thread = None
        self.running = False

        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#2e2e2e", foreground="white", font=("Helvetica", 12))
        style.configure("TButton", background="#4d4d4d", foreground="white", font=("Helvetica", 12), padding=6)
        style.configure("TEntry", fieldbackground="#4d4d4d", foreground="white", font=("Helvetica", 12))

        self.interval_label = ttk.Label(self.root, text="Time Interval (seconds):")
        self.interval_label.pack(pady=(20, 5))

        self.interval_entry = ttk.Entry(self.root, font=("Helvetica", 12))
        self.interval_entry.pack(pady=5)

        self.message_label = ttk.Label(self.root, text="Notification Message:")
        self.message_label.pack(pady=5)

        self.message_entry = ttk.Entry(self.root, font=("Helvetica", 12))
        self.message_entry.pack(pady=5)

        self.start_button = ttk.Button(self.root, text="Start", command=self.start_notifications)
        self.start_button.pack(pady=5)

        self.stop_button = ttk.Button(self.root, text="Stop", command=self.stop_notifications, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

    def show_popup_notification(self, message):
        popup = tk.Toplevel(self.root)
        popup.title("Task Reminder")
        popup.minsize(300, 120)
        popup.configure(bg="#2e2e2e")
        popup.attributes('-topmost', True)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#2e2e2e", foreground="white", font=("Helvetica", 12))
        style.configure("TButton", background="#4d4d4d", foreground="white", font=("Helvetica", 12), padding=6)

        content_frame = tk.Frame(popup, bg="#2e2e2e", padx=20, pady=10)
        content_frame.pack(expand=True, fill='both')

        message_label = ttk.Label(content_frame, text=message, wraplength=260)
        message_label.pack(expand=True, fill='both')

        dismiss_button = ttk.Button(content_frame, text="Dismiss", command=popup.destroy)
        dismiss_button.pack(pady=(10, 5))

        # Adjust window size based on content
        popup.update()

        # Calculate position for center of screen
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        window_width = popup.winfo_width()
        window_height = popup.winfo_height()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))

        # Set the position
        popup.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    def schedule_notifications(self, interval, message):
        while self.running:
            self.show_popup_notification(message)
            time.sleep(interval)

    def start_notifications(self):
        interval = int(self.interval_entry.get())
        message = self.message_entry.get()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.running = True
        self.thread = threading.Thread(target=self.schedule_notifications, args=(interval, message))
        self.thread.start()

    def stop_notifications(self):
        self.running = False
        if self.thread:
            self.thread.join()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def on_closing(self):
        self.stop_notifications()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    windll.shcore.SetProcessDpiAwareness(1)
    app = TaskReminderApp(root)
    root.mainloop()
