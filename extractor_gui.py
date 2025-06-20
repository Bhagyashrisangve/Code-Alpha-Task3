import os
import re
import shutil
import csv
import json
import logging
from tkinter import Tk, filedialog, Button, Label, messagebox, PhotoImage, Frame

# Setup logging
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, 'app.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Regex pattern for email 
email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')

# GUI
def start_extraction():
    folder = filedialog.askdirectory(title="Select Folder with .txt files")
    if not folder:
        messagebox.showwarning("No Folder Selected", "Please select a folder.")
        return

    logging.info(f"Selected folder: {folder}")
    processed_folder = os.path.join(folder, 'processed')
    os.makedirs(processed_folder, exist_ok=True)
    os.makedirs("output", exist_ok=True)

    email_set = set()

    for filename in os.listdir(folder):
        if filename.endswith('.txt'):
            filepath = os.path.join(folder, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    emails = email_pattern.findall(content)
                    email_set.update(emails)
                    logging.info(f"Extracted from: {filename} -> {len(emails)} emails")
                
                shutil.move(filepath, os.path.join(processed_folder, filename))
            except Exception as e:
                logging.error(f"Error processing {filename}: {e}")

    if email_set:
        # Save to CSV
        with open('output/extracted_emails.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Email'])
            for email in sorted(email_set):
                writer.writerow([email])
        
        # Save to JSON
        with open('output/extracted_emails.json', 'w', encoding='utf-8') as jsonfile:
            json.dump(sorted(email_set), jsonfile, indent=4)

        messagebox.showinfo("Success", f"Extracted {len(email_set)} unique emails.")
        logging.info(f"Extraction complete: {len(email_set)} emails saved.")
    else:
        messagebox.showinfo("No Emails Found", "No email addresses were found.")
        logging.info("No emails found.")

# Styled GUI setup 
root = Tk()
root.title("📧 Email Extractor Automation")
root.geometry("500x300")
root.configure(bg="#f0f8ff") 

# Frame to center content
frame = Frame(root, bg="#ffffff", bd=2, relief="ridge")
frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=200)

Label(frame, text="📂 Automated Email Extractor", font=("Helvetica", 16, "bold"), bg="#ffffff", fg="#333333").pack(pady=15)

Button(
    frame,
    text="📁 Select Folder and Extract Emails",
    command=start_extraction,
    font=("Arial", 12, "bold"),
    bg="#4caf50",
    fg="white",
    activebackground="#45a049",
    padx=20,
    pady=10,
    relief="flat",
    cursor="hand2"
).pack()

root.mainloop()
