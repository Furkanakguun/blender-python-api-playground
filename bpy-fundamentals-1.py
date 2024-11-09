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

# Adding a material to the cube
cube_material = bpy.data.materials.new(name="CubeMaterial")
cube_material.diffuse_color = (1, 0, 0, 1)  # Red color
cube.data.materials.append(cube_material)

# Adding a material to the sphere
sphere = bpy.data.objects["Sphere"]
sphere_material = bpy.data.materials.new(name="SphereMaterial")
sphere_material.diffuse_color = (0, 0, 1, 1)  # Blue color
sphere.data.materials.append(sphere_material)

# Add a sun light
bpy.ops.object.light_add(type='SUN', radius=1, location=(5, 5, 5))
light = bpy.context.object
light.data.energy = 5  # Adjust brightness

# Add a camera
bpy.ops.object.camera_add(location=(8, -8, 5), rotation=(1.109, 0, 0.785))
bpy.context.scene.camera = bpy.context.object

# Set render resolution
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080

# Render the image
# bpy.ops.render.render(write_still=True)
# bpy.data.images['Render Result'].save_render(filepath="/tmp/render.png")
