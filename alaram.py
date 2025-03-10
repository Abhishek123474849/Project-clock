import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import time
import threading

class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Alarm Clock using tkinter")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.root.configure(bg="red")
        
        # Styling
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 10), background="#4CAF50")
        self.style.configure("TLabel", font=("Arial", 12), background="#f0f0f0")
        
        # Variables for alarm
        self.alarm_thread = None
        self.alarm_running = False
        self.alarms = []
        
        # Create and place widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Current time display
        self.time_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.time_frame.pack(pady=10)
        
        self.time_label = tk.Label(self.time_frame, font=("Arial", 20), bg="#f0f0f0", fg="#333333")
        self.time_label.pack()
        
        self.update_time()
        
        # Set alarm frame
        self.alarm_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.alarm_frame.pack(pady=10)
        
        # Hour
        tk.Label(self.alarm_frame, text="Hour:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        self.hour_var = tk.StringVar()
        self.hour_combobox = ttk.Combobox(self.alarm_frame, textvariable=self.hour_var, width=5)
        self.hour_combobox['values'] = [str(i).zfill(2) for i in range(24)]
        self.hour_combobox.current(datetime.datetime.now().hour)
        self.hour_combobox.grid(row=0, column=1, padx=5, pady=5)
        
        # Minute
        tk.Label(self.alarm_frame, text="Minute:", bg="#f0f0f0").grid(row=0, column=2, padx=5, pady=5)
        self.minute_var = tk.StringVar()
        self.minute_combobox = ttk.Combobox(self.alarm_frame, textvariable=self.minute_var, width=5)
        self.minute_combobox['values'] = [str(i).zfill(2) for i in range(60)]
        self.minute_combobox.current(datetime.datetime.now().minute)
        self.minute_combobox.grid(row=0, column=3, padx=5, pady=5)
        
        # Second
        tk.Label(self.alarm_frame, text="Second:", bg="#f0f0f0").grid(row=0, column=4, padx=5, pady=5)
        self.second_var = tk.StringVar()
        self.second_combobox = ttk.Combobox(self.alarm_frame, textvariable=self.second_var, width=5)
        self.second_combobox['values'] = [str(i).zfill(2) for i in range(60)]
        self.second_combobox.current(0)
        self.second_combobox.grid(row=0, column=5, padx=5, pady=5)
        
        # Buttons
        self.button_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.button_frame.pack(pady=10)
        
        self.set_button = ttk.Button(self.button_frame, text="Set Alarm", command=self.set_alarm)
        self.set_button.grid(row=0, column=0, padx=10)
        
        self.stop_button = ttk.Button(self.button_frame, text="Stop Alarm", command=self.stop_alarm, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=10)
        
        # Alarm list
        self.list_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.list_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        tk.Label(self.list_frame, text="Active Alarms:", bg="#f0f0f0", font=("Arial", 12)).pack(anchor="w", padx=15)
        
        self.listbox_frame = tk.Frame(self.list_frame, bg="#f0f0f0")
        self.listbox_frame.pack(padx=15, pady=5, fill=tk.BOTH, expand=True)
        
        self.alarm_listbox = tk.Listbox(self.listbox_frame, width=30, height=5)
        self.alarm_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.listbox_frame, orient="vertical", command=self.alarm_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.alarm_listbox.config(yscrollcommand=scrollbar.set)
        
        delete_button = ttk.Button(self.list_frame, text="Delete Selected", command=self.delete_alarm)
        delete_button.pack(pady=5)
        
    def update_time(self):
        """Update the current time display"""
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
        
        # Check if any alarm time is reached
        self.check_alarms()
    
    def set_alarm(self):
        """Set a new alarm"""
        try:
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
            second = int(self.second_var.get())
            
            # Validation
            if not (0 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59):
                messagebox.showerror("Invalid Time", "Please enter a valid time!")
                return
            
            # Create alarm time
            now = datetime.datetime.now()
            alarm_time = now.replace(hour=hour, minute=minute, second=second)
            
            # If the alarm time is earlier than current time, set it for the next day
            if alarm_time < now:
                alarm_time += datetime.timedelta(days=1)
            
            # Add to alarms list
            alarm_str = alarm_time.strftime("%H:%M:%S")
            self.alarms.append((alarm_time, alarm_str))
            self.alarm_listbox.insert(tk.END, alarm_str)
            
            messagebox.showinfo("Alarm Set", f"Alarm set for {alarm_str}")
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values for hours, minutes, and seconds!")
    
    def check_alarms(self):
        """Check if any alarm time is reached"""
        if not self.alarms:
            return
        
        now = datetime.datetime.now()
        triggered_alarms = []
        
        for alarm_time, alarm_str in self.alarms:
            # Set seconds to 0 for comparison to avoid missing the alarm
            alarm_check = alarm_time.replace(microsecond=0)
            now_check = now.replace(microsecond=0)
            
            if alarm_check == now_check:
                triggered_alarms.append((alarm_time, alarm_str))
        
        # Trigger alarms
        for alarm in triggered_alarms:
            self.trigger_alarm(alarm[1])
            self.alarms.remove(alarm)
            self.update_alarm_listbox()
    
    def trigger_alarm(self, alarm_str):
        """Trigger the alarm sound and notification"""
        self.alarm_running = True
        self.stop_button.config(state="normal")
        
        # Show notification
        messagebox.showinfo("Alarm", f"Alarm time: {alarm_str}")
        
        # Play alarm sound in a separate thread
        self.alarm_thread = threading.Thread(target=self.play_alarm)
        self.alarm_thread.daemon = True
        self.alarm_thread.start()
    
    def play_alarm(self):
        """Play alarm sound"""
        # Play sound 5 times
        for _ in range(5):
            if not self.alarm_running:
                break
            # For Windows. Adjust for other OS.
            winsound.Beep(1000, 1000)  # Frequency: 1000Hz, Duration: 1000ms
            time.sleep(0.5)
        
        self.stop_alarm()
    
    def stop_alarm(self):
        """Stop the alarm sound"""
        self.alarm_running = False
        self.stop_button.config(state="disabled")
    
    def delete_alarm(self):
        """Delete selected alarm from the list"""
        try:
            selection = self.alarm_listbox.curselection()[0]
            selected_alarm = self.alarm_listbox.get(selection)
            
            # Remove from alarms list
            for alarm in self.alarms:
                if alarm[1] == selected_alarm:
                    self.alarms.remove(alarm)
                    break
            
            # Remove from listbox
            self.alarm_listbox.delete(selection)
            
        except IndexError:
            messagebox.showinfo("Selection Required", "Please select an alarm to delete.")
    
    def update_alarm_listbox(self):
        """Update the listbox display"""
        self.alarm_listbox.delete(0, tk.END)
        for alarm in self.alarms:
            self.alarm_listbox.insert(tk.END, alarm[1])

if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmClock(root)
    root.mainloop()