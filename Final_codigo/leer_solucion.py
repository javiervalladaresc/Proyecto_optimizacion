comunas_cantidad = {'santiago' : 0, 'renca':0,'maipu':0,'puente_alto':0,'san_bernardo':0,'sano_joaquin':0,
            'la_pintana':0,'el_bosque':0,'penalolen':0,'cerro_navia':0,'pudahuel':0,'macul':0,'cerrillos':0,
            'la_florida':0,'recoleta':0,'la_granja':0}

file = open('results.yml', 'r')
datos = []
for linea in file:
    datos.append(linea.strip())
file.close()

lista_trabajadores = {}

for i in range(len(datos)):
    if datos[i][0] == 'x':
        lista_trabajadores[datos[i]] = datos[i+1].split()

for trabajador in lista_trabajadores:
    if float(lista_trabajadores[trabajador][1]) >=0.01:
        lista_trabajadores[trabajador][1] = 1
    else:
        lista_trabajadores[trabajador][1] = 0
suma = 0


for trabajador in lista_trabajadores:
    suma += lista_trabajadores[trabajador][1]

file = open('datos.csv','r')
nombres = []
for linea in file:
    nombres.append(linea.split(','))
file.close()

contaminacion = 0

trabajador_asistiendo = []
for tra in lista_trabajadores:
    name = lista_trabajadores[tra]
    if name[1] == 1:
        numero = ''
        cont = 0
        while tra[2 + cont] != ']':
            numero = numero + tra[2 + cont]
            cont+=1
        trabajador_asistiendo.append(int(numero))
contador = 0

for i in nombres:
    if contador in trabajador_asistiendo:
        contaminacion += float(i[4])*float(i[5])
        comunas_cantidad[i[2]] += 1
    contador +=1


productos = {}
for i in range(len(datos)):
    if datos[i][0] == 'p':
        productos[datos[i]] = datos[i+1].split()

productos_lista = []
for p in productos:
    numero = ''
    cont = 0
    while p[2+cont] != ']':
        cont+=1
        numero = numero + p[2+cont]
    productos_lista.append(int(numero))
