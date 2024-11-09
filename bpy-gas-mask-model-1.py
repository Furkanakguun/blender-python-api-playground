import bpy
import math

# Clear all previous mesh objects
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# Main mask body (a rounded cube for the face covering)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8, location=(0, 0, 1))
mask_body = bpy.context.object
mask_body.scale[1] = 0.6  # Flatten for a more mask-like shape
mask_body.name = "MaskBody"

# Eye pieces
eye_distance = 0.35
eye_radius = 0.2

# Left Eye
bpy.ops.mesh.primitive_cylinder_add(radius=eye_radius, depth=0.1, location=(-eye_distance, 0.5, 1.1))
left_eye = bpy.context.object
left_eye.rotation_euler[0] = math.radians(90)
left_eye.name = "LeftEye"

# Right Eye
bpy.ops.mesh.primitive_cylinder_add(radius=eye_radius, depth=0.1, location=(eye_distance, 0.5, 1.1))
right_eye = bpy.context.object
right_eye.rotation_euler[0] = math.radians(90)
right_eye.name = "RightEye"

# Filter (a larger cylinder on the mouth area)
bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=0.3, location=(0, -0.6, 0.8))
filter_cylinder = bpy.context.object
filter_cylinder.rotation_euler[0] = math.radians(90)
filter_cylinder.name = "Filter"

# Straps (two toruses to simulate straps around the head)
bpy.ops.mesh.primitive_torus_add(major_radius=0.85, minor_radius=0.05, location=(0, 0, 1))
strap1 = bpy.context.object
strap1.rotation_euler[1] = math.radians(90)
strap1.name = "Strap1"

bpy.ops.mesh.primitive_torus_add(major_radius=0.9, minor_radius=0.05, location=(0, 0, 1.2))
strap2 = bpy.context.object
strap2.rotation_euler[0] = math.radians(90)
strap2.name = "Strap2"

# Optional: Add some materials for color
def add_material(obj, color):
    mat = bpy.data.materials.new(name=f"{obj.name}_Mat")
    mat.diffuse_color = color
    obj.data.materials.append(mat)

# Add colors
add_material(mask_body, (0.1, 0.1, 0.1, 1))  # Dark gray for the mask
add_material(left_eye, (0, 0, 0, 1))  # Black for the eye pieces
add_material(right_eye, (0, 0, 0, 1))  # Black for the eye pieces
add_material(filter_cylinder, (0.2, 0.2, 0.2, 1))  # Darker gray for the filter
add_material(strap1, (0.1, 0.1, 0.1, 1))  # Same as mask body for the straps
add_material(strap2, (0.1, 0.1, 0.1, 1))  # Same as mask body for the straps

print("Gas mask created with main body, eye pieces, filter, and straps!")
