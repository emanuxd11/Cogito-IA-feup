import pygame

class Menu:
    def __init__(self, items):
        self.items = items
        self.selected_index = 0
        self.font = pygame.font.Font("../fonts/PressStart2P-Regular.ttf", 50)
        self.background_image = pygame.image.load("../img/main_menu.png").convert()

    def draw(self, screen, x=0, y=0, centered=True):
        for i, item in enumerate(self.items):
            color = (255, 0, 0) if i == self.selected_index else (255, 255, 255)
            text_surface = self.font.render(item, True, color)
            if not centered:
                screen.blit(text_surface, (x - (len(self.items)) * 60 / 2, y + i * 60))
            else:
                left_gap, _ = text_surface.get_size()
                screen_width, _ = screen.get_size()
                left_gap = screen_width // 2 - left_gap // 2
                screen.blit(text_surface, (left_gap, y + i * 60))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.items)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.items)
            elif event.key == pygame.K_RETURN:
                return self.items[self.selected_index]
        return None

