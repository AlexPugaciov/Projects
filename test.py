
import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo


class MyBtn(tk.Button):
    def __init__(self, master, x, y, num, *args, **kwargs):
        super(MyBtn, self).__init__(master, *args, **kwargs)
        self.x = x
        self.y = y
        self.is_mine = False
        self.number = num

    def __repr__(self):
        return f"{self.number}"


class MineSvipper:
    window = tk.Tk()
    window.title('Minesweeper')
    row: int = 5
    columns: int = 5
    mines: int = 5


    def __init__(self):
        self.count: int = 1
        self.buttons_clic: list = list()
        self.buttons: list = list()
        self.bomb_btns: list = list()
        self.start()
        self.menu()
        self.insert_mines()
        self.neighbor()
        self.all_cells = self.row * self.columns
        self.window.mainloop()

    def reload(self):

        [elem.destroy() for elem in self.window.winfo_children()]

        self.__init__()

    def start(self):
        for i in range(self.row + 2):
            temp = []
            tk.Misc.rowconfigure(self.window, i, weight=1)
            for j in range(self.columns + 2):
                tk.Misc.columnconfigure(self.window, i, weight=1)
                if j == 0 or i == 0 or j == self.columns + 1 or i == self.row + 1:
                    btn = MyBtn(self.window, x=i, y=j, num='x')
                else:
                    btn = MyBtn(self.window, width=3, x=i, y=j, num=self.count, font='Calibri 15 bold')
                    btn.config(command=lambda click_btn=btn: self.click(click_btn))
                    self.count += 1
                    btn.bind('<Button-3>', self.right_click)
                    btn.grid(row=i, column=j, sticky='wens')
                temp.append(btn)
            self.buttons.append(temp)

    def menu(self):
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)
        set_menu = tk.Menu(menubar, tearoff=0)
        set_menu.add_command(label='Restart', command=self.reload)
        set_menu.add_command(label='Config', command=self.settings)
        set_menu.add_command(label='Exit', command=self.window.destroy)
        menubar.add_cascade(label="File", menu=set_menu)

    def settings(self):
        win_settings = tk.Toplevel(self.window)
        win_settings.title('Settings')
        entry_row = tk.Entry(win_settings)
        entry_row.insert(0, str(self.row))
        entry_row.grid(row=0, column=1, padx=20, pady=20)
        entry_column = tk.Entry(win_settings)
        entry_column.insert(0, str(self.columns))
        entry_column.grid(row=1, column=1, padx=20, pady=20)
        entry_bomb = tk.Entry(win_settings)
        entry_bomb.insert(0, str(self.mines))
        entry_bomb.grid(row=2, column=1, padx=20, pady=20)
        tk.Label(win_settings, text='Rows').grid(row=0, column=0)
        tk.Label(win_settings, text='Columns').grid(row=1, column=0)
        tk.Label(win_settings, text='Bombs').grid(row=2, column=0)
        tk.Button(win_settings, text='apply',
                  command=lambda: self.apply_setings(entry_row.get(), entry_column.get(), entry_bomb.get())). \
            grid(row=3, column=0, columnspan=2)

    def apply_setings(self, row, col, bomb):
        MineSvipper.row = int(row)
        MineSvipper.columns = int(col)
        MineSvipper.mines = int(bomb)
        self.reload()

    def right_click(self, event):
        btn = event.widget
        if not btn['state'] == 'disabled':
            if btn['text'] == 'B':
                btn['text'] = ''
            else:
                btn['text'] = 'B'
                btn['fg'] = 'red'

    def click(self, btn: MyBtn):
        color = ('pink', 'green', 'orange', 'blue', 'purple', 'yellow', 'red', 'navy')
        if btn.is_mine:
            [btn.config(text='BUM', bg='red', state='disabled', disabledforeground='black') for btn in self.bomb_btns]
            for row in self.buttons:
                [btn.config(state='disabled') for btn in row]
            showinfo('Game over', 'YOU LOSE')

        elif btn.number == '0':
            btn.config(disabledforeground=color[int(btn.number)], relief=tk.SUNKEN,
                       text='', state='disabled', bg='#DACECE')
            self.buttons_clic.append(btn)
            self.all_cells-=1
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if self.buttons[btn.x + dx][btn.y + dy] not in self.buttons_clic and\
                            self.buttons[btn.x + dx][btn.y + dy].number.isdigit():
                        self.click(self.buttons[btn.x + dx][btn.y + dy])
        else:
            btn.config(disabledforeground=color[int(btn.number)], relief=tk.SUNKEN, text=btn.number, state='disabled')
            self.buttons_clic.append(btn)
            self.all_cells -= 1
            if self.all_cells == self.mines:
                [btn.config(text='BUM', bg='red', state='disabled', disabledforeground='black') for btn in
                 self.bomb_btns]
                showinfo('Game over', 'YOU WIN')

    def neighbor(self):
        for i in range(1, self.row + 1):
            for j in range(1, self.columns + 1):
                if not self.buttons[i][j].is_mine:
                    num_bomb = 0
                    for i_dx in (-1, 0, 1):
                        for j_dx in (-1, 0, 1):
                            if self.buttons[i + i_dx][j + j_dx].is_mine:
                                num_bomb += 1
                    self.buttons[i][j].number = str(num_bomb)
                else:
                    self.buttons[i][j].number = '*'

    def insert_mines(self):
        bombs = self.get_mines_places()
        for btn in self.buttons:
            for b in btn:
                if b.number in bombs:
                    b.is_mine = True
                    self.bomb_btns.append(b)

    def get_mines_places(self):
        all_cells = list(range(1, self.count))
        shuffle(all_cells)
        return all_cells[:self.mines]


if __name__ == '__main__':
    game = MineSvipper()

