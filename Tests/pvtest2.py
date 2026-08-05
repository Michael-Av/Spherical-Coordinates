import pyvista as pv
import numpy as np

background_sphere = pv.Sphere(radius=1)

phi_vals = np.random.rand(100) * 2*np.pi
theta_vals = np.random.rand(100) * 2*np.pi

x = 0.9 * np.sin(theta_vals) * np.cos(phi_vals)
y = 0.9 * np.sin(theta_vals) * np.sin(phi_vals)
z = 0.9 * np.cos(theta_vals)

star_positions = np.column_stack((x,y,z))

stars = pv.PolyData(star_positions)

pl = pv.Plotter()
pl.add_mesh(background_sphere, color='black', show_edges=True)
pl.add_mesh(stars, color='white')
pl.show()
