import tkinter as tk
from tkinter import ttk
import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, Key

# Global variables
mouse = Controller()
clicking = False
stop_event = threading.Event()


def click_loop():
    """Background thread that clicks with live delay from slider"""
    while not stop_event.is_set():
        if clicking:
            current_delay = delay_slider.get()
            mouse.click(Button.left)
            time.sleep(current_delay)
        else:
            time.sleep(0.1)


def toggle_clicking():
    """Toggle clicking state and update GUI"""
    global clicking
    clicking = not clicking

    if clicking:
        start_button.config(text="Stop Clicking")
        status_label.config(text="Status: Clicking ON", foreground="green")
    else:
        start_button.config(text="Start Clicking")
        status_label.config(text="Status: Clicking OFF", foreground="red")


def on_f6_press(key):
    """Keyboard listener callback for F6"""
    if key == Key.f6:
        # Safely update GUI from the main thread
        root.after(0, toggle_clicking)


def on_closing():
    """Clean shutdown"""
    global clicking, keyboard_listener
    clicking = False
    stop_event.set()
    if 'keyboard_listener' in globals() and keyboard_listener.is_alive():
        keyboard_listener.stop()
    root.destroy()


# ------------------- GUI Setup -------------------
root = tk.Tk()
root.title("Auto Clicker")
root.geometry("420x360")
root.resizable(False, False)
root.configure(bg="#f0f0f0")
try:
    icon = tk.PhotoImage(file="./icon.png")  # Change "icon.png" if you use a different name
    root.iconphoto(False, icon)
except tk.TclError:
    print("Icon file not found or invalid. Using default icon.")

tk.Label(root, text="Auto Clicker", font=("Helvetica", 20, "bold"), bg="#f0f0f0").pack(pady=20)

start_button = ttk.Button(root, text="Start Clicking", command=toggle_clicking)
start_button.pack(pady=12)

# Delay Slider
delay_frame = tk.Frame(root, bg="#f0f0f0")
delay_frame.pack(pady=10)

tk.Label(delay_frame, text="Click Delay (seconds):", font=("Helvetica", 12), bg="#f0f0f0").pack()
delay_slider = ttk.Scale(delay_frame, from_=0.01, to=1.0, orient="horizontal", length=320)
delay_slider.set(0.1)
delay_slider.pack()

delay_label = tk.Label(delay_frame, text="Delay: 0.100 seconds", font=("Helvetica", 10), bg="#f0f0f0")
delay_label.pack(pady=5)


def update_delay_label(val):
    delay_label.config(text=f"Delay: {float(val):.3f} seconds")


delay_slider.config(command=update_delay_label)
update_delay_label(0.1)

# Status
status_label = tk.Label(root, text="Status: Clicking OFF", font=("Helvetica", 14), foreground="red", bg="#f0f0f0")
status_label.pack(pady=20)

# Hotkey info
tk.Label(root,
         text="Hotkey: Press F6 to Start/Stop\n(Works globally — even when window is in background)",
         font=("Helvetica", 10), fg="blue", bg="#f0f0f0", justify="center").pack(pady=10)

tk.Label(root,
         text="Move your mouse to the location you want to click.\nDelay changes take effect instantly.",
         font=("Helvetica", 9), fg="gray", bg="#f0f0f0", justify="center").pack(pady=5)

# ------------------- Start Threads -------------------
# Clicking thread
click_thread = threading.Thread(target=click_loop, daemon=True)
click_thread.start()

# Global F6 hotkey listener
keyboard_listener = Listener(on_press=on_f6_press)
keyboard_listener.start()

# Handle window close
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start GUI
root.mainloop()