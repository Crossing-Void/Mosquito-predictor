from tkinter.filedialog import asksaveasfile as saveFile
from modules.tkinter_template import EffectButton
import imageio
import os
import re
import time
import random


class Visualize:
    def __init__(self, app) -> None:
        self.app = app
        self.number = self.app.making_widget('IntVar')()
        self.pauseController = self.app.making_widget('IntVar')()
        self.buffer = self.app.making_widget('IntVar')()

    def __get_img(self, path):
        '''
        include extension
        '''
        parse = '.png'
        return sorted(
            [file for file in os.listdir(path) if os.path.splitext(
                os.path.join(path, file))[-1] == parse]
        )

    def __change_img(self):
        if not self.app.canvas.itemcget('visualize-img-0', 'image'):
            return
        for i in range(0, self.__length):
            if i == self.number.get():
                self.app.canvas.itemconfig(
                    f'visualize-img-{i}', state='normal')
                self.app.canvas.dtag(f'visualize-img-{i}', 'H')
                self.app.canvas.itemconfig(
                    f'visualize-label-{i}', state='normal')
                self.app.canvas.dtag(f'visualize-label-{i}', 'H')

            else:
                self.app.canvas.itemconfig(
                    f'visualize-img-{i}', state='hidden')
                self.app.canvas.addtag_withtag('H', f'visualize-img-{i}')
                self.app.canvas.itemconfig(
                    f'visualize-label-{i}', state='hidden')
                self.app.canvas.addtag_withtag('H', f'visualize-label-{i}')

        if self.number.get() != (self.__length-1):
            self.number.set(self.number.get()+1)
        else:
            self.number.set(0)

    def __select_img(self, num):
        self.number.set(num)
        self.app.canvas.delete('visualize-max')
        for i in range(0, self.__length):
            if i == self.number.get():
                self.app.canvas.itemconfig(
                    f'visualize-img-{i}', state='normal')
                self.app.canvas.dtag(f'visualize-img-{i}', 'H')
                self.app.canvas.itemconfig(
                    f'visualize-label-{i}', state='normal')
                self.app.canvas.dtag(f'visualize-label-{i}', 'H')

            else:
                self.app.canvas.itemconfig(
                    f'visualize-img-{i}', state='hidden')
                self.app.canvas.addtag_withtag('H', f'visualize-img-{i}')
                self.app.canvas.itemconfig(
                    f'visualize-label-{i}', state='hidden')
                self.app.canvas.addtag_withtag('H', f'visualize-label-{i}')

    def __show1D(self):
        def enter(arg):
            canvas.delete('label')
            canvas.create_window(2, 2, anchor='nw', tags=('label'), window=self.app.making_widget('Label')(canvas, font=self.app.font_get(16), text=arg,
                                                                                                           bg='lightblue'))
            for objID in canvas.find_all():
                if canvas.type(objID) == 'image':
                    if f'st{arg}' in canvas.gettags(objID):
                        canvas.itemconfig(objID, image=self.app.tk_image(
                            'sys\\st\\red.ico', 32
                        ))
                    else:
                        canvas.itemconfig(objID, image=self.app.tk_image(
                            'sys\\st\\blue.ico', 32
                        ))

        def click(arg):
            win = self.app.new_window(
                f'All Station 1D-{self.app.select_area.get()}-{arg}', 'station.ico', (960, 720))
            canvas = self.app.making_widget('Canvas')(
                win, width=960, height=720, bg='lightblue', highlightthickness=0)
            canvas.create_image(0, 0, anchor='nw', image=self.app.tk_image(f'{arg}.png', dirpath=os.path.join(self.app.datas, 'combines', f'{self.app.select_area.get()}from{self.app.select_date.get()}',
                                                                                                              f'ploting-1D({self.app.select_model.get()})', )
                                                                           ))
            canvas.grid()
        self.app.extremes1D.ploting_all_st()
        win = self.app.new_window(
            f'All Station 1D-{self.app.select_area.get()}', 'station.ico', (700, 500))
        canvas = self.app.making_widget('Canvas')(
            win, width=700, height=500, bg='lightblue', highlightthickness=0)
        canvas.grid()
        canvas.create_line(
            2, 52, 1000, 52, width=2, tags=('line1', 'hori'))
        canvas.create_line(
            102, 52, 102, 1000, width=2, tags=('line2', 'vert'))

        stDict = self.app.pastdata.areaStationsList[self.app.select_area.get()]
        # [['基隆', '26.7m', 121.740475, 25.133314]~~]
        stNo = list(stDict)
        stInfoList = [list(value.values()) for value in stDict.values()]

        width, height = int(canvas['width'])-103,  int(
            canvas['height'])-53
        iniPoint = 103, int(canvas['height'])

        minLon, maxLon = round(sorted(stInfoList, key=lambda x: x[2])[
            0][2], 2), round(sorted(stInfoList, key=lambda x: x[2])[-1][2], 2)
        minLat, maxLat = round(sorted(stInfoList, key=lambda x: x[3])[
            0][3], 2), round(sorted(stInfoList, key=lambda x: x[3])[-1][3], 2)

        pixelPerScale = round(
            min(width/(maxLon-minLon), height/(maxLat-minLat)), 2)

        # ---station---
        for value, No in zip(stInfoList, stNo):
            canvas.create_image(iniPoint[0]+(round(value[2], 2)-minLon)*pixelPerScale,
                                iniPoint[1]-(round(value[3], 2)-minLat)*pixelPerScale, image=self.app.tk_image(
                'sys\\st\\blue.ico', 32
            ), tags=(f'st{value[0]}'))
            canvas.tag_bind(
                f'st{value[0]}', '<Enter>', lambda event, args=value[0]: enter(args))
            canvas.tag_bind(
                f'st{value[0]}', '<Button-1>', lambda event, args=No: click(args))
        # ---station---
        # ---lon tick---
        for i in range(1, 11):
            if (rWidth := iniPoint[0]+100*i) <= int(canvas['width'])-80:
                canvas.create_line(rWidth, 53-5, rWidth, 53+5)
                canvas.create_text(rWidth, 53-5-10, anchor='s', font=self.app.font_get(
                    16), text=str(round(minLon+100*i*pixelPerScale**-1, 2)))
        # ---lon tick---
        # ---lat tick---
        for i in range(1, 11):
            if (rHeight := iniPoint[1]-100*i) > 53:
                canvas.create_line(103-5, rHeight, 103+5, rHeight)
                canvas.create_text(103-5-10, rHeight, anchor='e', font=self.app.font_get(
                    16), text=str(round(minLat+100*i*pixelPerScale**-1, 2)))
        # ---lat tick---

    def __show_max(self, arg):
        if not self.pauseController.get():
            return
        if self.buffer.get():
            self.app.soundeffects['wrong_01'].play()
            return
        self.buffer.set(1)
        self.app.canvas.delete('visualize-max')
        self.app.canvas.create_rectangle(self.app.canvas_side[0]-960, self.app.canvas_side[1]-720-20-100,
                                         self.app.canvas_side[0] -
                                         460, self.app.canvas_side[1]-720-20, fill='lightblue',
                                         tags=('visualize', 'visualize-max-frame', 'visualize-max'), outline='indigo', width=5)

        a, b, c, d = self.app.canvas.coords('visualize-max-frame')
        for i, color, text in zip(range(1, 5), ['green', 'pink', 'yellow', 'red'], ['舒適', '注意', '警告', '危險']):
            self.app.canvas.create_rectangle(a+125*(i-1), (b+d)/2-5, a+125*i, (b+d)/2+5, fill=color, tags=(
                'visualize', f'visualize-max-rec-{color}', 'visualize-max'), width=1)
            self.app.canvas.create_text(a+125*(i-0.5), (b+d)/2-5-10, fill=color, tags=(
                'visualize', f'visualize-max-text-{text}', 'visualize-max'), anchor='s', text=text,
                font=self.app.font_get(20))

        self.app.canvas.create_image(a, (b+d)/2+5+2, image=self.app.tk_image(
            'sys\\music\\play_up.png', height=int((d-b-10)/2)
        ), tags=('visualize', 'visualize-max', 'visualize-max-arrow'), anchor='n')
        label = self.app.making_widget('Label')(
            self.app.canvas, bg='green', font=self.app.font_get(30))
        self.app.canvas.create_window(c+4, b-2, anchor='nw', tags=(
            'visualize', 'visualize-max', 'visualize-max-label'), window=label)

        arg = round(arg)
        if arg < 0:
            arg = 0
        if arg > 1000:
            arg = 1000

        duration = random.randint(2, 3)+random.random()
        path_length = arg/2
        cumu = 0
        for i in range(1, 101):
            self.app.canvas.move('visualize-max-arrow', path_length/100, 0)
            cumu += arg/100
            label['text'] = round(cumu)
            if cumu > 750:
                label['bg'] = 'red'
            elif cumu > 500:
                label['bg'] = 'yellow'
            elif cumu > 250:
                label['bg'] = 'pink'
            self.app.canvas.update()
            time.sleep(duration/100)

        color_ = label['bg']
        for i in range(10):
            if label['bg'] == color_:
                label['bg'] = 'white'
            else:
                label['bg'] = color_
            self.app.canvas.update()
            time.sleep(0.3)
        self.buffer.set(0)

    def build_img_and_label(self):
        maximum_property_change_dict = {
            250: ('舒適', 'green'),
            500: ('注意', 'pink'),
            750: ('警告', 'yellow'),
        }

        self.__path = os.path.join(self.app.datas, 'combines',
                                   f'{self.app.select_area.get()}from{self.app.select_date.get()}', f'ploting-2D({self.app.select_model.get()})')
        self.__imgList = self.__get_img(self.__path)
        self.__length = len(self.__imgList)

        for num in range(self.__length):
            self.app.canvas.create_image(self.app.canvas_side[0],
                                         self.app.canvas_side[1]-20, anchor='se', image=self.app.tk_image(
                self.__imgList[num], height=720 if (rHeight := self.app.canvas_side[1]) >= 720 else rHeight, dirpath=self.__path),
                tags=('visualize', f'visualize-img-{num}', 'H'), state='hidden')
        for num in range(self.__length):
            for maximum_criteria, property_of_label in maximum_property_change_dict.items():
                if (value := self.app.extremes2D.maximumList[num]) <= maximum_criteria:
                    property_ = property_of_label
                    break
            else:
                property_ = ('危險', 'red')
            self.app.canvas.create_window(self.app.canvas_side[0],
                                          self.app.canvas_side[1]-20-720, anchor='se', window=self.app.making_widget(
                'Button')(self.app.canvas, font=self.app.font_get(30), text=property_[0],
                          bg=property_[1], command=lambda args=value: self.__show_max(args)),
                tags=('visualize', f'visualize-label-{num}', 'H'), state='hidden')

    def build_button(self):
        self.pauseController.set(0)
        self.app.canvas.delete('visualize-max')
        self.app.canvas.create_window(52, self.app.canvas_side[1]-20, anchor='sw', window=EffectButton(('gold', 'black'), self.app.canvas, image=self.app.tk_image('sys\\save.ico', 48),
                                                                                                       command=self.saving_gif, bg='lightblue'), tags=('visualize', 'visualizesavebutton')
                                      )
        self.app.canvas.create_window(0, self.app.canvas_side[1]-20, anchor='sw', window=EffectButton(
            ('gold', 'black'), self.app.canvas, bg='lightblue', command=self.pause, image=self.app.tk_image('sys\\music\\pause.png',
                                                                                                            width=48, height=48)), tags=('visualaize', 'visualizepausebutton')
        )
        self.app.canvas.create_window(0, self.app.canvas_side[1]-20, anchor='sw', window=EffectButton(
            ('gold', 'black'), self.app.canvas, bg='lightblue', command=self.pause, image=self.app.tk_image('sys\\music\\play.png',
                                                                                                            width=48, height=48)), tags=('visualaize', 'visualizeplaybutton', 'H'), state='hidden')
        self.app.canvas.create_window(104, self.app.canvas_side[1]-20, anchor='sw', window=EffectButton(
            ('gold', 'black'), self.app.canvas, bg='lightblue', command=self.__show1D, image=self.app.tk_image(os.path.join(self.app.bitmaps, 'help.ico'),
                                                                                                               width=64, height=64)), tags=('visualaize', 'visualize1Dbutton')
        )

        for i in range(self.__length):
            self.app.canvas.create_window(0, self.app.canvas_side[1]-20-60*(i+1), anchor='sw', window=self.app.making_widget('Radiobutton')(
                self.app.canvas, bg='lightblue', indicatoron=0, variable=self.number, value=i, selectcolor='purple', width=2,
                font=self.app.font_get(32), text=str(i), command=lambda args=i: self.__select_img(args)), tags=('visualaize', f'visualizenumberbutton-{i}', 'H'), state='hidden'
            )

    def saving_gif(self):
        file = saveFile(mode='wb', defaultextension='.gif',
                        initialfile=f'{self.app.select_area.get()} {self.app.select_date.get()} {self.app.select_model.get()}',
                        initialdir=os.path.join(self.app.images, 'usr'))
        if file:
            file.close()

            images = []
            for filename in self.__imgList:
                images.append(imageio.imread(
                    os.path.join(self.__path, filename)))
            imageio.mimsave(os.path.join(
                self.__path, 'temp.gif'), images, duration=self.app.frameFrequency.get()*10)

            with open(os.path.abspath(file.name), 'wb') as f, open(os.path.join(self.__path, 'temp.gif'), 'rb') as k:
                f.write(k.read())
            os.remove(os.path.join(self.__path, 'temp.gif'))

    def pause(self):
        if self.pauseController.get():
            self.pauseController.set(0)
            self.app.canvas.delete('visualize-max')
            self.app.canvas.itemconfig('visualizeplaybutton', state='hidden')
            self.app.canvas.addtag_withtag('H', 'visualizeplaybutton')
            self.app.canvas.itemconfig(
                'visulaizepausebutton', state='normal')
            for i in range(self.__length):
                self.app.canvas.itemconfig(
                    f'visualizenumberbutton-{i}', state='hidden')
        else:
            self.pauseController.set(1)
            self.app.canvas.itemconfig('visualizeplaybutton', state='normal')
            self.app.canvas.dtag('visualizeplaybutton', 'H')
            self.app.canvas.itemconfig(
                'visulaizepausebutton', state='hidden')
            for i in range(self.__length):
                self.app.canvas.itemconfig(
                    f'visualizenumberbutton-{i}', state='normal')
                self.app.canvas.dtag(f'visualizenumberbutton-{i}', 'H')
            for id_ in self.app.canvas.find_all():
                if self.app.canvas.type(id_) == 'image':
                    if self.app.canvas.itemcget(id_, 'state') == 'normal':
                        for tags in self.app.canvas.gettags(id_):
                            if (match := re.search('\d+', tags)):
                                self.number.set(int(match.group()))

    def show_animation(self):
        if (temp := time.time()) - self.app.imageTimer > self.app.frameFrequency.get()*10:
            if not self.pauseController.get():
                self.__change_img()
            self.app.imageTimer = temp
