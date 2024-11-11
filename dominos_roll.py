import bpy

# --- Clear Existing Objects ---
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# ---  Create the Ground Plane ---
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
ground = bpy.context.object  # Reference to the plane object

# Set the plane as a passive rigid body
bpy.ops.rigidbody.object_add()
ground.rigid_body.type = 'PASSIVE'  # Passive rigid body does not move
ground.rigid_body.collision_shape = 'BOX'  # Using BOX collision shape for efficiency

# ---  Create 5 Bricks in an Upright Position ---
# Define brick dimensions and initial position
brick_width = 0.5
brick_height = 2.5
brick_depth = 1.0
x_start = -3  # Starting X position to line up the bricks in a row

# Loop to create and position the bricks
for i in range(5):
    # Add a brick as a scaled cube
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x_start + i * 1.5, 0, brick_height / 2))
    brick = bpy.context.object
    brick.scale = (brick_width, brick_depth / 2, brick_height / 2)  # Scale to match brick dimensions

    # Add rigid body physics to each brick
    bpy.ops.rigidbody.object_add()
    brick.rigid_body.type = 'ACTIVE'  # Active rigid body is affected by physics
    brick.rigid_body.collision_shape = 'BOX'  # Using BOX collision for efficiency

    # Optional: Adjust physical properties
    brick.rigid_body.mass = 2  # Set mass of each brick
    brick.rigid_body.friction = 0.6  # Friction to prevent excessive sliding
    brick.rigid_body.restitution = 0.2  # Lower bounciness for a more stable effect

# ---  Apply an Initial Push to the First Brick ---
# Select the first brick (assumes it’s the first created object in the loop)
first_brick = bpy.context.scene.objects[0]

# Apply a small rotation to start the fall (10 degrees in radians)
first_brick.rotation_euler[1] = 0.1  # Rotate slightly around the Y-axis
first_brick.keyframe_insert(data_path="rotation_euler", frame=1)

# Alternatively, add a slight initial force (uncomment below if needed)
#first_brick.rigid_body.kinematic = True
#first_brick.location.x -= 0.1  # Adjust location slightly
#first_brick.keyframe_insert(data_path="location", frame=1)
#first_brick.rigid_body.kinematic = False

# --- Configure Scene Settings for Physics ---
# Enable the rigid body world and set gravity
if not bpy.context.scene.rigidbody_world:
    bpy.context.scene.rigidbody_world = bpy.data.worlds.new("RigidBodyWorld")

bpy.context.scene.gravity = (0, 0, -9.81)  # Set standard gravity

# Set the frame range for the simulation
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 120

# --- Step 6: Run the Simulation ---
# Set the current frame to 1 to initialize the physics simulation
bpy.context.scene.frame_set(1)

# --- End of Script ---
