import numpy as np
import pyvista as pv

# Parameters of the ellipsoid
a = 4  # Semi-major axis in x-direction
b = 4  	# Semi-minor axis in y-direction
#c = 8 	# Semi-major axis in z-direction (flow direction)
c = 12

# Create a 3D grid inside the ellipsoid's bounding box
cuboid_scale = 1.0  # Scale factor for the cuboid relative to the ellipsoid's bounding box
cx = cuboid_scale * a
cy = cuboid_scale * b
cz = cuboid_scale * c

x = np.linspace(-cx, cx, 20)
y = np.linspace(-cy, cy, 20)
z = np.linspace(-cz, cz, 20)
X, Y, Z = np.meshgrid(x, y, z)

# Ellipsoid boundary condition: points outside the ellipsoid are invalid
inside = (X / a)**2 + (Y / b)**2 + (Z / c)**2 <= 1

# Define the velocity field
U = np.zeros_like(X)  # x-component
V = np.zeros_like(Y)  # y-component
W = np.zeros_like(Z)  # z-component

# For valid points inside the ellipsoid
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        for k in range(X.shape[2]):
            if inside[i, j, k]:
                # Position vector of the point
                pos = np.array([X[i, j, k], Y[i, j, k], Z[i, j, k]])
                
                # Normal vector to the ellipsoid at the point
                normal = np.array([
                    2 * X[i, j, k] / a**2,
                    2 * Y[i, j, k] / b**2,
                    2 * Z[i, j, k] / c**2
                ])
                normal /= np.linalg.norm(normal)  # Normalize the normal vector
                
                # Tangential vector in the z-axis direction
                flow_direction = np.array([0, 0, 1])  # Straight along z-axis
                flow_tangent = flow_direction - np.dot(flow_direction, normal) * normal
                flow_tangent /= np.linalg.norm(flow_tangent)  # Normalize
                
                # Assign the tangential vector as velocity components
                U[i, j, k], V[i, j, k], W[i, j, k] = flow_tangent

# Remove vectors outside the ellipsoid
U[~inside] = 0
V[~inside] = 0
W[~inside] = 0

# Create a VTK structured grid
grid = pv.StructuredGrid()
grid.points = np.c_[X.ravel(), Y.ravel(), Z.ravel()]
grid.dimensions = X.shape
grid["vectors"] = np.c_[U.ravel(), V.ravel(), W.ravel()]

# Save the structured grid to a VTK file
grid.save("sgrid3d_ellipsoid_first_octant.vtk")
print("VTK file 'sgrid3d_ellipsoid_first_octant.vtk' created.")


