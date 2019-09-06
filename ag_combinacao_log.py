#Trabalho 1 - Inteligência Artificial
#Érick de Oliveira Teixeira - 2017001437
#Algoritmo Genético para otimização da função f(x) = x^2 para 0 <= x <= 31
#Versão de crossover por combinação dos pais com criação de arquivo de log

from random import randint
from time import time
import numpy as np
import sys

global tam_pop, mutacao, nro_ger

#Definição dos parâmetros do AG:
tam_pop = 4 #Tamanho da população
prob_mutacao = 0.01 #Probabilidade de mutação
nro_ger = 5 #Número de gerações

#Escrita no arquivo de log
nome_arq = str(tam_pop)+'_'+str(prob_mutacao*100)+'%_'+str(nro_ger)+'_comb.txt'
path_arq = 'Testes/'+nome_arq
arq = open(path_arq,'w')
arq.write('Tamanho da população: ' + str(tam_pop) + '\n')
arq.write('Taxa de mutação: ' + str(prob_mutacao*100) + ' %\n')
arq.write('Número de gerações: ' + str(nro_ger) + '\n')
arq.write('Operador de cruzamento: Combinação\n')

if tam_pop%2 != 0 or nro_ger == 0:
	print("Favor inserir nro de gerações maior que 0 e um tamanho da populacao divisível por 2")
	sys.exit()

def funcao(x): #Funcão a ser utilizada
	return x**2

def geraIndividuo(): #Gera cromossomo randômico
	individuo = []
	for i in range(0,5):
		cromossomo = randint(0,1)
		individuo.append(cromossomo)
	return individuo

def geraPopulacao(): #Gera população randômica
	populacao = []
	for i in range(0,tam_pop):
		populacao.append(geraIndividuo())
	return populacao

def bitsToDec(cromossomos): #Converte os bits dos cromossomos para decimal
	soma = cromossomos[4]
	soma += cromossomos[3] * 2
	soma += cromossomos[2] * 4
	soma += cromossomos[1] * 8
	soma += cromossomos[0] * 16
	return soma

def calcAptidao(populacao): #Calcula a aptidão dos indivíduos da população
	soma = 0
	aptidao = []
	for individuo in populacao:
		soma += funcao(bitsToDec(individuo)) #Somatório de f(x)
	for individuo in populacao:
		aptidao.append(funcao(bitsToDec(individuo))/soma) #Probabilidade de Seleção do indivíduo
	return aptidao

def selecionar(populacao, aptidao): #seleciona 2 indivíduos da população baseado na aptidão
	selecionados = []
	escolhas = np.random.choice(len(populacao), 2, p=aptidao, replace=False)
	selecionados.append(populacao[escolhas[0]])
	selecionados.append(populacao[escolhas[1]])
	return selecionados

def crossover(selecionados): #Realiza o crossover e aplica mutação (se for o caso)
	pai1 = selecionados[0]
	pai2 = selecionados[1]
	filho1 = []
	filho2 = []
	pto_corte = randint(1,5) #Randomização do ponto de corte para crossover
	for i in range(0,pto_corte): #Criação dos filhos 
		filho1.append(pai1[i])
		filho2.append(pai2[i])
	for i in range(pto_corte,5): #Criação dos filhos
		filho1.append(pai2[i])
		filho2.append(pai1[i])
	flags_mutacao_f1 = np.random.choice(2, 5, p=[1-prob_mutacao,prob_mutacao], replace=True) #Flags para indicar se ocorrerá mutação nos cromossomos do filho 1
	flags_mutacao_f2 = np.random.choice(2, 5, p=[1-prob_mutacao,prob_mutacao], replace=True) #Flags para indicar se ocorrerá mutação nos cromossomos do filho 2
	cont = 0
	for flag in flags_mutacao_f1: #Aplica mutações no filho 1 (se for o caso)
		if flag == 1 and filho1[cont] == 0:
			filho1[cont] = 1
		elif flag == 1 and filho1[cont] == 1:
			filho1[cont] = 0
		cont += 1
	cont = 0
	for flag in flags_mutacao_f2: #Aplica mutações no filho 2 (se for o caso)
		if flag == 1 and filho2[cont] == 0:
			filho2[cont] = 1
		elif flag == 1 and filho2[cont] == 1:
			filho2[cont] = 0
		cont += 1
	return [filho1,filho2] #A função retorna os dois novos indivíduos gerados

def ordenaPopulacao(populacao): #Ordena populacao[] para valores decrescentes de f(x)
	elementos = tam_pop-1
	ordenado = False
	while not ordenado: #Aplicação adaptada do algoritmo BubbleSort
		ordenado = True
		for i in range(elementos):
			if bitsToDec(populacao[i]) < bitsToDec(populacao[i+1]):
				populacao[i], populacao[i+1] = populacao[i+1],populacao[i]
				ordenado = False
	return populacao

inicio = time()
ger_atual = 1 #Geração atual
pop = geraPopulacao() #Gera população inicial
for i in range(0,nro_ger): #Início da evolução
	print("\nGeração {}:\n\nPopulação = {}".format(ger_atual,pop))
	arq.write("\nGeração {}:\n\nPopulação = {}".format(ger_atual,pop)+'\n')
	apt = calcAptidao(pop) #Calcula aptidão
	print("Aptidão = {}".format(apt))
	arq.write("Aptidão = {}".format(apt)+'\n')
	sel = selecionar(pop,apt) #Seleciona 2 indivíduos
	prox_ger = [] #Variável que guarda os integrantes da proxima geração
	for j in range(0,int(tam_pop/2)): #Gera a quantidade de filhos suficiente para formar a próxima geração
		sel = selecionar(pop,apt)
		print("Selecionados = {}".format(sel))
		arq.write("Selecionados = {}".format(sel)+'\n')
		filhos = crossover(sel)
		print("Filhos = {}".format(filhos))
		arq.write("Filhos = {}".format(filhos)+'\n')
		prox_ger.append(filhos[0])
		prox_ger.append(filhos[1])
	pop = prox_ger #Atualiza a geração com os novos indivíduos formados
	ger_atual += 1

fim = time()
pop = ordenaPopulacao(pop) #Ordena a população com vase em valores decrescentes de f(x)
print("\nPopulação Final:\n\n{}".format(pop))
arq.write("\nPopulação Final:\n\n{}".format(pop)+'\n')
for individuo in pop:
	print(bitsToDec(individuo), end=' ')
	arq.write(str(bitsToDec(individuo))+' ')

#Mostrando o melhor indivíduo após todas as gerações:
print("\n\nMelhor indivúduo:\n\nx = {} = {}\nf(x) = {}".format(pop[0],bitsToDec(pop[0]),funcao(bitsToDec(pop[0]))))
arq.write("\n\n\nMelhor indivúduo:\n\nx = {} = {}\nf(x) = {}".format(pop[0],bitsToDec(pop[0]),funcao(bitsToDec(pop[0])))+'\n')
erro = round((abs(bitsToDec(pop[0])-31)/31)*100,2)
print('Erro = {}'.format(str(erro)+' %'))
arq.write('Erro = {}'.format(str(erro)+' %\n'))
print('Tempo de execução: {} s'.format(round(fim-inicio,2)))
arq.write('Tempo de execução: {} s'.format(round(fim-inicio,2)))
arq.close()