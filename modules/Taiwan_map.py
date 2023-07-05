from tkinter import *
from tkinter.font import Font
import os


class Taiwan:
    base = (550, 775)
    countyPoint = {'基隆市': (491, 37, 'sw'), '澎湖縣': (34, 311, 'sw'),
                   '台北市': (404, 38, 'se'), '新北市': (420, 121, 'sw'),
                   '桃園市': (351, 81, 'nw'), '新竹市': (295, 128, 'se'),
                   '新竹縣': (355, 161, 'nw'), '苗栗縣': (286, 187, 'nw'),
                   '台中市': (259, 240, 'nw'), '南投縣': (299, 318, 'nw'),
                   '台東縣': (325, 491, 'nw'), '高雄市': (245, 493, 'nw'),
                   '花蓮縣': (400, 294, 'nw'), '台南市': (170, 453, 'nw'),
                   '宜蘭縣': (431, 184, 'nw'), '彰化縣': (210, 301, 'nw'),
                   '屏東縣': (241, 565, 'nw'), '雲林縣': (190, 348, 'nw'),
                   '嘉義縣': (249, 392, 'nw'), '嘉義市': (149, 420, 'se')
                   }

    def __init__(self, app) -> None:
        '''
        app(main exe)
        '''
        self.app = app

    def __show_county_name(self, height):
        '''
        864 font size 12
        '''
        def leftbutton(arg):
            self.app.select_area.set(arg)
            self.app.step_date()  # <-- Here
        # ---------------------------------------------

        def enter(arg):
            def inner_enter(arg):
                for child in self.info.winfo_children():
                    child.destroy()
                # ---getting info---
                for i in range(len(stInfoList)):
                    if stInfoList[i][0] == arg:
                        targetIndex = i
                        break
                targetList = stInfoList[targetIndex]  # list
                targetNo = stNo[targetIndex]  # str

                self.app.making_widget('Label')(self.info, text=targetList[0], font=self.app.font_get(16), bg='Coral',
                                                ).grid(sticky='we')
                self.app.making_widget('Label')(self.info, text=f'No.: {targetNo}', font=self.app.font_get(12), anchor='w'
                                                ).grid(sticky='we')
                self.app.making_widget('Label')(self.info, text=f'Alt: {targetList[1]}', font=self.app.font_get(12), anchor='w'
                                                ).grid(sticky='we')
                self.app.making_widget('Label')(self.info, text=f'Loc: ({round(targetList[2],2)}, {round(targetList[3], 2)})', font=self.app.font_get(12), anchor='w'
                                                ).grid(sticky='we')

                # ---getting info---

                for objID in self.canvas.find_all():
                    if self.canvas.type(objID) == 'image':
                        if f'st{arg}' in self.canvas.gettags(objID):
                            self.canvas.itemconfig(objID, image=self.app.tk_image(
                                'sys\\st\\red.ico', 32
                            ))
                        else:
                            self.canvas.itemconfig(objID, image=self.app.tk_image(
                                'sys\\st\\blue.ico', 32
                            ))
            for child in self.info.winfo_children():
                child.destroy()
            self.canvas.delete('all')
            self.canvas.create_window(2, 2, anchor='nw', tags=('label'), window=self.app.making_widget('Label')(self.canvas, font=self.app.font_get(20), text=arg,
                                                                                                                bg='lightblue'))

            self.canvas.create_line(
                2, 52, 1000, 52, width=2, tags=('line1', 'hori'))
            self.canvas.create_line(
                102, 2, 102, 1000, width=2, tags=('line2', 'vert'))

            stDict = self.app.pastdata.areaStationsList[arg]
            # [['基隆', '26.7m', 121.740475, 25.133314]~~]
            stNo = list(stDict)
            stInfoList = [list(value.values()) for value in stDict.values()]

            width, height = int(self.canvas['width'])-103,  int(
                self.canvas['height'])-53
            iniPoint = 103, int(self.canvas['height'])

            minLon, maxLon = round(sorted(stInfoList, key=lambda x: x[2])[
                0][2], 2), round(sorted(stInfoList, key=lambda x: x[2])[-1][2], 2)
            minLat, maxLat = round(sorted(stInfoList, key=lambda x: x[3])[
                0][3], 2), round(sorted(stInfoList, key=lambda x: x[3])[-1][3], 2)

            pixelPerScale = round(
                min(width/(maxLon-minLon), height/(maxLat-minLat)), 2)

            # ---station---
            for value in stInfoList:
                self.canvas.create_image(iniPoint[0]+(round(value[2], 2)-minLon)*pixelPerScale,
                                         iniPoint[1]-(round(value[3], 2)-minLat)*pixelPerScale, image=self.app.tk_image(
                    'sys\\st\\blue.ico', 32
                ), tags=(f'st{value[0]}'))
                self.canvas.tag_bind(
                    f'st{value[0]}', '<Enter>', lambda event, args=value[0]: inner_enter(args))
            # ---station---
            # ---lon tick---
            for i in range(1, 11):
                if (rWidth := iniPoint[0]+100*i) <= int(self.canvas['width'])-80:
                    self.canvas.create_line(rWidth, 53-5, rWidth, 53+5)
                    self.canvas.create_text(rWidth, 53-5-10, anchor='s', font=self.app.font_get(
                        16), text=str(round(minLon+100*i*pixelPerScale**-1, 2)))
            # ---lon tick---
            # ---lat tick---
            for i in range(1, 11):
                if (rHeight := iniPoint[1]-100*i) > 53:
                    self.canvas.create_line(103-5, rHeight, 103+5, rHeight)
                    self.canvas.create_text(103-5-10, rHeight, anchor='e', font=self.app.font_get(
                        16), text=str(round(minLat+100*i*pixelPerScale**-1, 2)))
            # ---lat tick---
        # ---------------------------------------------

        rate = ((1100 * height / 1551)/self.base[0],
                height/self.base[1]
                )

        for county, value in self.countyPoint.items():
            if county in self.app.pastdata.urlList:
                self.app.canvas.create_text(
                    value[0]*rate[0], value[1]*rate[1], anchor=value[2], text=county, font=self.app.font_get(round(12*height/864), True),
                    tags=('area', county, 'county', 'canTouch'), fill='black', activefill='violet')

                self.app.canvas.tag_bind(
                    county, '<Button-1>', lambda event, args=county: leftbutton(
                        args)
                )
                self.app.canvas.tag_bind(
                    county, '<Enter>', lambda event, args=county: enter(
                        args)
                )
            else:
                self.app.canvas.create_text(
                    value[0]*rate[0], value[1]*rate[1], anchor=value[2], text=county, font=self.app.font_get(round(12*height/864)),
                    tags=('area', county, 'county', 'cantTouch'), fill='gray')

    def __create_station_info(self, span):
        self.canvas = self.app.making_widget('Canvas')(self.app.canvas, bg='lightblue',
                                                       width=span, height=500)
        self.info = self.app.making_widget('Frame')(
            self.app.canvas, bg='aliceblue', width=Font(font=('Inconsolata', 12)).measure(
                'Loc: (121.04, 25.12)'), height=90)
        self.app.canvas.create_window(self.app.canvas_side[0], self.app.canvas_side[1]-20, anchor='se', tags=('area', 'areainfo'),
                                      window=self.canvas)
        self.app.canvas.create_window(self.app.canvas_side[0], self.app.canvas_side[1]-20-500-2, anchor='se',
                                      tags=('area', 'areainfoframe'), window=self.info)

    def show_taiwan(self, x):
        '''
        using canvas height
        '''
        height = self.app.canvas_side[1]
        widthSpan = 1100 * height / 1551
        self.app.canvas.create_image(
            x, 0, anchor='nw', image=self.app.tk_image(os.path.join('area', 'taiwan.jpg'), height=height), tags=('area', 'whole'))
        self.__show_county_name(height)
        self.__create_station_info(widthSpan)
