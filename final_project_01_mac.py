import bpy
import random

# Sahneyi Temizle
#bpy.ops.object.select_all(action='SELECT')
#bpy.ops.object.delete()

# Import aktarılan objeyi seç
flake = bpy.data.objects.get("Snowflake")

# Kar tanelerini çoğalt ve rastgele yerleştir
flake_count = 250
x_range = (-10, 10)
y_range = (-10, 10)
z_range = (0, 5)

for i in range(flake_count):
    # Kar tanesini kopyala
    new_flake = flake.copy()
    new_flake.scale = (1.3, 1.3, 1.3)
    new_flake.rotation_euler = (
        random.uniform(0, 6.28),
        random.uniform(0, 6.28),
        random.uniform(0, 6.28)
    )
    new_flake.location = (
        random.uniform(*x_range),
        random.uniform(*y_range),
        random.uniform(*z_range),
    )
    bpy.context.collection.objects.link(new_flake)
    
    # Rigidbody ekle
    bpy.context.view_layer.objects.active = new_flake
    bpy.ops.rigidbody.object_add()
    
    # Rigidbody ayarları
    new_flake.rigid_body.mass = 0.1
    new_flake.rigid_body.friction = 0.2
    new_flake.rigid_body.use_margin = True
    new_flake.rigid_body.collision_margin = 0.001
    new_flake.rigid_body.linear_damping = 0.95
    new_flake.rigid_body.angular_damping = 0.95
    new_flake.rigid_body.use_deactivation = False

# Orijinal objeyi gizle
flake.hide_viewport = True

# 2. Zemini oluştur
bpy.ops.mesh.primitive_plane_add(size=100, location=(0, 0, -2))
ground = bpy.context.active_object
bpy.ops.rigidbody.object_add()
ground.rigid_body.type = 'PASSIVE'

# 3. Beyaz materyali oluştur
material = bpy.data.materials.new(name="WhiteMaterial")
material.use_nodes = True
bsdf = material.node_tree.nodes["Principled BSDF"]

# 4. Base Color'u beyaz yap
bsdf.inputs["Base Color"].default_value = (1, 1, 1, 1)  # RGB: Beyaz, Alpha: 1

# 5. Roughness ve Specular ayarlarını düzenle
bsdf.inputs["Roughness"].default_value = 0.8  # Hafif mat görünüm
bsdf.inputs["IOR"].default_value = 0.2  # Hafif parlaklık

# zeminin materyalini ata
ground.data.materials.append(material)

# Wind Force Field ekle
bpy.ops.object.effector_add(type='WIND', location=(0, -5, 0))
wind = bpy.context.active_object
# Wind Force Field ayarları
wind.rotation_euler = (0, 0.45, 0)  # Rüzgar açısını biraz daha artırdım
wind.field.strength = 15.0  # Rüzgar gücünü artırdım
wind.field.flow = 2.5  # Akış düzgünlüğünü artırdım
wind.field.noise = 1.5  # Rüzgar türbülansını artırdım

# Turbulence Force Field ekle
bpy.ops.object.effector_add(type='TURBULENCE', location=(0, 0, 2))
turbulence = bpy.context.active_object
# Turbulence Force Field ayarları
turbulence.field.strength = 30.0  # Türbülans gücünü artırdım
turbulence.field.size = 7.0  # Türbülans alanı boyutunu artırdım
turbulence.field.flow = 1.5  # Akış düzgünlüğünü artırdım

# Background plane oluştur
bpy.ops.mesh.primitive_plane_add(size=50, location=(0, -10, 3.2))
background = bpy.context.active_object
background.rotation_euler.x = 1.5708  # 90 derece döndür (dikey duracak şekilde)
background.scale = (0.4, 0.22, 1.0)  # Daha geniş bir arka plan oluştur

# Texture oluştur
# Yeni material oluştur
mat = bpy.data.materials.new(name="Background_Material")
mat.use_nodes = True
nodes = mat.node_tree.nodes

# Tüm nodes'ları temizle
nodes.clear()

# Gerekli nodes'ları ekle
node_tex_coord = nodes.new('ShaderNodeTexCoord')
node_tex_image = nodes.new('ShaderNodeTexImage')
node_emit = nodes.new('ShaderNodeEmission')
node_output = nodes.new('ShaderNodeOutputMaterial')

# Texture'u yükle
node_tex_image.image = bpy.data.images.load("/Users/furkanakgun/Downloads/final_exam/snowyDark.png")

# Nodes'ları bağla
links = mat.node_tree.links
links.new(node_tex_coord.outputs['UV'], node_tex_image.inputs['Vector'])
links.new(node_tex_image.outputs['Color'], node_emit.inputs['Color'])
links.new(node_emit.outputs['Emission'], node_output.inputs['Surface'])

# Material'i plane'e ata
background.data.materials.append(mat)

# 2025 yazısını oluştur
numbers = "5202"
for idx, num in enumerate(numbers):
    # Background'ın önünde ve biraz yukarıda oluştur
    bpy.ops.object.text_add(location=(idx * 1.3 - 2, -5, 0))
    text = bpy.context.active_object
    text.data.body = num
    text.data.extrude = 0.1
    
    # Pivot noktasını merkeze al
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

    text.scale = (2.2, 2.2, 2.2)
    
    # Kameraya doğru döndür x=90, y=0, z=180
    text.rotation_euler.x = 1.5708
    text.rotation_euler.y = 0
    text.rotation_euler.z = 3.14159
    
    # Mesh'e çevir
    bpy.ops.object.convert(target='MESH')
    
    # Rigidbody ekle ve şeklini box yap
    bpy.ops.rigidbody.object_add()
    text.rigid_body.mass = 0.2
    text.rigid_body.friction = 0.5
    text.rigid_body.collision_shape = 'BOX'
    
    # Z ekseninde dönmeyi engelle
    text.rigid_body.linear_damping = 0.8  # Add some damping for stability
    text.rigid_body.angular_damping = 0.9  # Add angular damping
    
    # Kırmızı material oluştur ve ata
    mat = bpy.data.materials.new(name=f"Red_{num}")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 0, 0, 1)
    text.data.materials.append(mat)


bpy.ops.object.light_add(type='SUN', location=(10, 10, 10))
light = bpy.context.active_object
light.data.energy = 5  # Işık gücünü artır