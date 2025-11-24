import pyautogui
import keyboard
import time
import numpy as np
import customtkinter as ctk
from tkinter import colorchooser, simpledialog


TARGET_COLOR = (255, 0, 255)
COLOR_TOLERANCE = 30
SEARCH_ZONE_SIZE = 2
CHECK_DELAY = 0.009
TOGGLE_KEY = 'F6'

print("--- NEGRILLON COLOR BOT - by Kosailla ---")
print(f"Toggle Key : {TOGGLE_KEY}")
print(f"Target Color : {TARGET_COLOR}")


is_running = False


def check_for_target():
    screen_width, screen_height = pyautogui.size()

    center_x, center_y = screen_width // 2, screen_height // 2

    left = center_x - SEARCH_ZONE_SIZE // 2
    top = center_y - SEARCH_ZONE_SIZE // 2
    width = SEARCH_ZONE_SIZE
    height = SEARCH_ZONE_SIZE

    try:
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
    except pyautogui.FailSafeException:
        return False

    img_np = np.array(screenshot)
    color_diff = np.sum(np.abs(img_np - TARGET_COLOR), axis=2)

    if np.any(color_diff <= COLOR_TOLERANCE):
        return True
    
    return False

def main_loop():
    global is_running, TARGET_COLOR, CHECK_DELAY, COLOR_TOLERANCE, SEARCH_ZONE_SIZE, TOGGLE_KEY
    while True:
        if keyboard.is_pressed(TOGGLE_KEY):
            toggle_bot()
            time.sleep(0.3)

        if is_running:
            if check_for_target():
                pyautogui.click()
                time.sleep(0.1) 
        
        time.sleep(CHECK_DELAY)


def toggle_bot():
    global is_running
    is_running = not is_running
    if is_running:
        print("ENABLED")
    else:
        print("DISABLED")

    switch_var.set("on" if is_running else "off")

def update_target_color():
    global TARGET_COLOR
    color_code = colorchooser.askcolor(title="Choose Target Color")[0]
    if color_code:
        TARGET_COLOR = tuple(int(c) for c in color_code)
        print(f"Target Color Updated : {TARGET_COLOR}")

        hex_color = f'#{TARGET_COLOR[0]:02x}{TARGET_COLOR[1]:02x}{TARGET_COLOR[2]:02x}'
        color_preview.configure(bg=hex_color)
        color_label.configure(text=f"Actual Target : RGB({TARGET_COLOR[0]}, {TARGET_COLOR[1]}, {TARGET_COLOR[2]})")

def update_check_delay(new_delay):
    global CHECK_DELAY
    CHECK_DELAY = new_delay
    delay_label.configure(text=f"Check Delay : {CHECK_DELAY:.3f}s")
    print(f"Delay Check Updated : {CHECK_DELAY:.3f} seconds")

def update_color_tolerance(new_tolerance):
    global COLOR_TOLERANCE
    COLOR_TOLERANCE = int(new_tolerance)
    tolerance_label.configure(text=f"Color Tolerance : {COLOR_TOLERANCE}")
    print(f"Color Tolerance Updated : {COLOR_TOLERANCE}")

def update_toggle_key():
    global TOGGLE_KEY

    dialog = ctk.CTkInputDialog(text="Press Key", title="Switch Toggle Key")
    new_key = dialog.get_input()
    if new_key:
        TOGGLE_KEY = new_key
        toggle_key_label.configure(text=f"Toggle Key : {TOGGLE_KEY}")
        print(f"Toggle Key Updated : {TOGGLE_KEY}")

def update_search_zone_size(new_size):
    global SEARCH_ZONE_SIZE
    SEARCH_ZONE_SIZE = int(new_size)
    search_zone_label.configure(text=f"Target Zone : {SEARCH_ZONE_SIZE}x{SEARCH_ZONE_SIZE}")
    print(f"Target Zone Updated : {SEARCH_ZONE_SIZE}x{SEARCH_ZONE_SIZE}")


def create_menu():
    global switch_var, delay_label, tolerance_label, toggle_key_label, search_zone_label, color_label, color_preview

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("NEGRILLON Color Bot - By Kosailla")

    root.geometry("420x550") 


    main_frame = ctk.CTkFrame(root)
    main_frame.pack(padx=20, pady=20, fill="both", expand=True)

    switch_var = ctk.StringVar(value="on" if is_running else "off")
    switch = ctk.CTkSwitch(main_frame, text="ON/OFF", variable=switch_var, onvalue="on", offvalue="off", command=toggle_bot)
    switch.pack(pady=15)


    color_frame = ctk.CTkFrame(main_frame)
    color_frame.pack(pady=10, padx=10, fill="x")
    
    color_label = ctk.CTkLabel(color_frame, text=f"Actual Target : RGB({TARGET_COLOR[0]}, {TARGET_COLOR[1]}, {TARGET_COLOR[2]})")
    color_label.pack(pady=5)
    

    color_preview = ctk.CTkCanvas(color_frame, width=50, height=50, highlightthickness=0)
    hex_color = f'#{TARGET_COLOR[0]:02x}{TARGET_COLOR[1]:02x}{TARGET_COLOR[2]:02x}'
    color_preview.configure(bg=hex_color)
    color_preview.pack(pady=5)

    color_button = ctk.CTkButton(color_frame, text="Color Target", command=update_target_color)
    color_button.pack(pady=10)


    delay_label = ctk.CTkLabel(main_frame, text=f"Check Delay : {CHECK_DELAY:.3f}s")
    delay_label.pack(pady=5)
    delay_slider = ctk.CTkSlider(main_frame, from_=0.001, to=1.0, number_of_steps=999, command=update_check_delay)
    delay_slider.set(CHECK_DELAY)
    delay_slider.pack(pady=5, padx=20, fill="x")


    tolerance_label = ctk.CTkLabel(main_frame, text=f"Color Tolerance : {COLOR_TOLERANCE}")
    tolerance_label.pack(pady=5)
    tolerance_slider = ctk.CTkSlider(main_frame, from_=1, to=100, number_of_steps=99, command=update_color_tolerance)
    tolerance_slider.set(COLOR_TOLERANCE)
    tolerance_slider.pack(pady=5, padx=20, fill="x")


    toggle_key_label = ctk.CTkLabel(main_frame, text=f"Toggle Key : {TOGGLE_KEY}")
    toggle_key_label.pack(pady=5)
    toggle_key_button = ctk.CTkButton(main_frame, text="Change Toggle Key", command=update_toggle_key)
    toggle_key_button.pack(pady=10)


    search_zone_label = ctk.CTkLabel(main_frame, text=f"Target zone (Pixels) : {SEARCH_ZONE_SIZE}x{SEARCH_ZONE_SIZE}")
    search_zone_label.pack(pady=5)
    search_zone_slider = ctk.CTkSlider(main_frame, from_=1, to=50, number_of_steps=49, command=update_search_zone_size)
    search_zone_slider.set(SEARCH_ZONE_SIZE)
    search_zone_slider.pack(pady=5, padx=20, fill="x")

    root.mainloop()

if __name__ == "__main__":
    import threading
    menu_thread = threading.Thread(target=create_menu)
    menu_thread.daemon = True
    menu_thread.start()
    main_loop()