import bpy

# --- Step 1: Clear Existing Objects ---
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# --- Step 2: Create the Ground Plane ---
# Add a plane to serve as the ground
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
ground = bpy.context.object  # Reference to the plane object

# Set the plane as a passive rigid body (doesn't move but interacts with active bodies)
bpy.ops.rigidbody.object_add()
ground.rigid_body.type = 'PASSIVE'  # Set to passive, so it stays static
ground.rigid_body.restitution = 0.9  # Set bounciness on the plane as well

# --- Step 3: Create the Ball ---
# Add a UV sphere to act as the ball
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 5))
ball = bpy.context.object  # Reference to the ball object

# --- Step 4: Add Rigid Body Physics to the Ball ---
bpy.ops.rigidbody.object_add()  # Add rigid body physics to the ball
ball.rigid_body.type = 'ACTIVE'  # Set to active, so it will be affected by gravity

# Set physical properties to maximize bounce
ball.rigid_body.mass = 1         # Set mass of the ball (default is 1)
ball.rigid_body.friction = 0.2   # Lower friction to reduce sliding resistance
ball.rigid_body.restitution = 0.9  # Increase bounciness for both objects

# --- Step 5: Configure Scene Settings for Physics ---
# Ensure the rigid body world is enabled and set gravity
if not bpy.context.scene.rigidbody_world:
    bpy.context.scene.rigidbody_world = bpy.data.worlds.new("RigidBodyWorld")

# Set gravity for the entire scene
bpy.context.scene.gravity = (0, 0, -9.81)  # Standard gravity in m/s^2

# Set the frame range for the animation
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 60

# --- Step 6: Run the Simulation ---
# Set the current frame to 1 to initialize the physics simulation
bpy.context.scene.frame_set(1)

# --- End of Script ---