import pygame

import pygvisuals.widgets as gui


class SprigganApp:

    background_color = (0, 0, 0)
    # load from config file
    palette_colors = [
        (255, 255, 255),
        (0,     0,   0),
        (0,   255,   0),
        (255,   0,   0)
    ]
    palette_container_margin_left = 400
    palette_container_margin_top = 100
    palette_button_width = 50
    palette_button_height = 50
    palette_button_margin = 5

    def __init__(self):

        pygame.init()

        pygame.display.set_caption('Spriggan Sprite Designer')
        self.window_surface = pygame.display.set_mode((800, 600))

        self.background = pygame.Surface((800, 600))
        self.background.fill(self.background_color)

        self.palette_buttons = []
        # make a palette
        for c, i in zip(self.palette_colors, range(len(self.palette_colors))):

            x = self.palette_container_margin_left
            y = self.palette_container_margin_top + i * \
                (self.palette_button_height + self.palette_button_margin)
            dx = self.palette_button_width
            dy = self.palette_button_height

            b = gui.Button(x, y, dx, dy,
                           "",
                           callback=None).setBackground(c).setForeground((0, 0, 0))
            self.palette_buttons.append(b)

                # Here we create a sprite-group to gather all of our widgets.
        self.palette_group = pygame.sprite.LayeredDirty(self.palette_buttons)
        self.clock = pygame.time.Clock()
        self.is_running = True

    def run(self):
        while self.is_running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                self.palette_group.update(event)

            self.palette_group.draw(self.window_surface, self.background)
            pygame.display.update()
            # pygame.time.wait(100)
            # pygame.display.update()


if __name__ == "__main__":
    app = SprigganApp()
    app.run()
