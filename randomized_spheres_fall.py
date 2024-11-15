import bpy 
from random import randint
import random 
from math import radians 

# Clear Existing Objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

tk = bpy.data.texts["bco602tk.py"].as_module()

# Create Ground Plane
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, -5))
ground = bpy.context.object
ground.rotation_euler[0] = -0.285
bpy.ops.rigidbody.object_add()
ground.rigid_body.type = 'PASSIVE'

bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, -5))
ground = bpy.context.object
ground.rotation_euler[0] = 0.285
bpy.ops.rigidbody.object_add()
ground.rigid_body.type = 'PASSIVE'
 
num_spheres = 100
positions = [
    (-1, -1, -1),
    (-1, -1, -.9),
    (-1, -1, -.8),
    (-1, -1, -.7),
    (-1, -1, -.6),
    (-1, -1, -.5),
    (-1, -1, -.4),
    (-1, -1, -.3),
    (-1, -1, -.2),
    (-1, -1, -.1),
    (-1, -1, 0),
    (-1, -1, .1),
    (-1, -1, .2),
    (-1, -1, .3),
    (-1, -1, .4),
    (-1, -1, .5),
    (-1, -1, .6),
    (-1, -1, .7),
    (-1, -1, .8),
    (-1, -1, .9),
    (-1, -1, 1)
]

colors = [
    (1, 0, 0, 1),(0, 1, 0, 1),(0, 0, 1, 1),
    (1, 1, 0, 1),(1, 0, 1, 1),(0, 1, 1, 1)
]

for i in range(num_spheres):
    tk.create.sphere('sphere')
    x, y, z = (randint(-10, 10), randint(-10, 10), 12 + randint(-10, 10))
    tk.sel.translate((x, y, z))
    scale = random.uniform(0.2, 1.0)
    tk.sel.scale((scale, scale, scale))

    alpha = 1
    color1 = tk.makeMaterial('1', colors[randint(0, 5)], 0.5, 0, 0.1) 
    color2 = tk.makeMaterial('2', colors[randint(0, 5)], 0.5, 0, 0.1)
    color3 = tk.makeMaterial('3', colors[randint(0, 5)], 0.5, 0, 0.1)
    color4 = tk.makeMaterial('4', colors[randint(0, 5)], 0.5, 0, 0.1)
    color5 = tk.makeMaterial('5', colors[randint(0, 5)], 0.5, 0, 0.1)

    ob = bpy.context.object 
    me = ob.data 
    me.materials.append(color1) 
    me.materials.append(color2)
    me.materials.append(color3)
    me.materials.append(color4)
    me.materials.append(color5)

    tk.mode("EDIT")
    tk.act.select_by_loc((-1, -1, -1), (1, 1, 1), 'FACE', 'LOCAL') 
        
    ob.active_material_index = 1 
    bpy.ops.object.material_slot_assign()

    for j in positions:
        tk.act.select_by_loc(j, (1, 1, 1), 'FACE', 'LOCAL')
        ob.active_material_index = randint(0, 2)
        bpy.ops.object.material_slot_assign()

    tk.mode("OBJECT")
    bpy.ops.rigidbody.object_add()

# Set Gravity and Frame Settings
bpy.context.scene.gravity = (0, 0, -9.81)
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 60

# Enhanced Physics Settings
bpy.context.scene.rigidbody_world.substeps_per_frame = 120
bpy.context.scene.rigidbody_world.solver_iterations = 10

# Initialize Simulation
bpy.context.scene.frame_set(1)


# for i in range(num_spheres):
#     # Find a non-overlapping position
#     for _ in range(10):  # Try up to 10 times to find a non-overlapping position
#         x, y, z = random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(10, 15)
#         if all(math.dist((x, y, z), pos) >= min_distance for pos in positions):
#             positions.append((x, y, z))
#             break
#     else:
#         continue  