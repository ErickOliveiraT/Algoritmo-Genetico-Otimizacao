#Trabalho 1 - Inteligência Artificial
#Érick de Oliveira Teixeira - 2017001437
#Programa responsável por realizar uma bateria de testes nos algoritmos desenvolvidos

import os

#Configuração dos parâmetros:
params = [[4,0.01,5],[40,0.01,5],[100,0.01,5],[4,0.01,50],[40,0.01,50],[100,0.01,50],[4,0.05,5],[4,0.05,50],[4,0.05,100],[4,0.1,5],[4,0.1,50],[4,0.1,100],[40,0.1,100],[100,0.1,100]]
#Quantidade de execuções para cada configuração:
qnt_exec = 100
#Parâmetro de cruzamento:
p_cross = 'media'

cont = 0
for config in params:
	cont += 1
	print('Executando teste {} de {}'.format(cont,len(params)))
	c1 = str(config[0])
	c2 = str(config[1])
	c3 = str(config[2])
	command = 'python ag_{}_test.py {} {} {} {}'.format(p_cross,c1,c2,c3,qnt_exec)
	os.system(command)
print('Testes finalizados')