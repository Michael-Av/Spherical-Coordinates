import pyvista as pv
import numpy as np

pl = pv.Plotter()

grid = pv.ImageData(dimensions=(10, 10, 10), spacing=(1, 1, 1), origin=(0, 0, 0))
pl.add_mesh(grid, show_edges=True, color='lightgray', opacity=0.3)
pl.add_axes()
#pl.add_mesh(pv.Cube(center=(5, 5, 2)), color='tomato')

points = np.random.rand(100, 3)
cloud = pv.PolyData(points)
pl.add_mesh(cloud, style='points', color='red')


# 2. Fix the initial position (standing in one spot)
EYE_POS = np.array([5.0, 5.0, 2.0])
pl.camera.position = EYE_POS
pl.camera.focal_point = (5.0, 5.0, 2.0)

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
    
    state["yaw"] -= dx * 0.4
    state["pitch"] = np.clip(state["pitch"] + (dy * 0.4), -85, 85)
    
    rad_y, rad_p = np.radians(state["yaw"]), np.radians(state["pitch"])
    look_dir = np.array([
        np.cos(rad_p) * np.sin(rad_y),
        np.cos(rad_p) * np.cos(rad_y),
        np.sin(rad_p)
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