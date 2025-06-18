import vtk
import sys

# Script to set vectors to zero in a VTK structured grid.
# This script was created to modify the ellipsoid vector field. ( The toy problem for the BioMesh library. )
# For now we assume that the vector field moves forward in the Z direction.

vtk_file = sys.argv[1]
vector_tag = sys.argv[2]
z_min = float(sys.argv[3])
z_max = float(sys.argv[4])

# Read the VTK file.
reader = vtk.vtkStructuredGridReader()
reader.SetFileName(vtk_file)
reader.Update()
structuredGrid = reader.GetOutput()

# Access points and vectors in the VTK structured grid.
points = structuredGrid.GetPoints()
vectors = structuredGrid.GetPointData().GetArray(vector_tag);
num_points = points.GetNumberOfPoints()
if not vectors:
	print("No vector data. Make sure the tag is correct.")

# Set vectors to zero
for i in range(num_points):
    point = points.GetPoint(i)
    if point[2] < z_min or point[2] > z_max:
    	vectors.SetTuple3(i,0.0,0.0,0.0)

# Write the modified grid to a separate VTK file.
writer = vtk.vtkStructuredGridWriter()
writer.SetFileName("structured_grid.vtk")
writer.SetInputData(structuredGrid)
writer.Write()

