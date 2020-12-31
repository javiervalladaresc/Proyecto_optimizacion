import random

lista_nombres = ['raul','manuel','cristobal','diego','andres','claudio','javier',
                        'roberto','pedro','juan','antonio','alonso','sebastian','carlos','mauricio',
                        'pierre','alex','humberto','cristian','victor','felipe','jorge','aldo','roman',
                        'ximena','jimena','maria','laura','javiera','paula','pamela','juana','antonia','paloma','macarena',
                        'roberta','maria','valentina','alejandra','claudia','carla','lucia']

lista_de_apellidos = ['garcia','rodriguez','martinez','hernandez','lopez','gonzalez','perez','sanchez',
                        'ramirez','torres','flores','rivera','gomez','diaz','reyes','cruz','morales','ortiz','gutierrez']


comunas = {'santiago' : 5, 'renca':10,'maipu':17,'puente_alto':27,'san_bernardo':20,'sano_joaquin':10,
            'la_pintana':24,'el_bosque':16,'penalolen':12,'cerro_navia':10,'pudahuel':12,'macul':9,'cerrillos':10,
            'la_florida':20,'recoleta':7,'la_granja':18}

contaminacion = [ 0.53,0.16]

sueldos = [3000,2500,2700]

fase = [2,3,4]

file = open('datos.csv','w')

random.seed(42)

file.write('nombre,apellido,comuna,fase,distancia,contaminacion,sueldoxhora \n' )

contaminacion_codigo = []
sueldo_codigo = []
distancia_codigo = []
fase_codigo = []


for i in range(1300):
    nombre = random.choice(lista_nombres)
    apellido = random.choice(lista_de_apellidos)
    comuna = random.choice(list(comunas.keys()))
    distancia = str(comunas[comuna])
    sueldo = str(random.choice(sueldos ))
    fase = '2'
    cont = str(random.choice(contaminacion))
    contaminacion_codigo.append(cont)
    sueldo_codigo.append(sueldo)
    distancia_codigo.append(distancia)
    fase_codigo.append(fase)

    file.write(nombre + ',' + apellido + ',' + comuna + ',' + fase
                + ',' + distancia + ',' + cont + ',' + sueldo
                + '\n')

file.close()

file = open('datos_codigo.dat','w')

param = ['F','S','D','Cont']

for par in param:
    file.write('param '+par+':= \n')
    if par == 'F':
        for k in range(1300):
            file.write(str(k+1) + ' ' + str(fase_codigo[k]) + '\n')
        file.write('; \n \n')
    elif par == 'S':
        for k in range(1300):
            file.write(str(k+1) + ' ' + str(sueldo_codigo[k]) + '\n')
        file.write('; \n \n')
    elif par == 'D':
        for k in range(1300):
            file.write(str(k+1) + ' ' + str(distancia_codigo[k]) + '\n')
        file.write('; \n \n')
    elif par == 'Cont':
        for k in range(1300):
            file.write(str(k+1) + ' ' + str(contaminacion_codigo[k]) + '\n')
        file.write('; \n \n')
file.close()
