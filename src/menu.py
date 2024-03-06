import pygame

class Menu:
    def __init__(self, items):
        self.items = items
        self.selected_index = 0
        self.font = pygame.font.Font("../fonts/digital-7-mono.ttf", 60)
        self.background_image = pygame.image.load("../img/main_menu.png").convert()

    def draw(self, screen, x, y):
        for i, item in enumerate(self.items):
            color = (255, 0, 0) if i == self.selected_index else (255, 255, 255)
            text_surface = self.font.render(item, True, color)
            screen.blit(text_surface, (x- (len(self.items)) * 60 / 2, y + i * 60))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.items)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.items)
            elif event.key == pygame.K_RETURN:
                return self.items[self.selected_index]
        return None
