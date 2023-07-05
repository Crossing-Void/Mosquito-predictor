from tkinter import *
from PIL import ImageTk, Image, ImageColor
from datetime import date
import tkinter.font as Font
import time
import pygame
import os
import random


class Interface:
    '''
    Architecture:

      Project
        images
          bitmaps
            files
          covers
            files
        sounds
          files
        musics
          files
        datas
          files
        project.py

    Minimum:

      Project
        project.py
    '''
    pygame.init()
    pygame.mixer.init()

    image = {}

    @staticmethod
    def font_get(size, bold=False):
        return ('Inconsolata', size, 'bold' if bold else '')

    @staticmethod
    def font_span(fit_size, text):
        for size in range(1, 250):
            if Font.Font(font=('Inconsolata', size)).measure(text) > fit_size:
                break
        return size - 1

    def __init__(self, title: str, icon=None):
        '''
        images, bitmaps, covers, sounds, musics, datas, soundeffects(dict)
        '''
        # ---basic setting---

        self.images = 'images'  # for image that project would use
        self.bitmaps = 'images\\bitmaps'  # for icon that project will use
        self.covers = 'images\\covers'  # for cover that project will use
        self.sounds = 'sounds'  # for sound effect that project will use
        self.musics = 'musics'  # for music(bgm) that project will use
        self.datas = 'datas'    # for data(like record) that project will use

        # ---other extension---
        self.models = 'models'
        # ---other extension---
        try:
            self.soundeffects = {self.delete_extension(name): pygame.mixer.Sound(os.path.join(
                self.sounds, name))for name in os.listdir(self.sounds)
            }
        except:
            pass

        # ---basic setting---
        self.default_menu_content = ['background color', 'canvas cover']
        self.default_dashboard_content = ['time', 'date', 'table']

        self.__create_root(title, icon)
        self.__create_canvas()
        self.__create_menu_default()
        self.__create_dashboard()

    def __create_root(self, title, icon):
        '''
        root, side(tuple), isFullscreen(property)
        '''
        self.root = Tk()
        self.side = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.title(title)
        if icon:
            self.root.iconbitmap(os.path.join(self.bitmaps, icon))
        self.root.maxsize(*self.side)
        self.root.resizable(0, 0)
        self.root.state('zoomed')
        self.isFullscreen = True

    @ property
    def isFullscreen(self):
        return self.__isFullscreen

    @ isFullscreen.setter
    def isFullscreen(self, value):
        self.__isFullscreen = value
        self.root.wm_attributes('-fullscreen', self.isFullscreen)

    def __create_canvas(self):
        '''
        canvas, canvas_side(tuple)
        '''
        def esc(event):
            self.isFullscreen = not(self.isFullscreen)

        self.canvas = Canvas(self.root, width=self.side[0] * 0.8, height=self.side[1],
                             highlightthickness=0, bg='lightblue')
        self.canvas.focus_set()
        self.canvas_side = int(self.canvas['width']), int(
            self.canvas['height'])
        self.canvas.grid(row=1, column=1)
        self.canvas.bind('<Escape>', esc)

    def __create_menu_default(self):
        '''
        top_menu(is the horizontal one), __default_menu(the leftmost one for selective function)
        '''
        self.top_menu = self.create_menu(self.root)
        self.root.config(menu=self.top_menu)

        self.__default_menu = self.create_menu(self.top_menu)
        self.top_menu.add_cascade(
            label='Selective Function', menu=self.__default_menu)

    def __create_dashboard(self):
        '''
        dashboard, dashboard_side(tuple)
        '''
        self.dashboard = Frame(self.root, cursor='dot',
                               width=0.2*self.side[0], height=self.side[1])
        self.dashboard_side = int(self.dashboard['width']), int(
            self.dashboard['height'])

        self.dashboard.grid(row=1, column=2, sticky='snew')

    def __create_menu_by_category(self, category: str):
        if category == 'background color':
            def background_color():
                def color(position):
                    str_of_color = f'#{red.get():02x}{green.get():02x}{blue.get():02x}'
                    self.canvas.config(bg=str_of_color)

                def select_color(color):
                    self.canvas.config(bg=color)
                    win.destroy()

                win = self.new_window('Background Color', 'color.ico')

                red = Scale(win, font=self.font_get(20), bg='red', length=255, tickinterval=50, command=color,
                            from_=0, to=255, label='Red')
                green = Scale(win, font=self.font_get(20), bg='green', length=255, tickinterval=50, command=color,
                              from_=0, to=255, label='Green')
                blue = Scale(win, font=self.font_get(20), bg='blue', length=255, tickinterval=50, command=color,
                             from_=0, to=255, label='Blue')

                color_select = ['chocolate', 'lightblue',
                                'violet', 'silver', 'indigo']
                x, y, z = ImageColor.getrgb(self.canvas['bg'])
                red.set(x)
                green.set(y)
                blue.set(z)
                red.grid(row=1, column=1, rowspan=len(
                    color_select), sticky='sn')
                green.grid(row=1, column=2, rowspan=len(
                    color_select), sticky='sn')
                blue.grid(row=1, column=3, rowspan=len(
                    color_select), sticky='sn')

                index = 1
                for item in color_select:
                    Button(win, font=self.font_get(20), bg=item, height=15//len(color_select), fg='black', text=item,
                           command=lambda x=item: select_color(x)).grid(row=index, column=4, sticky='ew')
                    index += 1

            self.__default_menu.add_command(
                label='Background Color', command=background_color)
        if category == 'canvas cover':
            def canvas_cover():
                def click(num):
                    canvas.itemconfigure(f'rec{num}', state='normal')
                    for i in range(len(cover)):
                        if i != num:
                            canvas.itemconfigure(f'rec{i}', state='hidden')

                def double_click(num):
                    self.__canvas_cover(cover[num])
                    win.destroy()

                win = self.new_window(
                    'Windows Cover', 'wall paper.ico', self.side)
                scrollbar = Scrollbar(win)
                scrollbar.grid(row=1, column=2, sticky='ns')
                canvas = Canvas(win, width=self.side[0]-int(scrollbar['width']), height=self.side[1], bg=self.canvas['bg'],
                                yscrollcommand=scrollbar.set)
                canvas.grid(row=1, column=1)
                scrollbar['command'] = canvas.yview

                cover = [img for img in os.listdir(self.covers) if img.endswith('png')
                         or img.endswith('jpg') or img.endswith('jpeg')]
                wi_inter, hi_inter = 100, 120
                wi = (int(canvas['width']) - 2*wi_inter - 20)//3
                hi = wi * 3 // 4

                for i in range(len(cover)):

                    canvas.create_image(20+i % 3 * (wi + wi_inter), 20+i//3 * (hi + hi_inter), anchor='nw',
                                        image=self.tk_image(os.path.join(
                                            self.covers, cover[i]), wi, hi),
                                        tags=(f'img{i}'))

                    canvas.create_text(20+i % 3 * (wi + wi_inter) + wi//2, 20+i//3 * (hi + hi_inter)+20+24//2 + hi, font=self.font_get(24),
                                       text=cover[i], tags=(f'text{i}'))

                    x, y, x2, y2 = (20+i % 3 * (wi + wi_inter), 20+i//3 * (hi + hi_inter),
                                    20+i % 3 * (wi + wi_inter)+wi, 20+i//3 * (hi + hi_inter)+hi)
                    canvas.create_rectangle(x-4, y-4, x2+4, y2+4, width=4, outline='gold',
                                            state='hidden', tags=(f'rec{i}'))

                    canvas.tag_bind(f'img{i}', '<Button-1>',
                                    lambda event, x=i: click(x))
                    canvas.tag_bind(
                        f'img{i}', '<Double-Button-1>', lambda event, x=i: double_click(x))

                canvas['scrollregion'] = (
                    0, 0, int(canvas['width']), 20+i//3 *
                    (hi + hi_inter)+20+24//2 + hi+60
                )
                canvas.bind('<MouseWheel>', lambda event: canvas.yview_scroll(-(event.delta//120), 'units')
                            )

            self.__default_menu.add_command(
                label='Windows Cover', command=canvas_cover)

    def __canvas_cover(self, file):
        self.canvas.delete('cover')
        self.canvas.create_image(0, 0, anchor='nw', image=self.tk_image(
            os.path.join(self.covers, file), width=self.canvas_side[0], height=self.canvas_side[1]), tags=('cover'))

        self.canvas.tag_lower('cover', self.canvas.find_all()[0])


# ------------------------------------------------------------------------------------------------------------------


    def create_menu(self, root):
        '''
        Can made menu own and inner code also use, need to bind to top_menu
        '''
        return Menu(root, font=self.font_get(16), tearoff=0)

    def create_menu_optional(self, *option):
        for opt in option:
            if opt not in self.default_menu_content or type(opt) != str:
                raise Exception(f'The {opt} is not yet support')
            else:
                self.__create_menu_by_category(opt)
                self.default_menu_content.remove(opt)

    def create_dashboard_item_optional(self, option: str, row):
        '''
        time_show, date_show, table_button
        '''
        if option not in self.default_dashboard_content or type(option) != str:
            raise Exception(f'The {option} is not yet support')
        else:
            self.default_dashboard_content.remove(option)
        if option == 'time':
            self.__time = StringVar()
            self.time_show = Label(self.dashboard, textvariable=self.__time,
                                   font=self.font_get(self.font_span(self.dashboard_side[0], '00:00:00')), bd=1)
            self.time_show.grid(row=row, column=1)
        if option == 'date':
            self.__date = StringVar()

            self.date_show = Label(self.dashboard, textvariable=self.__date,
                                   font=self.font_get(self.font_span(self.dashboard_side[0], '2022/09/09  (Mon)')), bd=1)
            self.date_show.grid(row=row, column=1)
        if option == 'table':
            def click():
                if self.table_button['bg'] == 'gray':
                    self.table_button['bg'] = 'red'
                    self.canvas_obj_states(
                        self.canvas, 'hidden', 'cover', 'mosquito')
                    self.table_button.bind('<Leave>', lambda event: event)
                    self.table_button.bind('<Enter>', lambda event: event)
                elif self.table_button['bg'] == 'red':
                    self.table_button['bg'] = 'gray'
                    self.table_button.bind('<Enter>', enter)
                    self.table_button.bind('<Leave>', leave)

            def enter(event):
                self.canvas_obj_states(
                    self.canvas, 'hidden', 'cover', 'mosquito')
                self.table_button['bg'] = 'gray'

            def leave(event):
                self.canvas_obj_states(
                    self.canvas, 'normal', 'cover', 'mosquito')
                self.table_button['bg'] = 'white'

            self.table_button = Button(self.dashboard, width=1, font=self.font_get(16),
                                       bd=3, bg='white', command=click, text='P')
            self.table_button.place(
                x=self.dashboard_side[0], y=self.dashboard_side[1]-20, anchor='se')
            self.table_button.bind('<Enter>', enter)
            self.table_button.bind('<Leave>', leave)

    def time_flush(self):
        '''
        go with time(dafault) and date(default)
        '''
        day_change = dict(zip((0, 1, 2, 3, 4, 5, 6),
                              ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')))
        time_now = time.localtime(time.time())
        timeStr = f'{time_now.tm_hour:02d}:{time_now.tm_min:02d}:{time_now.tm_sec:02d}'
        dateStr = f'{time_now.tm_year:04d}/{time_now.tm_mon:02d}/{time_now.tm_mday:02d}  ({day_change[time_now.tm_wday]})'
        try:
            self.__time.set(timeStr)
        except:
            pass
        try:
            self.__date.set(dateStr)
        except:
            pass

    def new_window(self, title, icon=None, maxsize: tuple = None):
        '''
        child_root,
        '''
        self.child_root = Toplevel()
        self.child_root.title(title)
        if icon:
            self.child_root.iconbitmap(os.path.join(self.bitmaps, icon))
        if maxsize:
            self.child_root.maxsize(*maxsize)
            self.child_root.state('zoomed')
        self.child_root.resizable(0, 0)

        return self.child_root

    def tk_image(self, file, width=None, height=None, dirpath=None):
        # ---only parsing the path images\\---
        if file.split('\\')[0] == 'images':
            file = os.path.join(*(file.split('\\')[1:]))

        if dirpath:
            img = Image.open(os.path.join(dirpath, file))
        else:
            img = Image.open(os.path.join(self.images, file))
        size = img.size
        if width:
            if height:
                size = (width, height)
            else:
                rate = width / size[0]
                height = int(size[1] * rate)
                size = (width, height)
        elif height:
            rate = height / size[1]
            width = int(size[0] * rate)
            size = (width, height)
        name = f'{file}_{size[0]}x{size[1]}'
        if name not in Interface.image:
            img = img.resize(size, Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)
            Interface.image[name] = img
        return Interface.image[name]

    def making_widget(self, widget: str):
        try:
            return eval(widget)
        except:
            raise ValueError(f'The widget: {widget} does not exist in Tk')

    def canvas_obj_states(self, canvas, mode, *tag):
        '''
        canvas: select a canvas to make manipulation on it
        mode can accept: delete, hidden, normal
        tag(tuple): stand for remain tag
        '''
        for id_ in canvas.find_all():
            for tags in canvas.gettags(id_):
                if tags in tag:
                    break
            else:
                if mode == 'delete':
                    canvas.delete(id_)
                else:
                    if mode == 'normal':
                        if 'H' in canvas.gettags(id_):
                            pass
                        else:
                            canvas.itemconfigure(id_, state=mode)
                    else:
                        canvas.itemconfigure(id_, state=mode)

    def delete_extension(self, filename):
        return filename[:filename.rfind('.')]

    def str_tuple_date_change(self, arg):
        '''
        switch date tuple {(2022, 12, 12)} (includes datetime.date objs) and date string format {2022-12-12}
        '''
        if type(arg) == str:
            return (int(arg[:4]), int(arg[5:7]), int(arg[8:10]))
        elif type(arg) == tuple:
            return f'{arg[0]:04d}-{arg[1]:02d}-{arg[2]:02d}'
        elif type(arg) == date:
            return f'{arg.year:04d}-{arg.month:02d}-{arg.day:02d}'

    def directly_select_cover(self, covers=None):
        '''
        giving in filename
        '''
        if covers:
            self.__canvas_cover(os.path.join(self.covers, covers))
        else:
            self.__canvas_cover(random.choice(
                os.listdir(self.covers)
            ))


class BindButton(Button):
    def __init__(self, char, root=None, **option):
        self.char = char
        self.state = False
        super().__init__(root, **option)
        self.__bind()

    def __bind(self):
        def keypress(event):
            if self.char is None:
                self.config(relief='sunken')
                return
            if event.keysym == self.char:
                self.config(relief='sunken')

        def keyrelease(event):
            if self.char is None:
                self.config(relief='raised')
                if self.state:
                    self.invoke()
                else:
                    self.state = True
                return
            if event.keysym == self.char:
                self.config(relief='raised')
                if self.state:
                    self.invoke()
                else:
                    self.state = True

        self.bind('<KeyPress>', keypress)
        self.bind('<KeyRelease>', keyrelease)


class EffectButton(Button):
    def __init__(self, color: tuple, root=None, **option):
        '''
        color(first for bg, second for fg)
        '''
        self.color = color
        super().__init__(root, **option)
        self.bg = self['bg']
        self.fg = self['fg']
        self.__bind()

    def __bind(self):
        def enter(event):
            self.config(bg=self.color[0], fg=self.color[1])

        def leave(event):
            self.config(bg=self.bg, fg=self.fg)

        self.bind('<Enter>', enter)
        self.bind('<Leave>', leave)
# ------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    pass
