from modules import *
import time
import os


class MainPage(tkinter_template.Interface):
    def __init__(self, title, icon=None):
        '''
        inherite almost all property from father
        '''
        super().__init__(title, icon)
        # ---build modules obj---
        self.calendar = Calendar.Calendar(self)
        self.combiner = Combine.Combine(self)
        self.extremes1D = Extremes_1D.Extreme1D(self)
        self.extremes2D = Extremes_2D.Extreme2D(self)
        self.mosquito = Mosquito_producer.Mosquito(self)
        self.musicPlayer = Music.MusicPlayer(self)
        self.pastdata = Pastdata.AllStationDataGrabber(self)
        self.predicter = Predict.ToPredict(self)
        self.setting = Settings.Settings(self)
        self.taiwan = Taiwan_map.Taiwan(self)
        self.visualize = Visualize.Visualize(self)
        # ---build modules obj---

        # ---build user record---
        self.select_area = self.making_widget('StringVar')()
        self.select_date = self.making_widget('StringVar')()
        self.select_model = self.making_widget('StringVar')()
        # ---build user record---

        # --- system need---
        self.appTimer = time.time()  # for root update
        self.autoSwitch = self.making_widget('IntVar')()  # judge auto mode
        self.frameFrequency = self.making_widget('DoubleVar')(
            value=0.05)  # update frequency
        self.volumeController = self.making_widget('DoubleVar')(value=0.8)
        self.produceMosquitoTimer = time.time()  # for mosquito auto creating
        self.imageTimer = time.time()  # for fast change image so like .gif
        # --- system need---

        self.__dashboard_packing()
        self.setting.pad_option()
        self.setting.pad_setting()

        self.main_page()
        self.directly_select_cover()

    def __dashboard_packing(self):
        '''
        includes musicplayer and user select info and home button
        date_show, time_show,
        '''
        def create_user_info():
            infoFrame = self.making_widget('Frame')(
                self.dashboard, bd=2, relief='raise', bg='lightyellow')
            for i, var in enumerate(('select_area', 'select_date', 'select_model'), 1):
                self.making_widget('Label')(infoFrame, text=(var[var.rfind(
                    '_')+1:]+': ').capitalize(), font=self.font_get(16)).grid(row=i, column=1, sticky='we')
                self.making_widget('Label')(infoFrame, textvariable=self.__dict__[
                    var], font=self.font_get(16), bg='#FFF44F').grid(row=i, column=2, sticky='we')
            infoFrame.grid(row=4, column=1, sticky='nswe')

        def create_musicplayer():
            self.music_canvas = self.making_widget('Canvas')(
                self.dashboard, width=self.dashboard_side[0], height=500,
                bg='lightblue', bd=0, highlightthickness=0
            )
            self.musicPlayer.build_initial_layout()
            self.music_canvas.grid(row=5, column=1)

        def create_home_page():
            def temp():
                if self.table_button['bg'] == 'red':
                    self.soundeffects['wrong_01'].play()
                else:
                    self.main_page()
            home = tkinter_template.EffectButton(('gold', 'black'), self.dashboard, bg='lightblue', image=self.tk_image(
                'sys\\home.ico', width=48
            ), command=temp)
            home.place(x=0, y=self.dashboard_side[1]-20, anchor='sw')

        self.create_dashboard_item_optional('date', 2)
        self.create_dashboard_item_optional('time', 1)
        self.create_dashboard_item_optional('table', 3)
        create_user_info()
        create_musicplayer()
        create_home_page()

    def __select_function(self, labelList, y, tagName, func):
        def choice(event):
            func(labelList[choice_number]['text'])

        def select(arg):
            nonlocal choice_number
            if arg == 'down':
                if choice_number in range(0, length-1):
                    self.soundeffects['drop'].play()
                    choice_number += 1
                else:
                    return
            elif arg == 'up':
                if choice_number in range(1, length):
                    self.soundeffects['drop'].play()
                    choice_number -= 1
                else:
                    return

            for i in range(0, length):
                if i == choice_number:
                    self.canvas.itemconfig(
                        f'{tagName}arrow-{i}', state='normal')
                    self.canvas.dtag(f'{tagName}arrow-{i}', 'H')
                    labelList[i].config(
                        fg='indigo', bg='coral', relief='solid')
                else:
                    labelList[i].config(
                        fg='black', bg='lightblue', relief='flat')
                    self.canvas.itemconfig(
                        f'{tagName}arrow-{i}', state='hidden')
                    self.canvas.addtag_withtag('H', f'{tagName}arrow-{i}')

        choice_number = 0
        length = len(labelList)
        for num in range(length):
            self.canvas.create_window(self.canvas_side[0]/2-100, y+115*num, anchor='w',
                                      window=labelList[num], tags=(tagName, f'{tagName}name-{num}'))
            self.canvas.create_image(self.canvas_side[0]/2-180, y+115*num, anchor='e', image=self.tk_image('sys\\music\\play.png', width=60), tags=(tagName, 'H',
                                                                                                                                                    f'{tagName}arrow-{num}'),
                                     state='hidden')
        select('test')
        self.canvas.bind('<Down>', lambda event, args='down': select(args))
        self.canvas.bind('<Up>', lambda event, args='up': select(args))
        self.canvas.bind('<Return>', choice)

    # ------------------------progess------------------------
    def main_page(self):
        # -*--*--*--*--*--*--*--*--*--*--*--*--*--*-
        def main_page_process(args):
            if args == 'Start':
                self.canvas.unbind('<Up>')
                self.canvas.unbind('<Down>')
                self.canvas.unbind('<Return>')
                self.step_area()    # <-- Here
            elif args == 'Setting':
                win = self.new_window('Setting', 'setting.ico')
                tkinter_template.EffectButton(('gold', 'black'), win, bg='lightblue', text='Adjust Frames',
                                              font=self.font_get(50), command=self.setting.frame).grid()
                tkinter_template.EffectButton(('gold', 'black'), win, bg='lightblue', text='Adjust Volume',
                                              font=self.font_get(50), command=self.setting.volume).grid()
            elif args == 'Documentation':
                win = self.new_window('Documentation', 'help.ico')
                text = self.making_widget('Text')(
                    win, cursor='no', wrap='word', font=self.font_get(14), width=36, height=25)
                with open(os.path.join(self.datas, 'documentation.txt'), encoding='utf-8') as f:
                    for sentence in f:
                        text.insert('end', sentence)
                text['state'] = 'disabled'
                text.grid()
                text.bind(
                    '<MouseWheel>', lambda event: text.yview_scroll(
                        -(event.delta//120), 'units')
                )
        # -*--*--*--*--*--*--*--*--*--*--*--*--*--*-

        self.canvas_obj_states(self.canvas, 'delete', 'mosquito', 'cover')
        self.select_area.set('--')
        self.select_date.set('--')
        self.select_model.set('--')
        self.extremes2D.maximumList = []
        labelList = []
        for name in ('Start', 'Setting', 'Documentation'):
            labelList.append(
                self.making_widget('Label')(self.canvas, font=self.font_get(50), bg='lightblue',
                                            text=name)
            )
        self.canvas.create_text(self.canvas_side[0]/2, 50, font=self.font_get(75), anchor='n',
                                fill='gold', tags=('main', 'maintitle'), text='Mosquito Indicator')
        self.__select_function(labelList, 300, 'main', main_page_process)

    def step_area(self):
        self.canvas.delete('main')
        self.canvas.create_text(self.canvas_side[0], 0, anchor='ne', font=self.font_get(50),
                                fill='gold', tags=('area', 'areaheader'), text='Select City')
        self.taiwan.show_taiwan(0)

    def step_date(self):
        self.canvas.delete('area')
        self.canvas.create_text(0, 0, anchor='nw', font=self.font_get(50),
                                fill='gold', tags=('calendar', 'calendarheader'), text='Select Date')
        self.calendar.button_set()
        self.calendar.bind_canvas()
        self.calendar.show()

    def step_model(self):
        self.canvas.delete('calendar')
        # -*--*--*--*--*--*--*--*--*--*--*--*--*--*-

        def model_process(args):
            self.canvas.unbind('<Up>')
            self.canvas.unbind('<Down>')
            self.canvas.unbind('<Return>')
            self.select_model.set(args)
            self.predicter.analyze()
            self.step_ploting()
        # -*--*--*--*--*--*--*--*--*--*--*--*--*--*-
        labelList = []
        for name in self.predicter.get_all_models():
            labelList.append(
                self.making_widget('Label')(self.canvas, font=self.font_get(50), bg='lightblue',
                                            text=self.delete_extension(name))
            )
        self.canvas.create_text(self.canvas_side[0]/2, 40, font=self.font_get(50), anchor='n',
                                fill='gold', tags=('model', 'modelheader'), text='Select Model')
        self.__select_function(labelList, 200, 'model', model_process)

    def step_ploting(self):
        self.canvas.delete('model')
        self.extremes2D.ploting_week()

        self.canvas.create_text(0, 0, font=self.font_get(50), anchor='nw',
                                fill='gold', tags=('visualize', 'visualizeheader'), text='Result')
        self.visualize.build_img_and_label()
        self.visualize.build_button()


# ------------------------------------------------------------------------
interface = MainPage('Final Project', 'mos.ico')
interface.create_menu_optional('background color', 'canvas cover')

interface.mosquito.adding_mosquito()
while True:
    try:
        interface.canvas.update()
        interface.time_flush()
        interface.mosquito.mosquito_animation()
        interface.mosquito.auto_create_mosquito()
        interface.musicPlayer.set_ball()
        interface.visualize.show_animation()
    except:
        break
try:
    interface.root.destroy()
except:
    pass
