import time
import re
import os
import random


class Mosquito:
    def __init__(self, app) -> None:
        self.app = app

    def __create_image_for_mosquito(self):
        for mos in _mosquito.created_mosquito:
            self.app.canvas.create_image(
                *mos['position'], image=self.app.tk_image(mos['image'], mos['size']), anchor='nw', tags='mosquito')

    def adding_mosquito(self):
        _mosquito.mos(position=(random.randint(0, self.app.canvas_side[0]), random.randint(0, self.app.canvas_side[1])),
                      velocity=(random.choice(list(range(1, 4))+list(range(-3, 0))),
                                random.choice(list(range(1, 4))+list(range(-3, 0)))),
                      size=random.randint(50, 200),
                      image=f'mos\\mos{random.randint(*_mosquito.avaliable_image_count)}.png',
                      app=self)

    def auto_create_mosquito(self):
        if (temp := time.time()) - self.app.produceMosquitoTimer > 18:
            self.app.produceMosquitoTimer = temp
            self.adding_mosquito()

    def show_all_mosquito(self):
        def show():
            def get_info(mos):
                return mos['size'], mos['position'], mos['velocity'], mos['image']
            try:
                self.app.canvas_obj_states(canvas, 'delete', 'button')
            except Exception as e:
                self.app.autoSwitch.set(0)
                return
            # ----------------------------------------------------------------
            for num, mos in enumerate(_mosquito.created_mosquito, 0):
                info = get_info(mos)
                canvas.create_image(
                    5, 200*num+10, image=self.app.tk_image(info[3], info[0]), anchor='nw')
                canvas.create_text(
                    255, 200*num+10+50, text=f'X= {str(round(info[1][0]))}', font=self.app.font_get(36))

                canvas.create_text(
                    255, 200*num+10+150, text=f'Y= {str(round(info[1][1]))}', font=self.app.font_get(36))

                canvas.create_text(
                    505, 200*num+10+50, text=f'U= {str(round(info[2][0]))}', font=self.app.font_get(36))

                canvas.create_text(
                    505, 200*num+10+150, text=f'V= {str(round(info[2][1]))}', font=self.app.font_get(36))

                canvas.create_text(
                    755, 200*num+10+100, text=f'Size= {str(round(info[0]))}', font=self.app.font_get(30))

                if num != 0:
                    canvas.create_line(
                        0, 200*num+10, self.app.canvas_side[0], 200*num+10, fill='gold', width=3)
            # ----------------------------------------------------------------
            try:
                canvas.create_line(
                    0, 200*(num+1)+10, self.app.canvas_side[0], 200*(num+1)+10, fill='gold', width=3)
                canvas['scrollregion'] = (
                    0, 0, self.canvas_side[0], 200*(num+1)+10
                )
            except:
                pass

        def auto():
            if self.app.autoSwitch.get() == 1:
                canvas.delete('reloadCan')
                canvas.create_window(int(canvas['width']), 0, anchor='ne', window=self.app.making_widget('Button')(
                    win, image=self.app.tk_image(os.path.join('sys', 'mos\\reload_disabled.png')), state='disabled'), tags=('button', 'reloadCant'))
            else:
                canvas.delete('reloadCant')
                canvas.create_window(int(canvas['width']), 0, anchor='ne', window=self.app.making_widget('Button')(
                    win, image=self.app.tk_image(os.path.join('sys', 'mos\\reload.png')), command=show), tags=('button', 'reloadCan'))

        self.show = show
        self.app.autoSwitch.set(0)

        win = self.app.new_window(
            'Mosquito List', 'mos.ico', self.app.side
        )
        scrollbar = self.app.making_widget('Scrollbar')(win)
        scrollbar.grid(row=1, column=2, sticky='ns')
        canvas = self.app.making_widget('Canvas')(win, width=self.app.side[0]-int(scrollbar['width']), height=self.app.side[1], bg=self.app.canvas['bg'],
                                                  yscrollcommand=scrollbar.set)
        canvas.grid(row=1, column=1)
        scrollbar['command'] = canvas.yview
        canvas.bind(
            '<MouseWheel>', lambda event: canvas.yview_scroll(
                -(event.delta//120), 'units')
        )

        # ----------------------------------------------------------------
        canvas.create_window(int(canvas['width']), 0, anchor='ne', window=self.app.making_widget('Button')(
            win, image=self.app.tk_image(os.path.join('sys', 'mos\\reload.png')), command=show
        ), tags=('button', 'reloadCan'))

        canvas.create_window(int(canvas['width']), 130, anchor='ne', window=self.app.making_widget('Checkbutton')(
            win, onvalue=1, offvalue=0, image=self.app.tk_image(os.path.join('sys', 'mos\\auto.png')), variable=self.app.autoSwitch,
            indicatoron=False, command=auto), tags='button')

        # ----------------------------------------------------------------
        show()

    def mosquito_animation(self):
        if (temp := time.time()) - self.app.appTimer > self.app.frameFrequency.get():
            self.app.canvas.delete('mosquito')
            self.__create_image_for_mosquito()
            self.app.canvas.tag_raise('mosquito', 'cover')
            self.app.appTimer = temp

            for mos in _mosquito.created_mosquito:
                mos.move(self.app.canvas_side)
            if self.app.autoSwitch.get() == 1:
                self.show()


class _mosquito:
    number = 0  # for giving created obj a number
    avaliable_property = ('size', 'position', 'velocity', 'image', 'app')
    avaliable_image_count = 0, 20  # corresponding to image frame
    slow_rate, speed_rate = 2, 2   # with %
    oppsite_rate = 1  # with %
    created_mosquito = []

    def __init__(self, **kyargs) -> None:
        '''
        !! Avoid creating mosquito by call init method !!

        number(force)(int)
        position(select)(tuple), velocity(select)(tuple),
        size(select)(int), image(select)(str)
        '''
        self.__dict__.update(kyargs)
        self.created_mosquito.append(self)

    @ classmethod
    def mos(cls, **kyargs):
        cls.number += 1
        for arg in kyargs.copy():
            if arg not in cls.avaliable_property:
                kyargs.pop(arg)
        return cls(number=cls.number, **kyargs)

    def __getitem__(self, value):
        try:
            return self.__dict__[value]
        except:
            if value in self.avaliable_property:
                return None
            else:
                raise Exception(f'Property: {value} is not defined')

    def __setitem__(self, value, new):
        try:
            self[value]
            self.__dict__[value] = new
        except:
            raise Exception(f'Property: {value} is not defined')

    def __str__(self):
        return f'''{self.__class__.__name__} object: {self["number"]}, property: [
                position: {self["position"]}
                velocity: {self["velocity"]}
                size:     {self["size"]}
                image:    {self["image"]}
                ]'''

    __repr__ = __str__

    def __speed_change(self):
        v = self['velocity']
        num = random.randint(0, 99)
        if num < self.slow_rate:
            if random.randint(0, 1) % 2 == 0:
                self['velocity'] = (v[0]/1.25, v[1])
            else:
                self['velocity'] = (v[0], v[1]/1.25)
        elif self.slow_rate <= num < self.slow_rate + self.speed_rate:
            if random.randint(0, 1) % 2 == 0:
                self['velocity'] = (v[0]*1.25, v[1])
            else:
                self['velocity'] = (v[0], v[1]*1.25)

    def __oppsite(self):
        v = self['velocity']
        num = random.randint(0, 99)
        if num < self.oppsite_rate:
            if random.randint(0, 1) % 2 == 0:
                self['velocity'] = (-v[0], v[1])
            else:
                self['velocity'] = (v[0], -v[1])

    def __change_image(self):
        imgNum = int(re.search('\d+', self['image']).group())
        if imgNum == self.avaliable_image_count[1]:
            imgNum = self.avaliable_image_count[0]
        else:
            imgNum += 1

        self['image'] = f'mos\\mos{imgNum}.png'

    def __check_direction(self):
        if self['velocity'][0] > 0:
            self['image'] = self['image'][:self['image'].rfind(
                '.')]+'mirror.png'

    def __check_position_not_too_far(self, width, height):
        pos = self['position']
        if pos[0] < -5000 or pos[0] > width + 5000:
            self.created_mosquito.remove(self)
            del self
            return

        if pos[1] < -5000 or pos[1] > height + 5000:
            self.created_mosquito.remove(self)
            del self
            return

    def move(self, side):
        pos = self['position']
        v = self['velocity']

        self['position'] = (pos[0]+v[0], pos[1]+v[1])

        self.__speed_change()
        self.__oppsite()
        self.__change_image()
        self.__check_direction()
        self.__check_position_not_too_far(*side)
