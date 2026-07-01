import customtkinter as ctk
import subprocess
import sys
import os
import multiprocessing

def launch_simulator_process(script_name):
    if script_name == "CPU_Scheduling_Sim.py":
        import CPU_Scheduling_Sim
    elif script_name == "Memory_Management_OS.py":
        import Memory_Management_OS
    elif script_name == "Virtual_Memory_Managament.py":
        import Virtual_Memory_Managament
        import tkinter as tk
        root_window = tk.Tk()
        application = Virtual_Memory_Managament.VirtualMemoryGUI(root_window)
        root_window.mainloop()
    elif script_name == "Mass_Storage_Management.py":
        import Mass_Storage_Management
        app = Mass_Storage_Management.DiskSchedulerGUI()
        app.mainloop()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class OSMainMenu(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("OS Simulation Suite")
        self.geometry("900x650")
        self.resizable(False, False)

        self.bg_color = "#11121d"
        self.card_bg = "#1a1b26"
        self.card_border = "#24283b"
        
        self.accent_cpu = "#7aa2f7"      
        self.accent_memory = "#9ece6a"    
        self.accent_storage = "#ff9e64"  
        self.accent_vmem = "#bb9af7"      

        self.configure(fg_color=self.bg_color)

        self.create_header()

        self.create_grid()


    def create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=40, pady=(35, 10))

        title_label = ctk.CTkLabel(
            header_frame,
            text="OPERATING SYSTEM SIMULATION SUITE",
            font=ctk.CTkFont(family="Arial", size=26, weight="bold"),
            text_color="#c0caf5"
        )
        title_label.pack(anchor="w")

        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Interactive visualizations demonstrating core operating system principles and algorithms",
            font=ctk.CTkFont(family="Arial", size=13),
            text_color="#565f89"
        )
        subtitle_label.pack(anchor="w", pady=(5, 0))

    def create_grid(self):
        grid_container = ctk.CTkFrame(self, fg_color="transparent")
        grid_container.pack(fill="both", expand=True, padx=40, pady=(15, 20))

        grid_container.grid_columnconfigure(0, weight=1, uniform="grid")
        grid_container.grid_columnconfigure(1, weight=1, uniform="grid")
        grid_container.grid_rowconfigure(0, weight=1, uniform="grid")
        grid_container.grid_rowconfigure(1, weight=1, uniform="grid")

        modules = [
            {
                "title": "CPU Scheduling",
                "icon": "⚡",
                "desc": "Simulate and compare scheduling algorithms including FCFS, SJF (Preemptive & Non-Preemptive), Priority, and Round Robin. Generates dynamic Gantt charts and timing details.",
                "color": self.accent_cpu,
                "script": "CPU_Scheduling_Sim.py",
                "action_text": "Launch Simulator",
                "is_placeholder": False,
                "row": 0,
                "col": 0
            },
            {
                "title": "Memory Management",
                "icon": "💾",
                "desc": "Explore memory allocation strategies (First Fit, Next Fit, Best Fit, Worst Fit) using dynamic partitioned memory mapping. Track processes and fragmentation visualizer.",
                "color": self.accent_memory,
                "script": "Memory_Management_OS.py",
                "action_text": "Launch Simulator",
                "is_placeholder": False,
                "row": 0,
                "col": 1
            },
            {
                "title": "Virtual Memory Management",
                "icon": "🧠",
                "desc": "Simulate virtual memory page replacement algorithms (FIFO, LRU) with page faults, hits, and physical memory frame status visualization step-by-step.",
                "color": self.accent_vmem,
                "script": "Virtual_Memory_Managament.py",
                "action_text": "Launch Simulator",
                "is_placeholder": False,
                "row": 1,
                "col": 0
            },
            {
                "title": "Mass Storage Scheduling",
                "icon": "💿",
                "desc": "Simulate disk head queue planning algorithms (FCFS, SSTF, SCAN, C-SCAN, LOOK, C-LOOK). Visualizes head travel sequences and tracks detailed step computations.",
                "color": self.accent_storage,
                "script": "Mass_Storage_Management.py",
                "action_text": "Launch Simulator",
                "is_placeholder": False,
                "row": 1,
                "col": 1
            }
        ]

        for mod in modules:
            self.create_card(grid_container, mod)

    def create_card(self, parent, mod):
        card = ctk.CTkFrame(
            parent,
            fg_color=self.card_bg,
            border_color=self.card_border,
            border_width=2,
            corner_radius=12
        )
        card.grid(row=mod["row"], column=mod["col"], padx=12, pady=12, sticky="nsew")

        accent_strip = ctk.CTkFrame(
            card,
            fg_color=mod["color"],
            width=5,
            height=200,
            corner_radius=0
        )
        accent_strip.pack(side="left", fill="y")

        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        title_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        title_frame.pack(fill="x", anchor="w")

        icon_label = ctk.CTkLabel(
            title_frame,
            text=mod["icon"],
            font=ctk.CTkFont(size=24),
            text_color=mod["color"]
        )
        icon_label.pack(side="left", padx=(0, 10))

        title_label = ctk.CTkLabel(
            title_frame,
            text=mod["title"],
            font=ctk.CTkFont(family="Arial", size=17, weight="bold"),
            text_color="#c0caf5"
        )
        title_label.pack(side="left")

        desc_label = ctk.CTkLabel(
            content_frame,
            text=mod["desc"],
            font=ctk.CTkFont(family="Arial", size=12),
            text_color="#9ece6a" if not mod["is_placeholder"] else "#565f89",
            justify="left",
            anchor="nw",
            wraplength=320
        )
        desc_label.configure(text_color="#a9b1d6" if not mod["is_placeholder"] else "#565f89")
        desc_label.pack(fill="both", expand=True, pady=(15, 15))

        if mod["is_placeholder"]:
            btn = ctk.CTkButton(
                content_frame,
                text=mod["action_text"],
                fg_color="#24283b",
                text_color="#565f89",
                state="disabled",
                corner_radius=8,
                height=35,
                font=ctk.CTkFont(family="Arial", size=13, weight="bold")
            )
            card.bind("<Button-1>", lambda e: self.show_placeholder_info())
            content_frame.bind("<Button-1>", lambda e: self.show_placeholder_info())
            desc_label.bind("<Button-1>", lambda e: self.show_placeholder_info())
        else:
            btn = ctk.CTkButton(
                content_frame,
                text=mod["action_text"],
                fg_color="#24283b",
                hover_color=mod["color"],
                text_color="#c0caf5",
                corner_radius=8,
                height=35,
                font=ctk.CTkFont(family="Arial", size=13, weight="bold"),
                command=lambda s=mod["script"]: self.launch_script(s)
            )
        btn.pack(fill="x", side="bottom")


    def launch_script(self, script_name):
        if getattr(sys, 'frozen', False):
            try:
                p = multiprocessing.Process(target=launch_simulator_process, args=(script_name,))
                p.start()
            except Exception as e:
                self.show_message("Error", f"Failed to start simulator process:\n{str(e)}", is_error=True)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            script_path = os.path.join(base_dir, script_name)

            if not os.path.exists(script_path):
                self.show_message("File Not Found", f"Could not locate '{script_name}' in the project directory.", is_error=True)
                return

            try:
                subprocess.Popen([sys.executable, script_path])
            except Exception as e:
                self.show_message("Error", f"Failed to start simulator:\n{str(e)}", is_error=True)


    def show_message(self, title, message, is_error=False):
        try:
            from CTkMessagebox import CTkMessagebox
            icon_type = "cancel" if is_error else "info"
            CTkMessagebox(title=title, message=message, icon=icon_type)
        except ImportError:
            from tkinter import messagebox
            if is_error:
                messagebox.showerror(title, message)
            else:
                messagebox.showinfo(title, message)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = OSMainMenu()
    app.mainloop()

if False:
    import CPU_Scheduling_Sim
    import Memory_Management_OS
    import Virtual_Memory_Managament
    import Mass_Storage_Management
