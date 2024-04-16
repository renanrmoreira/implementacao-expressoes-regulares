# Algoritmo que implementa um (AFNε) em Python e como ele pode ser usado para reconhecer expressões regulares.
# Código realizado com auxilio do CHATGPT - 4 para algumas funções

class AFNE:
    transicao_vazia = None

    def __init__(self, estado_inicial):
        # Dicionário para as transições: chave é uma tupla (estado, símbolo), valor é um conjunto de estados
        self.transicoes = {}
        # Conjunto para manter os estados finais
        self.estados_finais = set()
        self.estado_inicial = estado_inicial

    # Método para adicionar transições ao autômato. Se não houver transição para o par cria um novo conjunto.
    def adicionando_transicao(self, org, symbol, dest):
        if (org, symbol) not in self.transicoes:
            self.transicoes[(org, symbol)] = set()
        self.transicoes[(org, symbol)].add(dest)

    def adicionando_estado_final(self, estado):
        self.estados_finais.add(estado)

    def fechamento_transicao_vazia(self, estados):
        # Calcula o fechamento transicao_vazia de um conjunto de estados
        lista_estados = list(estados)
        fechamento = set(estados)
        while lista_estados:
            estado = lista_estados.pop()
            # Para cada estado verifica as transições vazias e adiciona estados alcançáveis ao fechamento
            for next_estado in self.transicoes.get((estado, self.transicao_vazia), set()):
                if next_estado not in fechamento:
                    fechamento.add(next_estado)
                    lista_estados.append(next_estado)
        return fechamento

    def move(self, estados, symbol):
        # Se move para um conjunto de estados de acordo com o símbolo
        novos_estados = set()
        for estado in estados:
            novos_estados.update(self.transicoes.get((estado, symbol), set()))
        return novos_estados

    def estado_aceitacao(self, estados):
        # Checando se é um estado final
        return not self.estados_finais.isdisjoint(estados)

    def match(self, string):
        # Checando se o AFNe bate com a string
        estados_atuais = self.fechamento_transicao_vazia({self.estado_inicial})
        for symbol in string:
            estados_atuais = self.fechamento_transicao_vazia(self.move(estados_atuais, symbol))
        return self.estado_aceitacao(estados_atuais)

def main():
    # Este autômato é projetado para reconhecer a expressão regular 'aa*b?a*'

    afne = AFNE(estado_inicial=0)
    # transição representa o primeiro 'a' da expressão regular 'aa*'
    afne.adicionando_transicao(0, 'a', 1)
    # transição permite repetição do 'a' conforme a parte 'a*' da expressão
    afne.adicionando_transicao(1, 'a', 1)
    afne.adicionando_transicao(1, 'b', 2)
    # Caso não haja b´s após os a´s
    afne.adicionando_transicao(1, AFNE.transicao_vazia, 3)
    # transição permite a ocorrência de 'a' após 'b', como em 'aab' ou 'aaab'
    afne.adicionando_transicao(2, 'a', 3)
    afne.adicionando_transicao(3, 'a', 3),
    afne.adicionando_estado_final(3)

    """
    # Este autômato é projetado para reconhecer a expressão regular 'a+ba*'

    afne = AFNE(estado_inicial=0)
    # transição para o primeiro 'a', que deve ocorrer pelo menos uma vez
    afne.adicionando_transicao(0, 'a', 1)
    # loop no estado 1 para ler 'a' múltiplas vezes devido ao '+'
    afne.adicionando_transicao(1, 'a', 1)
    afne.adicionando_transicao(1, 'b', 2)
    # loop no estado 2 para ler 'a' zero ou mais vezes
    afne.adicionando_transicao(2, 'a', 2)
    afne.adicionando_estado_final(2)
    """
    strings_teste = ['aa', 'aaa', 'aab', 'aaab', 'ab', 'ba', 'b', 'aaba']
    for string in strings_teste:
        if afne.match(string):
            print(f'A string "{string}" é uma expressão regular reconhecida pelo AFNe.')
        else:
            print(f'A string "{string}" NÃO é uma expressão regular reconhecida pelo AFNe.')

if __name__ == '__main__':
    main()
