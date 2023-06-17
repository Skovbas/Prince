from csv import reader
import pygame
from os import walk
from settings import tile_size

def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter = ',')    
        for row in level:
            terrain_map.append(list(row))
        return terrain_map
    
def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    size = surface.get_size()
    bigger_img = pygame.transform.scale(surface, (int(size[0]*2), int(size[1]*2)))
    tile_num_x = int(bigger_img.get_size()[0] / tile_size)
    tile_num_y = int(bigger_img.get_size()[1] / tile_size)
    
    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size 
            y = row * tile_size
            new_surface = pygame.Surface((tile_size,tile_size))
            new_surface.blit(surface,(0,0), pygame.Rect(x,y,tile_size,tile_size))
            cut_tiles.append(new_surface)
            
    return cut_tiles

def import_folder(path):
    surface_list = []
    
    for _,_,image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            if 'enemy' in full_path or 'charecter' in full_path:
                size = image_surf.get_size()
                bigger_img = pygame.transform.scale(image_surf, (int(size[0]*1.9), int(size[1]*1.9)))
                surface_list.append(bigger_img)
            else:
                surface_list.append(image_surf)
            
    return surface_list
