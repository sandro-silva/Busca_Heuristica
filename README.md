# Busca Heurística

## Problema do Metrô de Paris

Implementação do algoritmo **A\*** para encontrar um caminho entre as estações **E1** e **E12**, considerando o tempo de viagem e o custo de baldeação.

### Configuração

- Algoritmo: **A\***
- Estado inicial: **E1**
- Estado objetivo: **E12**
- Velocidade média: **30 km/h**
- Baldeação: **4 minutos**
- Heurística: distância em linha reta até E12 convertida em tempo.

### Resultado

Caminho encontrado:

```text
E1 → E2 → E3 → E4 → E8 → E12
```

- Distância total: **47 km**
- Tempo de viagem: **94 minutos**
- Baldeação: **4 minutos**
- **Custo total: 98 minutos (1h38min)**

### Estrutura

```text
Busca_Heuristica/
├── README.md
├── main.py
```