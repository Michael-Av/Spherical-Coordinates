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
phi_vals = np.random.rand(100) * np.pi/2
theta_vals = np.random.rand(100) * np.pi/2

star_x = 0.9 * np.sin(phi_vals) * np.cos(theta_vals)
star_y = 0.9 * np.sin(phi_vals) * np.sin(theta_vals)
star_z = 0.9 * np.cos(phi_vals)

star_positions = np.column_stack((star_x,star_y,star_z))

stars = pv.PolyData(star_positions)

pl = pv.Plotter()
pl.add_mesh(background_sphere, color='black', show_edges=True)
pl.add_mesh(axes, color='red')
pl.add_mesh(stars, color='white')

cameraHandler.initialize(pl)

print("Controls:")
print("• Drag Left Mouse: Swivel your head around")
print("• Scroll Wheel: Optical lens zoom (Focal expansion)")

pl.show()