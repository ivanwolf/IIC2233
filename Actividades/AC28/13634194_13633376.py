import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df_examenes = pd.read_csv('examenes.csv', )
df_pacientes = pd.read_csv('pacientes_nuevos.csv')


examen0 = df_examenes.examen0
examen1 = df_examenes.examen1
examen2 = df_examenes.examen2
examen3 = df_examenes.examen3

condicion_sano = df_examenes.diagnostico == 'sano'
sanos = df_examenes[condicion_sano]
enf = df_examenes[~condicion_sano]


## 0 vs 1

plt.scatter(sanos.examen0, sanos.examen1, color='green')
plt.scatter(enf.examen0, enf.examen1, color='red')
plt.xlabel('Examen 0')
plt.ylabel('Examen 1')
plt.show()

## 0 vs 2

plt.scatter(sanos.examen0, sanos.examen2, color='green')
plt.scatter(enf.examen0, enf.examen2, color='red')
plt.xlabel('Examen 0')
plt.ylabel('Examen 2')
plt.show()

## 0 vs 3

plt.scatter(sanos.examen0, sanos.examen3, color='green')
plt.scatter(enf.examen0, enf.examen3, color='red')
plt.xlabel('Examen 0')
plt.ylabel('Examen 3')
plt.show()

## 1 vs 2

plt.scatter(sanos.examen1, sanos.examen2, color='green')
plt.scatter(enf.examen1, enf.examen2, color='red')
plt.xlabel('Examen 1')
plt.ylabel('Examen 2')
plt.show()

## 1 vs 3

plt.scatter(sanos.examen1, sanos.examen3, color='green')
plt.scatter(enf.examen1, enf.examen3, color='red')
plt.xlabel('Examen 1')
plt.ylabel('Examen 3')
plt.show()

## 2 vs 3

plt.scatter(sanos.examen2, sanos.examen3, color='green')
plt.scatter(enf.examen2, enf.examen3, color='red')
plt.xlabel('Examen 2')
plt.ylabel('Examen 3')
plt.show()


############# Ajustado con polinomios

fit01 = np.polyfit(examen0, examen1, 2)
fit02 = np.polyfit(examen0, examen2, 2)
fit03 = np.polyfit(examen0, examen3, 2)
fit12 = np.polyfit(examen1, examen2, 2)
fit13 = np.polyfit(examen1, examen3, 2)
fit23 = np.polyfit(examen2, examen3, 2)



## 0 vs 1

plt.scatter(sanos.examen0, sanos.examen1, color='green')
plt.scatter(enf.examen0, enf.examen1, color='red')
plt.xlabel('Examen 0')
plt.ylabel('Examen 1')
plt.plot(fit01)
plt.show()

## 0 vs 2

plt.scatter(sanos.examen0, sanos.examen2, color='green')
plt.scatter(enf.examen0, enf.examen2, color='red')
plt.xlabel('Examen 0')
plt.ylabel('Examen 2')
plt.plot(fit02)
plt.show()

## 0 vs 3

plt.scatter(sanos.examen0, sanos.examen3, color='green')
plt.scatter(enf.examen0, enf.examen3, color='red')
plt.xlabel('Examen 0')
plt.ylabel('Examen 3')
plt.plot(fit03)
plt.show()

## 1 vs 2

plt.scatter(sanos.examen1, sanos.examen2, color='green')
plt.scatter(enf.examen1, enf.examen2, color='red')
plt.xlabel('Examen 1')
plt.ylabel('Examen 2')
plt.plot(fit12)
plt.show()

## 1 vs 3

plt.scatter(sanos.examen1, sanos.examen3, color='green')
plt.scatter(enf.examen1, enf.examen3, color='red')
plt.xlabel('Examen 1')
plt.ylabel('Examen 3')
plt.plot(fit13)
plt.show()

## 2 vs 3

plt.scatter(sanos.examen2, sanos.examen3, color='green')
plt.scatter(enf.examen2, enf.examen3, color='red')
plt.xlabel('Examen 2')
plt.ylabel('Examen 3')
plt.plot(fit23)
plt.show()


print('El mejor espacio encontrado es del gráfico Examen 1 vs Examen 3')
print('Del punto correspondiente al peak del fit hacia la izquierda, los pacientes'
      'estan enfermos, en cambio, hacia la derecha estan los pacientes sanos')






