import pyvista as pv
import numpy as np
import cameraHandler

EYE_POS = np.array([0.0, 0.0, 0.0])

# background sphere
background_sphere = pv.Sphere(radius=1)

# axes
phi_ticks = np.radians(np.arange(0,181,10))
theta_ticks = np.radians(np.arange(0,360,10))

phi_points, theta_points = np.meshgrid(phi_ticks, theta_ticks, indexing='ij')

phi_points = phi_points.ravel()
theta_points = theta_points.ravel()

phi_points_deg = np.degrees(phi_points)
theta_points_deg = np.degrees(theta_points)

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

def get_horizon_labels():
    result = []
    for i in range(0, 360, 10):
        if i % 90 != 0: result.append(str(i) + "°")
        if i == 0: result.append("North")
        if i == 90: result.append("East")
        if i == 180: result.append("South")
        if i == 270: result.append("West")
    result.append("placeholder")
    return result

# stars
phi_vals = np.random.rand(100) * 2*np.pi
theta_vals = np.random.rand(100) * 2*np.pi

star_x = 0.9 * np.sin(phi_vals) * np.cos(theta_vals)
star_y = 0.9 * np.sin(phi_vals) * np.sin(theta_vals)
star_z = 0.9 * np.cos(phi_vals)

star_positions = np.column_stack((star_x,star_y,star_z))

stars = pv.PolyData(star_positions)

pl = pv.Plotter()
pl.add_mesh(background_sphere, color='black', show_edges=True)
pl.add_mesh(axes, color='red')
pl.add_point_labels(axis_points[9::36], get_horizon_labels()[:19], font_size = 30)
pl.add_point_labels(axis_points[27::36], get_horizon_labels()[18:], font_size = 30)
# pl.add_point_labels(axis_points, range(0,len(axis_points)), font_size=20)
pl.add_mesh(stars, color='white')

cameraHandler.initialize(pl)

print("Controls:")
print("• Drag Left Mouse: Swivel your head around")
print("• Scroll Wheel: Optical lens zoom (Focal expansion)")

pl.show()