import subprocess
import tkinter as tk
from tkinter import messagebox, simpledialog

class DiskPartGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DiskPart GUI")
        
        # Create buttons for DiskPart commands
        self.list_disk_button = tk.Button(root, text="List Disk", command=self.list_disk)
        self.list_disk_button.pack(pady=5)
        
        self.select_disk_button = tk.Button(root, text="Select Disk", command=self.select_disk)
        self.select_disk_button.pack(pady=5)
        
        self.create_partition_button = tk.Button(root, text="Create Partition", command=self.create_partition)
        self.create_partition_button.pack(pady=5)
        
        self.format_partition_button = tk.Button(root, text="Format Partition", command=self.format_partition)
        self.format_partition_button.pack(pady=5)
        
        self.clean_disk_button = tk.Button(root, text="Clean Disk", command=self.clean_disk)
        self.clean_disk_button.pack(pady=5)

    def run_diskpart_command(self, command):
        try:
            result = subprocess.run(["diskpart"], input=command, text=True, capture_output=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return None

    def list_disk(self):
        output = self.run_diskpart_command("list disk\n")
        if output:
            messagebox.showinfo("List Disk", output)

    def select_disk(self):
        disk_number = simpledialog.askinteger("Select Disk", "Enter disk number:")
        if disk_number is not None:
            output = self.run_diskpart_command(f"select disk {disk_number}\n")
            if output:
                messagebox.showinfo("Select Disk", output)

    def create_partition(self):
        disk_number = simpledialog.askinteger("Select Disk", "Enter disk number:")
        if disk_number is not None:
            size = simpledialog.askinteger("Create Partition", "Enter partition size (MB):")
            if size is not None:
                output = self.run_diskpart_command(f"select disk {disk_number}\ncreate partition primary size={size}\n")
                if output:
                    messagebox.showinfo("Create Partition", output)

    def format_partition(self):
        disk_number = simpledialog.askinteger("Select Disk", "Enter disk number:")
        if disk_number is not None:
            partition_number = simpledialog.askinteger("Format Partition", "Enter partition number:")
            if partition_number is not None:
                fs_type = simpledialog.askstring("Format Partition", "Enter file system type (e.g., NTFS, FAT32):")
                if fs_type:
                    output = self.run_diskpart_command(f"select disk {disk_number}\nselect partition {partition_number}\nformat fs={fs_type} quick\n")
                    if output:
                        messagebox.showinfo("Format Partition", output)

    def clean_disk(self):
        disk_number = simpledialog.askinteger("Clean Disk", "Enter disk number:")
        if disk_number is not None:
            output = self.run_diskpart_command(f"select disk {disk_number}\nclean\n")
            if output:
                messagebox.showinfo("Clean Disk", output)

if __name__ == "__main__":
    root = tk.Tk()
    app = DiskPartGUI(root)
    root.mainloop()