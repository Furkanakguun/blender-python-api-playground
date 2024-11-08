import bpy

# Clear all existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Create a Plane for the ground
bpy.ops.mesh.primitive_plane_add(size=10, enter_editmode=False, location=(0, 0, 0))

# Create a Cube
bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, location=(0, 0, 1))

# Create a Sphere
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, location=(3, 3, 1))

# Rotate and scale the Cube
cube = bpy.context.object
cube.rotation_euler = (0.785, 0.785, 0)  # Rotate 45 degrees on two axes
cube.scale = (1.5, 1.5, 0.5)  # Make it a flat cuboid
