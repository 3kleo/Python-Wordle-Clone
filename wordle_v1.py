# OOP
from unidecode import unidecode
from random import choice
from tkinter import *
from tkinter.font import Font
from time import sleep

# set languange for game on line 51


class Wordle:
    def __init__(self, width, height):
        self.top_word = None
        self.top_box = None
        self.keyboard_dict = None
        self.keyboard_keys = None
        self.canvas = None
        self.root = None
        self.width, self.height = width, height
        self.box_height = 70
        self.box_width = 70
        self.gap = 10
        self.pos_x = (self.width - (self.box_width * 5) - (self.gap * 4)) / 2
        self.new_pos_x = self.pos_x
        self.pos_y = 100
        self.new_pos_y = self.pos_y
        self.block = self.box_width + self.gap
        self.color_right = '#3aa394'
        self.color_place = '#d3ad69'
        self.color_wrong = '#312a2c'
        self.color_wrongFG = '#504a4b'
        self.color_empty = '#615458'
        self.color_kb = '#4c4347'
        self.color_help = '#312b2d'
        self.color_end_box = '#009afe'
        self.color_bg = '#6e5c62'
        self.font = "Exo 2.0"
        self.row_counter = 0
        self.column_counter = 0
        self.guess = ''
        self.kb_box_height = self.box_height * 0.7
        self.kb_box_width = self.box_width * 0.7
        self.kb_gap = 8
        self.kb_pos_x = (self.width - (self.kb_box_width * 10) - (self.kb_gap * 9)) / 2
        self.kb_new_pos_x = self.kb_pos_x
        self.kb_pos_y = self.pos_y + ((self.box_height + self.gap) * 6) * 1.02
        self.kb_new_pos_y = self.kb_pos_y
        self.kb_block = self.kb_box_width + self.kb_gap
        self.kb_row_counter = 0
        self.kb_column_counter = 0
        self.game_language = 'ptbr'  # supported: brazilian portuguese ('ptbr') and english ('en')
        self.end_game_words = ["Genial", "Fantástico", "Extraordinário", "Fenomenal", "Impressionante"] if self.game_language == 'ptbr' \
            else ["Genius", "Magnificent", "Impressive", "Splendid", "Great"]
        with open('words_' + self.game_language + '.txt', 'r', encoding='utf-8') as a:
            self.words = [unidecode(x.upper()) for x in a.read().split(', ')]
        self.word = choice(self.words)
        with open('accepted_words_' + self.game_language + '.txt', 'r', encoding='utf-8') as a:
            self.accepted_answers = [unidecode(x.upper()) for x in a.read().split(', ')]
        self.words.extend(self.accepted_answers)
        self.invalid_message = 'Palavra inválida' if self.game_language == 'ptbr' else 'Not in word list'
        self.game_on = True
        self.delay = 0.4

    def generate_gui(self):
        self.root = Tk(className=" Wordle Clone")
        self.canvas = Canvas(self.root, height=self.height, width=self.width, bg=self.color_bg)
        self.canvas.pack(expand=True)

        self.create_letter_boxes()
        self.special_keys()
        self.generate_keyboard()

        # title
        self.canvas.create_text((self.width / 2,
                                 self.pos_y / 5),
                                text='WORDLE CLONE',
                                font=(self.font, int(self.kb_box_height * 0.6)),
                                fill='white')

        # event listeners
        self.root.bind('<KeyPress>', self.kb_input)
        self.root.bind('<BackSpace>', self.kb_delete)
        self.root.bind('<Return>', self.kb_enter)

        self.root.mainloop()

    def create_letter_boxes(self):
        for y in range(7):
            for x in range(5):
                self.new_pos_x = self.pos_x + ((self.box_width + self.gap) * x)
                self.new_pos_y = self.new_pos_y
                self.create_box(self.new_pos_x, self.new_pos_y, self.box_width, self.box_height, self.color_empty)

            self.new_pos_y = self.pos_y + ((self.box_height + self.gap) * y)
            self.new_pos_x = self.pos_x

    def generate_keyboard(self):
        self.keyboard_keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
                              ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
                              ["Z", "X", "C", "V", "B", "N", "M"]]
        self.keyboard_dict = {}

        for r, key_row in enumerate(self.keyboard_keys):
            for i, key in enumerate(key_row):
                # create box
                self.keyboard_dict[key] = {'r': r, 'i': i}
                self.create_kb_key(key, self.color_kb)

    def kb_input(self, event=None, letter=None):
        if self.game_on:
            if letter is None:
                letter = unidecode(event.char.upper())
            if self.column_counter == 0:
                self.guess = ''
            if 0 <= self.column_counter < 5 and letter.isalpha():
                self.guess = self.guess + letter
                self.write_letters((self.pos_x + (self.block * self.column_counter)) + self.box_width * 0.5,
                                   (self.pos_y + ((self.gap + self.box_height) * self.row_counter)) + self.box_height * 0.5,
                                   letter,
                                   self.box_height)
                self.column_counter += 1

    # delete letters
    def kb_delete(self, event):
        if self.game_on:
            if self.column_counter == 0:
                return
            self.column_counter -= 1
            self.guess = self.guess[:-1]
            del_pos_x = self.pos_x + ((self.box_width + self.gap) * self.column_counter)
            del_pos_y = self.pos_y + ((self.box_height + self.gap) * self.row_counter)
            self.create_box(del_pos_x, del_pos_y, self.box_width, self.box_height, self.color_empty)

    def kb_enter(self, event):
        if self.guess in self.words:
            if self.game_on:
                if self.column_counter == 5 and self.row_counter == 5:
                    self.validate_guess()
                    #             print('game over')
                    if self.game_on:
                        self.top_text(self.word, self.color_end_box)
                    self.game_on = False
                elif self.column_counter == 5:
                    #             print(guess)
                    self.validate_guess()
                    self.row_counter += 1
                    self.column_counter = 0
        else:
            self.top_text(self.invalid_message, 'black')
            # sleep(0.5)
            self.root.update()
            self.delete_top_text()
            sleep(1)
            self.root.update()

            return

    def validate_guess(self):
        if self.guess == self.word:
            for i, v in enumerate(self.guess):
                if v == self.word[i]:  # letra na posicao certa
                    new_pos_x = self.pos_x + ((self.box_width + self.gap) * i)
                    new_pos_y = self.pos_y + ((self.box_height + self.gap) * self.row_counter)
                    self.create_box(new_pos_x, new_pos_y, self.box_width, self.box_height, self.color_right)
                    self.write_letters((self.pos_x + (self.block * i)) + (self.box_width * 0.5),
                                       (self.pos_y + ((self.gap + self.box_height) * self.row_counter)) + (self.box_height * 0.5),
                                       v,
                                       self.box_height)
                    self.create_kb_key(v, self.color_right)
                    self.root.update()
                    sleep(self.delay)
            self.game_on = False
            self.top_text(choice(self.end_game_words), self.color_end_box)
            return
        else:
            for i, v in enumerate(self.guess):
                if v == self.word[i]:  # letra na posicao certa
                    new_pos_x = self.pos_x + ((self.box_width + self.gap) * i)
                    new_pos_y = self.pos_y + ((self.box_height + self.gap) * self.row_counter)
                    self.create_box(new_pos_x, new_pos_y, self.box_width, self.box_height, self.color_right)
                    self.write_letters((self.pos_x + (self.block * i)) + (self.box_width * 0.5),
                                       (self.pos_y + ((self.gap + self.box_height) * self.row_counter)) + (self.box_height * 0.5),
                                       v,
                                       self.box_height)
                    self.create_kb_key(v, self.color_right)
                    self.root.update()
                    sleep(self.delay)

                elif v in self.word and self.word.count(v) >= self.guess.count(v):  # esta na palavra
                    new_pos_x = self.pos_x + ((self.box_width + self.gap) * i)
                    new_pos_y = self.pos_y + ((self.box_height + self.gap) * self.row_counter)
                    self.create_box(new_pos_x, new_pos_y, self.box_width, self.box_height, self.color_place)
                    self.write_letters((self.pos_x + (self.block * i)) + (self.box_width * 0.5),
                                       (self.pos_y + ((self.gap + self.box_height) * self.row_counter)) + (self.box_height * 0.5),
                                       v,
                                       self.box_height)
                    self.create_kb_key(v, self.color_place)
                    self.root.update()
                    sleep(self.delay)

                elif v in self.word and self.word.count(v) < self.guess.count(v) and i < self.guess.rfind(v):
                    new_pos_x = self.pos_x + ((self.box_width + self.gap) * i)
                    new_pos_y = self.pos_y + ((self.box_height + self.gap) * self.row_counter)
                    self.create_box(new_pos_x, new_pos_y, self.box_width, self.box_height, self.color_place)
                    self.write_letters((self.pos_x + (self.block * i)) + (self.box_width * 0.5),
                                       (self.pos_y + ((self.gap + self.box_height) * self.row_counter)) + (self.box_height * 0.5),
                                       v,
                                       self.box_height)
                    self.create_kb_key(v, self.color_place)
                    self.root.update()
                    sleep(self.delay)

                else:
                    new_pos_x = self.pos_x + ((self.box_width + self.gap) * i)
                    new_pos_y = self.pos_y + ((self.box_height + self.gap) * self.row_counter)
                    self.create_box(new_pos_x, new_pos_y, self.box_width, self.box_height, self.color_wrong)
                    self.write_letters((self.pos_x + (self.block * i)) + (self.box_width * 0.5),
                                       (self.pos_y + ((self.gap + self.box_height) * self.row_counter)) + (self.box_height * 0.5),
                                       v,
                                       self.box_height)
                    self.create_kb_key(v, self.color_wrong)
                    self.root.update()
                    sleep(self.delay)

    def create_box(self, x, y, box_w, box_h, color):
        self.canvas.create_rectangle(x,
                                     y,
                                     x + box_w,
                                     y + box_h,
                                     outline="",
                                     fill=color)

    def write_letters(self, x, y, letter, h):
        self.canvas.create_text(x,
                                y,
                                text=letter,
                                font=(self.font, int(h * 0.7)),
                                fill='white')

    def create_kb_key(self, letter, color):
        self.canvas.create_rectangle(self.kb_new_pos_x + (self.kb_block * self.keyboard_dict[letter]['i']) +
                                     (self.keyboard_dict[letter]['r'] * (self.kb_box_width * 0.3)),
                                     self.kb_new_pos_y + ((self.kb_box_height + self.kb_gap) * self.keyboard_dict[letter]['r']),
                                     (self.kb_new_pos_x + (self.kb_block * self.keyboard_dict[letter]['i'])) +
                                     self.kb_box_width + (self.keyboard_dict[letter]['r'] * (self.kb_box_width * 0.3)),
                                     self.kb_new_pos_y + ((self.kb_box_height + self.kb_gap) * self.keyboard_dict[letter]['r']) + self.kb_box_height,
                                     outline="",
                                     fill=color,
                                     tags=letter)
        # insert letter
        self.canvas.create_text((self.kb_pos_x + (self.kb_block * self.keyboard_dict[letter]['i']) +
                                 (self.kb_box_width * 0.5) + (self.keyboard_dict[letter]['r'] * (self.kb_box_width * 0.3)),
                                 (self.kb_pos_y + ((self.kb_gap + self.kb_box_height) * self.keyboard_dict[letter]['r'])) +
                                 (self.kb_box_height * 0.5)),
                                text=letter,
                                font=(self.font, int(self.kb_box_height * 0.5)),
                                fill='white',
                                tags=letter)

        self.canvas.tag_bind(letter, "<Button-1>", lambda e, var=letter: self.kb_input(letter=var))

    def top_text(self, top_word, color):
        answer_box_width = Font(family=self.font, size=int(self.kb_box_height * 0.5)).measure(top_word)
        answer_pos_x_1 = (self.width * 0.5 - (answer_box_width / 2)) * 0.98
        answer_pos_x_2 = (answer_pos_x_1 + answer_box_width) * 1.025  # * 0.57
        answer_pos_y_1 = self.pos_y * 0.5  # (((pos_y) - (pos_y / 4)) * 0.95) - answer_pos_y_2
        answer_pos_y_2 = answer_pos_y_1 * 1.9

        self.top_box = self.canvas.create_rectangle(answer_pos_x_1,
                                                    answer_pos_y_1,
                                                    answer_pos_x_2,
                                                    answer_pos_y_2,
                                                    outline="",
                                                    fill=color)

        self.top_word = self.canvas.create_text((self.width / 2,
                                                 (self.pos_y - (self.pos_y / 4)) * 0.95),
                                                text=top_word,
                                                font=(self.font, int(self.kb_box_height * 0.5)),
                                                fill='white')

    def delete_top_text(self):
        self.canvas.delete(self.top_box)
        self.canvas.delete(self.top_word)

    def special_keys(self):
        # positions
        enter_pos_x_1 = self.kb_new_pos_x + (self.kb_block * 7) + (2 * (self.kb_box_width * 0.3))
        # enter_pos_x_2 = (self.kb_new_pos_x + (self.kb_block * 9)) + self.kb_box_width + (2 * (self.kb_box_width * 0.5))
        enter_pos_y_1 = self.kb_new_pos_y + ((self.kb_box_height + self.kb_gap) * 2)
        enter_pos_y_2 = self.kb_new_pos_y + ((self.kb_box_height + self.kb_gap) * 2) + self.kb_box_height

        delete_pos_x_1 = self.kb_new_pos_x + (self.kb_block * 9) + (1 * (self.kb_box_width * 0.3))
        delete_pos_x_2 = (self.kb_new_pos_x + (self.kb_block * 9)) + self.kb_box_width + (1 * (self.kb_box_width * 0.6))
        delete_pos_y_1 = self.kb_new_pos_y + ((self.kb_box_height + self.kb_gap) * 1)
        delete_pos_y_2 = self.kb_new_pos_y + ((self.kb_box_height + self.kb_gap) * 1) + self.kb_box_height

        # enter key
        self.canvas.create_rectangle(enter_pos_x_1,
                                     enter_pos_y_1,
                                     delete_pos_x_2,
                                     enter_pos_y_2,
                                     outline="",
                                     fill=self.color_kb,
                                     tags='ENTER')

        self.canvas.create_text(((enter_pos_x_1 + delete_pos_x_2) / 2,
                                 enter_pos_y_1 + (self.kb_box_height * 0.5)),
                                text='ENTER',
                                font=(self.font, int(self.kb_box_height * 0.5)),
                                fill='white',
                                tags='ENTER')
        # DELETE
        self.canvas.create_rectangle(delete_pos_x_1,
                                     delete_pos_y_1,
                                     delete_pos_x_2,
                                     delete_pos_y_2,
                                     outline="",
                                     fill=self.color_kb,
                                     tags='⌫')

        self.canvas.create_text(((delete_pos_x_1 + delete_pos_x_2) / 2,
                                 delete_pos_y_1 + (self.kb_box_height * 0.5)),
                                text='⌫',
                                font=(self.font, int(self.kb_box_height * 0.5)),
                                fill='white',
                                tags='⌫')

        # bind special keys to action
        self.canvas.tag_bind('ENTER', "<Button-1>", lambda e, var='ENTER': self.kb_enter(var))
        self.canvas.tag_bind('⌫', "<Button-1>", lambda e, var='⌫': self.kb_delete(var))


wordle = Wordle(800, 800)
wordle.generate_gui()
