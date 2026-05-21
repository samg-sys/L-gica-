from itertools import combinations
from itertools import permutations
from Logica import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
import numpy as np
from types import MethodType

def escribir_numero(self, literal):
    if '-' in literal:
        atomo = literal[1:]
        neg = ' no'
    else:
        atomo = literal
        neg = ''
    n, c = self.unravel(atomo)
    return f"El número {n} {neg} está en la casilla ({c})"

def Ytoria_balanceada(lista):
    n = len(lista)
    if n == 0: return ""
    if n == 1: return lista[0]
    mid = n // 2
    # Combinamos las dos mitades en un solo string con el conectivo Y
    return "(" + Ytoria_balanceada(lista[:mid]) + "Y" + Ytoria_balanceada(lista[mid:]) + ")"

def Otoria_balanceada(lista):
    n = len(lista)
    if n == 0: return ""
    if n == 1: return lista[0]
    mid = n // 2
    # Combinamos las dos mitades en un solo string con el conectivo O
    return "(" + Otoria_balanceada(lista[:mid]) + "O" + Otoria_balanceada(lista[mid:]) + ")"

class Numero:

    '''
    Clase para representar el problema del hexagrama
    mágico donde ningún número se puede repetir y
    la suma de cualquier combinación en una recta
    debe dar 26.
    '''

    def __init__(self, N=20, C=12):
        self.N = N
        self.C = C
        self.NenC = Descriptor([N,C])
        self.NenC.escribir = MethodType(escribir_numero, self.NenC)
        r1 = self.regla1()
        r2 = self.regla2()
        r3 = self.regla3()
        r4 = self.regla4()
        self.reglas = [r1, r2, r3, r4]

    def regla1(self):
        # "La suma de los números en cada línea recta es 26"
        val_numeros = list(range(self.N)) 
        
        # Pre-cálculo: buscamos combinaciones que sumen 26. 
        # Sumamos x+1 porque los índices (0-11) representan los valores reales (1-12)
        comb_validas = [c for c in combinations(val_numeros, 4) if sum(x + 1 for x in c) == 26]
        
        # Índices de las casillas que conforman cada línea recta
        lineas = [
            [0, 2, 5, 7],   # l1
            [0, 3, 6, 10],  # l2
            [7, 8, 9, 10],  # l3
            [1, 2, 3, 4],   # l4
            [1, 5, 8, 11],  # l5
            [4, 6, 9, 11]   # l6
        ]
        
        formulas_lineas = []
        for linea in lineas:
            opciones_linea = []
            for comb in comb_validas:

                # Se evalúan todas las formas de ordenar los 4 números en esas 4 casillas
                for perm in permutations(comb):
                    casilla_0 = self.NenC.ravel([perm[0], linea[0]])
                    casilla_1 = self.NenC.ravel([perm[1], linea[1]])
                    casilla_2 = self.NenC.ravel([perm[2], linea[2]])
                    casilla_3 = self.NenC.ravel([perm[3], linea[3]])
                    
                    opciones_linea.append(Ytoria_balanceada([casilla_0, casilla_1, casilla_2, casilla_3]))
            
            formulas_lineas.append(Otoria_balanceada(opciones_linea))
            
        return Ytoria_balanceada(formulas_lineas)

    def regla2(self): #Todas las casillas deben estar ocupadas.
        casillas = [(c) for c in range(self.C)]
        lista = []
        for c in casillas:
            lista_o = []
            for n in range(self.N):
                lista_o.append(self.NenC.ravel([n, c]))
            lista.append(Ytoria_balanceada(lista_o))
        return Ytoria_balanceada(lista) #hecha (maybe)

    def regla3(self): #No pueden haber números repetidos.
        num_casillas = [(n,c) for n in range(self.N) for c in range(self.C)]
        lista = []
        for m in num_casillas:
            n,c = m
            otras_casillas = [(c1) for c1 in range(self.C) if (c1) != (c)]
            lista_o = []
            for k in otras_casillas:
                lista_o.append(self.NenC.ravel([n, k]))
            form = '(' + self.NenC.ravel([*m]) + '>-' + Otoria_balanceada(lista_o) + ')'
            lista.append(form)
        return Ytoria_balanceada(lista) #hecha (maybe)

    def regla4(self):
        # "Solo debe haber MÁXIMO un número por casilla"
        formulas = []
        for c in range(self.C):
            for n in range(self.N):
                for m in range(self.N):
                    if n != m:
                        formulas.append(f"({self.NenC.ravel([n, c])}>-{self.NenC.ravel([m, c])})")
        return Ytoria_balanceada(formulas) 
    
    def visualizar(self, I):
        fig, ax = plt.subplots()
        
        #Procedemos a crear las coordenadas para los dos triángulos de la estrella (uno invertido)
        #Tri 1
        t1 = np.array([[0, 1], [0.866, -0.5], [-0.866, -0.5]])
        #Tri 2
        t2 = np.array([[0, -1], [0.866, 0.5], [-0.866, 0.5]])
        
        #Creamos los triángulos con patches
        #( class matplotlib.patches.Patch(*, edgecolor=None, facecolor=None, color=None, linewidth=None, linestyle=None, antialiased=None, hatch=None, fill=True, capstyle=None, joinstyle=None, **kwargs) de matplotlib.org)
        tri1 = patches.Polygon(t1, edgecolor='black', facecolor='none', linewidth=2, linestyle='-', fill=False, closed=True)
        tri2 = patches.Polygon(t2, edgecolor='black', facecolor='none', linewidth=2, linestyle='-', fill=False, closed=True)
        
        ax.add_patch(tri1)
        ax.add_patch(tri2)
        
        #Las configuraciones del plot
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.set_aspect('equal')
        #plt.axis('off') # escondemos los ejes
        
        #Hacemos las direcciones de cada casilla
        direcciones = [
            [0, 1], #casilla 1
            [-0.866, 0.5], #casilla 2
            [-0.2886, 0.5], #casilla 3
            [0.2886, 0.5], #casilla 4
            [0.866, 0.5], #casilla 5
            [-0.5773, 0], #casilla 6
            [0.5773, 0], #casilla 7
            [-0.866, -0.5], #casilla 8
            [-0.2886, -0.5], #casilla 9
            [0.2886, -0.5], #casilla 10
            [0.866, -0.5], #casilla 11
            [0, -1] #casilla 12
        ]

        casilla_a_numero = {}

        for literal in I:
            if I[literal]:  #True
                if '-' in literal:
                    continue  #Ignora negaciones
                n, c = self.NenC.unravel(literal)
                casilla_a_numero[c] = n + 1  # +1 pq es una lista que va de  0 a 11 pero queremos que vaya de 1–12

        for c in range(self.C):
            if c in casilla_a_numero:
                scale = 0.95
                x, y = direcciones[c]
                valor = casilla_a_numero[c]
        
                ax.text(
                    x, y, str(valor),
                    fontsize=14,
                    ha='center',
                    va='center',
                    fontweight='bold',
                    color='r',
                    backgroundcolor='w'
                )


        #Ejecutamos
        plt.show()