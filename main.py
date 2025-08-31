
# Hey i see what you saw in the code 
#support by adding star to the repo dont be a silent reader
#this project is done using the pygame library and also greeting to  Tim aka Tech with tim 


print(r"""
                                                                                                            
                                                                                                            
       __   .__  .__                  __                
 __ __|  | _|__| |  |__  __ __  _____/  |_  ___________ 
|  |  \  |/ /  | |  |  \|  |  \/    \   __\/ __ \_  __ \
|  |  /    <|  | |   Y  \  |  /   |  \  | \  ___/|  | \/
|____/|__|_ \__| |___|  /____/|___|  /__|  \___  >__|   
           \/         \/           \/          \/       
                                                       
""")

import os 
import random
import math
import pygame
from os import listdir
from os.path import isfile,join


pygame.init()
#pygame joystick init
pygame.joystick.init()
#set the title of the window
pygame.display.set_caption("game by uki")


pygame.mixer.init()
# Music will be initialized after menu selection


jump_sound = pygame.mixer.Sound(join("assets", "Music", "jump.mp3"))  # Or use "Sounds" folder





#BG_COLOR = (255,255,255)


# Move joystick detection to global scope
joystick = None

# Joystick detection function
def detect_joystick():
    global joystick
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        #debugging print statement
      #  print(f"Controller detected: {joystick.get_name()}")
    else:
        joystick = None
        print("No controller detected")
#also call this as a global function
detect_joystick()

#screen dimensions
WIDTH,HEIGHT = 1700 ,1000

#frames per second - optimized for performance
FPS = 60
#player velocity
PLAYER_VEL = 10

#create the window
#window = pygame.display.set_mode((WIDTH,HEIGHT))


window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.DOUBLEBUF | pygame.HWSURFACE)

#menu button class
class ElegantMenuButton:
    def __init__(self, text, x, y, font_size=48, color=(200, 200, 255), hover_color=(255, 215, 0)):
        self.text = text
        self.font_size = font_size
        self.font = pygame.font.Font(None, font_size)
        self.color = color
        self.hover_color = hover_color
        self.hover = False
        self.scale = 1.0
        self.target_scale = 1.0
        self.pulse_timer = 0
        self.glow_alpha = 0
        self.target_glow = 0
        
        # Create button surface
        self.text_surface = self.font.render(text, True, color)
        self.rect = self.text_surface.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.original_center = (x, y)
        
        # Decorative elements
        self.ornament_timer = 0

    def update(self):
        # Smooth scaling animation
        scale_speed = 0.15
        self.scale += (self.target_scale - self.scale) * scale_speed
        
        # Glow effect
        glow_speed = 0.1
        self.glow_alpha += (self.target_glow - self.glow_alpha) * glow_speed
        
        # Pulse animation for ornaments
        self.pulse_timer += 0.08
        self.ornament_timer += 0.05
        
        if self.hover:
            self.target_scale = 1.15
            self.target_glow = 120
        else:
            self.target_scale = 1.0
            self.target_glow = 0

    def draw_ornaments(self, surface, x, y, text_width):
        
        ornament_color = (200, 200, 200, int(self.glow_alpha))
        
        # Left ornament
        left_x = x - text_width // 2 - 40
        pygame.draw.circle(surface, (150, 150, 150), (left_x, y), 3)
        pygame.draw.circle(surface, (100, 100, 100), (left_x - 15, y), 2)
        pygame.draw.circle(surface, (100, 100, 100), (left_x + 15, y), 2)
        
        # Right ornament
        right_x = x + text_width // 2 + 40
        pygame.draw.circle(surface, (150, 150, 150), (right_x, y), 3)
        pygame.draw.circle(surface, (100, 100, 100), (right_x - 15, y), 2)
        pygame.draw.circle(surface, (100, 100, 100), (right_x + 15, y), 2)
        
        # Animated sparkles when hovered
        if self.hover:
            sparkle_offset = math.sin(self.ornament_timer * 2) * 5
            pygame.draw.circle(surface, (255, 255, 200), #color
                             (int(left_x + sparkle_offset), int(y - 10)), 1)
            pygame.draw.circle(surface, (255, 255, 200), 
                             (int(right_x - sparkle_offset), int(y + 10)), 1)

    def draw(self, surface):
   
        self.update()
        
        # Choose color based on hover state
        current_color = self.hover_color if self.hover else self.color
        
        # Create text surface
        text_surface = self.font.render(self.text, True, current_color)
        
        # Apply scaling
        if self.scale != 1.0:
            scaled_width = int(text_surface.get_width() * self.scale)
            scaled_height = int(text_surface.get_height() * self.scale)
            text_surface = pygame.transform.scale(text_surface, (scaled_width, scaled_height))
        
        #  glow effect with improved transparency
        if self.glow_alpha > 0:
            glow_surface = pygame.Surface((text_surface.get_width() + 20, text_surface.get_height() + 20), pygame.SRCALPHA)
            glow_color = (*current_color[:3], int(self.glow_alpha // 3))
            pygame.draw.rect(glow_surface, glow_color, glow_surface.get_rect(), border_radius=10)
            glow_rect = glow_surface.get_rect()
            glow_rect.center = self.original_center
            surface.blit(glow_surface, glow_rect)
        
        # Center the scaled surface
        text_rect = text_surface.get_rect()
        text_rect.center = self.original_center
        surface.blit(text_surface, text_rect)
        
        # Draw ornaments
        self.draw_ornaments(surface, self.original_center[0], self.original_center[1], text_surface.get_width())

    def is_clicked(self, pos):
        """button click  chackpoint """
        return self.rect.collidepoint(pos)

    def update_hover(self, pos):
        """Update hover state based on mouse position"""
        self.hover = self.rect.collidepoint(pos)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def update_hover(self, pos):
        self.hover = self.rect.collidepoint(pos)

# main menu button class
class ElegantMenu:
    def __init__(self, window):
        self.window = window
        self.clock = pygame.time.Clock()
        self.logo_bounce = 0
        self.logo_bounce_speed = 0.03
        self.background_alpha = 0
        self.target_alpha = 180
        self.particle_timer = 0
        self.particles = []
        
        # Create dark atmospheric background
        self.create_background()
        
        # Load and create elegant title
        self.create_title()
        
        # Create elegant menu buttons
        self.create_buttons()
        
        # Initialize particles for atmosphere
        self.init_particles()
        
        # Improved audio management
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(join("assets", "Music", "background.mp3"))
            pygame.mixer.music.set_volume(0.4) #voulume controle 
            pygame.mixer.music.play(-1)
        except pygame.error:
            print("Could not load background music")
    
    def create_background(self):

        self.background_surface = pygame.Surface((WIDTH, HEIGHT))
 
        start_color = (0, 10, 15)  #top 
        end_color = (35, 35, 40)      #botom
        
    
        for y in range(HEIGHT):
            
            ratio = y / HEIGHT
            r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
            
            color = (r, g, b)
            pygame.draw.line(self.background_surface, color, (0, y), (WIDTH, y))
        
        # sub text
        for i in range(200):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            brightness = random.randint(40, 60)
            pygame.draw.circle(self.background_surface, (brightness, brightness, brightness), (x, y), 1)
    def create_title(self):
      
        # Main title font (larger)
        title_font = pygame.font.Font(None, 120)
        self.title_text = "PLATFORMER KNIGHT"
        self.title_surface = title_font.render(self.title_text, True, (255, 255, 255))
        
        # Subtitle
        subtitle_font = pygame.font.Font(None, 40)
        self.subtitle_text = "A Journey Through Shadows"
        self.subtitle_surface = subtitle_font.render(self.subtitle_text, True, (180, 180, 180))
        
        # Position title elements
        self.title_rect = self.title_surface.get_rect()
        self.title_rect.centerx = WIDTH // 2
        self.title_rect.y = 300
        
        self.subtitle_rect = self.subtitle_surface.get_rect()
        self.subtitle_rect.centerx = WIDTH // 2
        self.subtitle_rect.y = self.title_rect.bottom + 20
    
    def create_buttons(self):
      #button set 
        button_y_start = HEIGHT // 2 + 100
        button_spacing = 80
        
        self.start_button = ElegantMenuButton(" START GAME ", WIDTH // 2, button_y_start)
        self.options_button = ElegantMenuButton("OPTIONS", WIDTH // 2, button_y_start + button_spacing)
        self.quit_button = ElegantMenuButton("QUIT GAME", WIDTH // 2, button_y_start + button_spacing * 2)
        
        self.buttons = [self.start_button, self.options_button, self.quit_button]
    
    def init_particles(self):
     
        self.particles = []
        for _ in range(30):
            particle = {
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'speed': random.uniform(0.2, 0.8),
                'size': random.randint(10, 80),  
                'alpha': random.randint(20, 80),
                'direction': random.uniform(-0.5, 0.5)
            }
            self.particles.append(particle)
    
    def update_particles(self):
        """Update floating particles"""
        for particle in self.particles:
            particle['y'] -= particle['speed']
            particle['x'] += particle['direction']
            
            # Reset particle if it goes off screen
            if particle['y'] < -10:
                particle['y'] = HEIGHT + 10
                particle['x'] = random.randint(0, WIDTH)
            
            if particle['x'] < -10 or particle['x'] > WIDTH + 10:
                particle['x'] = random.randint(0, WIDTH)
    
    def draw_particles(self):
        
        for particle in self.particles:
            
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            color = (80, 80, 120, particle['alpha'])
            pygame.draw.circle(particle_surface, color, 
                             (particle['size'], particle['size']), particle['size'])
            self.window.blit(particle_surface, 
                           (int(particle['x'] - particle['size']), int(particle['y'] - particle['size'])))
    
    
    def draw_title_ornaments(self):
      
        title_center_x = self.title_rect.centerx
        title_y = self.title_rect.centery
        
       
        line_color = (150, 150, 150)
        
        # Left ornament
        left_start = title_center_x - self.title_surface.get_width() // 2 - 100
        left_end = title_center_x - self.title_surface.get_width() // 2 - 20
        pygame.draw.line(self.window, line_color, (left_start, title_y), (left_end, title_y), 2)
        
        # Right ornament  
        right_start = title_center_x + self.title_surface.get_width() // 2 + 20
        right_end = title_center_x + self.title_surface.get_width() // 2 + 100
        pygame.draw.line(self.window, line_color, (right_start, title_y), (right_end, title_y), 2)
        
        # Decorative diamonds
        diamond_size = 8
        pygame.draw.polygon(self.window, line_color, [
            (left_start - 10, title_y),
            (left_start - 10 - diamond_size, title_y - diamond_size),
            (left_start - 10, title_y - diamond_size * 2),
            (left_start - 10 + diamond_size, title_y - diamond_size)
        ])
        
        pygame.draw.polygon(self.window, line_color, [
            (right_end + 10, title_y),
            (right_end + 10 + diamond_size, title_y - diamond_size),
            (right_end + 10, title_y - diamond_size * 2),
            (right_end + 10 - diamond_size, title_y - diamond_size)
        ])
    
    def run(self):
     # loop menu 
        running = True
        
        while running:
            self.clock.tick(FPS)
            mouse_pos = pygame.mouse.get_pos()
            
            # Update animations
            self.logo_bounce += self.logo_bounce_speed
            self.particle_timer += 1
            
            # Fade in effect
            if self.background_alpha < self.target_alpha:
                self.background_alpha += 2
            
            # Update particles
            if self.particle_timer % 3 == 0:  
                self.update_particles()
            
            # Update button hover states
            for button in self.buttons:
                button.update_hover(mouse_pos)
            
            # Event handling
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return "quit"
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.start_button.is_clicked(mouse_pos):
                        pygame.mixer.music.fadeout(1000)
                        return "start"
                    elif self.quit_button.is_clicked(mouse_pos):
                        return "quit"
                    elif self.options_button.is_clicked(mouse_pos):
                       
                        pass
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        pygame.mixer.music.fadeout(1000)
                        return "start"
                    elif event.key == pygame.K_ESCAPE:
                        return "quit"
                
                # Controller support
                if joystick and event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0:  # A button
                        pygame.mixer.music.fadeout(1000)
                        return "start"
                    elif event.button == 1:  # B button
                        return "quit"
            
          
            self.draw()
            pygame.display.flip()
        
        return "quit"
    
    def draw(self):
        
        self.window.blit(self.background_surface, (0, 0))
        
        # Draw atmospheric particles
        self.draw_particles()
        
        # Border removed as requested
        # self.draw_ornate_border()
        
        # Draw animated title with bounce effect
        title_offset = int(math.sin(self.logo_bounce) * 3)
        title_pos = (self.title_rect.x, self.title_rect.y + title_offset)
        
        # Title glow effect with improved rendering
        glow_surface = pygame.Surface((self.title_surface.get_width() + 10, self.title_surface.get_height() + 10), pygame.SRCALPHA)
        glow_surface.fill((255, 255, 255, 30))
        glow_rect = glow_surface.get_rect()
        glow_rect.center = (self.title_rect.centerx, self.title_rect.centery + title_offset)
        self.window.blit(glow_surface, glow_rect)
        
        self.window.blit(self.title_surface, title_pos)
        
        # Draw title ornaments
        self.draw_title_ornaments()
        
        # Draw subtitle
        self.window.blit(self.subtitle_surface, self.subtitle_rect)
        
        # Draw elegant buttons
        for button in self.buttons:
            button.draw(self.window)
        
        # Draw version info
        font = pygame.font.Font(None, 28)
        version_text = font.render("v1.0 - made by uki", True, (100, 100, 100))
        version_rect = version_text.get_rect()
        version_rect.bottomleft = (20, HEIGHT - 20)
        self.window.blit(version_text, version_rect)
        
        # Controller info
        if joystick:
            controller_text = font.render("Controller Supported", True, (100, 100, 100))
            controller_rect = controller_text.get_rect()
            controller_rect.bottomright = (WIDTH - 20, HEIGHT - 20)
            self.window.blit(controller_text, controller_rect)

#load assets
def flip (sprites):
      return [pygame.transform.flip(sprite,True,False) for sprite in sprites]
#load sprite sheets
def load_sprite_sheets(dir1,dir2,width,height,direaction=False):
      path = join ("assets" ,dir1 ,dir2)
      images = [f for f in listdir(path) if isfile (join(path,f))]


      all_sprites = {}

      for image in images:
            sprite_sheet = pygame.image.load(join(path,image)).convert_alpha()

            sprite = []
            for i in range (sprite_sheet.get_width() // width):
                  surface = pygame.Surface((width,height) ,pygame.SRCALPHA,32)
                  rect = pygame.Rect(i * width ,0 , width , height)
                  surface.blit (sprite_sheet, (0,0 ),rect)
                  sprite.append (pygame.transform.scale2x(surface))

            if direaction:
                    all_sprites[image.replace(".png","") + "_right"] = sprite
                    all_sprites[image.replace(".png","") + "_left"] = flip(sprite)
            else:
                all_sprites[image.replace(".png","")] = sprite
      return all_sprites








#get the platform block 
def get_block(size):
      path = join("assets" , "Terrain" , "Terrain.png")
      image = pygame.image.load (path).convert_alpha()
      surface = pygame.Surface((size,size),pygame.SRCALPHA,32)
      rect = pygame.Rect(96,128,size,size)
      surface.blit(image,(0,0) ,rect)
      return pygame.transform.scale2x(surface)


# get the player character +
class Player(pygame.sprite.Sprite):
      COLOR = (255,0,0)
      GRAVITY = 1
      SPRITES = load_sprite_sheets("MainCharacters" , "PinkMan" ,32,32,True)
      ANIMATION_DELAY = 8


#player initialization
      def __init__(self, x,y,width ,heigt):
            super().__init__()
            self.rect= pygame.Rect(x,y,width,heigt)
            self.x_pos = float(x)  
            self.y_pos = float(y)  
            self.x_vel=0
            self.y_vel=0
            self.mask = None
            self.direction = "left"
            self.animation_count = 0 
            self.fall_count =0
            self.jump_count =0
            self.hit=False
            self.hit_count = 0
            
            # Health system
            self.max_health = 5
            self.current_health = self.max_health
            self.invulnerable = False
            self.invulnerable_timer = 0
            self.last_damage_time = 0

      #jumping player
      def jump(self):
            #how much higher the player can jump change the numaric value 
            self.y_vel = -self.GRAVITY * 6
            self.animation_count = 0
            self.jump_count +=1
            if self.jump_count == 1:
                  self.fall_count =0
            jump_sound.play() 

      def move(self,dx,dy):
            self.x_pos += dx
            self.y_pos += dy
            self.rect.x = int(self.x_pos)  
            self.rect.y = int(self.y_pos)


      def make_hit(self):
            # Only take damage if not invulnerable
            if not self.invulnerable and self.current_health > 0:
                self.hit = True
                self.hit_count = 0
                self.current_health -= 1
                self.invulnerable = True
                self.invulnerable_timer = 120  # 2 seconds of invincibility at 60 FPS
                
                # Flash effect when hit
                if self.current_health <= 0:
                    print("Game Over!")  

      def move_left(self,vel):
            self.x_vel = -vel
            if self.direction != "left":
                  self.direction = "left"
                  self.animation_count = 0
      def move_right(self,vel):
            self.x_vel = vel
            if self.direction != "right":
                  self.direction = "right"
                  self.animation_count = 0
      def loop(self,fps) :
            #player gravity 
            self.y_vel += min (1,(self.fall_count /fps) * self.GRAVITY)
            self.move(self.x_vel,self.y_vel)
            
            # Update invulnerability timer
            if self.invulnerable:
                self.invulnerable_timer -= 1
                if self.invulnerable_timer <= 0:
                    self.invulnerable = False
            
            if self.hit:
             self.hit_count += 1
            if self.hit_count > fps * 2:  # Hit effect lasts for 2 seconds
                self.hit = False
                self.hit_count = 0


            self.fall_count += 1
            self.update_sprite()

      def landed(self):
            self.fall_count = 0
            self.y_vel = 0
            self.jump_count = 0
      def hit_head(self):
            self.count =0
            self.y_vel *= -1

# player position update
      def update_sprite(self):
            sprite_sheet = "idle"
            if self.hit:
                  sprite_sheet = "hit"
            if self.y_vel < 0:
                  if self.jump_count == 1:
                        sprite_sheet = "jump"
                  elif self.jump_count > 1:
                        sprite_sheet = "double_jump"
            elif self.y_vel > self.GRAVITY * 2:
                  sprite_sheet = "fall"
            elif self.x_vel != 0:
                  sprite_sheet = "run"

           # if self.x_vel != 0:
              #    sprite_sheet = "run"
            sprite_sheet_name = sprite_sheet + "_" +self.direction
            sprites = self.SPRITES[sprite_sheet_name]
            
            # Smoother animation timing
            sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
            self.sprite =sprites[sprite_index]
            self.animation_count +=1 
            
            # Reset animation count to prevent overgoing
            if self.animation_count >= self.ANIMATION_DELAY * len(sprites) * 10:
                self.animation_count = 0 
            self.update()
      
      def update(self):
            self.rect= self.sprite.get_rect(topleft=(self.rect.x,self.rect.y))
            self.mask = pygame.mask.from_surface(self.sprite)

      def draw(self,win,offset_x) :
           # self.sprite = self.SPRITES["idle_" + self.direction][0]
            # Flash effect when invulnerable
            if self.invulnerable and (self.invulnerable_timer // 5) % 2:
                # Make player flash by not drawing every few frames
                return
            win.blit(self.sprite,(self.rect.x - offset_x,self.rect.y))
      
      def reset_health(self):
            """Reset player health to maximum"""
            self.current_health = self.max_health
            self.invulnerable = False
            self.invulnerable_timer = 0 


#background tiles getting here
def get_background(name):
       image = pygame.image.load(join("assets","Background", name))
       _,_, width ,height = image.get_rect()
       tiles=[]
       
      
      

       for i in range (WIDTH // width + 1):
          for j in range (HEIGHT // height + 1):
                pos =  [i * width,j * height]
                tiles.append(pos)
        
       return tiles ,image



# Health bar drawing function
def draw_health_bar(window, player):
   
    # Health bar position and dimensions
    bar_x = 20
    bar_y = 20
    bar_width = 200
    bar_height = 25
    border_width = 3
    
    # Colors
    bg_color = (60, 60, 60)  # Dark gray background
    border_color = (255, 255, 255)  # White border
    health_color = (220, 50, 50)  # Red health
    lost_health_color = (100, 30, 30)  # Darker red for lost health
    
    # Draw border
    pygame.draw.rect(window, border_color, 
                    (bar_x - border_width, bar_y - border_width, 
                     bar_width + border_width * 2, bar_height + border_width * 2))
    
    # Draw background
    pygame.draw.rect(window, bg_color, (bar_x, bar_y, bar_width, bar_height))
    
    # Calculate health bar fill
    health_percentage = player.current_health / player.max_health
    current_bar_width = int(bar_width * health_percentage)
    
    # Draw lost health (darker red)
    pygame.draw.rect(window, lost_health_color, (bar_x, bar_y, bar_width, bar_height))
    
    # Draw current health
    if current_bar_width > 0:
        pygame.draw.rect(window, health_color, (bar_x, bar_y, current_bar_width, bar_height))
    
    # Draw health text
    font = pygame.font.Font(None, 36)
    health_text = f"Health: {player.current_health}/{player.max_health}"
    text_surface = font.render(health_text, True, (255, 255, 255))
    window.blit(text_surface, (bar_x, bar_y + bar_height + 10))
    
    # Draw hearts for visual appeal
    heart_size = 20
    heart_spacing = 25
    hearts_x = bar_x + bar_width + 20
    hearts_y = bar_y + 2
    
    for i in range(player.max_health):
        heart_color = health_color if i < player.current_health else lost_health_color
        # Simple heart shape using circles
        pygame.draw.circle(window, heart_color, (hearts_x + i * heart_spacing, hearts_y + 8), 6)
        pygame.draw.circle(window, heart_color, (hearts_x + i * heart_spacing + 8, hearts_y + 8), 6)
        # Heart bottom point
        points = [
            (hearts_x + i * heart_spacing - 6, hearts_y + 8),
            (hearts_x + i * heart_spacing + 14, hearts_y + 8),
            (hearts_x + i * heart_spacing + 4, hearts_y + 18)
        ]
        pygame.draw.polygon(window, heart_color, points)


def draw(window, background, bg_image, player, objects, offset_x):
    # Clear screen efficiently
    window.fill((0, 0, 0))
    
    # Draw background tiles
    for tile in background:
        window.blit(bg_image, tile)
    
    # Optimized object drawing - only draw visible objects
    screen_rect = pygame.Rect(offset_x, 0, WIDTH, HEIGHT)
    
    for obj in objects:
        # Only draw objects that are on screen
        if obj.rect.colliderect(screen_rect):
            obj.draw(window, offset_x)
    
    player.draw(window, offset_x)
    
   
    draw_health_bar(window, player)
    

       
class Object(pygame.sprite.Sprite):
      def __init__(self,x,y,width,height,name=None):
            super().__init__()
            self.rect = pygame.Rect(x, y, width, height)
            self.image = pygame.Surface((width,height) , pygame.SRCALPHA)
            self.width = width
            self.height = height
            self.name = name

      def draw (self,win,offset_x):
            win.blit(self.image, (self.rect.x-offset_x,self.rect.y))


class Block(Object):
      def __init__ (self,x,y,size):
            super().__init__(x,y,size,size)
            block = get_block(size)
            self.image.blit(block,(0,0))
            self.mask= pygame.mask.from_surface(self.image)



class Fire(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "on"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


class Saw(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "saw")
        self.saw = load_sprite_sheets("Traps", "Saw", width, height)
        self.image = self.saw["on"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0

    def loop(self):
        sprites = self.saw["on"]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


class Spikes(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "spikes")
        spike_img = pygame.image.load(join("assets", "Traps", "Spikes", "Idle.png")).convert_alpha()
        self.image = pygame.transform.scale2x(spike_img)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(x, y))


class FallingPlatform(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "falling_platform")
        platform_img = pygame.image.load(join("assets", "Traps", "Falling Platforms", "Off.png")).convert_alpha()
        self.image = pygame.transform.scale2x(platform_img)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.fall_timer = 0
        self.falling = False
        self.fall_speed = 0
        self.original_y = y
        self.triggered = False

    def trigger_fall(self):
        if not self.triggered:
            self.triggered = True
            self.fall_timer = 30  # Delay before falling

    def update(self):
        if self.triggered and not self.falling:
            self.fall_timer -= 1
            if self.fall_timer <= 0:
                self.falling = True
        
        if self.falling:
            self.fall_speed += 0.5
            self.rect.y += self.fall_speed
            self.y_pos = float(self.rect.y)


class EndFlag(Object):
    ANIMATION_DELAY = 8

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "end_flag")
        # Load end flag images directly
        idle_img = pygame.image.load(join("assets", "Items", "Checkpoints", "End", "End (Idle).png")).convert_alpha()
        pressed_img = pygame.image.load(join("assets", "Items", "Checkpoints", "End", "End (Pressed) (64x64).png")).convert_alpha()
        
        self.idle_image = pygame.transform.scale2x(idle_img)
        self.pressed_image = pygame.transform.scale2x(pressed_img)
        self.image = self.idle_image
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.activated = False

    def activate(self):
        if not self.activated:
            self.activated = True
            self.image = self.pressed_image
            self.mask = pygame.mask.from_surface(self.image)

    def loop(self):
        
        if not self.activated:
            self.image = self.idle_image
        else:
            self.image = self.pressed_image



def handle_vertical_collision(player, objects, dy):
    collided_objects = []

    player_region = pygame.Rect(player.rect.x - 50, player.rect.y - 50, 
                               player.rect.width + 100, player.rect.height + 100)
    
    for obj in objects:
   
        if not player_region.colliderect(obj.rect):
            continue
            
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.y_pos = float(player.rect.y)
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.y_pos = float(player.rect.y)
                player.hit_head()
            collided_objects.append(obj)
    return collided_objects

def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collide_object = None
    
    
    player_region = pygame.Rect(player.rect.x - 50, player.rect.y - 50, 
                               player.rect.width + 100, player.rect.height + 100)
    
    for obj in objects:
        if not player_region.colliderect(obj.rect):
            continue
        if pygame.sprite.collide_mask(player, obj):
            collide_object = obj
            break
    player.move(-dx, 0)
    player.update()
    return collide_object

def handle_move(player, objects):
      keys = pygame.key.get_pressed()
      player.x_vel=0
      collide_left = collide(player, objects, -PLAYER_VEL *2)
      collide_right = collide(player, objects, PLAYER_VEL *2)
      if keys[pygame.K_LEFT]and not collide_left:
            player.move_left(PLAYER_VEL)
      if keys[pygame.K_RIGHT] and not collide_right:
            player.move_right(PLAYER_VEL)
      
      # Controller controls (if connected)
      if joystick:
        # Left analog stick or D-pad
        axis_x = joystick.get_axis(0)  # Left stick horizontal
        
        # D-pad (hat)
        hat = joystick.get_hat(0)
        
        # Move left/right based on analog stick or D-pad
        if (axis_x < -0.5 or hat[0] == -1) and not collide_left:
            player.move_left(PLAYER_VEL)
        elif (axis_x > 0.5 or hat[0] == 1) and not collide_right:
            player.move_right(PLAYER_VEL)
      vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
      to_check = [collide_left, collide_right, *vertical_collide]

      for obj in to_check:
        if obj and obj.name in ["fire", "saw", "spikes"]:
            player.make_hit()
        elif obj and obj.name == "falling_platform":
            obj.trigger_fall()
        elif obj and obj.name == "end_flag":
            obj.activate()
            return True  
      
      return False  
     

class Platform(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        path = join("assets", "Terrain", "Terrain.png")
        image = pygame.image.load(path).convert_alpha()
        surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
        rect = pygame.Rect(96, 65, size, size) 
        surface.blit(image, (0, 0), rect)
        platform_img = pygame.transform.scale2x(surface)
        self.image.blit(platform_img, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

def main_game(window):
    # Optimized audio management
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(join("assets", "Music", "background.mp3"))
        pygame.mixer.music.set_volume(0.6)  # Lower volume for better performance
        pygame.mixer.music.play(-1)
    except pygame.error:
        print("Could not load game music")
    
    clock = pygame.time.Clock()
    background, bg_image = get_background("Brown.png")

    block_size = 96

    # Player starts at the beginning of the level
    player = Player(100, 100, 50, 50)
    
  
    floor = [Block(i*block_size, HEIGHT - block_size, block_size) for i in range(-WIDTH // block_size, (WIDTH * 4) // block_size)]

    platforms = [
        Platform(0, HEIGHT - block_size * 2, block_size),
        Platform(block_size * 2, HEIGHT - block_size * 3, block_size),
        Platform(block_size * 4, HEIGHT - block_size * 2, block_size),
        Platform(block_size * 7, HEIGHT - block_size * 4, block_size),
        Platform(block_size * 9, HEIGHT - block_size * 5, block_size),
        Platform(block_size * 11, HEIGHT - block_size * 3, block_size),
        Platform(block_size * 13, HEIGHT - block_size * 6, block_size),
        Platform(block_size * 16, HEIGHT - block_size * 4, block_size),
        Platform(block_size * 18, HEIGHT - block_size * 4, block_size),
        Platform(block_size * 20, HEIGHT - block_size * 5, block_size),
        Platform(block_size * 22, HEIGHT - block_size * 3, block_size),
        Platform(block_size * 25, HEIGHT - block_size * 4, block_size),
        Platform(block_size * 27, HEIGHT - block_size * 2, block_size),
    ]
    
    fires = [
        Fire(block_size * 3, HEIGHT - block_size - 64, 16, 32),
        Fire(block_size * 6, HEIGHT - block_size - 64, 16, 32),
        Fire(block_size * 10, HEIGHT - block_size - 64, 16, 32),
        Fire(block_size * 14, HEIGHT - block_size - 64, 16, 32),
        Fire(block_size * 17, HEIGHT - block_size - 64, 16, 32),
        Fire(block_size * 21, HEIGHT - block_size - 64, 16, 32),
        Fire(block_size * 24, HEIGHT - block_size - 64, 16, 32),
    ]
    
    saws = [
        Saw(block_size * 8, HEIGHT - block_size * 5 - 32, 38, 38),
        Saw(block_size * 12, HEIGHT - block_size * 4 - 32, 38, 38),
        Saw(block_size * 19, HEIGHT - block_size * 5 - 32, 38, 38),
        Saw(block_size * 26, HEIGHT - block_size * 3 - 32, 38, 38),
    ]
    
    spikes = [
        Spikes(block_size * 5, HEIGHT - block_size - 32, 32, 32),
        Spikes(block_size * 15, HEIGHT - block_size - 32, 32, 32),
        Spikes(block_size * 23, HEIGHT - block_size - 32, 32, 32),
    ]
    
    falling_platforms = [
        FallingPlatform(block_size * 8, HEIGHT - block_size * 4, 64, 16),
        FallingPlatform(block_size * 19, HEIGHT - block_size * 6, 64, 16),
    ]
    
    end_flag = EndFlag(block_size * 28, HEIGHT - block_size * 3 - 64, 64, 64)

    # Combine all objects
    objects = [*floor, *platforms, *fires, *saws, *spikes, *falling_platforms, end_flag]

    offset_x = 0
    scroll_area_width = 200
    joystick_check_timer = 0
    level_completed = False
    game_over = False
    game_over_timer = 0
    
    # Transition effect variables
    transition_alpha = 0
    transition_surface = pygame.Surface((WIDTH, HEIGHT))
    transition_surface.fill((0, 0, 0))
    
    run = True
    while run:
        clock.tick(FPS)
        
       
        joystick_check_timer += 1
        if joystick_check_timer >= 300:  # Check every 5 seconds 
            detect_joystick()
            joystick_check_timer = 0
        
        # Batch event processing
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
                break
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()
                elif event.key == pygame.K_r:
                    # Quick reset
                    player.rect.x = 100
                    player.rect.y = 100
                    player.x_pos = 100.0
                    player.y_pos = 100.0
                    player.x_vel = 0
                    player.y_vel = 0
                    player.hit = False
                    player.hit_count = 0
                    player.reset_health()  
                    offset_x = 0
                    level_completed = False
                    game_over = False
                    game_over_timer = 0
                    transition_alpha = 0
                    # Reset falling platforms
                    for fp in falling_platforms:
                        fp.rect.y = fp.original_y
                        fp.y_pos = float(fp.original_y)
                        fp.falling = False
                        fp.triggered = False
                        fp.fall_timer = 0
                        fp.fall_speed = 0
                    end_flag.activated = False

            if event.type == pygame.JOYBUTTONDOWN:
                if joystick and event.button == 0 and player.jump_count < 2:
                    player.jump()
        
        if not level_completed and not game_over:
            # Normal gameplay fps
            player.loop(FPS)
            
            # Update only necessary animated objects
            screen_rect = pygame.Rect(offset_x, 0, WIDTH, HEIGHT)
            for fire in fires:
                if fire.rect.colliderect(screen_rect):
                    fire.loop()
            for saw in saws:
                if saw.rect.colliderect(screen_rect):
                    saw.loop()
            for fp in falling_platforms:
                fp.update()
            end_flag.loop()
            
            # Handle movement and check for level completion
            level_completed = handle_move(player, objects)
            
            # Check for game over (health = 0)
            if player.current_health <= 0:
                game_over = True
                game_over_timer = 180  # 3 seconds game over display
                pygame.mixer.music.fadeout(1000)  # Fade out music
            
            if level_completed:
                # Start victory sequence
                pygame.mixer.music.fadeout(1000)  
                
        elif game_over:
            # Game over state - countdown timer
            game_over_timer -= 1
            if game_over_timer <= 0:
                # Return to menu after game over timer
                return
                
        elif level_completed:
            # Level completed 
            transition_alpha += 8  
            if transition_alpha >= 255:
               
                return
        
   
        draw(window, background, bg_image, player, objects, offset_x)
        
       #game wind and over
        if level_completed:
           
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))  
            window.blit(overlay, (0, 0))
            
            # Victory message
            font_large = pygame.font.Font(None, 100)
            font_medium = pygame.font.Font(None, 50)
            
            victory_text = font_large.render("LEVEL COMPLETED!", True, (255, 215, 0))  #game over
            victory_rect = victory_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 60))
            window.blit(victory_text, victory_rect)
            
            # Subtitle text
            subtitle_text = font_medium.render("Well done, Knight!", True, (255, 255, 255))
            subtitle_rect = subtitle_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            window.blit(subtitle_text, subtitle_rect)
            
            # Return to menu text
            menu_text = font_medium.render("Returning to menu...", True, (200, 200, 200))
            menu_rect = menu_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 60))
            window.blit(menu_text, menu_rect)
            
          
            if transition_alpha > 0:
                transition_surface.set_alpha(min(255, transition_alpha))
                window.blit(transition_surface, (0, 0))
                
        elif game_over:
           
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180)) 
            window.blit(overlay, (0, 0))
            
            # Game over text
            font_large = pygame.font.Font(None, 100)
            font_medium = pygame.font.Font(None, 50)
            
            game_over_text = font_large.render("GAME OVER", True, (220, 50, 50))
            game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 60))
            window.blit(game_over_text, game_over_rect)
            
            # Subtitle text
            subtitle_text = font_medium.render("All health depleted!", True, (255, 255, 255))
            subtitle_rect = subtitle_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            window.blit(subtitle_text, subtitle_rect)
            
            # Return to menu text
            menu_text = font_medium.render("Returning to menu...", True, (200, 200, 200))
            menu_rect = menu_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 60))
            window.blit(menu_text, menu_rect)
            
            # Timer countdown 
            timer_seconds = max(0, game_over_timer // 60)
            if timer_seconds > 0:
                timer_text = font_medium.render(f"{timer_seconds}", True, (150, 150, 150))
                timer_rect = timer_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 120))
                window.blit(timer_text, timer_rect)
        
       
        pygame.display.flip()
        
       
        if not game_over and not level_completed:
            if ((player.rect.right - offset_x >= WIDTH - scroll_area_width and player.x_vel > 0) or 
                (player.rect.left - offset_x <= scroll_area_width and player.x_vel < 0)):
                offset_x += player.x_vel

def main(window):
  
    # Initialize joystick detection once
    detect_joystick()
    
    # Initialize audio system properly
    pygame.mixer.pre_init(44100, -16, 2, 512)  
    
    while True:
        # Show elegant menu first
        menu = ElegantMenu(window)
        menu_result = menu.run()
        
        if menu_result == "quit":
       
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            break
        elif menu_result == "start":
           
            main_game(window)
          

if __name__ == "__main__":
       main(window)