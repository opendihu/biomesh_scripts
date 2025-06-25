import json
import math

def generate_circle_points(n, radius, center=(0, 0, 0)):
    """Generates n points along the circumference of a circle with a given radius and center."""
    cx, cy, cz = center
    points = []
    for i in range(n):
        angle = 2 * math.pi * i / n  # even spacing in radians
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        z = cz  # same z for all points in the circle
        points.append({"x": x, "y": y, "z": z})
    return points

def generate_layered_circles(n, radii, center=(0, 0, 0)):
    """Generates points for multiple circles with varying radii.
    
    :param n: Number of points per circle.
    :param radii: List of radii for each circle layer.
    :param center: Center of the circles.
    :return: List of all points from all layers.
    """
    all_points = []
    for radius in radii:
        circle_points = generate_circle_points(n, radius, center)
        all_points.extend(circle_points)
    return all_points

def write_points_to_json(points, filename="coordinates.json"):
    """Writes the list of points to a JSON file with a 'seed_points' root key."""
    data = {"seed_points": points}
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Example usage:
if __name__ == "__main__":
    n = 24  # Number of points per circle
    radii = [1.98]  # First layer with radius 0.5, second layer with radius 1.0
    center = (0.0, 0.0, -6.5)  # Center for both circles (can be changed if needed)
    
    points = generate_layered_circles(n, radii, center)
    write_points_to_json(points)
    print(f"Successfully wrote layered circle points to coordinates.json")

