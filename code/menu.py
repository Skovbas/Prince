import pygame

class Button:
    def __init__(self, text, font, font_size, x, y):
        self.text = text
        self.font = pygame.font.Font(font, font_size)
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.is_hovered = False

    def render(self, screen):
        text_render = self.font.render(self.text, True, self._get_text_color())
        text_rect = text_render.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_render, text_rect)

        if self.is_hovered:
            underline_rect = pygame.Rect(self.x, self.y + self.height - 2, self.width, 2)
            pygame.draw.rect(screen, self._get_text_color(), underline_rect)

    def update(self):
        self.width, self.height = self.font.size(self.text)
        self.is_hovered = self._is_hovered()

    def _get_text_color(self):
        return (255, 220, 220) if self.is_hovered else (255, 255, 255)

    def _is_hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height
