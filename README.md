if 0 <= x < road_img.get_width() and 0 <= y < road_img.get_height():
        # Cek area 3x3 pixel di sekitar titik untuk memastikan berada di jalan
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                check_x = int(x + dx)
                check_y = int(y + dy)
                if not (0 <= check_x < road_img.get_width() and 
                       0 <= check_y < road_img.get_height() and
                       road_img.get_at((check_x, check_y))[:3] == ROAD_COLOR):
                    return False
        return True
    return False
