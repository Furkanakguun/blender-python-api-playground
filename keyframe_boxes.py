import bpy
import random

# Alias for the helper module
tk = bpy.data.texts["bco602tk.py"].as_module()

# Clear existing objects using the helper
tk.delete_all()

# Create a random material for the cubes
def create_random_material():
    mat_name = f"Material_{random.randint(1, 1000)}"
    color = (random.random(), random.random(), random.random(), 1)  # Random RGBA
    return tk.makeMaterial(name=mat_name, diffuse=color)

# Create a single cube with initial height and color
def create_random_cube(name, location):
    # Create cube using helper
    tk.create.cube(name)

    # Set cube location
    tk.spec.location(name, location)

    # Set initial height (z-axis scale)
    initial_height = random.uniform(1.0, 2.0)  # Random initial height
    tk.spec.scale(name, (1, 1, initial_height))

    # Assign a random material
    cube = bpy.data.objects[name]
    mat = create_random_material()
    tk.setMaterial(cube, mat)

    return cube

# Animate the cube's height without going below z=0
def animate_cube_height(cube):
    scene = bpy.context.scene
    start_frame = scene.frame_start
    end_frame = scene.frame_end

    for frame in range(start_frame, end_frame + 1, 10):  # Keyframes every 10 frames
        # Randomly adjust height but ensure z >= 0
        random_height = random.uniform(0.5, 3.0)  # Random height
        cube.scale.z = random_height / 2  # Scale height (Blender uses half-height)

        # Ensure cube's bottom remains at z=0
        cube.location.z = random_height / 2

        # Insert keyframes for location and scale
        cube.keyframe_insert(data_path="location", index=2, frame=frame)  # z-axis
        cube.keyframe_insert(data_path="scale", index=2, frame=frame)    # z-scale

# Main function to create a grid of cubes and animate their heights
def create_and_animate_cubes():
    grid_size = 10
    spacing = 0.5  # Distance between cubes

    for i in range(grid_size):
        for j in range(grid_size):
            # Define cube name and location
            name = f"Cube_{i}_{j}"
            location = (i * spacing, j * spacing, 0)

            # Create and animate cube
            cube = create_random_cube(name, location)
            animate_cube_height(cube)

# Set animation frame range
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 100

# Create and animate the cubes
create_and_animate_cubes()
