# Algoritmo A* para Navegação em Mapa
Grupo: Chrystopher Santos, Rafael Danoski e Thaynara Fumegali

Implementação de um algoritmo A* em Python para encontrar a melhor rota em um mapa.

## Requisitos

- Python 3.x

## Como Executar

1. **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/seu-projeto.git](https://github.com/chrystopher-santos/complexidade-algoritmo.git)
    ```

2. **Navegue até o diretório do projeto:**
    ```bash
    cd complexidade.algoritmo
    ```

3. **Execute o programa:**
    ```bash
    python main.py
    ```

4. **Forneça as coordenadas de destino:**
    - O programa irá solicitar que você insira as coordenadas de destino no formato `x y`.

5. **Observe a saída:**
    - O programa imprimirá o mapa com o caminho encontrado e o custo total, seguindo o formato:
        ```plaintext
        123 1,1 2,1 2,2 2,3 2,4 3,4 4,4 5,4 6,4
        ```
        - O número inicial é o custo total do trajeto.
        - As coordenadas seguintes são os pontos no mapa que formam o caminho.

## Formato do Mapa

O arquivo de mapa deve ter o seguinte formato:

10 8
0 7
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 -1 -1 -1 -1 -1 0 0
0 0 0 0 0 0 0 -1 0 0
0 0 0 0 0 0 0 -1 0 0
0 0 0 0 0 0 0 -1 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0

