import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from threading import Timer

# Dataset: A simple dictionary to store exercise information
exercise_dataset = {
    "Bench Press": {
        "muscle_group": "Chest",
        "description": "A compound exercise that targets the chest, shoulders, and triceps.",
        "ideal_sets_reps": "4 sets of 8-12 reps",
        "equipment": "Barbell or Dumbbells"
    },
    "Deadlift": {
        "muscle_group": "Back",
        "description": "A compound movement that targets the entire posterior chain, including the back, glutes, and hamstrings.",
        "ideal_sets_reps": "3 sets of 5-8 reps",
        "equipment": "Barbell"
    },
    "Squat": {
        "muscle_group": "Legs",
        "description": "A compound exercise that works the quads, hamstrings, glutes, and core.",
        "ideal_sets_reps": "4 sets of 6-10 reps",
        "equipment": "Barbell"
    },
    "Bicep Curl": {
        "muscle_group": "Arms",
        "description": "An isolation exercise targeting the biceps.",
        "ideal_sets_reps": "3 sets of 10-15 reps",
        "equipment": "Dumbbells or Barbell"
    },
    "Tricep Pushdown": {
        "muscle_group": "Arms",
        "description": "An isolation exercise focusing on the triceps.",
        "ideal_sets_reps": "3 sets of 10-15 reps",
        "equipment": "Cable Machine"
    }
}

# New datasets
fat_loss_tips = [
    "Incorporate high-intensity interval training (HIIT) into your workout.",
    "Increase your protein intake to help build muscle and burn fat.",
    "Stay hydrated and drink plenty of water throughout the day.",
    "Get adequate sleep to support metabolism and recovery."
]

stretches = {
    "Neck": ["Neck Tilt", "Neck Rotation"],
    "Shoulders": ["Cross-Body Shoulder Stretch", "Overhead Shoulder Stretch"],
    "Back": ["Cat-Cow Stretch", "Child's Pose"],
    "Legs": ["Hamstring Stretch", "Quadriceps Stretch"]
}

# Define a bold font
bold_font = ('Helvetica', 12, 'bold')

# Define initial states
fat_loss_expanded = False
stretches_expanded = False

# Function to suggest exercises based on the selected goal
def suggest_exercises(goal):
    if goal.lower() == "strength":
        exercises = ["Bench Press", "Deadlift", "Squat"]
    elif goal.lower() == "muscle building":
        exercises = ["Bench Press", "Squat", "Bicep Curl", "Tricep Pushdown"]
    elif goal.lower() == "fat loss":
        exercises = ["Squat", "Deadlift", "Bench Press"]
    else:
        return None

    return exercises

def display_suggestions():
    goal = goal_var.get()
    exercises = suggest_exercises(goal)
    
    if exercises:
        tree.delete(*tree.get_children())  # Clear existing entries
        for exercise in exercises:
            details = exercise_dataset[exercise]
            tree.insert("", tk.END, values=(exercise, details["muscle_group"], details["description"],
                                            details["ideal_sets_reps"], details["equipment"]))
    else:
        result_label_middle.config(text="Invalid goal. Please choose from 'Strength', 'Muscle Building', or 'Fat Loss'.")

def toggle_fat_loss_tips():
    global fat_loss_expanded
    if fat_loss_expanded:
        left_frame_inner.grid_forget()
        fat_loss_button.config(text="Show Fat Loss Tips")
        fat_loss_expanded = False
    else:
        left_frame_inner.grid(row=0, column=0, sticky='nsew')
        display_fat_loss_tips()  # Show the tips
        fat_loss_button.config(text="Minimize Fat Loss Tips")
        fat_loss_expanded = True

def display_fat_loss_tips():
    tips_text = "\n".join(fat_loss_tips)
    result_label_left.config(text=tips_text)

def toggle_stretches():
    global stretches_expanded
    if stretches_expanded:
        right_frame_inner.grid_forget()
        stretch_button.config(text="Show Stretches")
        stretches_expanded = False
    else:
        right_frame_inner.grid(row=0, column=0, sticky='nsew')
        display_stretches()  # Show the stretches
        stretch_button.config(text="Minimize Stretches")
        stretches_expanded = True

def display_stretches():
    body_part = stretch_var.get()
    stretches_list = stretches.get(body_part, [])
    
    if stretches_list:
        stretches_text = "\n".join(stretches_list)
        result_label_right.config(text=f"Stretches for {body_part}:\n{stretches_text}")
    else:
        result_label_right.config(text="Select a valid body part for stretches.")

def add_supplementation_schedule():
    supplement = supplement_entry.get()
    time = supplement_time_entry.get()
    if supplement and time:
        supplementation_schedule.append((supplement, time))
        messagebox.showinfo("Supplementation Added", f"Supplement: {supplement}, Time: {time}")
    else:
        messagebox.showwarning("Input Error", "Please enter both supplement and time.")

def set_water_reminder():
    interval = int(water_reminder_entry.get())
    def reminder():
        messagebox.showinfo("Water Reminder", "It's time to drink water!")
        Timer(interval * 60, reminder).start()
    reminder()

# Create the main window
root = tk.Tk()
root.title("Exercise and Health Tracker")
root.geometry("1200x800")

# Create frames for layout
left_frame = tk.Frame(root, bg="lightgreen")
middle_frame = tk.Frame(root, bg="lightblue")
right_frame = tk.Frame(root, bg="lightcoral")

# Grid layout for main frames
left_frame.grid(row=0, column=0, sticky='nsew')
middle_frame.grid(row=0, column=1, sticky='nsew')
right_frame.grid(row=0, column=2, sticky='nsew')

# Configure grid columns and rows to be equally sized but with different weights
root.grid_columnconfigure(0, weight=1)  # Left column
root.grid_columnconfigure(1, weight=3)  # Middle column wider
root.grid_columnconfigure(2, weight=1)  # Right column
root.grid_rowconfigure(0, weight=1)

# Create canvas widgets inside frames for expandable content
left_canvas = tk.Canvas(left_frame, bg="lightgreen")
left_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

right_canvas = tk.Canvas(right_frame, bg="lightcoral")
right_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a frame inside canvas for displaying content
left_frame_inner = tk.Frame(left_canvas, bg="lightgreen")
left_canvas.create_window((0, 0), window=left_frame_inner, anchor=tk.NW)

right_frame_inner = tk.Frame(right_canvas, bg="lightcoral")
right_canvas.create_window((0, 0), window=right_frame_inner, anchor=tk.NW)

# Create a frame for exercise suggestions
exercise_frame = tk.Frame(middle_frame, bg="lightblue")
exercise_frame.pack(fill=tk.BOTH, expand=True, pady=10)

# Dropdown menu for selecting fitness goal
goal_var = tk.StringVar(value="Select Goal")
goal_menu = ttk.Combobox(middle_frame, textvariable=goal_var, values=["Strength", "Muscle Building", "Fat Loss"])
goal_menu.pack(pady=10)
goal_menu.configure(font=bold_font)

# Button to suggest exercises based on selected goal
suggest_button = tk.Button(middle_frame, text="Suggest Exercises", command=display_suggestions)
suggest_button.pack(pady=10)
suggest_button.configure(font=bold_font)

# Entry and Button for supplementation plan
supplement_label = tk.Label(middle_frame, text="Supplementation Plan:", bg="lightblue", font=bold_font)
supplement_label.pack(pady=5)
supplement_entry = tk.Entry(middle_frame, width=30)
supplement_entry.pack(pady=5)
supplement_time_entry = tk.Entry(middle_frame, width=30)
supplement_time_entry.pack(pady=5)
add_supplementation_button = tk.Button(middle_frame, text="Add Supplementation Schedule", command=add_supplementation_schedule)
add_supplementation_button.pack(pady=10)
add_supplementation_button.configure(font=bold_font)

# Entry and Button for water reminder
water_reminder_label = tk.Label(middle_frame, text="Water Reminder Interval (minutes):", bg="lightblue", font=bold_font)
water_reminder_label.pack(pady=5)
water_reminder_entry = tk.Entry(middle_frame, width=30)
water_reminder_entry.pack(pady=5)
set_water_reminder_button = tk.Button(middle_frame, text="Set Water Reminder", command=set_water_reminder)
set_water_reminder_button.pack(pady=10)
set_water_reminder_button.configure(font=bold_font)

# Button to toggle fat loss tips
fat_loss_button = tk.Button(left_frame, text="Show Fat Loss Tips", command=toggle_fat_loss_tips)
fat_loss_button.pack(pady=10)
fat_loss_button.configure(font=bold_font)

# Dropdown menu for selecting body part for stretches
stretch_var = tk.StringVar(value="Select Body Part")
stretch_menu = ttk.Combobox(right_frame, textvariable=stretch_var, values=list(stretches.keys()))
stretch_menu.pack(pady=10)
stretch_menu.configure(font=bold_font)

# Button to toggle stretches
stretch_button = tk.Button(right_frame, text="Show Stretches", command=toggle_stretches)
stretch_button.pack(pady=10)
stretch_button.configure(font=bold_font)

# Result labels
result_label_left = tk.Label(left_frame_inner, text="", bg="lightgreen", justify=tk.LEFT)
result_label_left.pack(pady=10, padx=10)

result_label_right = tk.Label(right_frame_inner, text="", bg="lightcoral", justify=tk.LEFT)
result_label_right.pack(pady=10, padx=10)

result_label_middle = tk.Label(middle_frame, text="", bg="lightblue", justify=tk.LEFT)
result_label_middle.pack(pady=10)

# Create a treeview widget to display the exercises in the exercise frame
columns = ("Exercise", "Muscle Group", "Description", "Ideal Sets and Reps", "Equipment Needed")
tree = ttk.Treeview(exercise_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)
tree.pack(fill=tk.BOTH, expand=True)

# Run the main loop
root.mainloop()




