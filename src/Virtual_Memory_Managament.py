import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque

class PageFrame:
    def __init__(self, frame_id):
        self.frame_id = frame_id
        self.current_page = "-"

class VirtualMemoryManager:
    def __init__(self, num_frames):
        self.num_frames = num_frames
        self.frames = [PageFrame(i) for i in range(num_frames)]
        self.page_faults = 0
        self.page_hits = 0
        self.history = []

    def reset_simulation(self):
        self.frames = [PageFrame(i) for i in range(self.num_frames)]
        self.page_faults = 0
        self.page_hits = 0
        self.history = []

    def simulate_fifo(self, reference_string):
        self.reset_simulation()
        fifo_queue = deque()

        for page in reference_string:
            hit = False
            allocated_frame = -1

            for frame in self.frames:
                if frame.current_page == page:
                    hit = True
                    allocated_frame = frame.frame_id
                    self.page_hits += 1
                    break

            if not hit:
                self.page_faults += 1

                empty_frame = next((f for f in self.frames if f.current_page == "-"), None)

                if empty_frame:
                    empty_frame.current_page = page
                    fifo_queue.append(empty_frame.frame_id)
                    allocated_frame = empty_frame.frame_id
                else:
                    victim_frame_id = fifo_queue.popleft()
                    self.frames[victim_frame_id].current_page = page
                    fifo_queue.append(victim_frame_id)
                    allocated_frame = victim_frame_id

            frame_state = [f.current_page for f in self.frames]
            self.history.append((page, "Hit" if hit else "Fault", f"Frame {allocated_frame}", frame_state))

    def simulate_lru(self, reference_string):
        self.reset_simulation()
        lru_tracker = []

        for page in reference_string:
            hit = False
            allocated_frame = -1

            for frame in self.frames:
                if frame.current_page == page:
                    hit = True
                    allocated_frame = frame.frame_id
                    self.page_hits += 1
                    lru_tracker.remove(frame.frame_id)
                    lru_tracker.append(frame.frame_id)
                    break

            if not hit:
                self.page_faults += 1

                empty_frame = next((f for f in self.frames if f.current_page == "-"), None)

                if empty_frame:
                    empty_frame.current_page = page
                    lru_tracker.append(empty_frame.frame_id)
                    allocated_frame = empty_frame.frame_id
                else:
                    victim_frame_id = lru_tracker.pop(0)
                    self.frames[victim_frame_id].current_page = page
                    lru_tracker.append(victim_frame_id)
                    allocated_frame = victim_frame_id

            frame_state = [f.current_page for f in self.frames]
            self.history.append((page, "Hit" if hit else "Fault", f"Frame {allocated_frame}", frame_state))

class VirtualMemoryGUI:
    def __init__(self, root_window):
        self.root_window = root_window
        self.root_window.title("Virtual Memory Management Simulator (Paging)")
        self.root_window.geometry("850x700")

        self.algorithm_choice = tk.StringVar(value="FIFO")
        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(
            self.root_window,
            text="Virtual Memory Page Replacement Simulator",
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=10)

        note_label = tk.Label(
            self.root_window,
            text="Note: This simulator maps Virtual Pages into physical Frames.\n"
                 "When RAM is full, it triggers a page replacement strategy.",
            fg="blue"
        )
        note_label.pack(pady=5)

        tk.Label(self.root_window, text="Page Reference String (comma separated)").pack()
        self.reference_entry = tk.Entry(self.root_window, width=50)
        self.reference_entry.insert(0, "7,0,1,2,0,3,0,4,2,3")
        self.reference_entry.pack(pady=5)

        tk.Label(self.root_window, text="Number of Physical Frames").pack()
        self.frames_entry = tk.Entry(self.root_window, width=10)
        self.frames_entry.insert(0, "3")
        self.frames_entry.pack(pady=5)

        algorithm_frame = tk.Frame(self.root_window)
        algorithm_frame.pack(pady=10)

        algorithms = ["FIFO (First In First Out)", "LRU (Least Recently Used)"]
        for algo in algorithms:
            tk.Radiobutton(
                algorithm_frame,
                text=algo,
                variable=self.algorithm_choice,
                value=algo.split()[0]
            ).pack(side=tk.LEFT, padx=20)

        tk.Button(
            self.root_window,
            text="Simulate Paging",
            command=self.run_simulation,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(pady=10)

        self.summary_frame = tk.LabelFrame(self.root_window, text="Simulation Metrics Summary")
        self.summary_frame.pack(fill="x", padx=15, pady=5)

        self.metrics_label = tk.Label(self.summary_frame, text="Run simulation to see metrics.")
        self.metrics_label.pack(pady=5)

        self.table_frame = tk.Frame(self.root_window)
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        self.result_table = None

    def run_simulation(self):
        try:
            ref_str = [int(x.strip()) for x in self.reference_entry.get().split(",") if x.strip()]
            num_frames = int(self.frames_entry.get())

            if num_frames <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror("Input Error", "Frames must be a positive integer.")
            return

        manager = VirtualMemoryManager(num_frames)

        if self.algorithm_choice.get() == "FIFO":
            manager.simulate_fifo(ref_str)
        else:
            manager.simulate_lru(ref_str)

        total_requests = len(ref_str)
        hit_ratio = (manager.page_hits / total_requests) * 100 if total_requests else 0
        fault_ratio = (manager.page_faults / total_requests) * 100 if total_requests else 0

        self.metrics_label.config(
            text=f"Total Requests: {total_requests} | "
                 f"Hits: {manager.page_hits} ({hit_ratio:.1f}%) | "
                 f"Faults: {manager.page_faults} ({fault_ratio:.1f}%)"
        )

        if self.result_table:
            self.result_table.destroy()

        columns = ("Page Requested", "Status", "Target Frame") + tuple(
            f"Frame {i}" for i in range(num_frames)
        )

        self.result_table = ttk.Treeview(self.table_frame, columns=columns, show="headings")

        for col in columns:
            self.result_table.heading(col, text=col)
            self.result_table.column(col, width=100, anchor="center")

        self.result_table.pack(fill=tk.BOTH, expand=True)

        for step in manager.history:
            page, status, target, frame_states = step
            row_values = (page, status, target) + tuple(frame_states)

            item_id = self.result_table.insert("", tk.END, values=row_values)

            if status == "Hit":
                self.result_table.tag_configure("hit_tag", background="#E8F5E9")
                self.result_table.item(item_id, tags=("hit_tag",))
            else:
                self.result_table.tag_configure("fault_tag", background="#FFEBEE")
                self.result_table.item(item_id, tags=("fault_tag",))

if __name__ == "__main__":
    root_window = tk.Tk()
    application = VirtualMemoryGUI(root_window)
    root_window.mainloop()
