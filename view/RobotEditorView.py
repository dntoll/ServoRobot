import tkinter as tk

class RobotEditorView(tk.Frame):
    def __init__(self, parent, robot_states):
        super().__init__(parent)
        self.robot_states = robot_states
        
        # Create a listbox to display the robot states
        self.listbox = tk.Listbox(self)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        for i, state in enumerate(self.robot_states):
            self.listbox.insert(tk.END, f"Robot {i+1}")
        
        # Create a frame to hold the edit fields
        self.edit_frame = tk.Frame(self)
        self.edit_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Create labels and entry fields for each attribute of the robot state
        tk.Label(self.edit_frame, text="Distance from base").grid(row=0, column=0, sticky='w')
        self.distance_entry = tk.Entry(self.edit_frame)
        self.distance_entry.grid(row=0, column=1)
        
        tk.Label(self.edit_frame, text="Height over base").grid(row=1, column=0, sticky='w')
        self.height_entry = tk.Entry(self.edit_frame)
        self.height_entry.grid(row=1, column=1)
        
        tk.Label(self.edit_frame, text="Rotation radians").grid(row=2, column=0, sticky='w')
        self.rotation_entry = tk.Entry(self.edit_frame)
        self.rotation_entry.grid(row=2, column=1)
        
        tk.Label(self.edit_frame, text="Wrist world angle radians").grid(row=3, column=0, sticky='w')
        self.wrist_angle_entry = tk.Entry(self.edit_frame)
        self.wrist_angle_entry.grid(row=3, column=1)
        
        tk.Label(self.edit_frame, text="Grip").grid(row=4, column=0, sticky='w')
        self.grip_entry = tk.Entry(self.edit_frame)
        self.grip_entry.grid(row=4, column=1)
        
        # Create a save button
        self.save_button = tk.Button(self.edit_frame, text="Save", command=self.save)
        self.save_button.grid(row=5, column=0, columnspan=2)
        
        # Initialize the edit fields with the first robot state
        self.current_index = 0
        self.load_robot_state(self.robot_states[self.current_index])
    
    def load_robot_state(self, state):
        self.distance_entry.delete(0, tk.END)
        self.distance_entry.insert(0, state.distanceFromBase)
        self.height_entry.delete(0, tk.END)
        self.height_entry.insert(0, state.heightOverBase)
        self.rotation_entry.delete(0, tk.END)
        self.rotation_entry.insert(0, state.rotationRadians)
        self.wrist_angle_entry.delete(0, tk.END)
        self.wrist_angle_entry.insert(0, state.wristWorldAngleRadians)
        self.grip_entry.delete(0, tk.END)
        self.grip_entry.insert(0, state.grip)
    
    def save(self):
        # Update the current robot state with the values in the edit fields
        current_state = self.robot_states[self.current_index]
        current_state.distanceFromBase = float(self.distance_entry.get())
        current_state.heightOverBase = float(self.height_entry.get())
        current_state.rotationRadians = float(self.rotation_entry.get())
        current_state.wristWorldAngleRadians = float(self.wrist_angle_entry.get())
        current_state.grip = float(self.grip.get())

    def on_select(self, event):
        # Load the selected robot state into the edit fields
        selection_index = self.listbox.curselection()[0]
        self.current_index = selection_index
        selected_state = self.robot_states[selection_index]
        self.load_robot_state(selected_state)

