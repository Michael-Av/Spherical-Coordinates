import pyvista as pv
import numpy as np

# background sphere
background_sphere = pv.Sphere(radius=1)

# axes
phi_ticks = np.radians(np.arange(0,181,10))
theta_ticks = np.radians(np.arange(0,360,10))

phi_points, theta_points = np.meshgrid(phi_ticks, theta_ticks, indexing='ij')

phi_points = phi_points.ravel()
theta_points = theta_points.ravel()

x_axis_points = 0.95 * np.sin(theta_points) * np.cos(phi_points)
y_axis_points = 0.95 * np.sin(theta_points) * np.sin(phi_points)
z_axis_points = 0.95 * np.cos(theta_points)

axis_points = np.column_stack((x_axis_points,y_axis_points,z_axis_points))

connection_indices = []
for i in range(1, len(axis_points)+1):
    connection_indices.append([i,i-1]) # connects altitude lines
    if i >= 36:
        connection_indices.append([i,i-36]) # connects azimuth lines

axes = pv.PolyData(axis_points, lines=pv.CellArray.from_regular_cells(connection_indices))

# stars
phi_vals = np.random.rand(100) * 2*np.pi
theta_vals = np.random.rand(100) * 2*np.pi

star_x = 0.9 * np.sin(theta_vals) * np.cos(phi_vals)
star_y = 0.9 * np.sin(theta_vals) * np.sin(phi_vals)
star_z = 0.9 * np.cos(theta_vals)

star_positions = np.column_stack((star_x,star_y,star_z))

stars = pv.PolyData(star_positions)

pl = pv.Plotter()
pl.add_mesh(background_sphere, color='black', show_edges=True)
pl.add_mesh(axes, color='red')
pl.add_mesh(stars, color='white')

# 2. Fix the initial position (standing in one spot)
EYE_POS = np.array([0.0, 0.0, 0.0])
pl.camera.position = EYE_POS
pl.camera.focal_point = (0.0, 0.0, 0.0)

# Track rotation and FOV states
# Default view_angle is usually 30 degrees in VTK
state = {
    "yaw": 0.0, 
    "pitch": 0.0, 
    "last_pos": None, 
    "dragging": False,
    "fov": 30.0  # Tracks our field of view angle
}

# --- LOOK AROUND SYSTEM ---
def on_left_down(iren, event):
    state["dragging"] = True
    state["last_pos"] = iren.GetEventPosition()

def on_left_up(iren, event):
    state["dragging"] = False

def on_mouse_move(iren, event):
    if not state["dragging"]:
        return
    
    curr_pos = iren.GetEventPosition()
    dx = curr_pos[0] - state["last_pos"][0]
    dy = curr_pos[1] - state["last_pos"][1]
    state["last_pos"] = curr_pos
    
    state["yaw"] -= dx * 0.05
    state["pitch"] = np.clip(state["pitch"] + (dy * 0.05), -85, 85)
    
    rad_y, rad_p = np.radians(state["yaw"]), np.radians(state["pitch"])
    look_dir = np.array([
        np.cos(rad_p) * np.sin(rad_y),
        np.cos(rad_p) * np.cos(rad_y),
        -np.sin(rad_p)
    ])
    
    # Force coordinates to lock, change look direction
    pl.camera.position = EYE_POS
    pl.camera.focal_point = EYE_POS + look_dir
    pl.render()

# --- OPTICAL ZOOM SYSTEM (FIELD OF VIEW) ---
def on_mouse_wheel_forward(iren, event):
    # Narrows the field of view to zoom IN
    # Stay within a realistic range (e.g., 2 degrees minimum)
    state["fov"] = max(2.0, state["fov"] - 2.0)
    
    pl.camera.position = EYE_POS # Ensure position didn't slide
    pl.camera.view_angle = state["fov"]
    pl.render()

def on_mouse_wheel_backward(iren, event):
    # Widens the field of view to zoom OUT (fish-eye style)
    # Stay within a realistic range (e.g., 120 degrees maximum)
    state["fov"] = min(120.0, state["fov"] + 2.0)
    
    pl.camera.position = EYE_POS # Ensure position didn't slide
    pl.camera.view_angle = state["fov"]
    pl.render()

# Intercept default interactor controls
iren = pl.render_window.GetInteractor()

# Override rotation behaviors
iren.RemoveObservers("LeftButtonPressEvent")
iren.AddObserver("LeftButtonPressEvent", on_left_down)
iren.AddObserver("LeftButtonReleaseEvent", on_left_up)
iren.AddObserver("MouseMoveEvent", on_mouse_move)

# Override default mouse wheel (which would otherwise physically move the camera coordinates)
iren.RemoveObservers("MouseWheelForwardEvent")
iren.RemoveObservers("MouseWheelBackwardEvent")
iren.AddObserver("MouseWheelForwardEvent", on_mouse_wheel_forward)
iren.AddObserver("MouseWheelBackwardEvent", on_mouse_wheel_backward)

print("Controls:")
print("• Drag Left Mouse: Swivel your head around")
print("• Scroll Wheel: Optical lens zoom (Focal expansion)")

pl.show()