from __future__ import division
import pyomo.environ as pyo

model = pyo.AbstractModel()

model.gastos_fijos = pyo.Param(within = pyo.NonNegativeIntegers)
model.tra_permitidos = pyo.Param(within = pyo.NonNegativeIntegers)
model.cont_max = pyo.Param(within = pyo.NonNegativeIntegers)
model.prod_min = pyo.Param(within = pyo.NonNegativeIntegers)
model.precio_etico = pyo.Param(within = pyo.NonNegativeIntegers)
model.gan_min = pyo.Param(within = pyo.NonNegativeIntegers)
model.presupuesto = pyo.Param(within = pyo.NonNegativeIntegers)
model.fase = pyo.Param(within = pyo.NonNegativeIntegers)
model.min_tra = pyo.Param(within = pyo.NonNegativeIntegers)

model.n = pyo.Param(within = pyo.NonNegativeIntegers) #trabajadores
model.m = pyo.Param(within = pyo.NonNegativeIntegers) #alimentos

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
model.x = pyo.Var(model.J, domain=pyo.Binary)
model.p = pyo.Var(model.I, domain=pyo.NonNegativeReals)
model.t_pro = pyo.Var(model.I, domain=pyo.PositiveIntegers)
model.t_tra = pyo.Var(model.J, domain=pyo.PositiveIntegers)


#Funcion objetivo
def obj_expresion(m):
    return -sum(m.Q[i]*m.p[i]*m.t_pro[i] for i in m.I) + sum(m.Q[i]*m.C[i]*m.t_pro[i] for i in m.I) + sum(m.x[j]*m.S[j]*m.t_tra[j] for j in m.J) + m.gastos_fijos

model.OBJ = pyo.Objective(rule = obj_expresion)

#Restricciones
def restriccion_precio_sup(m,i):
    return m.precio_etico >= m.p[i] 
model.Precio_r_s = pyo.Constraint(model.I, rule=restriccion_precio_sup)

def restriccion_precio_inf(m,i):
    return m.p[i] >= m.C[i] - m.gan_min 
model.Precio_r_i = pyo.Constraint(model.I, rule=restriccion_precio_inf)

def restriccion_trabajadores(m):
    return  m.tra_permitidos >=  sum(m.x[j] for j in m.J)
model.Max_trab = pyo.Constraint(rule = restriccion_trabajadores)

def restriccion_trabajadores_inf(m):
    return    sum(m.x[j] for j in m.J) >= m.min_tra
model.Min_trab = pyo.Constraint(rule = restriccion_trabajadores_inf)

def restriccion_contaminacion(m):
    return  m.cont_max >= sum(m.x[j]*m.S[j]*m.Cont[j] for j in m.J) 
model.Max_cont = pyo.Constraint(rule = restriccion_contaminacion)

def restriccion_comuna(m,j):
        return  m.F[j] - m.fase >= m.x[j] 
model.Comuna_r = pyo.Constraint(model.J, rule = restriccion_comuna)

def restriccion_horastrabajo_i(m,j):
    return m.t_tra[j]>=4
model.horas_i = pyo.Constraint(model.J,rule = restriccion_horastrabajo_i)
def restriccion_horastrabajo_s(m,j):
    return 8 >= m.t_tra[j]
model.horas_s = pyo.Constraint(model.J,rule = restriccion_horastrabajo_s)


def restriccion_produccion(m,i):
    return m.Q[i]*m.t_pro[i] >= m.prod_min  
model.Produccion_r = pyo.Constraint(model.I,rule = restriccion_produccion)

def restriccion_presupuesto(m):
    return m.presupuesto >= sum(m.Q[i]*m.C[i]*m.t_pro[i] for i in m.I) + sum(m.x[j]*m.S[j]*m.t_tra[j] for j in m.J) 
model.Presupuesto_r = pyo.Constraint(rule = restriccion_presupuesto)
