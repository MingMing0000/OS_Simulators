import tkinter as tk
from tkinter import ttk, messagebox


class Partition:
    def __init__(self, partition_id, size):
        self.partition_id = partition_id
        self.size = size
        self.is_allocated = False


class Process:
    def __init__(self, process_name, size):
        self.process_name = process_name
        self.size = size
        self.allocated_partition = "-"
        self.result = "Not Allocated"


class MemoryManager:
    def __init__(self, partitions, processes):
        self.partitions = partitions
        self.processes = processes

    def reset_partitions(self):
        for partition in self.partitions:
            partition.is_allocated = False

        for process in self.processes:
            process.allocated_partition = "-"
            process.result = "Not Allocated"

    def first_fit(self):
        self.reset_partitions()

        for process in self.processes:
            for partition in self.partitions:

                if (
                    not partition.is_allocated
                    and partition.size >= process.size
                ):
                    process.allocated_partition = (
                        f"P{partition.partition_id}"
                    )
                    process.result = "Allocated"

                    partition.is_allocated = True
                    break

    def next_fit(self):
        self.reset_partitions()

        current_partition_index = 0

        for process in self.processes:

            checked_partitions = 0

            while checked_partitions < len(self.partitions):

                partition = self.partitions[current_partition_index]

                if (
                    not partition.is_allocated
                    and partition.size >= process.size
                ):
                    process.allocated_partition = (
                        f"P{partition.partition_id}"
                    )
                    process.result = "Allocated"

                    partition.is_allocated = True

                    current_partition_index = (
                        current_partition_index + 1
                    ) % len(self.partitions)

                    break

                current_partition_index = (
                    current_partition_index + 1
                ) % len(self.partitions)

                checked_partitions += 1

    def best_fit(self):
        self.reset_partitions()

        for process in self.processes:

            best_partition = None

            for partition in self.partitions:

                if (
                    not partition.is_allocated
                    and partition.size >= process.size
                ):
                    if best_partition is None:
                        best_partition = partition

                    elif partition.size < best_partition.size:
                        best_partition = partition

            if best_partition is not None:

                process.allocated_partition = (
                    f"P{best_partition.partition_id}"
                )

                process.result = "Allocated"

                best_partition.is_allocated = True

    def worst_fit(self):
        self.reset_partitions()

        for process in self.processes:

            worst_partition = None

            for partition in self.partitions:

                if (
                    not partition.is_allocated
                    and partition.size >= process.size
                ):
                    if worst_partition is None:
                        worst_partition = partition

                    elif partition.size > worst_partition.size:
                        worst_partition = partition

            if worst_partition is not None:

                process.allocated_partition = (
                    f"P{worst_partition.partition_id}"
                )

                process.result = "Allocated"

                worst_partition.is_allocated = True


class MemoryManagementGUI:
    def __init__(self, root_window):
        self.root_window = root_window

        self.root_window.title(
            "Fixed Partition Memory Management Simulator"
        )

        self.root_window.geometry("805x700")

        self.algorithm_choice = tk.StringVar(
            value="First Fit"
        )

        self.create_widgets()

    def create_widgets(self):

        title_label = tk.Label(
            self.root_window,
            text="Fixed Partition Memory Management Simulator",
            font=("Arial", 14, "bold")
        )

        title_label.pack(pady=10)

        note_label = tk.Label(
            self.root_window,
            text=(
                "Note: This simulator uses Fixed Partition Allocation.\n"
                "Each partition can only hold one process."
            ),
            fg="red"
        )

        note_label.pack(pady=5)

        tk.Label(
            self.root_window,
            text="Job Pool Sizes (comma separated)"
        ).pack()

        self.process_entry = tk.Entry(
            self.root_window,
            width=50
        )

        self.process_entry.pack(pady=5)

        tk.Label(
            self.root_window,
            text="Partition Sizes (comma separated)"
        ).pack()

        self.partition_entry = tk.Entry(
            self.root_window,
            width=50
        )

        self.partition_entry.pack(pady=5)

        algorithm_frame = tk.Frame(
            self.root_window
        )

        algorithm_frame.pack(pady=10)

        algorithms = [
            "First Fit",
            "Next Fit",
            "Best Fit",
            "Worst Fit"
        ]

        for algorithm in algorithms:

            tk.Radiobutton(
                algorithm_frame,
                text=algorithm,
                variable=self.algorithm_choice,
                value=algorithm
            ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            self.root_window,
            text="Allocate",
            command=self.allocate_memory
        ).pack(pady=10)
        partition_frame = tk.LabelFrame(
            self.root_window,
            text="Partition Reference"
        )

        partition_frame.pack(
            fill="x",
            padx=10,
            pady=5
        )

        self.partition_reference_label = tk.Label(
            partition_frame,
            text="Enter partition sizes and click Allocate.",
            justify="left",
            anchor="w"
        )

        self.partition_reference_label.pack(
            fill="x",
            padx=10,
            pady=5
        )

        self.result_table = ttk.Treeview(
            self.root_window,
            columns=(
                "Process",
                "Size",
                "Allocated Partition",
                "Result"
            ),
            show="headings"
        )

        self.result_table.heading(
            "Process",
            text="Process"
        )

        self.result_table.heading(
            "Size",
            text="Size"
        )

        self.result_table.heading(
            "Allocated Partition",
            text="Allocated Partition"
        )

        self.result_table.heading(
            "Result",
            text="Result"
        )

        self.result_table.column(
            "Process",
            width=80
        )

        self.result_table.column(
            "Size",
            width=80
        )

        self.result_table.column(
            "Allocated Partition",
            width=150
        )

        self.result_table.column(
            "Result",
            width=120
        )

        self.result_table.pack(
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=10
        )

    def allocate_memory(self):

        try:

            process_sizes = [
                int(size.strip())
                for size in self.process_entry.get().split(",")
            ]

            partition_sizes = [
                int(size.strip())
                for size in self.partition_entry.get().split(",")
            ]

        except ValueError:

            messagebox.showerror(
                "Input Error",
                "Please enter valid numbers."
            )

            return

        processes = []

        for index, size in enumerate(process_sizes):

            process_name = chr(65 + index)

            processes.append(
                Process(process_name, size)
            )

        partitions = []

        for index, size in enumerate(partition_sizes):

            partitions.append(
                Partition(index + 1, size)
            )

        partition_text = ""

        for partition in partitions:

            partition_text += (
                f"P{partition.partition_id} = "
                f"{partition.size}\n"
            )

        self.partition_reference_label.config(
            text=partition_text
        )

        memory_manager = MemoryManager(
            partitions,
            processes
        )

        selected_algorithm = (
            self.algorithm_choice.get()
        )

        if selected_algorithm == "First Fit":
            memory_manager.first_fit()

        elif selected_algorithm == "Next Fit":
            memory_manager.next_fit()

        elif selected_algorithm == "Best Fit":
            memory_manager.best_fit()

        elif selected_algorithm == "Worst Fit":
            memory_manager.worst_fit()

        self.result_table.delete(
            *self.result_table.get_children()
        )

        for process in processes:

            self.result_table.insert(
                "",
                tk.END,
                values=(
                    process.process_name,
                    process.size,
                    process.allocated_partition,
                    process.result
                )
            )


root_window = tk.Tk()

application = MemoryManagementGUI(
    root_window
)

root_window.mainloop()