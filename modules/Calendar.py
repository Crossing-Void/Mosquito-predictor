from modules.tkinter_template import EffectButton
from modules.Pastdata import AllStationDataGrabber
import calendar
import time
import datetime
import os
import send2trash


class Calendar:
    def __init__(self, app) -> None:
        self.app = app
        self.date_border = 2

        self.__today = self.__time_format('%Y %m %d')
        self.__today = (int(self.__today[:4]), int(
            self.__today[5:7]), int(self.__today[8:10]))
        # ---default Y and M
        self.__year = self.__today[0]
        self.__month = self.__today[1]

    def __time_format(self, fmt: str, time_=None):
        if time_ is None:
            time_ = time.localtime(time.time())
        return time.strftime(fmt, time_)

    def __set_date(self, args):
        self.app.canvas_obj_states(
            self.app.canvas, 'delete', 'cover', 'controlButton', 'calendarheader')

        if args == 'doubleleft':
            self.__year -= 1
        elif args == 'left':
            if self.__month == 1:
                self.__year -= 1
                self.__month = 12
            else:
                self.__month -= 1
        elif args == 'right':
            if self.__month == 12:
                if self.__year == self.__today[0]:
                    self.app.soundeffects['wrong_01'].play()
                else:
                    self.__year += 1
                    self.__month = 1
            else:
                if (self.__year == self.__today[0]) and (self.__month + 1 > self.__today[1]):
                    self.app.soundeffects['wrong_01'].play()
                else:
                    self.__month += 1
        elif args == 'doubleright':
            if (self.__year + 1 > self.__today[0]) or (self.__year + 1 == self.__today[0] and self.__month > self.__today[1]):
                self.app.soundeffects['wrong_01'].play()

            else:
                self.__year += 1
        elif args == 'main':
            self.__year = self.__today[0]
            self.__month = self.__today[1]

        self.show()

    def __grabbing_data(self, date: tuple):
        grabber = self.app.pastdata
        for code in grabber.areaStationsList[self.app.select_area.get()]:
            if not grabber.check_repeat(date):
                grabber.single_info(code, date)

    def show(self):
        def click(number):
            if (date := datetime.date(year, month, number)) > datetime.date(self.__today[0], self.__today[1], self.__today[2]):
                self.app.soundeffects['wrong_01'].play()
                a, b, c, d = self.app.canvas.coords(f'{number}rec')
                self.app.canvas.create_text(
                    (a+c)//2, (b+d)//2, text='Too\nEarly!', justify='center', font=self.app.font_get(20), fill='#990036', tags=('calendar', f'{number}warn'))
            else:
                self.app.select_date.set(
                    self.app.str_tuple_date_change(
                        (date.year, date.month, date.day))
                )
                for i in range(2, 9):
                    date_ = datetime.date(
                        *self.app.str_tuple_date_change(self.app.select_date.get())
                    ) - datetime.timedelta(i)
                    self.__grabbing_data((date_.year, date_.month, date_.day))
                try:
                    self.app.combiner.use()
                except:
                    self.app.soundeffects['wrong_01'].play()
                    send2trash.send2trash(os.path.join(
                        'datas', 'combines', f'{self.app.select_area.get()}from{self.app.select_date.get()}'))
                    self.app.main_page()
                    return
                self.app.soundeffects['correct_03'].play()
                self.app.step_model()

        year = self.__year
        month = self.__month

        temp_judge = (year == self.__today[0]) and (
            month == self.__today[1])

        week = calendar.monthcalendar(self.__year, self.__month)
        width = self.app.canvas_side[0]
        self.app.canvas.create_text(
            width//2, 0, text=f'{self.__year:04d}-{self.__month:02d}', tags=('calendar', 'dateYM'), font=self.app.font_get(72), anchor='n')
        _partition_x = width // 8
        _partition_y = int(self.app.canvas_side[1] - 180) // 6.5
        _ini_width = _partition_x
        for days in ['M', 'T', 'W', 'T', 'F', 'S', 'S']:
            self.app.canvas.create_text(_ini_width, 150, text=days, font=self.app.font_get(32),
                                        fill='red' if days == 'S' else 'black', tags=('calendar', f'dataW-{days}'))
            _ini_width += _partition_x

        _ini_height = int(_partition_y * 1.8)

        for week_ in week:
            _ini_width = _partition_x // 2
            num = 1
            for number in week_:
                self.app.canvas.create_rectangle(_ini_width, _ini_height, _ini_width+_partition_x, _ini_height+_partition_y,
                                                 width=self.date_border, tags=('calendar', str(number)+'rec'), fill='white', activefill='gold' if number else '',
                                                 outline='red' if temp_judge and self.__today[2] == number else 'black')

                if number:
                    self.app.canvas.tag_bind(
                        str(number)+'rec', '<Button-1>', lambda event, num=number: click(num))
                    self.app.canvas.create_text(_ini_width + int(_partition_x*3/4), _ini_height + int(_partition_y/4),
                                                text=str(number), font=self.app.font_get(24), tags=('calendar', str(number)+'num'),
                                                fill='red' if num >= 6 else 'black')
                num += 1
                _ini_width += _partition_x + self.date_border
            _ini_height += _partition_y + self.date_border
        self.app.canvas.create_line(_partition_x // 2 - self.date_border, int(_partition_y * 1.8) - self.date_border, _partition_x // 2 + 7 * (_partition_x + self.date_border) + self.date_border,
                                    int(_partition_y * 1.8) - self.date_border, width=self.date_border, tags=('calendar', 'deco'))

        self.app.canvas.create_line(_partition_x // 2 - self.date_border, _ini_height, _partition_x // 2 + 7 * (_partition_x + self.date_border) + self.date_border,
                                    _ini_height, width=self.date_border, tags=(
                                    'calendar', 'deco'))

        self.app.canvas.create_line(_partition_x // 2 - self.date_border, int(_partition_y * 1.8) - self.date_border, _partition_x // 2 - self.date_border,
                                    _ini_height + self.date_border, width=self.date_border, tags=('calendar', 'deco'))
        self.app.canvas.create_line(_partition_x // 2 + 7 * (_partition_x + self.date_border), int(_partition_y * 1.8) - self.date_border, _partition_x // 2 + 7 * (_partition_x + self.date_border),
                                    _ini_height + self.date_border, width=self.date_border, tags=('calendar', 'deco'))

    def button_set(self):
        self.app.canvas.create_window(
            self.app.canvas_side[0]-96*2-1, 0, anchor='ne', tags=('calendar', 'controlButton'),
            window=EffectButton(
                ('silver', 'black'), self.app.canvas, command=lambda: self.__set_date('left'), image=self.app.tk_image(os.path.join('sys', 'cal\\left.ico'), 96))),

        self.app.canvas.create_window(
            self.app.canvas_side[0]-96*3-1, 0, anchor='ne', tags=('calendar', 'controlButton'),
            window=EffectButton(('lightyellow', 'black'), self.app.canvas,
                                command=lambda: self.__set_date('doubleleft'), image=self.app.tk_image(
                os.path.join('sys', 'cal\\doubleleft.ico'), 96)),

        )
        self.app.canvas.create_window(
            self.app.canvas_side[0]-96*1-1, 0, anchor='ne', tags=('calendar', 'controlButton'),
            window=EffectButton(('silver', 'black'), self.app.canvas,
                                command=lambda: self.__set_date('right'), image=self.app.tk_image(
                os.path.join('sys', 'cal\\right.ico'), 96)),

        )
        self.app.canvas.create_window(
            self.app.canvas_side[0], 0, anchor='ne', tags=('calendar', 'controlButton'),
            window=EffectButton(('lightyellow', 'black'), self.app.canvas,
                                command=lambda: self.__set_date('doubleright'), image=self.app.tk_image(
                os.path.join('sys', 'cal\\doubleright.ico'), 96)),

        )

    def bind_canvas(self):
        self.app.canvas.bind('<Left>', lambda event,
                             args='left': self.__set_date(args))
        self.app.canvas.bind('<Right>', lambda event,
                             args='right': self.__set_date(args))
        self.app.canvas.bind('<space>', lambda event,
                             args='main': self.__set_date(args))

    def unbind_canvas(self):
        self.app.canvas.unbind('<Left>')
        self.app.canvas.unbind('<Right>')
        self.app.canvas.unbind('<space>')


if __name__ == '__main__':
    cal = Calendar()
