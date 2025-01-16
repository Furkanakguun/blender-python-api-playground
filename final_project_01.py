# 2024 BCO602
# Furkan Akgun
# 01.16.2025

import bpy
import random

flake_name = "Snowflake"
flake_count = 250
x_range = (-10, 10)
y_range = (-10, 10)
z_range = (0, 5)

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def duplicate_snowflakes(flake_name, count, x_range, y_range, z_range):
    """Kar tanelerini çoğaltır ve rastgele yerleştirir."""
    flake = bpy.data.objects.get(flake_name)
    if not flake:
        print("Snowflake object not found.")
        return

    # Snowflake nesnesini geçici olarak görünür hale getir
    flake.hide_viewport = False
    flake.hide_render = False

    for i in range(count):
        new_flake = flake.copy()
        new_flake.scale = (1.3, 1.3, 1.3)
        new_flake.rotation_euler = (
            random.uniform(0, 6.28),
            random.uniform(0, 6.28),
            random.uniform(0, 6.28),
        )
        new_flake.location = (
            random.uniform(*x_range),
            random.uniform(*y_range),
            random.uniform(*z_range),
        )
        bpy.context.collection.objects.link(new_flake)
        
        # Rigidbody ekle ve ayarlarını yap
        bpy.context.view_layer.objects.active = new_flake
        bpy.ops.rigidbody.object_add()
        configure_rigidbody(new_flake)

    # Snowflake nesnesini tekrar gizle
    flake.hide_viewport = True
    flake.hide_render = True


def configure_rigidbody(obj):
    """Rigidbody ayarlarını yapar."""
    obj.rigid_body.mass = 0.1
    obj.rigid_body.friction = 0.2
    obj.rigid_body.use_margin = True
    obj.rigid_body.collision_margin = 0.001
    obj.rigid_body.linear_damping = 0.95
    obj.rigid_body.angular_damping = 0.95
    obj.rigid_body.use_deactivation = False

def create_ground(size, location):
    """Zemin oluştur ve rigidbody ayarlarını uygula."""
    bpy.ops.mesh.primitive_plane_add(size=size, location=location)
    ground = bpy.context.active_object
    bpy.ops.rigidbody.object_add()
    ground.rigid_body.type = 'PASSIVE'
    return ground

def create_white_material():
    """Beyaz bir materyal oluştur."""
    material = bpy.data.materials.new(name="WhiteMaterial")
    material.use_nodes = True
    bsdf = material.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (1, 1, 1, 1)
    bsdf.inputs["Roughness"].default_value = 0.8
    bsdf.inputs["IOR"].default_value = 0.2
    return material

def add_wind_force(location, rotation, strength, flow, noise):
    """Rüzgar ekler ve ayarlarını yapar."""
    bpy.ops.object.effector_add(type='WIND', location=location)
    wind = bpy.context.active_object
    wind.rotation_euler = rotation
    wind.field.strength = strength
    wind.field.flow = flow
    wind.field.noise = noise

def add_turbulence_force(location, strength, size, flow):
    """Türbülans ekler ve ayarlarını yapar."""
    bpy.ops.object.effector_add(type='TURBULENCE', location=location)
    turbulence = bpy.context.active_object
    turbulence.field.strength = strength
    turbulence.field.size = size
    turbulence.field.flow = flow

def create_text_objects(numbers, start_location, scale, rotation):
    """Belirtilen numaralardan bir yazı oluşturur."""
    for idx, num in enumerate(numbers):
        # Text nesnesini ekle
        bpy.ops.object.text_add(location=(
            start_location[0] + idx * 1.3,  # Harfler arası mesafe
            start_location[1],
            start_location[2],
        ))
        text = bpy.context.active_object
        text.data.body = num
        text.data.extrude = 0.1  # Derinlik ekle

        # Pivot noktasını ortala
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

        # Ölçek ve rotasyonu uygula
        text.scale = scale
        text.rotation_euler = rotation

        # Mesh'e çevir ve Rigidbody ekle
        bpy.ops.object.convert(target='MESH')
        bpy.ops.rigidbody.object_add()
        configure_text_rigidbody(text)

        # Material ekle
        create_red_material(text, f"Red_{num}")

def configure_text_rigidbody(text):
    """Text nesnesine rigidbody ayarları uygular."""
    text.rigid_body.mass = 0.2
    text.rigid_body.friction = 0.5
    text.rigid_body.collision_shape = 'BOX'
    text.rigid_body.linear_damping = 0.8  # Lineer hareketi azalt
    text.rigid_body.angular_damping = 0.9  # Açısal hareketi azalt

def create_red_material(obj, material_name):
    obj.color = (1, 0, 0, 1) 
    # obj.data.materials.append(mat)

def create_background(size, location, image_path):
    """Arka plan oluştur ve materyal uygula."""
    bpy.ops.mesh.primitive_plane_add(size=size, location=location)
    background = bpy.context.active_object
    background.rotation_euler.x = 1.5708
    background.scale = (0.4, 0.22, 1.0)

    # Materyal oluştur
    mat = bpy.data.materials.new(name="Background_Material")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()

    # Gerekli düğümleri oluştur
    node_tex_coord = nodes.new('ShaderNodeTexCoord')
    node_tex_image = nodes.new('ShaderNodeTexImage')
    node_emit = nodes.new('ShaderNodeEmission')
    node_output = nodes.new('ShaderNodeOutputMaterial')

    # Texture'u bağla
    node_tex_image.image = bpy.data.images.load(image_path)
    links = mat.node_tree.links
    links.new(node_tex_coord.outputs['UV'], node_tex_image.inputs['Vector'])
    links.new(node_tex_image.outputs['Color'], node_emit.inputs['Color'])
    links.new(node_emit.outputs['Emission'], node_output.inputs['Surface'])

    background.data.materials.append(mat)

# Main method
# clear_scene()
duplicate_snowflakes("Snowflake", 250, (-10, 10), (-10, 10), (0, 5))
ground = create_ground(100, (0, 0, -2))
create_text_objects(
    numbers="5202",                # Yazılacak rakamlar
    start_location=(-2, -5, 0),    # Başlangıç konumu
    scale=(2.2, 2.2, 2.2),         # Ölçek
    rotation=(1.5708, 0, 3.14159)  # Döndürme açıları (x, y, z)
)
ground_material = create_white_material()
ground.data.materials.append(ground_material)
add_wind_force((0, -5, 0), (0, 0.45, 0), 15.0, 2.5, 1.5)
add_turbulence_force((0, 0, 2), 30.0, 7.0, 1.5)
# create_background(50, (0, -10, 3.2), "/Users/furkanakgun/Downloads/final_exam/snowyDark.png")
create_background(50, (0, -10, 3.2), "C://Users//fakgun//Downloads//final_exam//snowyDark.png")