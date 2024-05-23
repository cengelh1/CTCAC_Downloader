import tkinter as tk
from tkinter import filedialog
from functools import partial
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

def download_files(url, file_type, file_path, browser):
    download_directory = os.path.join(os.getcwd(), file_path)
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)

    # Debugging statement to print the value of url
    print("URL received:", url)

    # Validate the URL
    if not url:
        print("Error: URL cannot be empty.")
        return

    # Check if the URL starts with a valid scheme (e.g., http:// or https://)
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    try:
        if browser == 'Chrome':
            driver = webdriver.Chrome()
        elif browser == 'Firefox':
            driver = webdriver.Firefox()
        else:
            print("Error: Unsupported browser specified.")
            return

        driver.get(url)
        driver.implicitly_wait(10)

        if file_type == 'Excel':
            selector = "a[href$='.xlsx']"
        elif file_type == 'PDF':
            selector = "a[href$='.pdf']"
        else:
            driver.quit()
            return

        file_links = driver.find_elements(By.CSS_SELECTOR, selector)
        file_urls = [link.get_attribute("href") for link in file_links]

        for file_url in file_urls:
            response = requests.get(file_url)
            if response.status_code == 200:
                filename = os.path.join(download_directory, os.path.basename(file_url))
                with open(filename, "wb") as file:
                    file.write(response.content)

        driver.quit()

    except Exception as e:
        print("Error:", e)

def browse_button(entry):
    filename = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, filename)

def create_gui():
    window = tk.Tk()
    window.title("File Downloader")

    tk.Label(window, text="URL:").grid(row=0, column=0, sticky="w")
    url_entry = tk.Entry(window)
    url_entry.grid(row=0, column=1)

    tk.Label(window, text="File Type:").grid(row=1, column=0, sticky="w")
    file_type_var = tk.StringVar(window)
    file_type_var.set("Excel")  # default value
    file_type_menu = tk.OptionMenu(window, file_type_var, "Excel", "PDF")
    file_type_menu.grid(row=1, column=1)

    tk.Label(window, text="Browser:").grid(row=2, column=0, sticky="w")
    browser_var = tk.StringVar(window)
    browser_var.set("Firefox")  # default value
    browser_menu = tk.OptionMenu(window, browser_var, "Firefox", "Chrome")
    browser_menu.grid(row=2, column=1)

    tk.Label(window, text="Save Path:").grid(row=3, column=0, sticky="w")
    save_path_entry = tk.Entry(window)
    save_path_entry.grid(row=3, column=1)
    browse_button_func = partial(browse_button, save_path_entry)
    tk.Button(window, text="Browse", command=browse_button_func).grid(row=3, column=2)

    # Debugging statement to print the value of the URL entry widget
    def download_with_debug():
        print("URL entry value:", url_entry.get())
        download_files(url_entry.get(), file_type_var.get(), save_path_entry.get(), browser_var.get())
    tk.Button(window, text="Download", command=download_with_debug).grid(row=4, columnspan=2)

    window.mainloop()

if getattr(sys, 'frozen', False):  # When running as an executable
    # Set the current working directory to the script's directory
    os.chdir(sys._MEIPASS)

if __name__ == "__main__":
    create_gui()