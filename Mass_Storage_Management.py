import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def fcfs(head, requests, disk_size):
    return [head] + requests

def sstf(head, requests, disk_size):
    path = [head]
    reqs = requests.copy()
    current = head
    while reqs:
        nearest = min(reqs, key=lambda x: abs(x - current))
        path.append(nearest)
        current = nearest
        reqs.remove(nearest)
    return path

def scan(head, requests, disk_size):
    path = [head]
    reqs = sorted(requests)
    left = [r for r in reqs if r <= head]
    right = [r for r in reqs if r > head]
    
    for r in right:
        path.append(r)
    if not right or path[-1] != disk_size - 1:
        path.append(disk_size - 1)
    for r in reversed(left):
        path.append(r)
    return path

def c_scan(head, requests, disk_size):
    path = [head]
    reqs = sorted(requests)
    left = [r for r in reqs if r <= head]
    right = [r for r in reqs if r > head]
    
    for r in right:
        path.append(r)
    if not right or path[-1] != disk_size - 1:
        path.append(disk_size - 1)
    
    path.append(0)
    for r in left:
        path.append(r)
    return path

def look(head, requests, disk_size):
    path = [head]
    reqs = sorted(requests)
    left = [r for r in reqs if r <= head]
    right = [r for r in reqs if r > head]
    
    for r in right:
        path.append(r)
    for r in reversed(left):
        path.append(r)
    return path

def c_look(head, requests, disk_size):
    path = [head]
    reqs = sorted(requests)
    left = [r for r in reqs if r <= head]
    right = [r for r in reqs if r > head]
    
    for r in right:
        path.append(r)
    for r in left:
        path.append(r)
    return path

class DiskSchedulerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Disk Scheduling Simulator")
        self.geometry("1100x650")
        self.configure(bg="#f0f0f0")

        control_frame = tk.Frame(self, bg="#f0f0f0")
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

        font_label = ("Arial", 11)
        font_entry = ("Arial", 11)

        tk.Label(control_frame, text="Algorithm:", bg="#f0f0f0", font=font_label).pack(anchor=tk.W)
        self.algo_var = tk.StringVar(value="SSTF")
        algos = ["FCFS", "SSTF", "SCAN", "C-SCAN", "LOOK", "C-LOOK"]
        self.algo_combo = ttk.Combobox(control_frame, textvariable=self.algo_var, values=algos, state="readonly", font=font_entry)
        self.algo_combo.pack(anchor=tk.W, pady=(0, 15), fill=tk.X)

        tk.Label(control_frame, text="Initial Head Position:", bg="#f0f0f0", font=font_label).pack(anchor=tk.W)
        self.head_entry = tk.Entry(control_frame, font=font_entry)
        self.head_entry.pack(anchor=tk.W, pady=(0, 15), fill=tk.X)
        self.head_entry.insert(0, "53")

        tk.Label(control_frame, text="Disk Size (Tracks):", bg="#f0f0f0", font=font_label).pack(anchor=tk.W)
        self.size_entry = tk.Entry(control_frame, font=font_entry)
        self.size_entry.pack(anchor=tk.W, pady=(0, 15), fill=tk.X)
        self.size_entry.insert(0, "200")

        tk.Label(control_frame, text="Requests (comma-separated):", bg="#f0f0f0", font=font_label).pack(anchor=tk.W)
        self.req_entry = tk.Text(control_frame, height=4, width=30, font=font_entry)
        self.req_entry.pack(anchor=tk.W, pady=(0, 15))
        self.req_entry.insert(tk.END, "98, 183, 37, 122, 14, 124, 65, 67")

        sim_btn = tk.Button(control_frame, text="Simulate", command=self.simulate, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), relief=tk.FLAT, pady=5)
        sim_btn.pack(fill=tk.X, pady=(0, 20))

        tk.Label(control_frame, text="Computation Details:", bg="#f0f0f0", font=("Arial", 11, "bold")).pack(anchor=tk.W)
        self.comp_text = tk.Text(control_frame, height=18, width=45, state=tk.DISABLED, font=("Courier New", 10))
        self.comp_text.pack(anchor=tk.W)

        # Graph Panel
        self.graph_frame = tk.Frame(self, bg="white", bd=2, relief=tk.GROOVE)
        self.graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.fig.patch.set_facecolor('white')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def simulate(self):
        try:
            algo = self.algo_var.get()
            head = int(self.head_entry.get().strip())
            disk_size = int(self.size_entry.get().strip())
            req_str = self.req_entry.get("1.0", tk.END).strip()
            if not req_str:
                requests = []
            else:
                requests = [int(x.strip()) for x in req_str.split(',') if x.strip()]
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers for Head, Disk Size, and Requests.")
            return

        if not requests:
            messagebox.showerror("Input Error", "Requests list cannot be empty.")
            return
        if any(r < 0 or r >= disk_size for r in requests):
            messagebox.showwarning("Warning", f"Some requests are outside the disk size (0 to {disk_size-1}).")

        algorithms = {
            "FCFS": fcfs,
            "SSTF": sstf,
            "SCAN": scan,
            "C-SCAN": c_scan,
            "LOOK": look,
            "C-LOOK": c_look
        }

        func = algorithms.get(algo)
        path = func(head, requests, disk_size)

        self.update_graph(path)
        self.update_computations(path)

    def update_graph(self, path):
        self.ax.clear()
        
        y_values = list(range(len(path)))
        
        self.ax.plot(path, y_values, marker='o', color='black', linestyle='-', markersize=6)
        
        for i in range(len(path)-1):
            self.ax.annotate('', xy=(path[i+1], y_values[i+1]), xytext=(path[i], y_values[i]),
                             arrowprops=dict(arrowstyle="->", color='black', shrinkA=5, shrinkB=5))

        self.ax.set_yticks([])
        unique_ticks = sorted(list(set(path)))
        self.ax.set_xticks(unique_ticks)
        self.ax.xaxis.tick_top()
        
        self.ax.invert_yaxis()
        
        self.ax.set_title(f"{self.algo_var.get()} Disk Scheduling", pad=30, fontsize=16, fontweight='bold')
        
        self.fig.tight_layout()
        self.canvas.draw()

    def update_computations(self, path):
        self.comp_text.config(state=tk.NORMAL)
        self.comp_text.delete("1.0", tk.END)
        
        self.comp_text.insert(tk.END, "Computing for the total head movement:\n")
        
        total_movement = 0
        for i in range(len(path) - 1):
            start = path[i]
            end = path[i+1]
            movement = abs(end - start)
            total_movement += movement
            
            self.comp_text.insert(tk.END, f"from {start:<3} to {end:<3} =    {max(start, end):>3} - {min(start, end):<3} = {movement:>4}\n")
            
        self.comp_text.insert(tk.END, " " * 32 + "-" * 11 + "\n")
        self.comp_text.insert(tk.END, f"Total head movement = {total_movement:>13} tracks\n")
        self.comp_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    app = DiskSchedulerGUI()
    app.mainloop()
