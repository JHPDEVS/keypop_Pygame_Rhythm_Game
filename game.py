


import os.path
import threading
import time

import pygame as pg
import sys
import tkinter as tk
from tkinter import filedialog
import pygame.display
from Settings import *
from os import path
from scipy.fftpack import dct
from math import pi
import sys, math, wave, numpy , random ,colorsys , librosa
note_list = []
N = 7 # num of bars
HEIGHT2 = 64 # height of a bar
WIDTH2 = 64 # width of a barFPS = 60
notes = []
root = tk.Tk()
root.withdraw()
score = 0
combo = 0
count = 0
speed = 5
#
file_name = filedialog.askopenfilename(title="음악을 선택하세요", filetypes=(("wav 음악파일", "*.wav"), ("ogg 음악파일", "*.ogg")))
#file_name = '캐논변주곡.wav'
no_ext_filename,_ = os.path.splitext(file_name)
print(no_ext_filename)
fpsclock = pygame.time.Clock()

# WAV 파일 읽기
f = wave.open(file_name, 'rb') # rb모드는  wave_read 객체 반환(읽기) ,  wb모드는 wave_write (쓰기)
frequency = f.getframerate()
params = f.getparams() #  nchannels, sampwidth, framerate, nframes, comptype, compname 반환
nchannels, sampwidth, framerate, nframes = params[:4]
str_data  = f.readframes(nframes) # 최대 n프레임의 오디오를 bytes 객체로 읽고 반환


wave_data = numpy.frombuffer(str_data, dtype = numpy.short) # 데이터형태가 short인걸 numpy array로 데이터 변경시켜줌
wave_data.shape = -1,2
wave_data = wave_data.T
w, h = WIDTH,HEIGHT
note_list = []
z = 0
isPause =0
# librosa
x , sr = librosa.load(file_name)
onset_frames = librosa.onset.onset_detect(x, sr=sr, wait=1, pre_avg=1, post_avg=1, pre_max=1, post_max=1)
onset_times = librosa.frames_to_time(onset_frames)
duration = librosa.get_duration(filename=file_name)
if os.path.isfile(no_ext_filename+'.txt'):
    print("onset파일이 있습니다 넘어갑니다")
else:
    with open(no_ext_filename + '.txt', 'wt') as f:
        f.write('\n'.join(['%.4f' % onset_time for onset_time in onset_times]))
        f.close()
if os.path.isfile(no_ext_filename+'_노트.txt'):
    print("노트 파일이 있습니다 넘어갑니다")
else:
    print("노트 파일 생성")
    with open(no_ext_filename + '_노트.txt', 'wt') as f:
        f.write('\n'.join([str(64 * random.randrange(7)) for _ in range(len(onset_times))]))
        f.close()


class Game:
    def __init__(self):
        self.state = "intro"
        pg.init()
        self.basic_font = pg.font.Font('AppleSDGothicNeoM.ttf', 15)  # 폰트 설정
        self.title_font = pg.font.Font('AppleSDGothicNeoL.ttf', 15)  # 폰트 설정
        self.combo_font = pg.font.Font('Game Of Squids.ttf', 30)  # 폰트 설정
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        # self.aImage = pg.display.
        self.note_group = pg.sprite.Group
        self.note = pg.image.load("note.png")
        self.note1 = pg.image.load("note.png")
        self.note2 = pg.image.load("note2.png")
        self.note3 = pg.image.load("note3.png")
        self.note4 = pg.image.load("note4.png")
        self.perfect = pg.image.load("perfect.png")
        self.grate = pg.image.load("great.png")
        self.cool = pg.image.load("cool.png")
        self.nope = pg.image.load("blank.png")
        self.miss = pg.image.load("miss.png")
        self.circle = pygame.draw.rect(self.screen, self.rainbowColor(0),[0 , 0, 20, 20], 20, 20, 20, 20)
        self.a = pg.image.load("A.png")
        self.s = pg.image.load("S.png")
        self.d = pg.image.load("D.png")
        self.space = pg.image.load("Space.png")
        self.j = pg.image.load("J.png")
        self.k = pg.image.load("K.png")
        self.l = pg.image.load("L.png")
        self.bar = pg.image.load("bar.png")
        self.bar2 = pg.image.load("bar2.png")
        self.value = False
        self.aNote = []
        self.sNote = []

        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()

    def load_music_data(self):
        self.onset_times = self.read_beatmap_file() #음악 노트타이밍 불러오기
        self.onset_nums = self.read_note_file()  # 음악 노트 불러오기
        self.num_notes = len(self.onset_times)
        self.notes = [self.onset_times,self.onset_nums]
        for index,value in enumerate(self.onset_nums):
            if value==0:
                self.aNote.append(index)
            if value==65:
                self.sNote.append(index)

    def visualizer(self,num):
        num = int(num)
        h = abs(dct(wave_data[0][nframes - num:nframes - num + N]))
        h = [min(HEIGHT2, int(i ** (1 / 2.5) * HEIGHT2 / 100)) for i in h]
        self.screen.blit(self.nope, (36, 220))
        self.draw_bars(h)


    def rainbowColor(self , x):
        color = [[218, 94, 124], [237, 151, 39], [129, 240, 213], [129, 182, 240], [129, 240, 213],[237, 151, 39],[218, 94, 124]]
        value = int(x/64)
        if x<=384:
            return color[value]
        else:
            return color[0]

    def vis(self):
            self.num -= framerate / 60
            if self.num > 0:
                self.visualizer(self.num)
                self.screen.blit(self.info, (448 - 70, 768 - 108))
                self.screen.blit(self.musicTitle, (20, 768 - 112))
                self.screen.blit(self.score, (14, 14))
                self.screen.blit(self.combo, (140, 590))
                self.screen.blit(self.fullnote, (14, 590))
                self.screen.blit(self.speed, (350, 590))
            else:
                self.screen.blit(self.score, (448/2-15, 450))
            pygame.display.flip()

    def get_time(self):
        seconds = max(0, pygame.mixer.music.get_pos() / 1000)
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        hms = ('%02d:%02d' % (m, s))
        return hms

    def get_current_time(self):
        seconds = max(0, pygame.mixer.music.get_pos() /1000)
        return seconds
    def draw_bars(self,h):
        bars = []
        global notes
        global count
        global combo
        global speed
        notes.clear()
        for i in h:
            bars.append([len(bars) * WIDTH2,  768 - i, WIDTH2 - 1, i])
        for i in bars:
            pygame.draw.rect(self.screen, self.rainbowColor(0), i, int(pi/2),3,3,3)
            note_list.append([i[0],0,i[3]])
        for i in range(0,self.num_notes):
            if self.get_current_time() >= self.notes[0][i]:
                # self.screen.blit(self.note_circle, (note_list[1][i], note_list[i][1]))
                # self.note_group.add(self.note_circle)
                if note_list[i][1]<=620:
                    notes.append(pygame.draw.rect(self.screen, self.rainbowColor(self.notes[1][i]),[self.notes[1][i] + 20,note_list[i][1],20,20], 5,20,20,20))
                    note_list[i][1] += speed
                    t= threading.Thread(target=self.ifMiss)
                    t.start()
        self.screen.blit(self.bar2, (0, 570))
        if (self.get_current_time() <= 5):
            self.screen.blit(self.a, self.a_rect)
            self.screen.blit(self.s, self.s_rect)
            self.screen.blit(self.d, self.d_rect)
            self.screen.blit(self.space, self.space_rect)
            self.screen.blit(self.j, self.j_rect)
            self.screen.blit(self.k, self.k_rect)
            self.screen.blit(self.l, self.l_rect)

    def ifMiss(self):
        global notes
        global combo
        if notes[0].top >= 618:
                self.nope = pg.image.load("blank.png")
                # 벽 넘어가면 Miss 뜨게 하였으나 버그가 많아 일시적으로 비활성...
                if self.value == False:
                    self.nope = self.miss
                    combo = 0
                    notes.pop(0)
                    time.sleep(1000)
                else:
                    self.value = False
                    notes.pop(0)
                    time.sleep(1000)

    def run(self):
        global score
        global combo
        global count
        global speed
        global duration
        self.playing = True
        while self.playing:

            self.events()
            self.draw()
            if(self.state == "main_game"):
                self.info = self.basic_font.render(self.get_time(), True,(0,0,0))
                self.musicTitle = self.title_font.render(no_ext_filename, True, (0, 0, 0))
                self.score =  self.combo_font.render(str(score), True, (0, 0, 0))
                self.fullnote = self.title_font.render(str(count)+ "/"+str(self.num_notes), True, (0, 0, 0))
                self.combo = self.combo_font.render("Combo : "+str(combo), True, (0, 0, 0))
                self.speed = self.title_font.render("현재 속도 : " + str(speed), True, (0, 0, 0))
                self.timebar = pygame.draw.rect(self.screen,self.rainbowColor(0),[0,0,448 *((self.get_current_time()/duration)),10])
                fpsclock.tick(60)
                self.vis()


    def quit(self):
        pg.quit()
        sys.exit()

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        if(self.get_current_time() >=5):
            self.screen.blit(self.bar, self.bar_rect)


    def intro(self):
        # 화면 그리기
        self.background = pg.image.load("main_menu.png")
        self.screen.blit(self.background, (0, 0))

        self.events()
        pg.display.flip()
    def main_game(self):
        # 화면 그리기

        ##########################################
        # ASD SPACE JKL 충돌범위 지정              #
        self.a_rect = self.a.get_rect()
        self.a_rect.left = 8
        self.a_rect.top = 544

        self.s_rect = self.s.get_rect()
        self.s_rect.left = 72
        self.s_rect.top = 544

        self.d_rect = self.d.get_rect()
        self.d_rect.left = 138
        self.d_rect.top = 544

        self.space_rect = self.space.get_rect()
        self.space_rect.left = 202
        self.space_rect.top = 544

        self.j_rect = self.j.get_rect()
        self.j_rect.left = 266
        self.j_rect.top = 544

        self.k_rect = self.k.get_rect()
        self.k_rect.left = 330
        self.k_rect.top = 544

        self.l_rect = self.l.get_rect()
        self.l_rect.left = 394
        self.l_rect.top = 544

        self.bar_rect = self.bar.get_rect()
        self.bar_rect.left = 0
        self.bar_rect.top = 544

        ########################################
        pygame.mixer.init(frequency=frequency)
        pygame.mixer.music.load(file_name)
       # self.beep = pygame.mixer.Sound("beep.wav")
        pygame.mixer.music.play()  # -1시 게임음악 반복재생
        pygame.mixer.music.set_endevent()
        self.background = pg.image.load("main_ground.png")
        self.screen.blit(self.background, (0, 0))
        self.load_music_data()





        g.run()

    def state_manager(self):
        if self.state == 'intro':
            self.intro()

        if self.state == 'main_game':
            self.main_game()

    def read_beatmap_file(self):
        # read newline separated floats
        with open(no_ext_filename+".txt", 'rt') as f:
            text = f.read()
        onset_times = [float(string) for string in text.split('\n') if string != '']

        return onset_times

    def read_note_file(self):
        with open(no_ext_filename + "_노트.txt", 'rt') as f:
            text = f.read()
        onset_num = [int(string) for string in text.split('\n') if string != '']

        return onset_num

    def events(self):
        # catch all events here
        global isPause;
        global notes
        global score
        global combo
        global count
        global speed
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            elif event.type == pg.KEYDOWN and self.state != "intro":
                if event.key == pg.K_ESCAPE:
                   self.quit()
                if event.key == pg.K_a:
                  #  self.beep.play()
                    self.note = self.note1
                    self.screen.blit(self.note, (0, 0))
                    for i in notes:
                        if(self.a_rect.colliderect(i)):
                            if abs(self.a_rect.top - i.top) < 10:
                                self.nope = self.perfect
                                if combo >= 1:
                                    score = score + (1000 * combo)
                                else:
                                    score = score + 1000
                            elif abs(self.a_rect.top - i.top) <= 15:
                                self.nope = self.grate

                                if combo >= 1:
                                    score = score + (500 * combo)
                                else:
                                    score = score + 500
                            else:
                                self.nope = self.cool
                                if combo >= 1:
                                    score = score + (300 * combo)
                                else:
                                    score = score + 300
                            count = count +1
                            combo = combo +1
                            i.top = 620
                            self.value = True
                            notes.clear()
                        # else:
                        #     if abs(self.a_rect.top - i.top) <=40:
                        #         self.nope = self.miss
                        #
                        #     print(abs(self.a_rect.top - i.top))
                    pg.display.flip()
                if event.key == pg.K_s:
                    self.note = self.note2
                    self.screen.blit(self.note,(64,0))
                    for i in notes:
                        if (self.s_rect.colliderect(i)):
                            if abs(self.s_rect.top - i.top) < 10:
                                self.nope = self.perfect
                                if combo >= 1:
                                    score = score + (1000 * combo)
                                else:
                                    score = score + 1000
                            elif abs(self.s_rect.top - i.top) <= 15:
                                self.nope = self.grate
                                if combo >= 1:
                                    score = score + (500 * combo)
                                else:
                                    score = score + 500
                            else:
                                self.nope = self.cool
                                if combo >= 1:
                                    score = score + (300 * combo)
                                else:
                                    score = score + 300
                            i.top = 620
                            notes.clear()
                            self.value = True
                            combo = combo + 1
                            count = count +1
                    pg.display.flip()
                if event.key == pg.K_d:
                   # self.beep.play()
                    self.note = self.note3
                    self.screen.blit(self.note,(128,0))
                    for i in notes:
                        if (self.d_rect.colliderect(i)):
                            if abs(self.d_rect.top - i.top) < 10:
                                self.nope = self.perfect
                                if combo >= 1:
                                    score = score + (1000 * combo)
                                else:
                                    score = score + 1000
                            elif abs(self.d_rect.top - i.top) <= 15:
                                self.nope = self.grate
                                if combo >= 1:
                                    score = score + (500 * combo)
                                else:
                                    score = score + 500
                            else:
                                self.nope = self.cool
                                if combo >= 1:
                                    score = score + (300 * combo)
                                else:
                                    score = score + 300
                            i.top = 620
                            notes.clear()
                            self.value = True
                            count = count +1
                            combo = combo + 1
                    pg.display.flip()
                if event.key == pg.K_j:
                 #   self.beep.play()
                    self.note = self.note3
                    self.screen.blit(self.note,(258,0))
                    for i in notes:
                        if (self.j_rect.colliderect(i)):
                            if abs(self.j_rect.top - i.top) < 10:
                                self.nope = self.perfect
                                if combo >= 1:
                                    score = score + (1000 * combo)
                                else:
                                    score = score + 1000
                            elif abs(self.j_rect.top - i.top) <= 15:
                                self.nope = self.grate
                                if combo >= 1:
                                    score = score + (500 * combo)
                                else:
                                    score = score + 500
                            else:
                                self.nope = self.cool
                                if combo >= 1:
                                    score = score + (300 * combo)
                                else:
                                    score = score + 300
                            i.top = 620
                            notes.clear()
                            self.value = True
                            count = count +1
                            combo = combo + 1
                    pg.display.flip()
                if event.key == pg.K_k:
                #    self.beep.play()
                    self.note = self.note2
                    self.screen.blit(self.note,(312,0))
                    for i in notes:
                        if (self.k_rect.colliderect(i)):
                            if abs(self.k_rect.top - i.top) < 10:
                                self.nope = self.perfect
                                if combo >= 1:
                                    score = score + (1000 * combo)
                                else:
                                    score = score + 1000
                            elif abs(self.k_rect.top - i.top) <= 15:
                                self.nope = self.grate
                                if combo >= 1:
                                    score = score + (500 * combo)
                                else:
                                    score = score + 500
                            else:

                                self.nope = self.cool
                                if combo >= 1:
                                    score = score + (300 * combo)
                                else:
                                    score = score + 300
                            i.top = 620
                            notes.clear()
                            self.value = True
                            count = count +1
                            combo = combo + 1
                    pg.display.flip()
                if event.key == pg.K_EQUALS:
                    if speed ==6:
                        speed = speed+4
                    elif speed ==5:
                        speed = speed+1
                if event.key == pg.K_MINUS:
                    if speed == 10:
                        speed = speed - 4
                    elif speed == 6:
                        speed = speed -1
                if event.key == pg.K_l:
                #    self.beep.play()
                    self.note = self.note1
                    self.screen.blit(self.note,(380,0))
                    for i in notes:
                        if (self.l_rect.colliderect(i)):
                            if abs(self.l_rect.top - i.top) < 10:
                                self.nope = self.perfect
                                if combo >= 1:
                                    score = score + (1000 * combo)
                                else:
                                    score = score + 1000
                            elif abs(self.l_rect.top - i.top) <= 15:
                                self.nope = self.grate
                                if combo >= 1:
                                    score = score + (500 * combo)
                                else:
                                    score = score + 500
                            else:
                                self.nope = self.cool
                                score = score + 300
                            i.top = 620
                            notes.clear()
                            print(abs(self.l_rect.top - i.top))
                            self.value = True
                            count = count +1
                            combo = combo + 1
                    pg.display.flip()
                if event.key == pg.K_SPACE:
                 #   self.beep.play()
                    self.note = self.note4
                    self.screen.blit(self.note,(192,0))
                    for i in notes:
                        if (self.space_rect.colliderect(i)):
                            if abs(self.space_rect.top - i.top) < 10:
                                self.nope = self.perfect
                                if combo >= 1:
                                    score = score +( 1000 * combo)
                                else:
                                    score = score + 1000
                            elif abs(self.space_rect.top - i.top) <= 15:
                                self.nope = self.grate
                                if combo >= 1:
                                    score = score + (500 * combo)
                                else:
                                    score = score + 500
                            else:
                                self.nope = self.cool
                                if combo >= 1:
                                    score = score + (300 * combo)
                                else:
                                    score = score + 300
                            i.top = 620
                            notes.clear()
                            print(notes)
                            print(abs(self.space_rect.top - i.top))
                            self.value = True
                            count = count +1
                            combo = combo + 1
                    pg.display.flip()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.state = 'main_game'



# PLAY Game
g = Game()
g.num = nframes
while True:
    g.state_manager()