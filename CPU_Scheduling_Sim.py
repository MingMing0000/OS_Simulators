import customtkinter as ctk
import tkinter as tk 
from tkinter import messagebox
import CTkTable
from CTkTable import *
from CTkMessagebox import CTkMessagebox
from CPU_scheduling_algorithms import SchedulingAlgorithms

processes = []

def add_process():
        name = name_input.get()
        at = arrival_input.get()
        bt = burst_input.get()
        prio = priority_input.get() or "0"

        if not (name and at and bt):
            CTkMessagebox(title="Input Error", message="Please fill in all required fields (Name, Arrival Time, Burst Time).", icon="cancel")
            return

        try:
            at = int(at)
            bt = int(bt)
            prio = int(prio)
        except ValueError:
            CTkMessagebox(title="Input Error", message="Arrival Time, Burst Time, and Priority must be integers.", icon="cancel")
            return

        processes.append({"name": name, "at": at, "bt": bt, "prio": prio, "rem_bt": bt})
        
        table.add_row([name, at, bt, prio])

        name_input.delete(0, ctk.END)
        arrival_input.delete(0, ctk.END)
        burst_input.delete(0, ctk.END)
        priority_input.delete(0, ctk.END)

def clear_all():
        global table
        processes.clear()
        table.destroy()
        table = CTkTable(master=table_frame, values=[table_headers], colors=["gray14", "gray16"], header_color="gray20", text_color="white")
        table.pack(fill="both", expand=True)
        canvas.delete("all")
        computations.set("Avg Turnaround Time: 0.00 ms   |   Avg Waiting Time: 0.00 ms")

def run_simulation():
    if not processes:
        CTkMessagebox(title="Warning", message="No processes to simulate.", icon="warning")
        return

    algo = algo_var.get()
    
    for p in processes:
        p['rem_bt'] = p['bt']

    if algo == "FCFS":
         schedule, avg_tat, avg_wt = SchedulingAlgorithms.simulate_fcfs(processes)
    elif algo == "SJF - Non-Preemptive":
         schedule, avg_tat, avg_wt = SchedulingAlgorithms.simulate_sjf(processes)
    elif algo == "SJF - Preemptive":
         schedule, avg_tat, avg_wt = SchedulingAlgorithms.simulate_srtf(processes)
    elif algo == "Priority - Non-Preemptive":
         schedule, avg_tat, avg_wt = SchedulingAlgorithms.simulate_priority_nonpreemptive(processes)
    elif algo == "Priority - Preemptive":
         schedule, avg_tat, avg_wt = SchedulingAlgorithms.simulate_priority_preemptive(processes)
    elif algo == "Round Robin":
        try:
            tq = int(quantum_entry.get())
            if tq <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Time Quantum must be a positive integer.")
            return
        schedule, avg_tat, avg_wt = SchedulingAlgorithms.simulate_rr(processes, tq)

    computations.set(f"Avg Turnaround Time: {avg_tat:.2f} ms   |   Avg Waiting Time: {avg_wt:.2f} ms")
    draw_gantt_chart(schedule)

def draw_gantt_chart(schedule):
    canvas.delete("all")
    if not schedule:
        return

    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    
    if canvas_width <= 1: 
        app.update()
        canvas_width = canvas.winfo_width()

    total_time = schedule[-1][2]
    if total_time == 0: return

    pad_x = 20
    usable_width = canvas_width - (2 * pad_x)
    scale = usable_width / total_time
    
    y1 = canvas_height // 2 - 25
    y2 = canvas_height // 2 + 25

    colors = ["#FF595E", "#8AC926", "#1982C4", "#6A4C93", "#FFCA3A", "#F15BB5"]
    color_map = {}
    color_idx = 0

    for block in schedule:
        name, start, end = block
        
        if name not in color_map:
            color_map[name] = colors[color_idx % len(colors)]
            color_idx += 1
            
        x1 = pad_x + (start * scale)
        x2 = pad_x + (end * scale)

        canvas.create_rectangle(x1, y1, x2, y2, fill=color_map[name], outline="white", width=2)
        canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=name, font=("Arial", 12, "bold"), fill="white")
        canvas.create_text(x1, y2 + 15, text=str(start), font=("Arial", 10), fill="gray80")
        canvas.create_text(x2, y2 + 15, text=str(end), font=("Arial", 10), fill="gray80")

app = ctk.CTk()
app.title("CPU Scheduling Simulator")
app.geometry("805x700")

label =ctk.CTkLabel(app, text="Process Input", font=ctk.CTkFont(size=16, weight="bold"))
label.pack(pady=10)

input_frame = ctk.CTkFrame(app)
input_frame.pack(fill="x", padx=10, pady=5)

ctk.CTkLabel(input_frame, text="Process Name:").grid(row=0, column=0, padx=5, pady=5)
name_input = ctk.CTkEntry(input_frame, width=70)
name_input.grid(row=0, column=1, padx=5, pady=5)

ctk.CTkLabel(input_frame, text="Arrival Time:").grid(row=0, column=2, padx=5, pady=5)
arrival_input = ctk.CTkEntry(input_frame, width=70)
arrival_input.grid(row=0, column=3, padx=5, pady=5)

ctk.CTkLabel(input_frame, text="Burst Time:").grid(row=0, column=4, padx=5, pady=5)
burst_input = ctk.CTkEntry(input_frame, width=70)
burst_input.grid(row=0, column=5, padx=5, pady=5)

ctk.CTkLabel(input_frame, text="Priority:").grid(row=0, column=6, padx=5, pady=5)
priority_input = ctk.CTkEntry(input_frame, width=70)
priority_input.grid(row=0, column=7, padx=5, pady=5)

add_btn = ctk.CTkButton(input_frame, text="Add Process", command=add_process)
add_btn.grid(row=0, column=8, padx=15, pady=5)

control_frame = ctk.CTkFrame(app)
control_frame.pack(fill="x", padx=10, pady=10)

ctk.CTkLabel(control_frame, text="Algorithm:").grid(row=0, column=0, padx=5, pady=5)
algo_var = ctk.StringVar(value="FCFS")
algorithms = ["FCFS", "SJF - Non-Preemptive", "SJF - Preemptive", "Priority - Non-Preemptive", "Priority - Preemptive", "Round Robin"]
algo_dropdown = ctk.CTkComboBox(control_frame, variable=algo_var, values=algorithms, state="readonly", width=190)
algo_dropdown.grid(row=0, column=1, padx=5, pady=5)

ctk.CTkLabel(control_frame, text="Time Quantum (for RR):").grid(row=0, column=2, padx=(20, 5))
quantum_entry = ctk.CTkEntry(control_frame, width=40)
quantum_entry.grid(row=0, column=3, padx=5, pady=5)
quantum_entry.insert(0, "2")

run_btn = ctk.CTkButton(control_frame, text="Run Simulation", command=run_simulation, fg_color="#2FA572")
run_btn.grid(row=0, column=4, padx=10, pady=5)

clear_btn = ctk.CTkButton(control_frame, text="Clear All", command=clear_all, fg_color="#E85D04")
clear_btn.grid(row=0, column=5, pady=5)

table_frame = ctk.CTkFrame(app, fg_color="transparent")
table_frame.pack(fill="both", expand=True, padx=20, pady=10)

table_headers = ["Name", "Arrival Time", "Burst Time", "Priority"]

table = CTkTable(master=table_frame, values=[table_headers], colors=["gray14", "gray16"], header_color="gray20", text_color="white")
table.pack(fill="both", expand=True)

computations = ctk.StringVar(value="Avg Turnaround Time: 0.00 ms   |   Avg Waiting Time: 0.00 ms")
ctk.CTkLabel(app, textvariable=computations, font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)

gantt_frame = ctk.CTkFrame(app)
gantt_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
ctk.CTkLabel(gantt_frame, text="Gantt Chart", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=10, pady=10)
            
canvas = tk.Canvas(gantt_frame, bg="#2b2b2b", highlightthickness=0, height=100)
canvas.pack(fill="both", expand=True, padx=10, pady=(0, 10))

app.mainloop()