import pygame, time
from support import import_csv_layout, import_cut_graphics
from settings import tile_size,  screen_width
from tiles import StaticTile, AnimatedTile
from enemy import Enemy
from character import Prince
from particles import ParticleEffect

class Level:
	def __init__(self,level_data,surface):
		# general setup
		self.display_surface = surface
		self.world_shift = 0
		self.current_x = None
		self.last_call_time = 0

		# player 
		player_layout = import_csv_layout(level_data['player'])
		self.player = pygame.sprite.GroupSingle()
		self.goal = pygame.sprite.GroupSingle()
		self.player_setup(player_layout)
		
		# Create enemies
		enemy_layout = import_csv_layout(level_data['enemy'])
		self.enemy_sprites = self.create_enemy_group(enemy_layout)
  
		# dust
		self.dust_sprite = pygame.sprite.GroupSingle()
		self.player_on_ground = False

		# terrain setup
		terrain_layout = import_csv_layout(level_data['terrain'])
		self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')
  
		# wall 
		wall_layout = import_csv_layout(level_data['wall'])
		self.wall_sprites = self.create_tile_group(wall_layout, 'wall')
  
		# skull 
		skull_layout = import_csv_layout(level_data['skull'])
		self.skull_sprites = self.create_tile_group(skull_layout, 'skull')

		# window 
		window_layout = import_csv_layout(level_data['window'])
		self.window_sprites = self.create_tile_group(window_layout, 'window')
  
		# fire 
		fire_layout = import_csv_layout(level_data['torch'])
		self.fire_sprites = self.create_tile_group(fire_layout, 'torch')
  
		# sound 
		self.finis = pygame.mixer.Sound('./sound/potion.wav')
	
	# Create map and all things on background
	def create_tile_group(self,layout,type):
		sprite_group = pygame.sprite.Group()

		for row_index, row in enumerate(layout):
			for col_index,val in enumerate(row):
				if val != '-1':
					x = col_index * tile_size
					y = row_index * tile_size

					if type == 'terrain':
						terrain_tile_list = import_cut_graphics('./graphics/terrain/wall.png')
						tile_surface = terrain_tile_list[int(val)]
						sprite = StaticTile(tile_size,x,y,tile_surface)
					if type == 'wall':
						wall_tile_list = import_cut_graphics('./graphics/terrain/wall/wall3.png')
						tile_surface = wall_tile_list[int(val)]
						sprite = StaticTile(tile_size, x, y, tile_surface)
					if type == 'skull':
						skull_tile_list = import_cut_graphics('./graphics/terrain/skull/skull.png')
						tile_surface = skull_tile_list[int(val)]
						sprite = StaticTile(tile_size, x, y, tile_surface)
					if type == 'window':
						window_tile_list = import_cut_graphics('./graphics/terrain/window/window.jpeg')
						tile_surface = window_tile_list[int(val)]
						sprite = StaticTile(tile_size, x, y, tile_surface)
					if type == 'torch':
						sprite = AnimatedTile(tile_size, x, y, './graphics/terrain/fire')
     
					sprite_group.add(sprite)
		return sprite_group
	
	# Create enemy 
	def create_enemy_group(self, layout):
		sprite_group = pygame.sprite.Group()

		for row_index, row in enumerate(layout):
			for col_index, val in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size

				if val != '-1':
					enemy = Enemy((x, y), self.display_surface)
					sprite_group.add(enemy)

		return sprite_group
 
	# Create player
	def player_setup(self, layout):
		for row_index, row in enumerate(layout):
			for col_index,val in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size
				if val == '0':
					sprite = Prince((x, y), self.display_surface, self.create_jump_particles)
					self.player.add(sprite)
				if val == '1':
					hat_surface = pygame.image.load('./graphics/terrain/door/door15.png')
					size = hat_surface.get_size()
					bigger_img = pygame.transform.scale(hat_surface, (int(size[0]*2), int(size[1]*2)))
					sprite = StaticTile(tile_size, x, y, bigger_img)
					self.goal.add(sprite)     
      
    # Create jump animation 
	def create_jump_particles(self,pos):
		if self.player.sprite.facing_right:
			pos -= pygame.math.Vector2(0,17)
		else:
			pos += pygame.math.Vector2(0,-17)
		jump_particle_sprite = ParticleEffect(pos,'jump')
		self.dust_sprite.add(jump_particle_sprite)
	
	# Collision
	def horizontal_movement_collision(self):
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed

		for sprite in self.terrain_sprites.sprites  ():
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0: 
					player.rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right

		if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
			player.on_left = False
		if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
			player.on_right = False

	def vertical_movement_collision(self):
		player = self.player.sprite
		player.apply_gravity()

		for sprite in self.terrain_sprites.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.y > 0: 
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True

		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False
		if player.on_ceiling and player.direction.y > 0.1:
			player.on_ceiling = False

	def vertical_enemy_collission(self):
		for enemy in self.enemy_sprites.sprites():
			enemy.apply_gravity()
			
			for sprite in self.terrain_sprites.sprites():
				if sprite.rect.colliderect(enemy.rect):
					if enemy.direction.y > 0:
						enemy.rect.bottom = sprite.rect.top
						enemy.direction.y = 0
					elif enemy.direction.y < 0:
						enemy.rect.top = sprite.rect.bottom
						enemy.direction.y = 0		

	# Map scrolling, camera
	def scroll_player_x(self):
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < screen_width / 4 and direction_x < 0:
			self.world_shift = 8
			player.speed = 0
		elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
			self.world_shift = -8
			player.speed = 0
		else:
			self.world_shift = 0
			player.speed = 8

	def get_player_on_ground(self):
		if self.player.sprite.on_ground:
			self.player_on_ground = True
		else:
			self.player_on_ground = False

	# Create landing dust animation
	def create_landing_dust(self):
		if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
			if self.player.sprite.facing_right:
				offset = pygame.math.Vector2(0,20)
			else:
				offset = pygame.math.Vector2(0,20)
			fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset,'land')
			self.dust_sprite.add(fall_dust_particle)

	# Create a enemy animation
	def enemy_attack(self):
		current_time = time.time()

		if current_time - self.last_call_time < 1:
			return

		self.last_call_time = current_time

		player = self.player.sprite
		for enemy in self.enemy_sprites.sprites():
			if enemy.alives:
				if player.rect.x >= (enemy.rect.centerx - (3 * enemy.rect.width)) and player.rect.x < enemy.rect.centerx:
					enemy.attack(player)
	
	# Check if enemy are still alive
	def check_enemy_health(self):
		for enemy in self.enemy_sprites.sprites():
			if enemy.health <= 0:
				enemy.health = 0
				enemy.alives = False
				enemy.update_status()
    
    # Health
	def draw_health(self,player1,x,y):
		player = player1.sprite
		ration = player.health / 100
		pygame.draw.rect(self.display_surface, (255,255,255),(x-2,y-2, 204, 14))
		pygame.draw.rect(self.display_surface, (139,0,0),(x,y, 200, 10))
		pygame.draw.rect(self.display_surface, (255,0,0),(x,y, 200 * ration, 10))
    
    # Check if character is still alive
	def menu_call(self,menu_reboot):
		charecter = self.player.sprite
		if charecter.health <= 0:
			menu_reboot()
	
	def finish(self, menu_reboot):
		player = self.player.sprite
		finish = self.goal.sprite
		
		if player.rect.colliderect(finish.rect):
			self.finis.play()
			time.sleep(2)
			menu_reboot()
    
	def run(self):
		# run the entire game / level
		# terrain 
		self.terrain_sprites.update(self.world_shift)
		self.terrain_sprites.draw(self.display_surface)

		# wall
		self.wall_sprites.update(self.world_shift)
		self.wall_sprites.draw(self.display_surface)

		# skull
		self.skull_sprites.update(self.world_shift)
		self.skull_sprites.draw(self.display_surface)

		# window
		self.window_sprites.update(self.world_shift)
		self.window_sprites.draw(self.display_surface)

		# torch
		self.fire_sprites.update(self.world_shift)
		self.fire_sprites.draw(self.display_surface)
  
		# dust
		self.dust_sprite.update(self.world_shift)
		self.dust_sprite.draw(self.display_surface) 

		# enemy
		self.enemy_sprites.update(self.world_shift)
		self.enemy_sprites.draw(self.display_surface)
		self.enemy_attack()
		self.check_enemy_health()
  
		# player spot
		self.player.update(self.enemy_sprites)
		self.horizontal_movement_collision()
		self.draw_health(self.player, 20, 20)
  
		self.get_player_on_ground()
		self.vertical_movement_collision()
		self.vertical_enemy_collission()
		self.create_landing_dust()

		self.scroll_player_x()
		self.player.draw(self.display_surface)
		self.goal.update(self.world_shift)
		self.goal.draw(self.display_surface)
