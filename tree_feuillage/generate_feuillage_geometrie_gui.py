
from numpy import *
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import sys
import tkinter as Tk
from tkinter.ttk import *
from tinker_generate_tree_interface import *

##    global arbre

plt.ion()


class GUITkinter(Tk.Frame) :
    def __init__(self) :
        Tk.Frame.__init__(self)
        self.master.title("Generateur d'arbre")	#Ça, c'est du nom!
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NSEW")

        self.f = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.f.add_subplot(111)
        self.rangeStrates = arange(3)
        self.couleur = 205/256
        self.contour = 150/256

        self.nbpt_init = [10,8,7,6,5,4]
        self.rayon_init = [2,1.5,0.9,0.5,0.3,0.1]
        self.couleur_init = array([205,200,195,190,185,180])
        self.contour_init = 150
        self.courbure_init = 0.5

        self.comp = 0

        self.objectStrate = StrateParameterList()
        self.CreateWidjets()


    def CreateWidjets(self) :

        classbidon = StrateParameterList()
        classbidon.addstrate(2, 0.1, 0, 0, 0.5)
##        print(type(classbidon.liste[0].nbpt))

        self.arbre = ArbreClass(self.ax, classbidon.liste[0])
##        self.arbre.create_arbre()

        root = Tk.Frame(self, borderwidth=2, relief="groove") # root.wm_title("")
        root.grid(column=0, row=0, sticky="NSEW")

        self.canvas = FigureCanvasTkAgg(self.f, master=root)
        print(dir(self.canvas))
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)


        # frame arbre and buttons
        Frame_arbre = Tk.LabelFrame(root, text="Arbre", padx=20, pady=20)
        Frame_arbre.pack(fill="both",  side = Tk.LEFT) # , expand="yes"

        Frame_strates = Tk.LabelFrame(Frame_arbre, text="nb of strates", padx=5, pady=5)
        Frame_strates.pack(fill="both")
        self.nbStrates = Tk.Spinbox(Frame_strates, from_=0, to=10)
        self.nbStrates.pack(padx=5,pady=5)

        Tk.Button(Frame_arbre, text ='Create' ,command=self.arbrecreate ).pack(padx=5, pady=5)

        # frame feuillage
        Frame_feuillage = Tk.LabelFrame(root, text="Feuillage", padx=20, pady=20)
        Frame_feuillage.pack(fill="both") # , expand="yes"


        # menu déroulant de selection de strate
        self.listeStrates = Combobox(Frame_feuillage, textvariable = 'Strate', values = self.rangeStrates, state = 'disabled')
##        self.listeStrates.set(StrateSelect)
        self.listeStrates.bind('<<ComboboxSelected>>', self.methodeTest) # Executer une méthode -après- sélection d'un élément
        self.listeStrates.pack(padx=5,pady=5)
##

        # slider nbpoint
        self.scale_point = Tk.Scale(Frame_feuillage, orient='horizontal', from_=3, to=30, \
                      resolution=1, tickinterval=5, length=150, \
                      label='nombre de points', command=self.getSliderPoint, \
                      state = 'disabled')
        self.scale_point.pack(padx=5,pady=5)
        self.scale_point.set(10)

        # slider courbure
        self.scale_courbure = Tk.Scale(Frame_feuillage, orient='horizontal', from_=0.1, to=2, \
                      resolution=0.1, tickinterval=1, length=150, \
                      label='courbure', command=self.getSliderCourbure, \
                      state = 'disabled')
        self.scale_courbure.pack(padx=5,pady=5)
        self.scale_courbure.set(0.5)

        # slider rayon
        self.scale_rayon = Tk.Scale(Frame_feuillage, orient='horizontal', from_=0.1, to=5, \
                      resolution=0.1, tickinterval=2.5, length=150, \
                      label='rayon', command=self.getSliderrayon, \
                      state = 'disabled')
        self.scale_rayon.pack(padx=5,pady=5)
        self.scale_rayon.set(2)
##        self.scale_rayon['state'] = 'normal'

        Tk.mainloop()


    def _quit():
        root.quit()
        root.destroy()

    def arbrecreate(self) :
        del(self.objectStrate)
        self.objectStrate = StrateParameterList()
        self.comp = 1
        self.ax.clear()
        indice = int(self.nbStrates.get())

        print(indice)
        print(self.nbpt_init[indice])
        print(self.rayon_init[indice])
        print(self.couleur_init[indice])
        for i in arange(indice) :
            # créé successivement les strates de l'arbre
            self.objectStrate.addstrate(self.nbpt_init[i], self.rayon_init[i], self.couleur_init[i], self.contour_init, self.courbure_init)
            self.arbre = ArbreClass(self.ax, self.objectStrate.liste[i])
##            self.arbre.create_arbre()
            self.arbre.plot_arbre()
        self.canvas.draw()


        # autorise la modification de la fenetre "feuillage"
        self.listeStrates['values'] = list(range(indice))
        self.scale_rayon['state'] = 'normal'
        self.scale_courbure['state'] = 'normal'
        self.scale_point['state'] = 'normal'
        self.listeStrates['state'] = 'readonly'

        pause(0.001)

    def getButton2(self) :
        self.ax.clear()
        if self.comp :
            i = int(self.listeStrates.get())
            self.objectStrate.setstrate(self)
            for strate in self.objectStrate.liste :
                self.arbre = ArbreClass(self.ax,strate)
                self.arbre.plot_arbre()
            self.canvas.draw()
            pause(0.001)
        else :
            i = 0
            self.listeStrates.set(0)

    def getButton3(self) :
        self.ax.clear()
        self.arbre.plot_arbre()
        self.canvas.draw()
        pause(0.001)

    def getSliderPoint(self, pos) :
##        print(pos)
        self.getButton2()

    def getSliderCourbure(self, pos) :
##        print(pos)
        self.getButton2()

    def getSliderrayon(self, pos) :
##        print(pos)
        self.getButton2()

    def methodeTest(self, blblb) :
        i = int(self.listeStrates.get())
        # met les sliders sur les valeurs correspondants à la strate i
        self.scale_rayon.set(self.objectStrate.liste[i].rayon)
        self.scale_courbure.set(self.objectStrate.liste[i].courbure)
        self.scale_point.set(self.objectStrate.liste[i].nbpt)


class StrateParameterList() :
    def __init__(self) :
        self.liste = list()

    def addstrate(self, nbpt, rayon, couleur, contour, courbure) :
        temp = StrateParameter(nbpt, rayon, couleur, contour, courbure)
        self.liste.append(temp)

    def setstrate(self, arbre) :
        indice = int(arbre.listeStrates.get())
        self.liste[indice].nbpt = arbre.scale_point.get()
        self.liste[indice].rayon = arbre.scale_rayon.get()
        self.liste[indice].couleur = arbre.couleur_init[indice]
        self.liste[indice].contour = arbre.contour_init
        self.liste[indice].courbure = arbre.scale_courbure.get()


class StrateParameter():
    def __init__(self, nbpt, rayon, couleur, contour, courbure) :
        self.nbpt = nbpt
        self.courbure = courbure
        self.rayon = rayon
        self.couleur = couleur
        self.contour = contour

a=GUITkinter()





##        # button feuillage create
##        Tk.Button(Frame_feuillage, text ='Create' ,command=self.getButton2 ).pack(padx=5, pady=5)
##        Tk.Button(Frame_feuillage, text ='Modify' ,command=self.getButton2 ).pack(padx=5, pady=5)
##        Tk.Button(Frame_feuillage, text ='Plot' ,command=self.getButton3 ).pack(padx=5, pady=5)

##        Tk.Button(Frame_arbre, text ='Modify' ,command=self.getButton2 ).pack(padx=5, pady=5)
##        Tk.Button(Frame_arbre, text ='Plot' ,command=self.getButton3 ).pack(padx=5, pady=5)

##    button = Button(master=root, text='Quit', command=_quit)
##    button.pack(side=Tk.TOP)

##
##    def on_key_event(self, event):
##        print('you pressed %s' % event.key)
##        key_press_handler(event, canvas, toolbar)

##    canvas.mpl_connect('key_press_event', on_key_event)

