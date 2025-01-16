# 2024 BCO602
# Furkan Akgun
# 01.16.2025

import bpy
import random

# Alias for the helper module
tk = bpy.data.texts["bco602tk.py"].as_module()

# Clear existing objects using the helper
tk.delete_all()

def create_plane():
    bpy.ops.mesh.primitive_plane_add(size=25, location=(7, 9, -1.2))

# Küp parametreleri
num_cubes_x = 10  # X ekseninde küp sayısı
num_cubes_y = 10  # Y ekseninde küp sayısı
spacing = 2.0  # Küpler arası mesafe
frames_per_digit = 20  # Her sayı için animasyon süresi (örneğin 20 frame)

# Her bir rakam için küplerin pozisyonları
digit_shapes = {
    0: [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (1, 2), (6, 2), (1, 3), (6, 3), (1, 4), (6, 4), (1, 5), (6, 5), (1, 6), (6, 6), (1, 7), (6, 7), (1, 8), (6, 8), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9)],
    1: [(4, 1), (5, 1), (3, 2), (4, 2), (5, 2), (2, 3), (4, 3), (5, 3), (4, 4), (5, 4), (4, 5), (5, 5), (4, 6), (5, 6), (4, 7), (5, 7), (2, 8), (3, 8), (4, 8), (5, 8), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9)],
    2: [(2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (1, 2), (7, 2), (7, 3), (6, 4), (5, 5), (4, 6), (3, 7), (2, 8), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9)],
    3: [(2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (1, 2), (7, 2), (7, 3), (6, 4), (5, 5), (6, 6), (7, 7), (1, 8), (7, 8), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9)],
    4: [(5, 1), (6, 1), (4, 2), (5, 2), (6, 2), (3, 3), (5, 3), (6, 3), (2, 4), (5, 4), (6, 4), (1, 5), (5, 5), (6, 5), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (5, 7), (6, 7), (5, 8), (6, 8), (5, 9), (6, 9)],
    5: [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (1, 2), (1, 3), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 5), (7, 6), (7, 7), (1, 8), (7, 8), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9)],
    6: [(2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (1, 2), (1, 3), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (1, 5), (6, 5), (1, 6), (6, 6), (1, 7), (6, 7), (1, 8), (6, 8), (2, 9), (3, 9), (4, 9), (5, 9)],
    7: [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 2), (7, 3),(6, 4), (5, 5), (4, 6), (3, 7), (2, 8), (2, 9)],
    8: [(2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (1, 2), (7, 2), (1, 3), (7, 3), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (1, 5), (7, 5), (1, 6), (7, 6), (1, 7), (7, 7), (1, 8), (7, 8), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9)],
    9: [(2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (1, 2), (7, 2), (1, 3), (7, 3), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 5), (7, 6), (7, 7), (1, 8), (7, 8), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9)]
}


def animate_cubes():
    # Tüm küpleri oluştur
    cubes = {}
    for y in range(num_cubes_y):
        for x in range(num_cubes_x):
            bpy.ops.mesh.primitive_cube_add(location=(x * spacing, y * spacing, 0))
            cube = bpy.context.active_object
            cube.name = f"Cube_{x+1}_{y+1}"
            cubes[(x + 1, y + 1)] = cube

    # Rakamları sırasıyla animasyonla göster
    for digit, positions in digit_shapes.items():
        start_frame = (digit) * frames_per_digit + 1  # Her sayı için başlangıç frame'i
        end_frame = start_frame + 10

        for pos, cube in cubes.items():
            # Varsayılan olarak tüm küpleri sıfır pozisyonda bırak
            cube.location.z = 0
            cube.keyframe_insert(data_path="location", frame=start_frame)

            # Eğer küp ilgili sayı için aktifse yukarı kaldır
            if pos in positions:
                cube.location.z =  - 2.0  # Aşşağı pozisyon ( Bu kısım yanlış olmuş harf pozisyonları ters. Kamerayı aşağıdan baktırırsak doğru sonuç gözükecektir.)
            else:
                cube.location.z = 0  # Diğerleri sabit
            cube.keyframe_insert(data_path="location", frame=end_frame)

def main(): 
    # Set animation frame range
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = 200 # 10x20 200 frame animasyon suresi
    create_plane()
    animate_cubes()
    
    
main()
    


