import webbrowser
import time

import os
import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui


# Clearing the Screen
os.system('cls')
print("Ce code génère des pages aléatoires de Wikipédia.")
print(" ")
time.sleep(2)
print("combien de page Wikipédia à générer ?")
n = int(input())
for i in range(n):
    webbrowser.open('https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard')
    

