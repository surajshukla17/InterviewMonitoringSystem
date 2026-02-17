import tkinter as tk
import os

def start_project():
    os.system("python main.py")

app = tk.Tk()
app.title("Interview Monitoring System")
app.geometry("350x200")

label = tk.Label(app, text="Interview Monitoring System", font=("Arial", 14))
label.pack(pady=20)

start_btn = tk.Button(app, text="Start Monitoring", font=("Arial", 12), command=start_project)
start_btn.pack(pady=10)

exit_btn = tk.Button(app, text="Exit", font=("Arial", 12), command=app.destroy)
exit_btn.pack(pady=10)

app.mainloop()
