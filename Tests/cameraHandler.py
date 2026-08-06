import numpy as np

EYE_POS = np.array([0.0, 0.0, 0.05])

# Track rotation and FOV states
# Default view_angle is usually 30 degrees in VTK
state = {
    "yaw": 90.0, 
    "pitch": -20.0, 
    "last_pos": None, 
    "dragging": False,
    "fov": 70.0,  # Tracks our field of view angle
    "plot": None     # Temporary, this will be set to the 3D plot when the program starts
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
    state["plot"].camera.position = EYE_POS
    state["plot"].camera.focal_point = EYE_POS + look_dir
    state["plot"].render()

    # adjust ground opacity if looking down
    if state["pitch"] < 0:
        return
    actors = state["plot"].actors
    opacity = 1 - 3*state["pitch"] / 90
    if opacity < 0: opacity = 0
    actors['ground'].prop.opacity = opacity
    state['plot'].update()


# --- OPTICAL ZOOM SYSTEM (FIELD OF VIEW) ---
def on_mouse_wheel_forward(iren, event):
    # Narrows the field of view to zoom IN
    # Stay within a realistic range (e.g., 10 degrees minimum)
    state["fov"] = max(10.0, state["fov"] - 3.0)
    
    state["plot"].camera.position = EYE_POS # Ensure position didn't slide
    state["plot"].camera.view_angle = state["fov"]
    state["plot"].render()

def on_mouse_wheel_backward(iren, event):
    # Widens the field of view to zoom OUT (fish-eye style)
    # Stay within a realistic range (e.g., 120 degrees maximum)
    state["fov"] = min(120.0, state["fov"] + 3.0)
    
    state["plot"].camera.position = EYE_POS # Ensure position didn't slide
    state["plot"].camera.view_angle = state["fov"]
    state["plot"].render()

def initialize(plot):
#     # Intercept default interactor controls
    plot.camera.position = EYE_POS
    plot.camera.focal_point = EYE_POS
    #plot.camera.azimuth = 90.0
    plot.camera.zoom(0.5)
    plot.camera.view_angle = state["fov"]

    iren = plot.render_window.GetInteractor()
    state["plot"] = plot

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
