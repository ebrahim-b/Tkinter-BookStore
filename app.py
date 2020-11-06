from tkinter import *
from tkinter.ttk import Treeview
from data import Database

database = Database("books.db")

class Root(Tk):

    def __init__(self):
        super().__init__()
        self.title('Bookshop Manager')
        self.geometry('580x500')

        frame_search = Frame(self)
        frame_search.grid(row=0 , column=0)

        lbl_search = Label(frame_search, text='Search By Name: ', font=('bold',12), pady=20)
        lbl_search.grid(row=0,column=0,sticky=W)

        self.title_search = StringVar()
        self.title_search_entry = Entry(frame_search, textvariable=self.title_search)
        self.title_search_entry.grid(row=0, column=1)


        frame_fields = Frame(self)
        frame_fields.grid(row=1, column=0)

        # Title
        self.title_text = StringVar()
        title_label = Label(frame_fields, text='Title', font=('bold', 12))
        title_label.grid(row=0, column=0, sticky=E)
        self.title_entry = Entry(frame_fields, textvariable=self.title_text)
        self.title_entry.grid(row=0, column=1, sticky=W)


        # author
        self.author_text = StringVar()
        author_label = Label(frame_fields, text='Author', font=('bold', 12))
        author_label.grid(row=0, column=2, sticky=E)
        self.author_entry = Entry(frame_fields, textvariable=self.author_text)
        self.author_entry.grid(row=0, column=3, sticky=W)


        # year
        self.year_text = StringVar()
        year_label = Label(frame_fields, text='Year', font=('bold', 12))
        year_label.grid(row=1, column=0, sticky=E)
        self.year_entry = Entry(frame_fields, textvariable=self.year_text)
        self.year_entry.grid(row=1, column=1, sticky=W)


        # isbn
        self.isbn_text = StringVar()
        isbn_label = Label(frame_fields, text='ISBN', font=('bold', 12), pady=20)
        isbn_label.grid(row=1, column=2, sticky=E)
        self.isbn_entry = Entry(frame_fields, textvariable=self.isbn_text)
        self.isbn_entry.grid(row=1, column=3, sticky=W)


        frame_bookshop = Frame(self)
        frame_bookshop.grid(row=4, column=0, columnspan=4, rowspan=6, pady=20, padx=20)

        columns = ['id', 'Title', 'Author', 'Year', 'ISBN']
        self.bookshop_tree_view = Treeview(frame_bookshop, columns=columns, show="headings")
        self.bookshop_tree_view.column("id", width=30)
        for col in columns[1:]:
            self.bookshop_tree_view.column(col, width=120)
            self.bookshop_tree_view.heading(col, text=col)
        self.bookshop_tree_view.bind('<<TreeviewSelect>>', self.select_book)
        self.bookshop_tree_view.pack(side="left", fill="y")
        scrollbar = Scrollbar(frame_bookshop, orient='vertical')
        scrollbar.configure(command=self.bookshop_tree_view.yview)
        scrollbar.pack(side="right", fill="y")
        self.bookshop_tree_view.config(yscrollcommand=scrollbar.set)


        frame_btns = Frame(self)
        frame_btns.grid(row=3, column=0)

        add_btn = Button(frame_btns, text='Add Book', width=12,command=self.add_book)
        add_btn.grid(row=0, column=0, pady=20)

        remove_btn = Button(frame_btns, text='Remove Book', width=12, command=self.remove_book)
        remove_btn.grid(row=0, column=1)

        update_btn = Button(frame_btns, text='Update Book', width=12, command=self.update_book)
        update_btn.grid(row=0, column=2)

        clear_btn = Button(frame_btns, text='Clear Input', width=12, command=self.clear_text)
        clear_btn.grid(row=0, column=3)

        search_btn = Button(frame_search, text='Search',  width=12,command=self.search_title)
        search_btn.grid(row=0, column=2)

        
        self.book_list()

    def add_book(self):
        if self.author_text.get() != '' and self.title_text.get() != '' and self.year_text.get() != '' and self.isbn_text.get() != '':
            database.insert(self.title_text.get(), self.author_text.get(),self.year_text.get(), self.isbn_text.get())
            self.book_list()
            self.clear_text()

    def select_book(self,event):
        try:  
            global selected_item          
            index = self.bookshop_tree_view.selection()[0]
            selected_item = self.bookshop_tree_view.item(index)['values']
            self.title_entry.delete(0, END)
            self.title_entry.insert(END, selected_item[1])
            self.author_entry.delete(0, END)
            self.author_entry.insert(END, selected_item[2])
            self.year_entry.delete(0, END)
            self.year_entry.insert(END, selected_item[3])
            self.isbn_entry.delete(0, END)
            self.isbn_entry.insert(END, selected_item[4])
        except IndexError:
            pass

    def remove_book(self):
        database.remove(selected_item[0])        
        self.clear_text()
        self.book_list()

    def update_book(self):
        database.update(selected_item[0], self.title_text.get(), self.author_text.get(),
                self.year_text.get(), self.isbn_text.get())
        self.book_list()

    
    def clear_text(self):
        self.title_entry.delete(0, END)
        self.author_entry.delete(0, END)
        self.year_entry.delete(0, END)
        self.isbn_entry.delete(0, END)

    def book_list(self,title = ''):
        for i in self.bookshop_tree_view.get_children():
            self.bookshop_tree_view.delete(i)
        for row in database.fetch(title):
            self.bookshop_tree_view.insert('', 'end', values=row)


    def search_title(self):
        hostname = self.title_search.get()
        self.book_list(hostname)
    




root = Root()
root.mainloop()