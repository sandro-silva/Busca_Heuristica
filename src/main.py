import heapq


# Distâncias fornecidas na tabela da atividade
distancias = {
    "E1":  {"E2": 11, "E3": 20, "E4": 27, "E8": 28,
            "E12": 30},
    "E2":  {"E1": 11, "E3": 9, "E4": 16, "E8": 19,
            "E12": 23},
    "E3":  {"E1": 20, "E2": 9, "E4": 7, "E8": 15,
            "E9": 10, "E12": 21, "E13": 13},
    "E4":  {"E1": 27, "E2": 16, "E3": 7, "E5": 13,
            "E8": 13, "E12": 21, "E13": 11},
    "E5":  {"E4": 13, "E6": 3, "E7": 2},
    "E6":  {"E5": 3, "E7": 4},
    "E7":  {"E5": 2, "E6": 4, "E8": 22},
    "E8":  {"E4": 13, "E7": 22, "E12": 7},
    "E9":  {"E3": 10, "E11": 12},
    "E11": {"E9": 12, "E12": 15},
    "E12": {"E8": 7, "E4": 21, "E3": 21},
    "E13": {"E3": 13, "E4": 11, "E14": 5},
    "E14": {"E13": 5}
}


# Linhas do metrô
linhas = {
    "azul": ["E1", "E2", "E3", "E4", "E5"],
    "amarela": ["E5", "E6", "E7", "E8"],
    "verde": ["E12", "E8", "E4", "E13", "E14"],
    "vermelha": ["E11", "E9", "E3", "E13"]
}


VELOCIDADE = 30          # km/h
BALDEACAO = 4            # minutos


# Converte distância em km para tempo em minutos
def tempo_viagem(distancia):
    return distancia / (VELOCIDADE / 60)


# Heurística
def heuristica(estacao, objetivo):
    distancia = distancias_completas[estacao][objetivo]
    return tempo_viagem(distancia)


# Matriz completa de distâncias
distancias_completas = {
    "E1":  [0,11,20,27,40,43,39,28,18,10,18,30,30,32],
    "E2":  [11,0,9,16,29,32,28,19,11,4,17,23,21,24],
    "E3":  [20,9,0,7,20,22,19,15,10,11,21,21,13,18],
    "E4":  [27,16,7,0,13,16,12,13,13,18,26,21,11,17],
    "E5":  [40,29,20,13,0,3,2,21,25,31,38,27,16,20],
    "E6":  [43,32,22,16,3,0,4,23,28,33,41,30,17,20],
    "E7":  [39,28,19,12,2,4,0,22,25,29,38,28,13,17],
    "E8":  [28,19,15,13,21,23,22,0,9,22,18,7,25,30],
    "E9":  [18,11,10,13,25,28,25,9,0,13,12,12,23,28],
    "E10": [10,4,11,18,31,33,29,22,13,0,20,27,20,23],
    "E11": [18,17,21,26,38,41,38,18,12,20,0,15,35,39],
    "E12": [30,23,21,21,27,30,28,7,12,27,15,0,31,37],
    "E13": [30,21,13,11,16,17,13,25,23,20,35,31,0,5],
    "E14": [32,24,18,17,20,20,17,30,39,23,39,37,5,0]
}

estacoes = list(distancias_completas.keys())

distancias_completas = {
    estacao: {
        estacoes[j]: valores[j]
        for j in range(len(valores))
    }
    for estacao, valores in distancias_completas.items()
}


# Construção do grafo
grafo = {}

for linha, estacoes_linha in linhas.items():

    for i in range(len(estacoes_linha) - 1):

        origem = estacoes_linha[i]
        destino = estacoes_linha[i + 1]

        distancia = distancias_completas[origem][destino]
        custo = tempo_viagem(distancia)

        grafo.setdefault((origem, linha), [])
        grafo.setdefault((destino, linha), [])

        grafo[(origem, linha)].append(
            ((destino, linha), custo)
        )

        grafo[(destino, linha)].append(
            ((origem, linha), custo)
        )


# Adiciona baldeações
for estacao in estacoes:

    linhas_estacao = [
        linha for linha, lista in linhas.items()
        if estacao in lista
    ]

    for linha1 in linhas_estacao:
        for linha2 in linhas_estacao:

            if linha1 != linha2:

                grafo.setdefault((estacao, linha1), [])

                grafo[(estacao, linha1)].append(
                    ((estacao, linha2), BALDEACAO)
                )


# A*
def busca_a_estrela(inicio, objetivo):

    linha_inicial = next(
        linha for linha, lista in linhas.items()
        if inicio in lista
    )

    estado_inicial = (inicio, linha_inicial)

    fila = []

    h = heuristica(inicio, objetivo)

    heapq.heappush(
        fila,
        (h, 0, estado_inicial)
    )

    custos = {
        estado_inicial: 0
    }

    pais = {}

    while fila:

        f, g, atual = heapq.heappop(fila)

        estacao, linha = atual

        if estacao == objetivo:

            caminho = []

            while atual in pais:
                caminho.append(atual)
                atual = pais[atual]

            caminho.append(estado_inicial)

            caminho.reverse()

            return caminho, g

        for vizinho, custo in grafo.get(atual, []):

            novo_g = g + custo

            if novo_g < custos.get(vizinho, float("inf")):

                custos[vizinho] = novo_g

                h = heuristica(vizinho[0], objetivo)

                f = novo_g + h

                pais[vizinho] = atual

                heapq.heappush(
                    fila,
                    (f, novo_g, vizinho)
                )

    return None, float("inf")


caminho, custo = busca_a_estrela("E1", "E12")


print("Caminho encontrado:")

for estacao, linha in caminho:
    print(estacao, "-", linha)

print(f"\nCusto total: {custo:.2f} minutos")