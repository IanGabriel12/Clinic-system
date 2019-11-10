from interface import *
from tkinter import *

altura = 400
largura = 500
raiz = Tk()
Interface(raiz, largura, altura)
raiz.title('Hello world')
raiz.geometry(f'{largura}x{altura}')
raiz.mainloop()