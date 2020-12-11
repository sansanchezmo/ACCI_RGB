'''
  ACCI_RGB (Algoritmo Criptográfico de Codificación de Imágenes RGB)
  Es un algoritmo diseñado en Python que busca utilizar las propiedades de la
  aritmética modular como herramienta para crear un sistema de codificación y
  decodificación de imágenes.

  Desarrolladores
    Josué David Briceño Urquijo
    jbriceno@unal.edu.co
    Estudiantes de Ingeniería de Sistemas y Computación
    Universidad Nacional de Colombia

    Santiago Sánchez Mora
    sansanchezmo@unal.edu.co
    Estudiantes de Ingeniería de Sistemas y Computación
    Universidad Nacional de Colombia
'''

from hashlib import sha256
from sympy import Matrix, lcm
from PIL import Image
from IPython.display import display
from IPython.display import Image as IM
import string
import sympy
import random
import sys
import numpy as np

#---Generación de la Semilla para la Clave A-----------------------------------#

def randomSeed(AKey):
  AHash = sha256(AKey.encode('utf-8')).hexdigest()
  ASeed = int(AHash, 16)
  return ASeed

#---Generación de la Matriz de la Clave A--------------------------------------#

def makeAMatrix(AKey):
  random.seed(randomSeed(AKey))
  while True:
    try:
      AMatrix = [[random.randint(-sys.maxsize - 1, sys.maxsize) for j in range(3)] for i in range(3)]
      Matrix(AMatrix).inv_mod(256)
      return AMatrix
    except:
      True
      #print("Reintentando conseguir matriz invertible.")

#---Generación de la Clave S1--------------------------------------------------#

def makeFirstSmoke(AMatrix):
  return Matrix(AMatrix).det() * Matrix(AMatrix).inv_mod(256).det()

#---Generación de la Matriz Conmutativa----------------------------------------#

def findASolution(AMatrix):
  A = AMatrix
  U = [[       0,           A[1][0],           A[2][0],          -A[0][1],         0,                 0,          -A[0][2],                 0,        0],
       [ A[0][1], A[1][1] - A[0][0],           A[2][1],	                0,	-A[0][1],	                0,	               0,	         -A[0][2],        0],
       [ A[0][2],           A[1][2], A[2][2] - A[0][0],	                0,         0,	         -A[0][1],                 0,	                0, -A[0][2]],
       [-A[1][0],                 0,	               0, A[0][0] - A[1][1],   A[1][0],	          A[2][0],	        -A[1][2],                 0,        0],
       [       0,          -A[1][0],                 0,	          A[0][1],         0,	          A[2][1],                 0,	         -A[1][2],	      0],
       [       0,                 0,	        -A[1][0],          	A[0][2],	 A[1][2], A[2][2] - A[1][1],	               0,                 0, -A[1][2]],
       [-A[2][0],                 0,	               0,          -A[2][1],         0,	                0, A[0][0] - A[2][2],           A[1][0],  A[2][0]],
       [       0,          -A[2][0],	               0,	                0,	-A[2][1],	                0,           A[0][1],	A[1][1] - A[2][2],	A[2][1]], 
       [       0,                 0,          -A[2][0],                 0,	       0,          -A[2][1],           A[0][2],	          A[1][2],        0]]

  U = Matrix(U)
  
  NewSols = []
  for sol in U.nullspace():
    m = lcm([val.q for val in sol])
    x = m * sol
    NewSols.append(x)

  return NewSols

#---Codificación de Números a Letras-------------------------------------------#

def encodeNumberToLetters(number):
  chars = []
  chars.extend(string.digits + string.ascii_letters)
  letters = ""
  while number > 0:
    INumber = number % len(chars)
    letters += chars[INumber]
    number //= len(chars)

  return letters

#---Codificación de Letras a Números-------------------------------------------#

def encodeLettersToNumber(letters):
  chars = []
  chars.extend(string.digits + string.ascii_letters)
  number = 0
  i = 0
  for a in letters:
    number += (len(chars) ** i ) * chars.index(a)
    i += 1

  return number

#---Generación de la Clave T---------------------------------------------------#

def makeTKey(TMatrix):
  TKey = ""
  for sol in TMatrix:
    for value in list(sol):
      if value >= 0:
        key = str(value)
        key = "0" + key
      else:
        key = str(value)[1:]
        key = "1" + key

      leng = len(key)
      leng = str(leng)
      TKey += str(len(leng)) + leng + key

  return encodeNumberToLetters(int(TKey))

#---Generación de la Matriz Solución de la Conmutatividad----------------------#

def makeTMatrix(TKey):
  TKey = str(encodeLettersToNumber(TKey))
  i = 0
  solCounter = 0
  TMatrix = []
  sol = []
  while i < len(TKey):
    ll = int(TKey[i])
    i += 1
    leng = int(TKey[i:i + ll])
    i += ll
    if int(TKey[i]) == 0:
      value = int(TKey[i + 1:i + leng])
    else:
      value = -int(TKey[i + 1:i + leng])
    
    i += leng
    sol.append(value)
    solCounter += 1
    if solCounter == 9:
      TMatrix.append(Matrix(sol))
      solCounter = 0
      sol = []

  return TMatrix

#---Generación de la Matriz B apartir de la Clave Personal B-------------------#

def createBMatrix(BSeed, TKey):
  random.seed(BSeed)

  NewSols = makeTMatrix(TKey)

  while True:
    try:
      LMatrix = []
      freeVariables = [random.randint(-sys.maxsize - 1, sys.maxsize) for i in range(3)]
      for i in range(9):
        cell = NewSols[0][i] * freeVariables[0] + NewSols[1][i] * freeVariables[1] + NewSols[2][i] * freeVariables[2]
        LMatrix.append(cell)

      BMatrix = [[LMatrix[i], LMatrix[i + 1], LMatrix[i + 2]] for i in range(0, 9, 3)]
      Matrix(BMatrix).inv_mod(256)
      return BMatrix
    except:
      True
      #print("Reintentando conseguir matriz invertible.")

#---Generación de la Clave S2--------------------------------------------------#

def makeSecondSmoke(BMatrix, S1Key):
  S1Key = encodeLettersToNumber(S1Key)
  return S1Key * Matrix(BMatrix).det() * Matrix(BMatrix).inv_mod(256).det()

#---Generación de la Clave B---------------------------------------------------#

def makeBKey(BMatrix):
  BKey = ""
  for row in BMatrix:
    for value in row:
      if value >= 0:
        key = str(value)
        key = "0" + key
      else:
        key = str(value)[1:]
        key = "1" + key

      leng = len(key)
      leng = str(leng)
      BKey += str(len(leng)) + leng + key
      
  return encodeNumberToLetters(int(BKey))

#---Generación de la Matriz B a partir de la Clave B---------------------------#

def makeBMatrix(BKey):
  BKey = str(encodeLettersToNumber(BKey))
  i = 0
  solCounter = 0
  BMatrix = []
  sol = []
  while i < len(BKey):
    ll = int(BKey[i])
    i += 1
    leng = int(BKey[i:i + ll])
    i += ll
    if int(BKey[i]) == 0:
      value = int(BKey[i + 1:i + leng])
    else:
      value = -int(BKey[i + 1:i + leng])
    
    i += leng
    sol.append(value)
    solCounter += 1
    if solCounter == 3:
      BMatrix.append(sol)
      solCounter = 0
      sol = []

  return BMatrix

#---Creación de la primera instancia de claves---------------------------------#

def firstKeyIteration(AKey):
  AMatrix = makeAMatrix(AKey)
  S1Value = makeFirstSmoke(AMatrix)

  if S1Value >= 0:
    S1Key = "0" + str(S1Value)
    S1Key = encodeNumberToLetters(int(S1Key))
  else:
    S1Key = "1" + str(S1Value)[1:]
    S1Key = encodeNumberToLetters(int(S1Key))

  TMatrix = findASolution(AMatrix)
  TKey = makeTKey(TMatrix)

  print("La clave pública T es:", end=" ")
  print(TKey)

  global gTKey
  global gS1Key

  gTKey = TKey

  print("La clave pública S1 es:", end=" ")
  print(S1Key)

  gS1Key = S1Key

#---Creación de la segunda instancia de claves---------------------------------#

def secondKeyIteration(TKey, S1Key, BTKey):
  BSeed = randomSeed(BTKey)
  BMatrix = createBMatrix(BSeed, TKey)
  BKey = makeBKey(BMatrix)
  S2Value = makeSecondSmoke(BMatrix, S1Key)

  if S2Value >= 0:
    S2Key = "0" + str(S2Value)
    S2Key = encodeNumberToLetters(int(S2Key))
  else:
    S2Key = "1" + str(S2Value)[1:]
    S2Key = encodeNumberToLetters(int(S2Key))

  global gBKey
  global gS2Key

  print("La clave privada B es:", end=" ")
  print(BKey)

  gBKey = BKey

  print("La clave pública S2 es:", end=" ")
  print(S2Key)

  gS2Key = S2Key

#---Algoritmo de Cifrado y Decifrado-------------------------------------------#

def cipherSmoker(message, matrix):
  message = [(row + random.randint(0, 255)) % 256 for row in message] 
  message = Matrix(message)
  result = message.transpose() * Matrix(matrix)
  newResult = [row % 256 for row in list(result)]
  return newResult

def cipherDirect(message, matrix):
  message = Matrix(message)
  result = message.transpose() * Matrix(matrix)
  newResult = [row % 256 for row in list(result)]
  return newResult

def decipherSmoker(message, matrix):
  message = Matrix(message)
  result = message.transpose() * matrix
  newResult = [(row - random.randint(0, 255)) % 256 for row in list(result)]
  return newResult

def decipherDirect(message, matrix):
  message = Matrix(message)
  result = message.transpose() * matrix
  newResult = [row % 256  for row in list(result)]
  return newResult

#---Función para mostrar imagen------------------------------------------------#

def showImage(path):
  print()
  display(IM(path))
  print()

#---Funciónes para cifrar y decifrar la imagen---------------------------------#

def cipherAImage(data, matrix, smoke):
  matrix = makeAMatrix(matrix)
  random.seed(smoke)
  enc = []
  for row in data:
    NRow = []
    for cell in row:
      NRow.append(cipherSmoker(cell, matrix))
    enc.append(NRow)
  return enc

def cipherBImage(data, matrix):
  matrix = makeBMatrix(matrix)
  enc = []
  for row in data:
    NRow = []
    for cell in row:
      NRow.append(cipherDirect(cell, matrix))
    enc.append(NRow)
  return enc

def decipherAImage(data, matrix):
  matrix = Matrix(makeAMatrix(matrix)).inv_mod(256)
  dec = []
  for row in data:
    NRow = []
    for cell in row:
      NRow.append(decipherDirect(cell, matrix))
    dec.append(NRow)
  return dec

def decipherBImage(data, matrix, smoke):
  matrix = Matrix(makeBMatrix(matrix)).inv_mod(256)
  random.seed(smoke)
  dec = []
  for row in data:
    NRow = []
    for cell in row:
      NRow.append(decipherSmoker(cell, matrix))
    dec.append(NRow)
  return dec

#---Selección de Claves Personales---------------------------------------------#

gTKey = ""
gS1Key = ""
gS2Key = ""
gBKey = ""

AKey = input("Inserte la Clave Personal A\n")

firstKeyIteration(AKey)

'''
TKey = input("Inserte la Clave T\n")
S1Key = input("Inserte la Clave S1\n")
'''

BTKey = input("Inserte una Clave Personal B\n")

secondKeyIteration(gTKey, gS1Key, BTKey)

#---Encriptación y Decifrado de Imágenes---------------------------------------#

fileName = input("Inserte el nombre del archivo\n")

# IMPORTANTE
# Las direcciones de los archivos pueden cambiar dependiendo del sistema
#   operativo que se utilice. En caso de Windows, deberá importarse la librería
#   os, para conseguir una dirección específica cerca al archivo .py

path = "/content/" + fileName + ".png"
path2 = "/content/" + fileName + "Enc1.png"
path3 = "/content/" + fileName + "Enc2.png"
path4 = "/content/" + fileName + "Dec1.png"
path5 = "/content/" + fileName + "Dec2.png"

image = Image.open(path)

ImageData = np.asarray(image)
showImage(path)

ImageEnc1 = cipherAImage(ImageData, AKey, gS2Key)
ImageEnc1 = np.asarray(ImageEnc1)

image2 = Image.fromarray(ImageEnc1.astype(np.uint8)).save(path2)
showImage(path2)

ImageEnc2 = cipherBImage(ImageEnc1, gBKey)
ImageEnc2 = np.asarray(ImageEnc2)

image3 = Image.fromarray(ImageEnc2.astype(np.uint8)).save(path3)
showImage(path3)

ImageDec1 = decipherAImage(ImageEnc2, AKey)
ImageDec1 = np.asarray(ImageDec1)

image4 = Image.fromarray(ImageDec1.astype(np.uint8)).save(path4)
showImage(path4)

ImageDec2 = decipherBImage(ImageDec1, gBKey, gS2Key)
ImageDec2 = np.asarray(ImageDec2)

image5 = Image.fromarray(ImageDec2.astype(np.uint8)).save(path5)
showImage(path5)
