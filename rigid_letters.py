import bpy
from math import radians

# Clear all objects
bpy.ops.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

# Create and name Text object
bpy.ops.object.text_add(location=(0, 0, 0))
obj = bpy.context.object
obj.name = 'Letter'
obj.data.name = 'LetterData'
# Data attributes
obj.data.body = 'S'
obj.data.font = bpy.data.fonts[0]
obj.data.offset_x = 0
obj.data.offset_y = 0
obj.data.shear = 0
obj.data.space_character = 0
obj.data.size = 3
obj.data.space_word = 0
obj.data.extrude = 0.1
# Rotate 90 degrees
bpy.ops.transform.rotate(value=radians(90), orient_axis='X')
# Convert to a mesh
bpy.ops.object.convert(target='MESH')
bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')
# Rigidbody
bpy.ops.rigidbody.object_add()
bpy.context.object.rigid_body.type = 'ACTIVE'
bpy.context.object.rigid_body.collision_shape = 'MESH'
# plane
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
bpy.ops.rigidbody.object_add()
bpy.context.object.rigid_body.type = 'PASSIVE'
bpy.context.object.rigid_body.collision_shape = 'MESH'