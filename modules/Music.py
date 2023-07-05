from modules.tkinter_template import EffectButton
from mutagen.mp3 import MP3
import tkinter.font as Font
import pygame
import random
import os


#  !!  height = 500  !!
#  !!  fontsi = 16   !!


class MusicPlayer:
    fontSize = 16

    def __init__(self, app) -> None:
        '''
        app
        '''
        self.app = app

        # ---system need---
        self.__music_now = self.app.making_widget(
            'StringVar')()  # for show playing music name now
        self.__pass_time = self.app.making_widget(
            'StringVar')()  # for store how offset is
        self.__length = self.app.making_widget(
            'StringVar')()     # for store how long the music is
        self.__enter_rec = self.app.making_widget('IntVar')(
            value=0)  # judge if user enter playduration rectangle
        self.__page_number = self.app.making_widget('IntVar')(
        )  # judge the current page is
        # ---system need---

    def __get_balance_height(self, width: int, text: str):
        '''
        input fit width and text, produce a balance(height) (using 4/3 approximation)
        '''
        for i in range(width+1):
            if self.app.font_span(width-i, text)*4/3 - i < 0:
                balance = i - 1
                break
        return balance

    def __second_fmt_change(self, sec):
        '''
        passing int -> '00:00'
        passing str -> 254
        '''
        if type(sec) in (int, float):
            if 0 <= sec <= 59*60 + 59:
                return f'{int(sec//60):02d}:{int(sec%60):02d}'
            else:
                self.canvas.itemconfigure(
                    'musicplayerplaybutton-pause', state='hidden')
                self.canvas.itemconfigure(
                    'musicplayerplaybutton-play', state='normal')
                return '00:00'
        elif type(sec) == str:
            return 60*int(sec[:2]) + int(sec[3:5])

    def __music_now_label_change_color(self, dashboard, now_music):
        for child in dashboard.winfo_children():
            if type(child) == self.app.making_widget('Label'):
                if child['text'] == self.__music_now.get():
                    child['fg'] = 'Indigo'
                else:
                    if child['text'] != 'Empty!':
                        child['fg'] = 'black'

    def __load_music_list(self, dashboard, page):
        def get_number():
            for number in range(1, 51):
                if (Font.Font(font=('Inconsolata', self.fontSize)).measure('n'*number)) > self.canvas_side[0] - self.fontSize*4/3:
                    return number - 1

        def enter(event, args, play_):
            play_.grid(row=args, column=2)
            others = [effectbutton for effectbutton in dashboard.winfo_children() if type(
                effectbutton) == EffectButton]
            others.remove(play_)
            for other in others:
                other.grid_forget()

        def leave(event, play_):
            if Font.Font(font=('Inconsolata', self.fontSize)).measure('n'*get_number()) \
               < event.x \
               < Font.Font(font=('Inconsolata', self.fontSize)).measure('n'*(get_number()+1)):
                pass
            else:
                play_.grid_forget()

        def dashboardleave(event):
            for play in dashboard.winfo_children():
                if type(play) == EffectButton:
                    play.grid_forget()

        musicPerPage = 7
        musicList = [music for music in os.listdir(self.app.musics)
                     if os.path.splitext(os.path.join(self.app.musics, music))[-1] == '.mp3']

        for child in dashboard.winfo_children():
            child.destroy()

        for musicIndex in range(start := musicPerPage*(page-1), end := musicPerPage*page):
            try:
                label = self.app.making_widget('Label')(dashboard, font=self.app.font_get(self.fontSize),
                                                        text=self.app.delete_extension(musicList[musicIndex]), bg='lightblue', anchor='w',
                                                        width=get_number())
                play = EffectButton(('aqua', 'black'), dashboard, bg='lightblue',
                                    image=self.app.tk_image(os.path.join(
                                        'sys', 'music\\play.png'), width=int(self.fontSize*4/3)),
                                    command=lambda args=musicList[musicIndex]: self.playAMusic(args))
                label.bind('<Enter>', lambda event, args=musicIndex -
                           start+1, play_=play: enter(event, args, play_))
                label.bind('<Leave>', lambda event,
                           play_=play: leave(event, play_))
                label.grid(row=musicIndex-start+1, column=1, sticky='we')
            except IndexError:

                if musicIndex == start:
                    self.app.making_widget('Label')(dashboard,
                                                    font=self.app.font_get(50), text='Empty!', bg='lightblue',
                                                    fg='red').grid()
                    break

        dashboard.bind('<Leave>', dashboardleave)

    def __set_page(self, page=0, extend_func=None):
        if extend_func:
            if extend_func == 'right':
                if (now := self.__page_number.get()) == 5:
                    self.app.soundeffects['wrong_01'].play()
                else:
                    self.__page_number.set(now+1)
            elif extend_func == 'left':
                if (now := self.__page_number.get()) == 1:
                    self.app.soundeffects['wrong_01'].play()
                else:
                    self.__page_number.set(now-1)
        else:
            self.__page_number.set(page)
        self.__load_music_list(self.listFrame, self.__page_number.get())
    # ---------------------------------------------------------------------------------

    def get_mp3_info(self, filename, info):
        '''
        info(str){length, bitrate}
        '''
        return eval(f'MP3(os.path.join(self.app.musics, filename)).info.{info}')

    def build_initial_layout(self):
        '''
        canvas, canvas_side
        '''

        # auto play
        try:
            self.playAMusic(random.choice(os.listdir(self.app.musics)))
        except:
            pass
        # auto play

        self.canvas = self.app.music_canvas
        self.canvas_side = int(self.canvas['width']), int(
            self.canvas['height'])

        cumulateHeight = 0

        def header():
            '''
            This do icon and title
            '''
            nonlocal cumulateHeight
            fit_height = self.__get_balance_height(
                self.canvas_side[0], 'Music List')  # for not to deformed
            cumulateHeight += fit_height
            self.canvas.create_image(
                0, 0, image=self.app.tk_image('sys\\music\\musicplayer.ico', fit_height), anchor='nw',
                tags=('musicplayer', 'musicplayericon'))
            self.canvas.create_text(fit_height, 0, text='Music List', anchor='nw', font=self.app.font_get(
                self.app.font_span(self.canvas_side[0]-fit_height, 'Music List')), tags=('musicplayer', 'musicplayertitle'))
            self.canvas.create_line(0, cumulateHeight, self.canvas_side[0], cumulateHeight, width=2, tags=('musicplayer',
                                                                                                           'musicplayerline1'))
            cumulateHeight += 2 + 1

        def playing():
            '''
            This do now playing indication
            '''
            def pause():
                pygame.mixer.music.pause()
                self.canvas.itemconfigure(
                    'musicplayerplaybutton-pause', state='hidden')
                self.canvas.itemconfigure(
                    'musicplayerplaybutton-play', state='normal')
            pause()

            def play():
                if self.__pass_time.get() == '00:00':
                    self.playAMusic(self.__music_now.get()+'.mp3')
                    return
                pygame.mixer.music.unpause()
                self.canvas.itemconfigure(
                    'musicplayerplaybutton-pause', state='normal')
                self.canvas.itemconfigure(
                    'musicplayerplaybutton-play', state='hidden')

            nonlocal cumulateHeight
            self.canvas.create_window(self.canvas_side[0]//2, cumulateHeight, anchor='n', window=self.app.making_widget(
                'Label')(self.canvas, font=self.app.font_get(self.fontSize), bg='lightblue', textvariable=self.__music_now),
                tags=('musicplayer', 'musicplayernow')
            )
            cumulateHeight += self.fontSize * 4 / 3
            self.canvas.create_rectangle(self.canvas_side[0]*0.2, cumulateHeight, self.canvas_side[0]*0.8, cumulateHeight+50,
                                         width=0, tags=('musicplayer', 'musicplayerdurationrec'))
            self.canvas.tag_bind('musicplayerdurationrec',
                                 '<Enter>', lambda event: self.__enter_rec.set(1))
            self.canvas.tag_bind('musicplayerdurationrec',
                                 '<Leave>', lambda event: self.__enter_rec.set(0))
            cumulateHeight += 25
            self.canvas.create_line(self.canvas_side[0]*0.2, cumulateHeight, self.canvas_side[0]*0.8, cumulateHeight, width=1,
                                    tags=('musicplayer', 'musicplayerdurationbar'))
            self.canvas.create_window(self.canvas_side[0]*0.1, cumulateHeight, window=self.app.making_widget(
                'Label')(self.canvas, font=self.app.font_get(self.fontSize), bg='lightblue', textvariable=self.__pass_time),
                tags=('musicplayer', 'musicplayertimer')
            )
            self.canvas.create_window(self.canvas_side[0]*0.9, cumulateHeight, window=self.app.making_widget(
                'Label')(self.canvas, font=self.app.font_get(self.fontSize), bg='lightblue', textvariable=self.__length),
                tags=('musicplayer', 'musicplayerlength')
            )
            cumulateHeight += 25
            self.canvas.create_line(0, cumulateHeight, self.canvas_side[0], cumulateHeight, width=2, tags=('musicplayer',
                                                                                                           'musicplayerline2'))
            self.canvas.create_window(self.canvas_side[0]/2, cumulateHeight, anchor='s', window=EffectButton(
                ('aqua', 'black'), self.canvas, command=pause, bg='lightblue', image=self.app.tk_image(
                    'sys\\music\\pause.png', height=15
                )), tags=('musicplayer', 'musicplayerplaybutton-pause'))
            self.canvas.create_window(self.canvas_side[0]/2, cumulateHeight, anchor='s', window=EffectButton(
                ('aqua', 'black'), self.canvas, command=play, bg='lightblue', image=self.app.tk_image(
                    'sys\\music\\play.png', height=15
                )), tags=('musicplayer', 'musicplayerplaybutton-play'), state='hidden')
            cumulateHeight += 3

        def music_list():
            '''
            This do music list frame
            '''
            nonlocal cumulateHeight
            self.listFrame = self.app.making_widget('Frame')(self.canvas, width=self.canvas_side[0],
                                                             height=self.canvas_side[1]-50-cumulateHeight, bg='lightblue')
            self.canvas.create_window(0, cumulateHeight, window=self.listFrame, anchor='nw', tags=('musicplayer',
                                                                                                   'musicplayerlistframe'))
            cumulateHeight = 450
            self.canvas.create_line(0, cumulateHeight, self.canvas_side[0], cumulateHeight, width=3, tags=('musicplayer',
                                                                                                           'musicplayerline3'))
            cumulateHeight += 3

        def change_page():
            '''
            This do page change function
            '''
            # start = 15, interval 10 real width 30
            # start = 3
            nonlocal cumulateHeight

            for i in range(1, 6):
                self.canvas.create_window(15+40*(i-1), self.canvas_side[1], window=self.app.making_widget('Radiobutton')(self.canvas, bg='white', indicatoron=0, variable=self.__page_number, value=i, selectcolor='purple', width=2,
                                                                                                                         font=self.app.font_get(self.fontSize), text=str(i), command=lambda args=i: self.__set_page(args)), anchor='sw',
                                          tags=('musicpplayer', f'musicplayerpagebutton{i}'))
            self.canvas.create_window(*self.canvas_side, window=EffectButton(('aqua', 'black'), self.canvas, bg='lightblue',
                                                                             image=self.app.tk_image('sys\\music\\right.png', 27), command=lambda args='right': self.__set_page(extend_func=args)), tags=('musicplayer', 'musicplayerrightbutton'), anchor='se')
            self.canvas.create_window(self.canvas_side[0]-27-10, self.canvas_side[1], window=EffectButton(('aqua', 'black'), self.canvas, bg='lightblue',
                                                                                                          image=self.app.tk_image('sys\\music\\left.png', 27), command=lambda args='left': self.__set_page(extend_func=args)), tags=('musicplayer', 'musicplayerrightbutton'), anchor='se')

        header()
        playing()
        music_list()
        change_page()
        self.__set_page(1)

    def playAMusic(self, file):
        try:
            self.canvas.itemconfigure(
                'musicplayerplaybutton-pause', state='normal')
            self.canvas.itemconfigure(
                'musicplayerplaybutton-play', state='hidden')
        except:
            pass

        self.__length.set(self.__second_fmt_change(
            self.get_mp3_info(file, 'length')))
        self.__music_now.set(self.app.delete_extension(file))
        pygame.mixer.music.load(os.path.join(self.app.musics, file))
        pygame.mixer.music.play()

    # ---- need put in while loop ----
    def set_ball(self):
        time_pass = pygame.mixer.music.get_pos() / 1000

        self.__music_now_label_change_color(
            self.listFrame, self.__music_now.get())
        self.__pass_time.set(self.__second_fmt_change(
            time_pass
        ))

        self.canvas.delete('musicplayerdurationball')
        ball_r = 3
        progress = time_pass / self.__second_fmt_change(
            self.__length.get())  # ratio
        a, b, c, d = self.canvas.coords('musicplayerdurationbar')
        center = (c-a)*progress

        if self.__enter_rec.get():
            self.canvas.create_oval(
                a+center-ball_r*3, b-ball_r*3, a+center+ball_r*3, b+ball_r*3, fill='white', tags=('musicplayer', 'musicplayerdurationball')
            )

        else:
            self.canvas.create_oval(
                a+center-ball_r, b-ball_r, a+center+ball_r, b+ball_r, fill='black', tags=('musicplayer', 'musicplayerdurationball')
            )
