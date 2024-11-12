import bpy
import random
import math

# Clear Existing Objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

tk = bpy.data.texts["bco602tk.py"].as_module()

# Create Ground Plane
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
ground = bpy.context.object
ground.rotation_euler[0] = -0.385
bpy.ops.rigidbody.object_add()
ground.rigid_body.type = 'PASSIVE'

bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
ground = bpy.context.object
ground.rotation_euler[0] = 0.385
bpy.ops.rigidbody.object_add()
ground.rigid_body.type = 'PASSIVE'
 
 
# Number of Spheres and Minimum Distance Between Them
num_spheres = 25
min_distance = 1.5

# Track Positions to Avoid Overlapping
positions = [] 

for i in range(num_spheres):
    # Find a non-overlapping position
    for _ in range(10):  # Try up to 10 times to find a non-overlapping position
        x, y, z = random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(10, 15)
        if all(math.dist((x, y, z), pos) >= min_distance for pos in positions):
            positions.append((x, y, z))
            break
    else:
        continue  # Skip this sphere if a position wasn't found
    
    # Create Sphere with Random Position and Scale
    bpy.ops.mesh.primitive_uv_sphere_add(location=(x, y, z))
    sphere = bpy.context.object
    scale = random.uniform(0.2, 1.0)
    sphere.scale = (scale, scale, scale)
    
    # Add Rigid Body Physics
    bpy.ops.rigidbody.object_add()
    sphere.rigid_body.type = 'ACTIVE'
    
    # Create materials
    alpha = 0.9
    red = tk.makeMaterial('Red', (1, 0, 0, alpha), 0.5, 0, 0.1)
    green = tk.makeMaterial('Green', (0, 1, 0, alpha), 0.5, 0, 0.1)
    blue = tk.makeMaterial('Blue', (0, 0, 1, alpha), 0.8, 0.8, 0.2)
    # material = bpy.data.materials.new(name=f"SolidColorMaterial_{i}")
    # material.use_nodes = True
    # bsdf = material.node_tree.nodes["Principled BSDF"]
    # bsdf.inputs["Base Color"].default_value = (random.random(), random.random(), random.random(), 1)  # Random RGB color
    
    # Assign the material to the sphere
    sphere.data.materials.clear()  # Clear any existing materials
    sphere.data.materials.append(red)  # Apply the new material

# Set Gravity and Frame Settings
bpy.context.scene.gravity = (0, 0, -9.81)
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 60

# Enhanced Physics Settings
bpy.context.scene.rigidbody_world.substeps_per_frame = 120
bpy.context.scene.rigidbody_world.solver_iterations = 10

# Initialize Simulation
bpy.context.scene.frame_set(1)
