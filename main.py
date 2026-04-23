import customtkinter as ctk
from tkinter import messagebox, filedialog

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Banker's Algorithm Simulator - Ultimate")
app.geometry("1100x750")

alloc_entries = []
max_entries = []

# -------- FUNCTIONS -------- #

def toggle_mode():
    mode = ctk.get_appearance_mode()
    ctk.set_appearance_mode("light" if mode == "Dark" else "dark")

def reset_all():
    process_entry.delete(0, "end")
    resource_entry.delete(0, "end")
    available_entry.delete(0, "end")
    output.delete("1.0", "end")
    for widget in matrix_frame.winfo_children():
        widget.destroy()

def save_output():
    file = filedialog.asksaveasfilename(defaultextension=".txt")
    if file:
        with open(file, "w") as f:
            f.write(output.get("1.0", "end"))

def create_table():
    global alloc_entries, max_entries
    for widget in matrix_frame.winfo_children():
        widget.destroy()

    alloc_entries = []
    max_entries = []

    try:
        n = int(process_entry.get())
        m = int(resource_entry.get())
    except:
        messagebox.showerror("Error", "Invalid Input")
        return

    ctk.CTkLabel(matrix_frame, text="Allocation", font=("Segoe UI", 14, "bold")).grid(row=0, column=1)
    ctk.CTkLabel(matrix_frame, text="Maximum", font=("Segoe UI", 14, "bold")).grid(row=0, column=3)

    for i in range(n):
        ctk.CTkLabel(matrix_frame, text=f"P{i}").grid(row=i+1, column=0)

        alloc_row = []
        max_row = []

        for j in range(m):
            a = ctk.CTkEntry(matrix_frame, width=50)
            a.grid(row=i+1, column=1+j, padx=3, pady=3)
            alloc_row.append(a)

            b = ctk.CTkEntry(matrix_frame, width=50)
            b.grid(row=i+1, column=3+j, padx=3, pady=3)
            max_row.append(b)

        alloc_entries.append(alloc_row)
        max_entries.append(max_row)

def run_algorithm():
    try:
        n = int(process_entry.get())
        m = int(resource_entry.get())

        allocation = []
        maximum = []
        available = list(map(int, available_entry.get().split()))

        for i in range(n):
            alloc = [int(e.get()) for e in alloc_entries[i]]
            maxm = [int(e.get()) for e in max_entries[i]]

            for j in range(m):
                if alloc[j] > maxm[j]:
                    messagebox.showerror("Error", "Allocation > Max")
                    return

            allocation.append(alloc)
            maximum.append(maxm)

        need = [[maximum[i][j] - allocation[i][j] for j in range(m)] for i in range(n)]

        finish = [False]*n
        safe_seq = []
        work = available[:]

        while len(safe_seq) < n:
            found = False
            for i in range(n):
                if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                    for j in range(m):
                        work[j] += allocation[i][j]
                    safe_seq.append(i)
                    finish[i] = True
                    found = True
            if not found:
                break

        output.delete("1.0", "end")

        output.insert("end", "🔹 NEED MATRIX\n\n")
        for i in range(n):
            output.insert("end", f"P{i}: {need[i]}\n")

        if len(safe_seq) == n:
            output.insert("end", "\n✅ SYSTEM IS SAFE\n")
            output.insert("end", "➡ Sequence: " + " → ".join(f"P{i}" for i in safe_seq))
        else:
            output.insert("end", "\n❌ SYSTEM IS UNSAFE")

    except:
        messagebox.showerror("Error", "Invalid Input")

# -------- UI -------- #

title = ctk.CTkLabel(app, text="Banker's Algorithm Simulator",
                     font=("Segoe UI", 28, "bold"))
title.pack(pady=15)

top = ctk.CTkFrame(app, corner_radius=20)
top.pack(pady=10, padx=20)

ctk.CTkLabel(top, text="Processes").grid(row=0, column=0, padx=10)
process_entry = ctk.CTkEntry(top, width=100)
process_entry.grid(row=0, column=1)

ctk.CTkLabel(top, text="Resources").grid(row=0, column=2, padx=10)
resource_entry = ctk.CTkEntry(top, width=100)
resource_entry.grid(row=0, column=3)

# Buttons
btn_frame = ctk.CTkFrame(app, fg_color="transparent")
btn_frame.pack(pady=10)

ctk.CTkButton(btn_frame, text="📊 Create Table", command=create_table,
              width=150).grid(row=0, column=0, padx=8)

ctk.CTkButton(btn_frame, text="▶ Run", command=run_algorithm,
              fg_color="#00a86b", width=120).grid(row=0, column=1, padx=8)

ctk.CTkButton(btn_frame, text="🌙 Toggle Mode", command=toggle_mode,
              width=150).grid(row=0, column=2, padx=8)

ctk.CTkButton(btn_frame, text="💾 Save", command=save_output,
              width=120).grid(row=0, column=3, padx=8)

ctk.CTkButton(btn_frame, text="🔄 Reset", command=reset_all,
              fg_color="#d9534f", width=120).grid(row=0, column=4, padx=8)

matrix_frame = ctk.CTkFrame(app, corner_radius=20)
matrix_frame.pack(pady=10)

ctk.CTkLabel(app, text="Available Resources").pack()
available_entry = ctk.CTkEntry(app, width=200)
available_entry.pack(pady=5)

output = ctk.CTkTextbox(app, width=800, height=250, corner_radius=20)
output.pack(pady=15)

app.mainloop()