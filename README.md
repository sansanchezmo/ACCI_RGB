# ACCI_RGB
Para hacer uso de nuestro algoritmo se requiere de una imagen en formato .png sin transparencia. Este es el elemento clave y primario. Ya que las imágenes son, en esencia, un arreglo matricial de una tripleta de bytes, podemos convertirla y trabajar con ella haciendo uso del álgebra lineal y de la aritmética modular junto con su inverso multiplicativo para hacer que la magia ocurra. En este caso, cada tripleta de bytes representará un vector de información. Este vector de información será el que trataremos en nuestro algoritmo de encriptación.\
Para mayor información de los métodos matemáticos utilizados para desarrollar la aplicación visite la sección [Project Information](https://github.com/sashhhita/ACCI_RGB/tree/main/Project%20Information).\
Asimismo, para acceder al archivo .py del algoritmo, visite la sección [Python Prototipe](https://github.com/sashhhita/ACCI_RGB/tree/main/Python%20Prototype).\
### Requerimientos Funcionales
Para el desarrollo de la aplicación se utilizó una gran variedad de librerías de Python, de las cuales vale la pena destacar las 4 que tienen mayor influencia y relevancia sobre el funcionamiento del algoritmo, es decir, su us dentro de la aplicación es crucial:
#### Pillow
```python
import pil
```
La librería Pillow es utilizada para obtener los vectores 3x1 de cada pixel de la imágen insertada, en donde la información de cada vector corresponde a los colres que forman el pixel con base en el modelo RGB.
#### SymPy
```python
import sympy
```
#### Random
```python
import random
```
#### NumPy
```python
import numpy
```
### Desarrolladores
Josué David Briceño Urquijo\
*jbriceno@unal.edu.co*\
***Estudiantes de Ingeniería de Sistemas y Computación***\ 
Santiago Sánchez Mora\
*sansanchezmo@unal.edu.co*\
***Estudiantes de Ingeniería de Sistemas y Computación*** 

### Supervisor
Francisco Albeiro Gómez Jaramillo\
***fagomezj@gmail.com***\
***Docente asociado al Departamento de Matemáticas***\
***PhD en Computer Science***

> Universidad Nacional de Colombia ©\
Facultad de Ingeniería\
11 de diciembre de 2020\
Colombia
