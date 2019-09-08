#Trabalho 1 - Inteligência Artificial
#Érick de Oliveira Teixeira - 2017001437
#Algoritmo Genético para otimização da função f(x) = x^2 para 0 <= x <= 31
#Versão para testes com crossover por média dos pais

from random import randint
import numpy as np
import sys

global tam_pop, prob_mutacao, nro_ger

#Captura dos parâmetros do AG:
tam_pop = int(sys.argv[1]) #Tamanho da população
prob_mutacao = float(sys.argv[2]) #Probabilidade de mutação
nro_ger = int(sys.argv[3]) #Número de gerações
qnt_exec = int(sys.argv[4]) #Quantidade de execuções

#Escrita no arquivo de log
nome_arq = str(tam_pop)+'_'+str(prob_mutacao*100)+'%_'+str(nro_ger)+'_media_freq.txt'
path_arq = 'Testes/'+nome_arq
arq = open(path_arq,'w')
arq.write('Tamanho da população: ' + str(tam_pop) + '\n')
arq.write('Taxa de mutação: ' + str(prob_mutacao*100) + ' %\n')
arq.write('Número de gerações: ' + str(nro_ger) + '\n')
arq.write('Operador de cruzamento: Média\n')
arq.write('Quantidade de execuções: {}\n\n'.format(str(qnt_exec)))

if nro_ger == 0:
	print("Favor inserir nro de gerações maior que 0")
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

def get_bin(x):
	bits = []
	nbin = format(x, 'b')
	if len(nbin) < 5:
		for i in range(0,5-len(nbin)):
			bits.append(0)
	for char in nbin:
		if char == '0':
			bits.append(0)
		else:
			bits.append(1)
	return bits

def crossover(selecionados): #Realiza o crossover e aplica mutação (se for o caso)
	pai1 = selecionados[0]
	pai2 = selecionados[1]
	media = int((bitsToDec(pai1)+bitsToDec(pai2))/2) #Calcula média entre os dois pais
	filho = get_bin(media) #Forma o filho com base na média dos dois pais
	flags_mutacao_f = np.random.choice(2, 5, p=[1-prob_mutacao,prob_mutacao], replace=True) #Flags para indicar se ocorrerá mutação nos cromossomos do filho
	cont = 0
	for flag in flags_mutacao_f: #Aplica mutações no filho 1 (se for o caso)
		if flag == 1 and filho[cont] == 0:
			filho[cont] = 1
		elif flag == 1 and filho[cont] == 1:
			filho[cont] = 0
		cont += 1	
	return filho

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

cont = 0
melhores = []
while cont < qnt_exec:
	ger_atual = 1 #Geração atual
	pop = geraPopulacao() #Gera população inicial
	for i in range(0,nro_ger): #Início da evolução
		apt = calcAptidao(pop) #Calcula aptidão
		sel = selecionar(pop,apt) #Seleciona 2 indivíduos
		prox_ger = [] #Variável que guarda os integrantes da proxima geração
		for j in range(0,int(tam_pop)): #Gera a quantidade de filhos suficiente para formar a próxima geração
			sel = selecionar(pop,apt)
			filho = crossover(sel)
			prox_ger.append(filho)
		pop = prox_ger #Atualiza a geração com os novos indivíduos formados
		ger_atual += 1

	pop = ordenaPopulacao(pop) #Ordena a população com vase em valores decrescentes de f(x)
	melhores.append(bitsToDec(pop[0]))
	cont += 1

m = np.array(melhores)
uniqueValues, occurCount = np.unique(m, return_counts=True)

for i in range(0,len(occurCount)):
	freq = round((occurCount[i]*100)/qnt_exec,2)
	print('x = {}: {} ocorrencia(s) -- {} %'.format(uniqueValues[i],occurCount[i],freq))
	arq.write('x = {}: {} ocorrencia(s) -- {} %'.format(uniqueValues[i],occurCount[i],freq)+'\n')
arq.close()