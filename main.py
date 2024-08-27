import pygame
from random import choice

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((640, 320))
        self.game_font = pygame.font.SysFont("Verdana", 24)
        self.gameover_font = pygame.font.SysFont("Verdana", 48)
        pygame.display.set_caption("Final Task")
        self.load_images()
        self.new_game()
        self.clock = pygame.time.Clock()
        self.main_loop()
    
    def load_images(self):
        self.images = []
        for name in ["coin", "monster", "robot"]:
            self.images.append(pygame.image.load(name + ".png"))
    
    def new_game(self):
        self.x = 170-self.images[2].get_width()
        self.y = 315-self.images[2].get_height()
        self.points = 0
        self.play = False
        self.jumping = False
        self.gameover = False
        self.gravity = 0.5
        self.height = 14
        self.velocity = self.height
        self.coins = []
        self.monsters = []
        self.c_speed = 2
        self.m_speed = 3
        self.text_pos = 200
        self.display_text = True
        self.text = self.game_font.render("Press SPACE to jump", True, (255, 0, 0))
    
    def main_loop(self):
        while True:
            self.check_events()
            self.draw_window()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.gameover:
                        self.play = True
                        self.jumping = True
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_RETURN:
                    self.new_game()
            if event.type == pygame.QUIT: 
                exit()
    
    def draw_window(self):
        self.window.fill(self.background_color())
        pygame.draw.line(self.window, (255, 215, 0), (0, 317), (640, 317), 5)
        self.window.blit(self.game_font.render(f"Points: {self.points}", True, (255, 0, 0)), (480, 10))
        if self.display_text:
            self.window.blit(self.text, (self.text_pos, 140))
        self.window.blit(self.images[2], (self.x, self.y))
        if self.play:
            if not self.gameover:
                self.text_pos -= self.c_speed
            if self.text_pos < -self.text.get_width():
                self.display_text = False
            self.generate_coins()
            self.generate_monsters()
            if self.jumping:
                self.jump()
        if self.gameover:
            self.window.blit(self.gameover_font.render("GAME OVER", True, (255, 0, 0)), (255, 100))
            self.window.blit(self.game_font.render("Press ENTER to restart or ESC to exit", True, (255, 0, 0)), (180, 205))
        pygame.display.flip()
        self.clock.tick(60)
    
    def background_color(self):
        return (135, 206, 250) if self.points < 50 else (0, 0, 0)

    def jump(self):
        if not self.gameover:
            self.y -= self.velocity
            self.velocity -= self.gravity
            if self.velocity < -self.height:
                self.jumping = False
                self.velocity = self.height 

    def generate_coins(self):
        if len(self.coins) < 5:
            for x_pos in [640, 685, 730, 775, 820]:
                self.coins.append([x_pos, 160, False])
        self.update_coins()
    
    def update_coins(self):
        for coin in self.coins:
            self.window.blit(self.images[0], (coin[0], coin[1]))
            if not self.gameover:
                coin[0] -= self.c_speed
                if (coin[0]+self.images[0].get_width() >= self.x and coin[0] <= self.x+self.images[2].get_width() and 
                    coin[1]+self.images[0].get_height() >= self.y and coin[1] <= self.y+self.images[2].get_height()):
                    coin[2] = True
                    self.points += 1
                    self.update_speed()
        self.coins = [c for c in self.coins if not c[2] and c[0] > -self.images[0].get_width()]

    def update_speed(self):
        if self.points % 5 == 0 and self.points <= 50:
            self.m_speed += 0.2
            self.c_speed += 0.2
    
    def generate_monsters(self):
        if len(self.monsters) < 2:
            for x_pos in [640, 890, 1140, 1390, 1640]:
                self.monsters.append([x_pos, choice([315-self.images[1].get_height(), 70])])
        self.update_monsters()

    def update_monsters(self):
        for monster in self.monsters:
            self.window.blit(self.images[1], (monster[0], monster[1]))
            if not self.gameover:
                monster[0] -= self.m_speed
                if (monster[0]+self.images[1].get_width() >= self.x+15 and monster[0]+15 <= self.x+self.images[2].get_width() and 
                    monster[1]+self.images[1].get_height() >= self.y+15 and monster[1]+15 <= self.y+self.images[2].get_height()):
                    self.gameover = True
        self.monsters = [m for m in self.monsters if m[0] > -self.images[1].get_width()]

if __name__ == "__main__":
    Game()