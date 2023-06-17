import pygame, time
from support import import_folder

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, display_surface):
        super().__init__()
        self.import_character_assests()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.display_surface = display_surface
        
        self.direction = pygame.math.Vector2(0, 0)
        self.gravity = 0.8
        self.health = 500
        self.alives = True
        
        # Status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def import_character_assests(self):
        character_path = './graphics/enemy/'
        self.animations = {'idle': [], 'die': [], 'attack': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
    
    def animate(self):
        animation = self.animations[self.status]        
        
        # loop over frame index    
        if self.alives == False:
            self.frame_index = 3
        else:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(animation):
                self.status = 'idle'
                self.frame_index = 0
            
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        # set the rect
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)
    
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y 
    
    def attack(self, target):
        self.status = 'attack'
        attaking_rect = pygame.Rect(self.rect.centerx - self.rect.width,self.rect.y,self.rect.width, self.rect.height)
        if attaking_rect.colliderect(target.rect):
                target.health -= 10
        # pygame.draw.rect(surface, (0,255,0), attaking_rect)
    
    def update_status(self):
        if self.alives == False:
            self.status = 'die'
    
    def update(self, world_shift):
        self.animate()
        self.rect.x += world_shift

    def draw(self, surface):
        surface.blit(self.image, self.rect)