import numpy as np
from scipy.integrate import odeint
import tkinter as tk
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Reactor parameters ---
Q_fission = 1000
m_fuel = 1000
c_fuel = 500
h_conv = 1000
A_ht = 10
m_coolant = 500
c_coolant = 4000
T_inlet = 300
mdot_coolant = 10

# --- System dynamics ---
def system_dynamics(y, t):
    T_fuel, T_coolant = y
    
    # Calculate rate of heat transfer to the cooland from fuel
    Q_ht = h_conv * A_ht * (T_fuel - T_coolant)

    # Calculate fuel temperature rate change
    dT_fuel_dt = (Q_fission - Q_ht) / (m_fuel * c_fuel) 

    # Calculate coolant temperature rate change
    dT_coolant_dt = (Q_ht - mdot_coolant * c_coolant * (T_coolant - T_inlet)) / (m_coolant * c_coolant)
    
    return [dT_fuel_dt, dT_coolant_dt]

# --- Initial conditions ---
T_fuel_0 = 400
T_coolant_0 = 310
initial_conditions = [T_fuel_0, T_coolant_0]

# --- Time points for simulation ---
t = np.linspace(0, 3600, 500)
solution = odeint(system_dynamics, initial_conditions, t)
T_fuel_sim = solution[:, 0]
T_coolant_sim = solution[:, 1]

# --- Tkinter setup ---
root = tk.Tk()
root.title("CANDU Reactor Temperature Monitor")
root.geometry("1200x700")

# Load and set background image
bg_image = Image.open("images/candu_reactor.png")
bg_image = bg_image.resize((620, 500))
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=1200, height=700)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Fixed positions for text labels
fuel_x, fuel_y = 555, 375 
coolant_x, coolant_y = 555, 150

# Fuel text with background
fuel_box = canvas.create_rectangle(fuel_x - 150, fuel_y - 20, fuel_x + 150, fuel_y + 20,
                                   fill="black", outline="")
fuel_text = canvas.create_text(fuel_x, fuel_y,
                               text=f"Fuel Temperature: {T_fuel_0:.2f} K",
                               font=("Helvetica", 16), fill="red")

# Coolant text with background
coolant_box = canvas.create_rectangle(coolant_x - 150, coolant_y - 20, coolant_x + 150, coolant_y + 20,
                                      fill="black", outline="")
coolant_text = canvas.create_text(coolant_x, coolant_y,
                                  text=f"Coolant Temperature: {T_coolant_0:.2f} K",
                                  font=("Helvetica", 16), fill="blue")

# --- Matplotlib figure inside Tkinter ---
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
line1, = ax.plot([], [], label="Fuel Temperature", color="red")
line2, = ax.plot([], [], label="Coolant Temperature", color="blue")
ax.set_xlim(0, 600)
ax.set_ylim(min(T_coolant_sim)-5, max(T_fuel_sim)+5)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Temperature (K)")
ax.set_title("CANDU Reactor Temperature Monitor Simulation")
ax.legend()
ax.grid(True)

# Embed figure
canvas_fig = FigureCanvasTkAgg(fig, master=root)
canvas_fig.get_tk_widget().place(x=710, y=0)
canvas_fig.draw()

# --- Update function ---
index = 0
def update_temperature():
    global index
    if index < len(t):
        
        canvas.itemconfig(fuel_text, text=f"Fuel Temperature: {T_fuel_sim[index]:.2f} K")
        canvas.itemconfig(coolant_text, text=f"Coolant Temperature: {T_coolant_sim[index]:.2f} K")
        index += 1
        # Update graph
        line1.set_data(t[:index], T_fuel_sim[:index])
        line2.set_data(t[:index], T_coolant_sim[:index])
        canvas_fig.draw()
         # Update text

        root.after(7200, update_temperature)

# Start updates
update_temperature()

root.mainloop()
