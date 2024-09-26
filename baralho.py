import random
import itertools

Manilhas = ["4 de Paus", "7 de Copas", "Ás de Espadas", "7 de Ouros"]
Ordem = {"4": 4, "5": 5, "6": 6, "7": 7, "Dama": 8, "Valete": 9, "Rei": 10, "Ás": 11, "2": 12, "3": 13}
Naipes = ["Copas", "Espadas", "Ouros", "Paus"]
class Carta:
    def __init__(self, num, naipe):
        self.num = num
        self.naipe = naipe
    
    def __str__(self):
        return str(self.num) + ' de ' + str(self.naipe)

    def __repr__(self):
        return f"{self.num} de {self.naipe}"
    
    def __gt__(carta1, carta2):
       ponto1, ponto2 = 0, 0
       for i in range(4):
           if str(carta1) == Manilhas[i]:
               ponto1 = i
           elif str(carta2) == Manilhas[i]:
               ponto2 = i
       if ponto1 > ponto2:
           return False
       elif ponto1 < ponto2:
           return True
       else:
           if Ordem[carta1.num] > Ordem[carta2.num]:
                return True
           else:
               return False
    
    def __eq__(carta1, carta2: 'Carta'):
        if Ordem[carta1.num] == Ordem[carta2.num]:
            return True
        else:
            return False
        
    def __lt__(self, carta2):
        return not self.__gt__(carta2) and not self.__eq__(carta2)
    
class Baralho:
    def __init__(self):
        self.cartas = []
        for naipe in Naipes:
            for numero in Ordem:
                carta = Carta(numero, naipe)
                self.cartas.append(carta)
    
    def show(self):
        return self.cartas  

class Jogador:
    def __init__(self, cartas):
        self.cartas = cartas
    
    def show(self):
        return self.cartas

    
if __name__ == '__main__':
    print('Bem vindo ao Truco Mineiro! As cartas serão sorteadas aos jogadores. ')
    rotacao = 0
    dupla1P = 0
    dupla2P = 0
    baralho = Baralho()
    turno = [1, 2, 3, 4]
    turno = turno[rotacao:] + turno[rotacao:] #Dinâmica de rotação do baralho
    rotacao += 1
    if rotacao == 4: rotacao = 0

    while dupla1P < 12 and dupla2P < 12:
        ganho = -1
        valor = 2
        random.shuffle(baralho.show())
        jogador = []
        j = 0
        for i in range(4):
            jogador.append(Jogador(baralho.show()[j:j + 3]))
            j += 3
        
        ciclo = itertools.cycle(turno)
        vez = next(ciclo)
        prox = next(ciclo)
        parcial1 = 0
        parcial2 = 0
        
        for _ in range(3): #Ciclo de rodadas
            cartasD1 = []
            cartasD2 = []
            jogada = {}
            mesa = []
            for i in range(4): #Para cada jogador, uma jogada
                x = input(f"Vez do jogador {vez}. Digite qualquer coisa para iniciar sua jogada")
                print(f"Cartas na mesa: {mesa}")
                print(f"Suas cartas: {jogador[vez - 1].show()}")
                while True: #Gravar pedido de truco e carta jogada pelo jogador[vez]
                    x = input("Digite a ordem da carta que deseja jogar ou 'truco' para pedir truco")
                    if str(x).lower() == 'truco':
                        res = input(f"Jogador {vez} pede truco. Jogador {prox}, aceitas? Digite 'S' para aceitar e qualquer outra coisa para fugir").lower()
                        if res == 's':
                            valor += 2
                            print(f"Truco aceito! Jogador {vez} deve terminar sua jogada")
                        else:
                            ganho = vez % 2
                            break   
                    elif int(x) > 0 and int(x) < len(jogador[vez - 1].show()) + 1:
                        if vez == 1 or vez == 3:
                            cartasD1.append(jogador[vez - 1].show()[int(x) - 1])  
                        else:
                            cartasD2.append(jogador[vez - 1].show()[int(x) - 1])
                        jogada[vez - 1] = Carta(jogador[vez - 1].show()[int(x) - 1].num, jogador[vez - 1].show()[int(x) - 1].naipe)    
                        mesa.append(jogador[vez - 1].show()[int(x) - 1])
                        jogador[vez - 1].show().pop(int(x) - 1)
                        vez = prox
                        prox = next(ciclo)
                        break
                    else:
                        print("Digite um valor válido! (A ordem das cartas é contada da esquerda pra direita começando em 1)")
                if ganho != -1:
                    break
            # Definição do resultado parcial da rodada
            """
            if cartasD1[0] > cartasD1[1]:
                maior1 = cartasD1[0]
            else:
                maior1 = cartasD1[1]
            if cartasD2[0] > cartasD2[1]:
                maior2 = cartasD2[0]
            else:
                maior2 = cartasD2[1]
            """
            if ganho == - 1:
                maior1 = max(jogada[0], jogada[2])
                maior2 = max(jogada[1], jogada[3])
                if maior1 > maior2:
                    parcial1 += 1
                    if maior1 == jogada[0]:
                        while True:
                            vez = next(ciclo)
                            if vez == 1:
                                break
                    else:
                        while True:
                            vez = next(ciclo)
                            if vez == 3:
                                break
                elif maior1 == maior2: #Caso de empate
                    if parcial1 == 1 and parcial2 == 1:
                        print(f"Não houve vitoriosos. Placar: Dupla 1: {dupla1P} x Dupla 2: {dupla2P}")
                    elif parcial1 == 1:
                        ganho = 1
                    elif parcial2 == 1:
                        ganho = 0
                    else:
                        print("Empate. A dupla que vencer a próxima mão é vencedora")
                        parcial1 += 0.5
                        parcial2 += 0.5
                        continue
                else:
                    parcial2 += 1
                    if maior1 == jogada[1]:
                        while True:
                            vez = next(ciclo)
                            if vez == 2:
                                break
                    else:
                        while True:
                            vez = next(ciclo)
                            if vez == 4:
                                break
                if parcial1 > 1: ganho = 1
                elif parcial2 > 1: ganho = 0
            if ganho == 0:
                print(f"Vitória da Dupla 2! +{valor} pontos")
                dupla2P += valor
            else:
                print(f"Vitória da Dupla 1! +{valor} pontos")
                dupla1P += valor
            print(f"Placar: Dupla 1: {dupla1P} x Dupla 2: {dupla2P}")
            break
    
    if dupla1P > dupla2P:
        print(f"DUPLA 1 MANDOU VER! PARABÉNS! Placar final: {dupla1P} x {dupla2P}")
    else:
        print(f"DUPLA 2 DETONOU! PARABÉNS! Placar final: {dupla2P} x {dupla1P}")
            

            
                
            


            



                

                


        


