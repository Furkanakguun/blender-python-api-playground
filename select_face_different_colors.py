import bpy
import bmesh
from math import radians

tk = bpy.data.texts["bco602tk.py"].as_module()
# Create materials
alpha = 0.9
red = tk.makeMaterial('Red', (1, 0, 0, alpha), 0.5, 0, 0.1)
green = tk.makeMaterial('Green', (0, 1, 0, alpha), 0.5, 0, 0.1)
blue = tk.makeMaterial('Blue', (0, 0, 1, alpha), 0.8, 0.8, 0.2)
# Will fail if scene is empty
tk.mode("OBJECT")
tk.delete_all()
tk.create.sphere("sphere_1")

ob = bpy.context.object
me = ob.data
me.materials.append(red)
me.materials.append(blue)
me.materials.append(green)
tk.mode("EDIT")
tk.act.select_by_loc((0, 0, 0), (1, 1, 1), 'FACE', 'GLOBAL')
# use second material slot
ob.active_material_index = 1
bpy.ops.object.material_slot_assign()
tk.mode("OBJECT")
tk.sel.rotate_z(radians(90))
tk.mode("EDIT")
tk.act.select_by_loc((0, 0, 0), (1, 1, 1), 'FACE', 'GLOBAL')
ob.active_material_index = 2
bpy.ops.object.material_slot_assign()

tk.mode("OBJECT")