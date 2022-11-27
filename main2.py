import random
import numpy as np

TAMANHO_CROMOSSOMO = 192
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.8

class Cromossomo:
    
    def __init__(self):
        self.genes=[]
        for i in range(TAMANHO_CROMOSSOMO):
            self.genes.append(0)
    
    def gerarGenes(self):
        for i in range(TAMANHO_CROMOSSOMO):
            self.genes[i] = random.randint(0,1)
    
    def getFitness(self,fn):
        return fn(self.genes)

    def cruzamentoPontoFixo(self,mate):
        crossover_point = random.randint(0,191)
        child = Cromossomo()
        flag=0
        for i in range(TAMANHO_CROMOSSOMO):
            if flag==0:
                child.genes[i] = self.genes[i]
                if i==crossover_point:
                    flag = 1
            elif flag==1:
                child.genes[i] = mate.genes[i]
        return child

    def cruzamentoPontoAleatorio(self,mate):
        crossover_point = random.randint(0,191)
        child = Cromossomo()
        flag=0
        for i in range(TAMANHO_CROMOSSOMO):
            if flag==0:
                child.genes[i] = self.genes[i]
                if i==crossover_point:
                    flag = 1
            elif flag==1:
                child.genes[i] = mate.genes[i]
                crossover_point = random.randint(i,191)
                if i == crossover_point:
                    flag = 0
        return child
    
    def mutate(self,mrate):
        if mrate<0 or mrate>1:
            mrate=0
        for i in range(TAMANHO_CROMOSSOMO):
            x=random.randint(0,100)
            if x<(mrate*100):
                self.genes[i] = 1 if self.genes[i]==0 else 0


class Population:
    
    def __init__(self, fn):
        self.pop_size = 0
        self.cromossomos=[]
        self.prox_geracao=[]
        self.funcao_aptidao = fn
    
    def inicializarPopulacao(self, p=10):
        self.pop_size = p
        for i in range(self.pop_size):
            self.cromossomos.append(Cromossomo())
            self.cromossomos[i].gerarGenes()
    
    def adicionarCromossomo(self, x):
        self.cromossomos.append(x)
        self.pop_size+=1

    def removerCromossomo(self, i):
        self.cromossomos.pop(i)
        self.pop_size-=1
    
    def getMelhorAptidao(self):
        best_val = 0
        best_index = 0
        for i in range(self.pop_size):
            this_val = self.cromossomos[i].getFitness(self.funcao_aptidao)
            if (this_val>best_val):
                best_val = this_val
                best_index = i
        return self.cromossomos[best_index],best_index
            
    
    def selecaoPorTorneio(self, sample_size=3):
        if sample_size>self.pop_size:
            sample_size=3
        tour = Population(self.funcao_aptidao)
        for i in range(sample_size):
            tour.adicionarCromossomo(self.cromossomos[random.randint(0,9)])
        par1,i = tour.getMelhorAptidao()
        tour.removerCromossomo(i)
        par2,i = tour.getMelhorAptidao()
        del tour
        return par1, par2

    def selecaoPorRoleta(self):
        popTemp = Population(self.funcao_aptidao)
        aptidaoPopulacao = 0
        for i in range(len(self.cromossomos)):
            popTemp.adicionarCromossomo(self.cromossomos[i])
        aptidoes = []
        for i in range(len(self.cromossomos)):
            aptidaoCromossomo = self.cromossomos[i].getFitness(self.funcao_aptidao)
            aptidoes.append(aptidaoCromossomo)
            aptidaoPopulacao += aptidaoCromossomo

        chromosome_probabilities = [chromosome/aptidaoPopulacao for chromosome in aptidoes]
        
        return np.random.choice(np.array(popTemp.cromossomos), 2, p=np.array(chromosome_probabilities))

    def reproducao(self, par1, par2):
        child = par1.cruzamentoPontoAleatorio(par2)
        child.mutate(MUTATION_RATE)
        return child
    
    def gerarProximaGeracao(self,elite=1,target=-1): # Gera a (i+1)ésima geração
        n_size = self.pop_size
        if elite==1:
            n_size-=1
            self.prox_geracao.append(self.getMelhorAptidao()[0])
        for i in range(self.pop_size):
            p1,p2 = self.selecaoPorTorneio()
            self.prox_geracao.append(self.reproducao(p1,p2))
        self.cromossomos = self.prox_geracao.copy()
        self.prox_geracao.clear()
        if self.getMelhorAptidao()[0].getFitness(self.funcao_aptidao)==target:
            return True
        return False


class KnightBoard:
    @staticmethod
    def pos2board(pos):
        bpos=[(pos[1]-1),0]
        if pos[0]=="A":
            bpos[1]=0
        elif pos[0]=="B":
            bpos[1]=1
        elif pos[0]=="C":
            bpos[1]=2
        elif pos[0]=="D":
            bpos[1]=3
        elif pos[0]=='E':
            bpos[1]=4
        elif pos[0]=="F":
            bpos[1]=5
        elif pos[0]=="G":
            bpos[1]=6
        elif pos[0]=="H":
            bpos[1]=7
        return bpos
    
    def __init__(self, kpos=["E4"]):
        self.kn_pos = self.pos2board([kpos[0],int(kpos[1])])
        self.ori_pos = self.kn_pos.copy()
        self.board=[0]*8
        for i in range(8):
            self.board[i] = [0]*8
        self.board[self.kn_pos[0]][self.kn_pos[1]]=1
    
    def reset(self):
        self.kn_pos = self.ori_pos
        for i in range(8):
            self.board[i] = [0]*8
        self.board[self.kn_pos[0]][self.kn_pos[1]]=1
    
    def isVisited(self, pos):
        return self.board[pos[0]][pos[1]]==1
    
    @staticmethod
    def decodeMove(enc_mv):
        return (enc_mv[0]*4+enc_mv[1]*2+enc_mv[2])
    @staticmethod
    def encodeMove(mv):
        if mv==0:
            return [0,0,0]
        elif mv==1:
            return [0,0,1]
        elif mv==2:
            return [0,1,0]
        elif mv==3:
            return [0,1,1]
        elif mv==4:
            return [1,0,0]
        elif mv==5:
            return [1,0,1]
        elif mv==6:
            return [1,1,0]
        elif mv==7:
            return [1,1,1]
    
    def move(self, enc_mv):
        mv = self.decodeMove(enc_mv)
        if mv==0:
            if self.kn_pos[0]>=2 and self.kn_pos[1]<=6:
                if self.isVisited([self.kn_pos[0]-2,self.kn_pos[1]+1]):
                    return False
                self.kn_pos = [self.kn_pos[0]-2,self.kn_pos[1]+1]
                self.board[self.kn_pos[0]][self.kn_pos[1]]=1
                return True
            return False
        elif mv==1:
            if self.kn_pos[0]>=1 and self.kn_pos[1]<=5:
                if self.isVisited([self.kn_pos[0]-1,self.kn_pos[1]+2]):
                    return False
                self.kn_pos = [self.kn_pos[0]-1,self.kn_pos[1]+2]
                self.board[self.kn_pos[0]][self.kn_pos[1]]=1
                return True
            return False
        elif mv==2:
            if self.kn_pos[0]<=6 and self.kn_pos[1]<=5:
                if self.isVisited([self.kn_pos[0]+1,self.kn_pos[1]+2]):
                    return False
                self.kn_pos = [self.kn_pos[0]+1,self.kn_pos[1]+2]
                self.board[self.kn_pos[0]][self.kn_pos[1]]=1
                return True
            return False
        elif mv==3:
            if self.kn_pos[0]<=5 and self.kn_pos[1]<=6:
                if self.isVisited([self.kn_pos[0]+2,self.kn_pos[1]+1]):
                    return False
                self.kn_pos = [self.kn_pos[0]+2,self.kn_pos[1]+1]
                self.board[self.kn_pos[0]][self.kn_pos[1]]=1
                return True
            return False
        elif mv==4:
            if self.kn_pos[0]<=5 and self.kn_pos[1]>=1:
                if self.isVisited([self.kn_pos[0]+2,self.kn_pos[1]-1]):
                    return False
                self.kn_pos = [self.kn_pos[0]+2,self.kn_pos[1]-1]
                self.board[self.kn_pos[0]][self.kn_pos[1]]=1
                return True
            return False
        elif mv==5:
            if self.kn_pos[0]<=6 and self.kn_pos[1]>=2:
                if self.isVisited([self.kn_pos[0]+1,self.kn_pos[1]-2]):
                    return False
                self.kn_pos = [self.kn_pos[0]+1,self.kn_pos[1]-2]
                self.board[self.kn_pos[0]][self.kn_pos[1]]=1
                return True
            return False
        elif mv==6:
            if self.kn_pos[0]>=1 and self.kn_pos[1]>=2:
                if self.isVisited([self.kn_pos[0]-1,self.kn_pos[1]-2]):
                    return False
                self.kn_pos = [self.kn_pos[0]-1,self.kn_pos[1]-2]
                self.board[self.kn_pos[0]][self.kn_pos[1]]=1
                return True
            return False
        elif mv==7:
            if self.kn_pos[0]>=2 and self.kn_pos[1]>=1:
                if self.isVisited([self.kn_pos[0]-2,self.kn_pos[1]-1]):
                    return False
                self.kn_pos = [self.kn_pos[0]-2,self.kn_pos[1]-1]
                self.board[self.kn_pos[0]][self.kn_pos[1]]=1
                return True
            return False

    def tryRepair(self,mv_list,index):
        ori_mv=self.decodeMove(mv_list[index*3:(index+1)*3])
        for i in range(8):
            if i!=ori_mv:
                enc=self.encodeMove(i)
                if self.move(enc):
                    mv_list[index*3]=enc[0]
                    mv_list[index*3+1]=enc[1]
                    mv_list[index*3+2]=enc[2]
                    return True
        return False
        
    def getMovimentosValidos(self,mv_list):# Funcao aptidao. Avaliacao de movimentos legais.
        self.reset()
        num_mvs = len(mv_list)//3
        assert len(mv_list)%3==0
        count = 0
        for i in range(num_mvs):
            if not (self.move(mv_list[i*3:(i+1)*3])):
                if not (self.tryRepair(mv_list,i)):
                    break
            count+=1
        return count
        
    def printMovimentos(self,mv_list): # print movimentos em ordem
        self.reset()
        num_mvs = len(mv_list)//3
        assert len(mv_list)%3==0
        mv_arr = [-1]*8
        for i in range(8):
            mv_arr[i] = [-1]*8
        mv_arr[self.kn_pos[0]][self.kn_pos[1]]=0
        for i in range(num_mvs):
            if not (self.move(mv_list[i*3:(i+1)*3])):
                break
            mv_arr[self.kn_pos[0]][self.kn_pos[1]]=i+1
        print("-----Matriz de movimentos-----")
        for i in reversed(range(8)):
            print(mv_arr[i])
        return

while True:
    pos = []
    pos.append(chr(random.randint(ord('A'), ord('H'))))
    pos.append(random.randint(1,8))
    print("Posição inicial do cavalo: ",pos)
    break
	

knboard = KnightBoard([pos[0],pos[1]])
chb=Population(knboard.getMovimentosValidos)
chb.inicializarPopulacao(50)


for i in range(2000):
    if i%350==0:
        MUTATION_RATE=0.1
    if i%350==50:
        MUTATION_RATE=0.01
    

    if (chb.gerarProximaGeracao(1,63)):
        print("Solução encontrada na geração: ", i)
        break
    
x,_=chb.getMelhorAptidao()
if (x.getFitness(knboard.getMovimentosValidos))!=63:
	print("Não foi possível encontrar uma solução em 2000 gerações")
	print("Aptidão Final: ",x.getFitness(knboard.getMovimentosValidos))
knboard.printMovimentos(x.genes)

