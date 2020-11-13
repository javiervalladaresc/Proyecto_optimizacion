from __future__ import division
import pyomo.environ as pyo

model = pyo.AbstractModel()

#Parametros fijos de nuestro modelo
model.gastos_fijos = pyo.Param(within = pyo.NonNegativeIntegers)
model.tra_permitidos = pyo.Param(within = pyo.NonNegativeIntegers)
model.cont_max = pyo.Param(within = pyo.NonNegativeIntegers)
model.prod_min = pyo.Param(within = pyo.NonNegativeIntegers)
model.precio_etico = pyo.Param(within = pyo.NonNegativeIntegers)
model.gan_min = pyo.Param(within = pyo.NonNegativeIntegers)
model.presupuesto = pyo.Param(within = pyo.NonNegativeIntegers)
model.fase = pyo.Param(within = pyo.NonNegativeIntegers)
model.min_tra = pyo.Param(within = pyo.NonNegativeIntegers)

#Largo de los datos
model.n = pyo.Param(within = pyo.NonNegativeIntegers) #Numero de trabajadores
model.m = pyo.Param(within = pyo.NonNegativeIntegers) #Numero de alimentos

#Indices de nuestros datos
model.I = pyo.RangeSet(1, model.m)
model.J = pyo.RangeSet(1, model.n)

#Parametros de alimentos
model.C = pyo.Param(model.I)
model.Q = pyo.Param(model.I)


#Parametros de trabajadores
model.S = pyo.Param(model.J)
model.F = pyo.Param(model.J)
model.D = pyo.Param(model.J)
model.Cont = pyo.Param(model.J)

#Variables de decision
model.x = pyo.Var(model.J, within=pyo.Binary)
model.p = pyo.Var(model.I, within=pyo.NonNegativeReals,bounds=(0,1700))
model.t_pro = pyo.Var(model.I, within=pyo.NonNegativeReals, bounds=(1,12), initialize=1)
model.t_tra = pyo.Var(model.J, within=pyo.NonNegativeReals, bounds=(0,8), initialize=0)




#Funcion objetivo
def obj_expresion(m):
    return -30*sum(m.Q[i]*m.p[i]*m.t_pro[i] for i in m.I) + 30*sum(m.Q[i]*m.C[i]*m.t_pro[i] for i in m.I) + sum(m.x[j]*m.S[j]*m.t_tra[j] for j in m.J) + m.gastos_fijos

model.OBJ = pyo.Objective(rule = obj_expresion)

#Restricciones
def restriccion_precio_sup(m,i): #Restriccion para un precio etico 
    return m.precio_etico >= m.p[i] 
model.Precio_r_s = pyo.Constraint(model.I, rule=restriccion_precio_sup)


def restriccion_horasproduccion(m,i): #Restriccion para las horas de produccion
    return 12 >= m.t_pro[i]
model.horasprod = pyo.Constraint(model.I,rule= restriccion_horasproduccion)


def restriccion_precio_inf(m,i): #Restriccion para una ganancia minima
    return m.p[i] >= m.C[i] + m.gan_min 
model.Precio_r_i = pyo.Constraint(model.I, rule=restriccion_precio_inf)


def restriccion_trabajadores(m): #Restriccion de numero de trabajadores por salud 
    return  m.tra_permitidos >=  sum(m.x[j] for j in m.J)
model.Max_trab = pyo.Constraint(rule = restriccion_trabajadores)


def restriccion_trabajadores_inf(m): #Restriccion de la cantidad minima de trabajadores
    return    sum(m.x[j] for j in m.J) >= m.min_tra
model.Min_trab = pyo.Constraint(rule = restriccion_trabajadores_inf)


def restriccion_contaminacion(m): #Restriccion para la contaminacion maxima permitida
    return  m.cont_max >= sum(m.x[j]*m.S[j]*m.Cont[j] for j in m.J) 
model.Max_cont = pyo.Constraint(rule = restriccion_contaminacion)


def restriccion_comuna(m,j): #Restriccion por comuna en cuarentena
    return  m.F[j] - m.fase >= m.x[j] 
model.Comuna_r = pyo.Constraint(model.J, rule = restriccion_comuna)

def activacion_horastrabajo(m,j): #Activacion variable tiempo
    return 1000*m.x[j] >= m.t_tra[j]
model.activar_var = pyo.Constraint(model.J,rule = activacion_horastrabajo)

def restriccion_horastrabajo_i(m,j): #Restriccion de horas de trabajo
    return  m.t_tra[j] - 80 + 1000*(1-m.x[j]) >= 0
model.horas_i = pyo.Constraint(model.J,rule = restriccion_horastrabajo_i)


def restriccion_horastrabajo_s(m,j): #Restriccion de horas de trabajo maximo para un trabajador
    return 1000*(1-m.x[j]) >= m.t_tra[j] - 160
model.horas_s = pyo.Constraint(model.J,rule = restriccion_horastrabajo_s)


def restriccion_produccion(m,i): #Restriccion de horas minimas de un trabajador
    return 30*m.Q[i]*m.t_pro[i] >= m.prod_min  
model.Produccion_r = pyo.Constraint(model.I,rule = restriccion_produccion)

def restriccion_hrsproduccion(m,i):
    return 360 >= m.t_pro[i]
model.hrsproduccion = pyo.Constraint(model.I, rule = restriccion_hrsproduccion)

def restriccion_presupuesto(m): #Restriccion de presupuesto de la empresa
    return m.presupuesto >= 30*sum(m.Q[i]*m.C[i]*m.t_pro[i] for i in m.I) + sum(m.x[j]*m.S[j]*m.t_tra[j] for j in m.J) 
model.Presupuesto_r = pyo.Constraint(rule = restriccion_presupuesto)


