import os
from pathlib import Path
from tkinter.filedialog import askdirectory
from urllib.parse import urlparse

import customtkinter
import requests

# test link http://ipv4.download.thinkbroadband.com/5MB.zip

# get downloads dir
home_dir = Path.home()
default_location = home_dir / "Downloads"
selected_location = None

def button_callback():
    global selected_location

    if not selected_location:
        selected_location = default_location

    response = requests.get(link, stream=True)
    response.raise_for_status()

    file_path = os.path.join(selected_location, os.path.basename(urlparse(link).path))

    total_size = int(response.headers.get('content-length', 0))
    downloaded_size = 0

    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
                downloaded_size += len(chunk)

                progress = downloaded_size / total_size
                download_progressbar.set(progress)

                app.update_idletasks()


def add_link_button_callback():
    global link
    file_name_label.configure(text="Processing....")

    dialog = customtkinter.CTkInputDialog(text="Input file link here", title="Downloader")
    link = dialog.get_input()
    if link:
        try:
            response = requests.get(link, stream=True)
            response.raise_for_status()

            parsed_url = urlparse(link)
            file_name_label.configure(text=f"File Name: {os.path.basename(parsed_url.path)}")
            download_button.configure(state="normal")
        except requests.RequestException as e:
            file_name_label.configure(text=f"Error: {e}")
    else:
        file_name_label.configure(text="No link provided")

def save_location_button_callback():
    global selected_location
    select_location = askdirectory()
    if select_location:
        selected_location = select_location
        file_location_label.configure(text=selected_location)
    else:
        file_location_label.configure(text="No directory selected")


# window
app = customtkinter.CTk()
app.title("File Downloader")
app.geometry("600x300")

# grid
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(0, weight=1)

# frame1
main_frame = customtkinter.CTkFrame(app)
main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

# r0
title_label = customtkinter.CTkLabel(main_frame, text="File Downloader", font=("Arial", 20, "bold"))
title_label.grid(row=0, column=0, pady=(0, 20))

# r1
file_name_label = customtkinter.CTkLabel(main_frame, text="No file selected", fg_color="transparent")
file_name_label.grid(row=1, column=0, pady=(0, 20))

add_link_button = customtkinter.CTkButton(main_frame, text="Add Link", command=add_link_button_callback)
add_link_button.grid(row=1, column=1, pady=(0, 20), padx=10, sticky="e")


#r2
file_location_label = customtkinter.CTkLabel(main_frame, text=str(default_location), fg_color="transparent")
file_location_label.grid(row=2, column=0, pady=(0, 20))

save_location_button = customtkinter.CTkButton(main_frame, text="Location", command=save_location_button_callback)
save_location_button.grid(row=2, column=1, pady=(0, 20), padx=10, sticky="e")


#r3
download_progressbar = customtkinter.CTkProgressBar(main_frame, orientation="horizontal", width=400, mode="determinate")
download_progressbar.set(0)
download_progressbar.grid(row=3, column=0, pady=20)

download_button = customtkinter.CTkButton(main_frame, text="Download", command=button_callback, state="disabled")
download_button.grid(row=3, column=1, pady=(0, 20), padx=10, sticky="w")

# Run the app
app.mainloop()
