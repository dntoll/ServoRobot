import tkinter as tk

class RobotEditorView(tk.Frame):
    def __init__(self, parent, recording, controller):
        super().__init__(parent)
        self.recording = recording
        self.controller = controller


        # Create a listbox to display the indicies
        self.indiciesListBox = tk.Listbox(self)
        self.indiciesListBox.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.indiciesListBox.bind('<<ListboxSelect>>', self.on_selectIndex)
        
        # Create a listbox to display the robot states
        self.stateListBox = tk.Listbox(self)
        self.stateListBox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.stateListBox.bind('<<ListboxSelect>>', self.on_select)
        
        
        # Create a frame to hold the edit fields
        self.edit_frame = tk.Frame(self)
        self.edit_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Create labels and entry fields for each attribute of the robot state
        tk.Label(self.edit_frame, text="Name").grid(row=0, column=0, sticky='w')
        self.name_entry = tk.Entry(self.edit_frame)
        self.name_entry.grid(row=0, column=1)

        tk.Label(self.edit_frame, text="Distance from base").grid(row=1, column=0, sticky='w')
        self.distance_entry = tk.Entry(self.edit_frame)
        self.distance_entry.grid(row=1, column=1)
        
        tk.Label(self.edit_frame, text="Height over base").grid(row=2, column=0, sticky='w')
        self.height_entry = tk.Entry(self.edit_frame)
        self.height_entry.grid(row=2, column=1)
        
        tk.Label(self.edit_frame, text="Rotation radians").grid(row=3, column=0, sticky='w')
        self.rotation_entry = tk.Entry(self.edit_frame)
        self.rotation_entry.grid(row=3, column=1)
        
        tk.Label(self.edit_frame, text="Wrist world angle radians").grid(row=4, column=0, sticky='w')
        self.wrist_angle_entry = tk.Entry(self.edit_frame)
        self.wrist_angle_entry.grid(row=4, column=1)
        
        tk.Label(self.edit_frame, text="Grip").grid(row=5, column=0, sticky='w')
        self.grip_entry = tk.Entry(self.edit_frame)
        self.grip_entry.grid(row=5, column=1)
        
        # Create a save button
        self.save_button = tk.Button(self.edit_frame, text="Store", command=self.store)
        self.save_button.grid(row=6, column=0, columnspan=1)

        self.copy_button = tk.Button(self.edit_frame, text="Copy", command=self.copy)
        self.copy_button.grid(row=6, column=1, columnspan=1)

        self.copy_button = tk.Button(self.edit_frame, text="Play", command=self.play)
        self.copy_button.grid(row=6, column=2, columnspan=1)

        self.copy_button = tk.Button(self.edit_frame, text="Relax", command=self.relax)
        self.copy_button.grid(row=7, column=1, columnspan=1)

        self.copy_button = tk.Button(self.edit_frame, text="Delete", command=self.removeCurrentState)
        self.copy_button.grid(row=7, column=2, columnspan=1)

        self.copy_button = tk.Button(self.edit_frame, text="Set Index to State", command=self.setIndexToState)
        self.copy_button.grid(row=8, column=1, columnspan=1)

        self.copy_button = tk.Button(self.edit_frame, text="Append After Index", command=self.appendAfterIndex)
        self.copy_button.grid(row=8, column=2, columnspan=1)

        self.copy_button = tk.Button(self.edit_frame, text="Delete Index", command=self.removeIndex)
        self.copy_button.grid(row=9, column=2, columnspan=1)
        

        # Initialize the edit fields with the first robot state
        self.current_state_index = 0
        self.current_index_index = 0

        self.update()

        if self.recording.getNumStates() > 0:
            
            self.setState(self.recording.getState(self.current_state_index))

    def setIndexToState(self):
        self.controller.setIndexToState(self.current_state_index, self.current_index_index)
        self.update()

    def appendAfterIndex(self):
        self.controller.appendAfterIndex(self.current_state_index, self.current_index_index)
        self.update()

    def removeIndex(self):
        self.controller.removeIndex(self.current_index_index)
        self.update()
    
    def copy(self):
        self.controller.duplicateCurrentState(self.current_state_index)
        self.update()

    def relax(self):
        self.controller.setStateToRelax(self.current_state_index)
        self.update()

    def removeCurrentState(self):
        self.controller.removeCurrentState(self.current_state_index)
        self.update()

    def play(self):
        self.controller.play()

    def update(self):
        self.stateListBox.delete(0, tk.END)
        for i in range(0, self.recording.getNumStates()):
            state = self.recording.getState(i)
            self.stateListBox.insert(tk.END, f"{state.name}")
        self.stateListBox.select_set(self.current_state_index)

        #Then the indicies
        self.indiciesListBox.delete(0, tk.END)
        for i in range(0, self.recording.getNumIndicies()):
            state = self.recording.getIndex(i)
            self.indiciesListBox.insert(tk.END, f"{state.name}")
        self.indiciesListBox.select_set(self.current_state_index)

    
    def setState(self, state):
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, state.name)

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
    


    def store(self):


        # Update the current robot state with the values in the edit fields

        try:
            current_state = self.recording.getState(self.current_state_index)
            current_state.name = str(self.name_entry.get())
            current_state.distanceFromBase = float(self.distance_entry.get())
            current_state.heightOverBase = float(self.height_entry.get())
            current_state.rotationRadians = float(self.rotation_entry.get())
            current_state.wristWorldAngleRadians = float(self.wrist_angle_entry.get())
            current_state.grip = float(self.grip_entry.get())

            self.controller.setState(current_state)
            self.controller.storeState(self.current_state_index)

            self.update()
        except Exception as e:
            print("RobotEditorView.save", e, flush=True)

    def on_selectIndex(self, event):
        selection_index = self.indiciesListBox.curselection()[0]
        self.current_index_index = selection_index
        print ("Selected index")

    def on_select(self, event):
        # Load the selected robot state into the edit fields

        try:
            print(self.stateListBox.curselection())
            selection_index = self.stateListBox.curselection()[0]
            self.current_state_index = selection_index
            selected_state = self.controller.recording.getState(selection_index)
            self.controller.setState(selected_state)
            self.setState(selected_state)
        except Exception as e:
            print("RobotEditorView", e)

