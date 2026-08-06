import pyvista as pv
import numpy as np
import Tests.cameraHandler

def createAxesGrid():
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
    for i in range(1, len(axis_points)):
        connection_indices.append([i,i-1]) # connects altitude lines
        if i >= 36:
            connection_indices.append([i,i-36]) # connects azimuth lines

    axes = pv.PolyData(axis_points, lines=pv.CellArray.from_regular_cells(connection_indices))
    return axes

def get_horizon_labels():
    result = []
    for i in range(0, 360, 10):
        if i % 90 != 0: result.append(str(360-i) + "°")
        if i == 0: result.append("North")
        if i == 90: result.append("West")
        if i == 180: result.append("South")
        if i == 270: result.append("East")
    return result

def getStarSizeScales(appMagnitudes):
    starScalars = []
    for appMagnitude in appMagnitudes:
        starScalars.append(-0.185*appMagnitude + 1.25)
    return starScalars

def getGround():
    phi_vals = np.radians(np.arange(0, 360, 10))
    theta_vals = [np.pi/2]*36

    points_x = np.sin(theta_vals) * np.cos(phi_vals)
    points_y = np.sin(theta_vals) * np.sin(phi_vals)
    points_z = np.cos(theta_vals)

    points = np.column_stack((points_x, points_y, points_z))
    
    faces = [36]
    faces.extend(range(36))

    ground = pv.PolyData(points, faces=faces)
    return ground

def plotVisibleStars(names, altitudes, azimuths, appMagnitudes, showLabels):
    phi_values = [0]*len(altitudes)
    for i in range(len(altitudes)):
        phi_values[i] = np.pi/2 - altitudes[i]

    theta_values = [0]*len(azimuths)
    for i in range(len(azimuths)):
        theta_values[i] = 2*np.pi - azimuths[i]

    star_x = 0.9 * np.sin(phi_values) * np.cos(theta_values)
    star_y = 0.9 * np.sin(phi_values) * np.sin(theta_values)
    star_z = 0.9 * np.cos(phi_values)

    label_phis = phi_values.copy()
    label_thetas = theta_values.copy()
    for i in range(len(label_phis)):
        label_phis[i] -= 0.005
        # label_thetas[i] += 0.05

    label_x = 0.9 * np.sin(label_phis) * np.cos(label_thetas)
    label_y = 0.9 * np.sin(label_phis) * np.sin(label_thetas)
    label_z = 0.9 * np.cos(label_phis)

    star_positions = np.column_stack((star_x,star_y,star_z))
    label_positions = np.column_stack((label_x, label_y, label_z))

    stars = pv.PolyData(star_positions)
    # labels = pv.PolyData(label_positions)

    # background sphere
    background_sphere = pv.Sphere(radius=1)

    # azimuth and altitude lines
    axes = createAxesGrid()

    pl = pv.Plotter()
    pl.add_mesh(background_sphere, color='black', show_edges=True)
    pl.add_mesh(axes, color='red')

    stars["my_sizes"] = getStarSizeScales(appMagnitudes)
    
    starSpheres = stars.glyph(geom=pv.Sphere(radius=0.004), scale="my_sizes", orient=False)
    pl.add_mesh(starSpheres, color='white', lighting=False)
    pl.add_mesh(getGround(), name='ground', color='green', copy_mesh = False)

    # print(len(labels.points))
    print(len(names))

    if showLabels:
        pl.add_point_labels(label_positions, names, text_color='white', font_size = 15, always_visible = True, margin=10, shape_opacity=0, show_points=False, justification_horizontal='center')
    pl.add_point_labels(axes.points[9::36], get_horizon_labels()[:19], font_size = 20, text_color='white', shape = None, always_visible = True, show_points=False)
    pl.add_point_labels(axes.points[27:640:36], get_horizon_labels()[18:], font_size = 20, text_color='white', shape = None, always_visible = True, show_points=False)

    Tests.cameraHandler.initialize(pl)

    print("Controls:")
    print("• Drag Left Mouse: Swivel your head around")
    print("• Scroll Wheel: Optical lens zoom (Focal expansion)")

    pl.show()