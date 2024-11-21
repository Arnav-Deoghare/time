import tkinter as tk
from tkinter import ttk

def create_gui(root, tracker):
    root.title("Screen Time Tracker - Digital Wellbeing")
    root.geometry("600x400")
    root.config(bg="#2f2f2f")  # Dark gray background

    # Gradient background (Simple for now)
    canvas = tk.Canvas(root, height=400, width=600)
    canvas.pack(fill="both", expand=True)
    canvas.create_rectangle(0, 0, 600, 400, fill="#333333", outline="")

    # Title label
    title_label = tk.Label(root, text="Screen Time Tracker", font=("Arial", 16), fg="white", bg="#333333")
    title_label.pack(pady=10)

    # Time spent label
    time_label = tk.Label(root, text="Total Screen Time: 00:00", font=("Arial", 14), fg="white", bg="#333333")
    time_label.pack(pady=5)

    # Progress bar
    progress = ttk.Progressbar(root, length=200, mode="determinate", maximum=100)
    progress.pack(pady=10)

    # Listbox for active apps/websites
    app_listbox = tk.Listbox(root, height=10, width=50, bg="#444444", fg="white", selectmode=tk.SINGLE)
    app_listbox.pack(pady=10)

    # Buttons for starting and stopping tracking
    start_button = tk.Button(root, text="Start Tracking", command=tracker.start_tracking, bg="#555555", fg="white")
    start_button.pack(pady=10)

    stop_button = tk.Button(root, text="Stop Tracking", command=tracker.stop, bg="#555555", fg="white")
    stop_button.pack(pady=5)

    # Close event to stop the program when the window is closed
    root.protocol("WM_DELETE_WINDOW", lambda: tracker.stop())

def update_display(self, formatted_time):
    """Update the GUI with formatted time."""
    time_label.config(text=f"Total Screen Time: {formatted_time}")
