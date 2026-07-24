import tkinter as tk

from functools import partial
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


class Gui:
    def __init__(self, db):
        self.db = db
        self.actual_frame = None
        # === настройка окна ===
        self.window = tk.Tk()  # окно
        self.window.title('Digital Diary')
        self.window.geometry('1024x768')
        self.window.iconbitmap(default='fav.ico')

        self.main_frame = ttk.Frame(self.window)
        self.main_frame.pack(fill='both', expand=True)

        # === панель меню ===
        self.menu_panel = ttk.Frame(self.main_frame, borderwidth=1, relief='solid')
        self.menu_panel.pack(fill='x', pady=(5, 10), padx=5)
        self.new_entry_btn = ttk.Button(self.menu_panel, text='Новая запись', command=self.new_entry)
        self.new_entry_btn.pack(side='left', padx=5, pady=5)

        # === контейнер для контента ===
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill='both', expand=True)

        # == контейнер для списка записей ==
        self.entrys_panel = ttk.Frame(self.content_frame, borderwidth=1, relief='solid')
        self.entrys_panel.pack(side='left', padx=5, pady=5, fill='both', expand=True)
        # canvas для прокрутки
        self.canvas = tk.Canvas(self.entrys_panel)
        self.canvas.bind("<Configure>", self.configure_frame)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.canvas.pack(side='left', fill='both', expand=True, padx=(3, 0), pady=3)
        # скроллбар
        self.scrollbar = ttk.Scrollbar(self.entrys_panel, orient='vertical', command=self.canvas.yview)
        self.scrollbar.pack(side='right', fill='y', pady=5, padx=(10, 5))
        self.canvas['yscrollcommand'] = self.scrollbar.set

        self.list_frame = ttk.Frame(self.canvas)
        self.list_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            )
        self.list_frame_window = self.canvas.create_window(
            (0, 0),
            window=self.list_frame, anchor='nw'
            )
        self.list_label = ttk.Label(
            self.list_frame,
            text='Список записей',
            anchor='center',
            borderwidth=0.5,
            relief='groove'
            )
        self.list_label.pack(side='top', fill='x', padx=(0, 4), pady=(0, 5))
        # self.a_frame = self.add_frame_show()
        self.show_list_entrys()

    def read_frame(self):
        # == контейнер для чтения записи ==
        r_frame = ttk.Frame(self.content_frame, borderwidth=1, relief='solid')

        def close_button():
            r_frame.pack_forget()

        # номер записи
        entry_id = ttk.Label(r_frame, text='Test id', borderwidth=0.5, relief='ridge')
        entry_id.pack(anchor='nw', padx=5, pady=5)
        # тема
        entry_theme = ttk.Label(r_frame, text='Test theme', borderwidth=0.5, relief='ridge')
        entry_theme.pack(anchor='nw', padx=5, pady=5)
        # крестик
        close_btn = ttk.Button(r_frame, text='❌', command=close_button)
        close_btn.pack(anchor='ne', padx=5, pady=5)
        # дата
        entry_date = ttk.Label(r_frame, text='01.01.1970')
        entry_date.pack(anchor='nw')
        # текст
        entry_text = ttk.Label(r_frame, text='Test text', borderwidth=1, relief='sunken', background='white')
        entry_text.pack(anchor='nw', fill='both', expand=True,  padx=5, pady=5)
        # кнопка редактирования
        update_btn = ttk.Button(r_frame, text='Редактировать запись')
        update_btn.pack(side='left', fill='x', expand=True)
        # кнопка для удаления
        delete_btn = ttk.Button(r_frame, text='Удалить запись')
        delete_btn.pack(side='right', fill='x', expand=True)
        return r_frame, entry_id, entry_theme, entry_date, entry_text, update_btn, delete_btn

    def add_frame(self):
        # == контейнер для добавления записи ==
        a_frame = ttk.Frame(self.content_frame, borderwidth=1, relief='solid')
        # a_frame.pack(side='right', padx=(10, 5), pady=5, fill='both', expand=True)
        # надпись для поля темы
        theme_label = ttk.Label(a_frame, text='Тема:')
        theme_label.pack(anchor='nw', padx=10, pady=(5, 0))
        # поле для темы
        theme_area = ttk.Entry(a_frame)
        theme_area.pack(anchor='nw', padx=10, pady=10, fill='x')
        # надпись для текстового поля
        text_label = ttk.Label(a_frame, text='Текст:')
        text_label.pack(anchor='nw', padx=10, pady=0)
        # текстовое поле
        text_area = ScrolledText(a_frame)
        text_area.pack(anchor='nw', padx=10, pady=10, fill='both', expand=True)
        # кнопка для добавления

        def add_entry():
            self.db.add_entry(theme_area.get(), text_area.get(1.0, 'end'))
            theme_area.delete(0, 'end')
            text_area.delete('1.0', 'end')
            self.update_list_frame()

        add_btn = ttk.Button(a_frame, text='Добавить запись', command=add_entry)
        add_btn.pack(side='left', fill='x', expand=True)
        # кнопка для очистки поля ввода
        clear_btn = ttk.Button(
            a_frame,
            text='Очистить',
            command=lambda: text_area.delete('1.0', 'end')
            )
        clear_btn.pack(side='right', fill='x', expand=True)
        # self.actual_frame = a_frame
        return a_frame

    def update_frame(self):
        # == контейнер для редактирования записи ==
        u_frame = ttk.Frame(self.content_frame, borderwidth=1, relief='solid')
        # надпись для поля темы
        u_theme_label = ttk.Label(u_frame, text='Тема:')
        u_theme_label.pack(anchor='nw', padx=10, pady=(5, 0))
        # поле для темы
        u_theme_area = ttk.Entry(u_frame)
        u_theme_area.pack(anchor='nw', padx=10, pady=10, fill='x')
        # надпись для текстового поля
        u_text_label = ttk.Label(u_frame, text='Текст:')
        u_text_label.pack(anchor='nw', padx=10, pady=0)
        # текстовое поле
        u_text_area = ScrolledText(u_frame)
        u_text_area.pack(anchor='nw', padx=10, pady=10, fill='both', expand=True)
        # кнопка для обновления
        u_btn = ttk.Button(u_frame, text='Ок')
        u_btn.pack(side='left', fill='x', expand=True)
        # кнопка отмены

        def cancel_update():
            u_frame.pack_forget()
            u_theme_area.delete(0, 'end')
            u_text_area.delete('1.0', 'end')

        cancel_btn = ttk.Button(u_frame, text='Отмена', command=cancel_update)
        cancel_btn.pack(side='right', fill='x', expand=True)
        return u_frame, u_theme_area, u_text_area, u_btn

    def read_button(self, entry_id, entry_theme, entry_date, entry_text, r_frame, id, theme, date, text):
        if self.actual_frame:
            self.actual_frame.pack_forget()
        entry_id.configure(text=f'Запись № {id}')
        entry_theme.configure(text=theme)
        entry_date.configure(text=date)
        entry_text.configure(text=text)
        r_frame.pack(side='right', padx=(10, 5), pady=5, fill='both', expand=True)
        self.actual_frame = r_frame

    def update_list_frame(self):
        # в цикле удаляем все виджеты записей
        for w in self.list_frame.winfo_children():
            w.destroy()
        self.show_list_entrys()  # отрисовываем список по новой

    def delete_button(self, r_frame, entry_id):
        # функция кнопки удаления
        r_frame.pack_forget()
        id = int(entry_id.cget('text').removeprefix('Запись № '))
        self.db.delete_entry(id)
        self.update_list_frame()

    def update_button(self, r_frame, u_frame, u_theme_area, u_text_area, entry_theme, entry_text):
        r_frame.pack_forget()
        u_frame.pack(side='right', padx=(10, 5), pady=5, fill='both', expand=True)
        if u_theme_area.get() == '':
            u_theme_area.insert(0, entry_theme.cget('text'))
        if u_text_area.get(1.0, 'end') == '\n':
            u_text_area.insert(1.0, entry_text.cget('text'))

    def update_confirm(self, entry_id, u_theme_area, u_text_area, u_frame):
        id = int(entry_id.cget('text').removeprefix('Запись № '))
        new_theme = u_theme_area.get()
        new_text = u_text_area.get(1.0, 'end')
        print(f'new_theme - {new_theme}, new_text - {new_text}')
        self.db.update_entry(id, new_theme, new_text)
        u_frame.pack_forget()
        self.update_list_frame()

    def show_list_entrys(self):
        # функция отрисовки всех записей из БД
        entrys = self.db.get_all_entrys()
        r_frame, entry_id, entry_theme, entry_date, entry_text, update_btn, delete_btn = self.read_frame()
        u_frame, u_theme_area, u_text_area, ok_btn = self.update_frame()

        def action_delete():
            self.delete_button(r_frame, entry_id)

        delete_btn.configure(command=action_delete)

        def action_update():
            self.update_button(r_frame, u_frame, u_theme_area, u_text_area, entry_theme, entry_text)

        update_btn.configure(command=action_update)

        def action_update_confirm():
            self.update_confirm(entry_id, u_theme_area, u_text_area, u_frame)

        ok_btn.configure(command=action_update_confirm)

        for i in entrys:

            entry_frame = ttk.Frame(self.list_frame, borderwidth=1, relief='solid')
            entry_frame.pack(fill='x', pady=2, padx=(0, 5))

            entry = ttk.Label(entry_frame, text=f'{i.id} {i.theme} {i.date}')
            entry.pack(side='left', fill='x', padx=(3, 0))

            action_read = partial(
                self.read_button,
                entry_id, entry_theme, entry_date, entry_text, r_frame,
                i.id, i.theme, i.date, i.text
                )
            read_btn = ttk.Button(entry_frame, text='Читать', command=action_read)
            read_btn.pack(side='right', fill='x', padx=(0, 3))

    def configure_frame(self, event):
        # Меняем ширину list_frame под ширину canvas
        self.canvas.itemconfig(self.list_frame_window, width=event.width)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def new_entry(self):
        if self.actual_frame:
            self.actual_frame.pack_forget()
        a_frame = self.add_frame()
        a_frame.pack(side='right', padx=(10, 5), pady=5, fill='both', expand=True)
        self.actual_frame = a_frame

    def run(self):
        self.window.mainloop()
