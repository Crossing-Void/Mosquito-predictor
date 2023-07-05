import os
import pygame


class Settings:
    def __init__(self, app) -> None:
        self.app = app
        self.frame = self.__frames
        self.volume = self.__volume

    def __frames(self):
        def temp(position):
            if self.app.frameFrequency.get() <= 0.03:
                canvas.itemconfigure('runfast', state='normal')
                canvas.itemconfigure('run', state='hidden')
                canvas.itemconfigure('walk', state='hidden')
            elif self.app.frameFrequency.get() <= 0.07:
                canvas.itemconfigure('runfast', state='hidden')
                canvas.itemconfigure('run', state='normal')
                canvas.itemconfigure('walk', state='hidden')
            else:
                canvas.itemconfigure('runfast', state='hidden')
                canvas.itemconfigure('run', state='hidden')
                canvas.itemconfigure('walk', state='normal')

        win = self.app.new_window('Adjust Frames', 'frame.ico')
        canvas = self.app.making_widget('Canvas')(
            win, width=700, height=100, bg='coral', highlightthickness=0)
        scale = self.app.making_widget('Scale')(win, relief='solid', bd=3, length=400, orient='horizontal', from_=0.01, to=0.11, resolution=0.01,
                                                tickinterval=0.05, showvalue=0, width=15, variable=self.app.frameFrequency, font=self.app.font_get(16), command=temp)
        label = self.app.making_widget('Label')(
            win, font=self.app.font_get(30, True), textvariable=self.app.frameFrequency, bg='coral')
        for img in ['walk', 'run', 'runfast']:
            canvas.create_image(
                700, 0, anchor='ne', image=self.app.tk_image(os.path.join('sys', f'frame\\{img}.png'), 100), state='hidden',
                tags=img)
        canvas.create_window(
            0, 0, anchor='nw', window=scale)
        canvas.create_window(
            0, 60, anchor='nw', window=label)
        canvas.grid()
        temp(None)

    def __volume(self):
        def temp_(position):
            pygame.mixer.music.set_volume(self.app.volumeController.get())
            if self.app.volumeController.get() == 0.0:
                canvas.itemconfigure(
                    'Volume_mute', state='normal')
                canvas.itemconfigure(
                    'Volume_medium', state='hidden')
                canvas.itemconfigure(
                    'Volume_high', state='hidden')
            elif self.app.volumeController.get() <= 0.5:
                canvas.itemconfigure(
                    'Volume_mute', state='hidden')
                canvas.itemconfigure(
                    'Volume_medium', state='normal')
                canvas.itemconfigure(
                    'Volume_high', state='hidden')
            else:
                canvas.itemconfigure(
                    'Volume_mute', state='hidden')
                canvas.itemconfigure(
                    'Volume_medium', state='hidden')
                canvas.itemconfigure(
                    'Volume_high', state='normal')

        win = self.app.new_window('Adjust Volume', 'Volume.ico')
        canvas = self.app.making_widget('Canvas')(
            win, width=700, height=100, bg='coral', highlightthickness=0)
        scale = self.app.making_widget('Scale')(win, relief='solid', bd=3, length=400, orient='horizontal', from_=0, to=1, resolution=0.1,
                                                tickinterval=0.2, showvalue=0, width=15, variable=self.app.volumeController, font=self.app.font_get(16), command=temp_)
        label = self.app.making_widget('Label')(
            win, font=self.app.font_get(30, True), textvariable=self.app.volumeController, bg='coral')
        for img in ['Volume_mute', 'Volume_medium', 'Volume_high']:
            canvas.create_image(
                700, 0, anchor='ne', image=self.app.tk_image(os.path.join('sys', f'volume\\{img}.ico'), 100), state='hidden',
                tags=img)
        canvas.create_window(
            0, 0, anchor='nw', window=scale)
        canvas.create_window(
            0, 60, anchor='nw', window=label)
        canvas.grid()
        temp_(None)

    def pad_setting(self):
        settingMenu = self.app.create_menu(self.app.top_menu)
        self.app.top_menu.add_cascade(label='Setting', menu=settingMenu)
        settingMenu.add_command(label='Adjust Frames',
                                command=self.frame)
        settingMenu.add_command(label='Adjust Volume',
                                command=self.volume)

    def pad_option(self):
        optMenu = self.app.create_menu(self.app.top_menu)
        self.app.top_menu.add_cascade(label='Option', menu=optMenu)
        optMenu.add_command(label='Add Mosquito',
                            command=self.app.mosquito.adding_mosquito)
        optMenu.add_command(label='Mosquito List',
                            command=self.app.mosquito.show_all_mosquito)
