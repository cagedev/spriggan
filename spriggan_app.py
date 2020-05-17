import pygame
import pygvisuals.widgets as gui
import math

import glob  # or pathlib?


class SprigganApp:

    window_surface = None

    # TODO: load from config file
    # file_buttons
    file_container_margin_left = 28
    file_container_margin_top = 28
    file_button_width = 56
    file_button_height = 28
    # TODO: file_button_sprites = {save, load, etc}...
    # do it with text until then

    filelist_container_margin_left = 560
    filelist_container_margin_top = 28
    filelist_widget_width = 196
    filelist_widget_height = 480

    media_dir = './media'
    base_save_filename = 'spriggan_save'
    base_export_filename = 'spriggan_export'
    base_save_ext = 'json'
    base_export_ext = 'png'
    load_files_filter = 'spriggan*.json'

    background_color = (0, 0, 0)
    saved_color = (0,255,0)
    unsaved_color = (255, 0, 0)

    # palette
    palette_colors = [
        (255, 255, 255),
        (153,   0, 255),  # purple
        (204,   0,   0),  # red
        (0, 153,   0),  # green
        (255, 204,   0),  # yellow
        (0,  51, 204),  # blue
        (255, 102, 255),  # pink
    ]
    palette_container_margin_left = 480
    palette_container_margin_top = 100
    palette_button_width = 50
    palette_button_height = 50
    palette_button_margin = 5
    selected_color = 0

    # image_grid
    image_grid_margin_top = 96
    image_grid_margin_left = 28
    image_grid_size_x = 14
    image_grid_size_y = 14
    image_pixel_size = 20
    image_pixel_margin = 5
    image_grid = []
    grid_x_min = image_grid_margin_left
    grid_x_max = grid_x_min + image_grid_size_x * \
        (image_pixel_size + image_pixel_margin)
    grid_y_min = image_grid_margin_top
    grid_y_max = grid_y_min + image_grid_size_y * \
        (image_pixel_size + image_pixel_margin)

    def __init__(self):

        pygame.init()

        print('grid_x_min:', self.grid_x_min)
        print('grid_x_max:', self.grid_x_max)
        print('grid_y_min:', self.grid_y_min)
        print('grid_y_max:', self.grid_y_max)

        pygame.display.set_caption('Spriggan Sprite Designer')
        self.window_surface = pygame.display.set_mode((800, 600))

        self.background = pygame.Surface((800, 600))
        self.background.fill(self.background_color)

        # offload making palette to own class?
        self.palette_buttons = []
        for c, i in zip(self.palette_colors, range(len(self.palette_colors))):

            x = self.palette_container_margin_left
            y = self.palette_container_margin_top + i * \
                (self.palette_button_height + self.palette_button_margin)
            dx = self.palette_button_width
            dy = self.palette_button_height

            b = gui.Button(x, y, dx, dy, '',
                           callback=lambda x=i: self.setcolor(x)).setBackground(c).setForeground((0, 0, 0))
            self.palette_buttons.append(b)
        self.palette_group = pygame.sprite.LayeredDirty(self.palette_buttons)

        # setup other buttons
        self.file_buttons = []
        x = self.file_container_margin_left
        y = self.file_container_margin_top
        dx = self.file_button_width
        dy = self.file_button_height
        button_file_save = gui.Button(x, y, dx, dy, 'SAVE', callback=self.file_save).setBackground(
            (0, 196, 0)).setForeground((0, 0, 0))
        self.file_buttons.append(button_file_save)
        x += dx
        button_file_load = gui.Button(x, y, dx, dy, 'LOAD', callback=self.file_load).setBackground(
            (0, 0, 196)).setForeground((0, 0, 0))
        self.file_buttons.append(button_file_load)
        x += dx
        button_file_export = gui.Button(x, y, dx, dy, 'EXPORT', callback=self.file_export).setBackground(
            (196, 0, 0)).setForeground((0, 0, 0))
        self.file_buttons.append(button_file_export)
        x += dx
        button_file_list = gui.Button(x, y, dx, dy, 'LIST', callback=self.file_list).setBackground(
            (255, 0, 0)).setForeground((0, 0, 0))
        self.file_buttons.append(button_file_list)
        self.file_group = pygame.sprite.LayeredDirty(self.file_buttons)

        # setup files list
        self.filelist_widgets = []
        x = self.filelist_container_margin_left
        y = self.filelist_container_margin_top
        dx = self.filelist_widget_width
        dy = self.filelist_widget_height
        listbox_file_load = gui.listbox.Listbox(x, y, dx, dy)
        listbox_file_load.insert(0, 'test0')
        listbox_file_load.insert(1, 'test1')
        listbox_file_load.insert(2, 'test2')
        listbox_file_load.insert(3, 'test3')
        listbox_file_load.insert(4, 'test4')
        listbox_file_load.insert(5, 'test5')
        self.filelist_widgets.append(listbox_file_load)
        self.filelist_group = pygame.sprite.LayeredDirty(self.filelist_widgets)


        # setup image_grid
        self.image_grid = [[0 for x in range(self.image_grid_size_x)]
                           for y in range(self.image_grid_size_y)]

        self.clock = pygame.time.Clock()
        self.is_running = True


    def setcolor(self, c):
        self.selected_color = c
        # print(self.selected_color)


    def draw_bead(self, s, x, y, dx, dy, c, f=pygame.draw.rect):
        # pygame.draw.rect(
        #     self.window_surface, self.palette_colors[self.image_grid[j][i]],
        #     [x, y, self.image_pixel_size, self.image_pixel_size])
        f(s, c, [x, y, dx, dy])


    def draw_grid(self):
        for j in range(self.image_grid_size_y):
            for i in range(self.image_grid_size_x):

                x = self.image_grid_margin_left + \
                    (self.image_pixel_size + self.image_pixel_margin) * \
                    i + self.image_pixel_margin
                y = self.image_grid_margin_top + \
                    (self.image_pixel_size + self.image_pixel_margin) * \
                    j + self.image_pixel_margin

                self.draw_bead(self.window_surface, x, y, self.image_pixel_size, self.image_pixel_size,
                               self.palette_colors[self.image_grid[j][i]], f=pygame.draw.rect)

                # pygame.draw.rect(
                #     self.window_surface, self.palette_colors[self.image_grid[j][i]],
                #     [x, y, self.image_pixel_size, self.image_pixel_size])


    def file_list(self):
        # TODO: probably should use pathdir or something...
        data_files = glob.glob(self.media_dir + '/*.' +
                                  self.base_save_ext, recursive=True)
        print('saves:', data_files)
        print('exports:', glob.glob(self.media_dir + '/*.' +
                                    self.base_export_ext, recursive=True))
        print(self.filelist_widgets[0].setList(data_files))


    def set_unsaved(self):
        self.file_buttons[0].setBackground(self.unsaved_color)
        self.saved = False


    def set_saved(self):
        self.file_buttons[0].setBackground(self.saved_color)
        self.saved = True


    def file_save(self):
        print('file_save')
        self.set_saved()


    def file_load(self):
        print('file_load')


    def file_export(self):
        print('file_export')


    def run(self):
        self.saved = False

        while self.is_running:
            time_delta = self.clock.tick(60) / 1000.0

            # get events and do updates
            for event in pygame.event.get():
                # if QUIT
                if event.type == pygame.QUIT:
                    self.is_running = False

                # if CLICK ON GRID
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    # Change the x/y screen coordinates to grid coordinates
                    x = pos[0]
                    y = pos[1]
                    # Check if within grid:
                    if x >= self.grid_x_min and x < self.grid_x_max:
                        if y >= self.grid_y_min and y < self.grid_y_max:
                            x = x - self.grid_x_min
                            y = y - self.grid_y_min

                            col = x // (self.image_pixel_size +
                                        self.image_pixel_margin)
                            row = y // (self.image_pixel_size +
                                        self.image_pixel_margin)
                            self.image_grid[row][col] = self.selected_color
                            print("mouseclick(", pos, ") -> (", row, ",", col, ")")
                            self.set_unsaved()

                self.palette_group.update(event)
                self.file_group.update(event)
                self.filelist_group.update(event)

            self.palette_group.draw(self.window_surface, self.background)
            self.file_group.draw(self.window_surface, self.background)
            self.filelist_group.draw(self.window_surface, self.background)
            self.draw_grid()
            pygame.display.update()
            # pygame.time.wait(100)
            # pygame.display.update()


if __name__ == "__main__":
    app = SprigganApp()
    app.run()
