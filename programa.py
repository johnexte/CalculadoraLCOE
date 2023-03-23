"""
    CALCULADORA DEL COSTO NIVELADO DE ENERGÍA
    
    DESARROLADORES:
        - John Esteban Pulido Salinas 202013192
        - Luis Orlando Pérez Monsalve 202015274
        - Daniel Andrés Posada Perez  202013165
"""

"""
    RECOLECCIÓN DE LOS DATOS NECESARIOS PARA EL CÁLCULO DEL LCOE:
"""

#Se importan las librerias:

from os import system

#Se limpia la consola:

system("cls")

#Se definen las funciones necesarias para pedir datos:

def pedirDatos(textoConsola: str, tipo: str):
    """
        textoConsola (str): lo que se le va a imprimir al usuario
        tipo (str): 'int','float','str'
    """
    while True:
        try:
            ingresado = input(textoConsola)
            if tipo == 'int':
                dato = int(ingresado.strip().replace('%',''))
                break
            elif tipo == 'float':
                dato = float(ingresado.strip().replace('%',''))
                break
            elif tipo == 'str':
                dato = ingresado.strip()
                break
            else:
                print("¡El tipo de dato es incorrecto!")
        except:
            print('Ingrese bien el tipo de dato solicitado...')
    return dato


print('-'*30,'CALCULADORA DE LCOE','-'*30,'\n')
input('Presione enter para comemzar...')
print()

#Generales:
print('-'*30,'PARAMETROS GENERALES','-'*30,'\n')
vidaUtil = pedirDatos('Ingrese la vida útil del proyecto (T) [años]: ', 'int') #T
factorPlanta = pedirDatos('Ingrese el factor de planta (CF) [%]: ', 'float') #CF
tasaDescuento = pedirDatos('Ingrese la tasa de descuento para el proyecto de generación (WACC) [%]: ','float') #gamma
inversionTotal = pedirDatos('Ingrese la inversión total del proyecto (SP) [MMUSD/MW] [USD/W]: ','float') #SP 
delta = pedirDatos('Ingrese el factor de impuestos que incrementa los costos de inversión [%]: ','float') #d
degradacionSistema = pedirDatos('Ingrese el porcentaje de degradación del sistema en un año [%]: ','float')

#Costos de operación:
print()
print('-'*30,'PARAMETROS COSTOS OP','-'*30,'\n')
costosOMF = pedirDatos('Ingrese el costo de operación y mantenimiento fijo del proyecto al año [USD/MWh/año]: ','float') #f
costosOMV = pedirDatos('Ingrese los costos de operación y mantenimientos variables: [USD/MWh]: ', 'float') #w
cambioOMF = pedirDatos('Ingrese el porcentaje de cambio anual de los costos fijos [%]: ','float')
cambioOMV = pedirDatos('Ingrese el porcentaje de cambio anual de los costos varianles [%]: ','float')
print()

#Se reasignan los nombres de las variables para seguir la nomenclatura de las fórmulas:

T =vidaUtil #[años]
CF = factorPlanta/100 # Qué porcentaje se uso realemnete la planta en un año
r = tasaDescuento/100 # WACC
SP = inversionTotal #[MMUSD/MW]=[USD/W] Inversion inicial del proyecto en millones de dolares por MW generados
wi = costosOMV #[USD/MWh] son los costos varibles por MWh
fi = costosOMF #[USD/MWh] son los costos fijos por MWh
f0 = cambioOMF/100
w0 = cambioOMV/100
x0 = degradacionSistema/100
d = delta/100
 
#Calculo de nuevas variables:

y = 1/(1+r) #factor de descuento
xt = [] #Porcentajes de funcionalidad en el año t con respecto a la capacidad inicial
x = 1
for t in range(T):
    x -= x0
    xt.append(x)
ft = []
f = fi
for t in range(T):
    ft.append(f)
    f = f*(1+f0)
wt = []
w = wi
for t in range(T):
    wt.append(w)
    w = wi*(1+w0)

"""
    DESARROLLO DE LOS CÁLCULOS:
"""

# Se definen las funciones necesarias para calcular el LCOE:

def calcularCostosInversion(SP,CF,xt,y,T):
    degradacion = 0
    for t in range(T):
        degradacion += xt[t]*y**t
    LCOE_INV = SP*1000000/(8760*CF*degradacion)
    return LCOE_INV

def calcularCostosOMF(ft,y,CF,xt):
    fijos = 0
    for t in range(T):
        fijos += ft[t]*y**t
    degradacion = 0
    for t in range(T):
        degradacion += xt[t]*y**t
    LCOE_OMF = fijos*1000/(8760*CF*degradacion)
    return LCOE_OMF

def calcularCostosOMV(wt,xt,y):
    variables = 0
    for t in range(T):
        variables += wt[t]*xt[t]*y**t
    degradacion = 0
    for t in range(T):
        degradacion += xt[t]*y**t
    LCOE_OMV = variables/degradacion
    return LCOE_OMV

LCOE_INV = calcularCostosInversion(SP,CF,xt,y,T)*(1+d)
LCOE_OMF = calcularCostosOMF(ft,y,CF,xt)
LCOE_OMV = calcularCostosOMV(wt,xt,y)
LCOE = LCOE_INV + LCOE_OMF + LCOE_OMV

"""
    VISUALIZACIÓN DE LOS CÁLCULOS:
"""
print('-'*30,'RESULATDOS CÁLCULOS','-'*30,'\n')
print('EL LCOE TOTAL calculado es ',round(LCOE,3),' [USD/MWh]')
print('-'*70)
print('EL LCOE de inversión calculado es ',round(LCOE_INV,3),' [USD/MWh]')
print('EL LCOE de costos fijos calculado es ',round(LCOE_OMF,3),' [USD/MWh]')
print('EL LCOE de costos variables calculado es ',round(LCOE_OMV,3),' [USD/MWh]')
print('-'*70)

input('Presione cualquier tecla para finalizar....')