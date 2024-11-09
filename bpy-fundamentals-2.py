import bpy
import math

# --- SECTION 1: Clear Existing Objects ---
# Start by clearing all existing objects to avoid conflicts with previous scenes
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# --- SECTION 2: Create a Grid of Cubes ---
# Define grid size and spacing
rows = 5
cols = 5
spacing = 3  # Distance between cubes

# Create grid of cubes
for row in range(rows):
    for col in range(cols):
        # Calculate position
        x = col * spacing
        y = row * spacing
        z = 0
        
        # Add cube at calculated position
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
        
# ====== SECTION 3 Createa a collection and add objets to it ====== 
if "MyCollection" not in bpy.data.collections:
    new_collection = bpy.data.collectsions.new("MyCollection")
    bpy.context.scene.collection.children.link(new_collection)
else:
    new_collection = bpy.data.collections["MyCollection"]

# Add three spheres to the collection
for i in range(3):
    # Create a sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(i * 2, -10, 0))
    
    # Reference the created sphere and unlink from main Scene Collection if needed
    obj = bpy.context.object
    if bpy.context.scene.collection.objects.get(obj.name):
        bpy.context.scene.collection.objects.unlink(obj)
    
    # Link the sphere to the new collection
    new_collection.objects.link(obj) 


# --- SECTION 4: Modify Vertices of a Cube ---
# Add another cube to modify its vertices
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 10, 0))
cube = bpy.context.object  # Reference the cube object

# Switch to object mode to access and modify vertex data
bpy.ops.object.mode_set(mode='OBJECT')
for vertex in cube.data.vertices:
    vertex.co.z += math.sin(vertex.co.x * 2)  # Modify Z based on X to create a wave effect


# --- SECTION 5: Create a Material and Apply It to an Object ---
# Create a new material with nodes enabled
material = bpy.data.materials.new(name="MyMaterial")
material.use_nodes = True

# Set material color to blue
bsdf = material.node_tree.nodes["Principled BSDF"]
bsdf.inputs['Base Color'].default_value = (0.1, 0.5, 0.8, 1)  # Blue color

# Apply the material to the cube we just created
cube.data.materials.append(material)


# --- SECTION 6: Animate Cube Rotation ---
# Create another cube for animation
bpy.ops.mesh.primitive_cube_add(size=2, location=(5, 5, 0))
animated_cube = bpy.context.object

# Set keyframes to animate rotation around Z-axis
frames = [1, 30, 60, 90]
angles = [0, math.radians(90), math.radians(180), math.radians(270)]

for frame, angle in zip(frames, angles):
    animated_cube.rotation_euler[2] = angle  # Set Z rotation
    animated_cube.keyframe_insert(data_path="rotation_euler", index=2, frame=frame)

# --- End of Script ---