"""Script de experimentação para medição do efeito da representação computacional."""

import random
import statistics
import time
from src.grafo import GrafoMatriz, GrafoLista
from src.algoritmos import contar_triangulos

SEMENTE = 42


def gerar_arestas_aleatorias(n: int, p: float, semente: int):
    """
    Gera a lista de arestas aleatórias para um grafo G(n, p) com probabilidade p.
    Percorre apenas os pares com u < v e usa uma semente fixa para garantir reprodutibilidade.
    """
    random.seed(semente)
    arestas = []
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < p:
                arestas.append((u, v))
    return arestas


def construir_grafo(cls_grafo, n: int, arestas):
    """Constrói uma instância de grafo populando com a mesma lista de arestas."""
    g = cls_grafo(n)
    for u, v in arestas:
        g.adicionar_aresta(u, v)
    return g


def medir_tempo_mediana(g, repeticoes: int = 3):
    """Executa contar_triangulos pelo menos 3 vezes e reporta a mediana dos tempos."""
    tempos = []
    qtd_triangulos = 0
    for _ in range(repeticoes):
        inicio = time.perf_counter()
        qtd_triangulos = contar_triangulos(g)
        fim = time.perf_counter()
        tempos.append(fim - inicio)
    return statistics.median(tempos), qtd_triangulos


def calcular_espaco(nome_impl: str, n: int, m: int) -> int:
    """
    Calcula a quantidade de posições ocupadas pela estrutura de dados:
    - n^2 na matriz de adjacência
    - n + 2m na lista de adjacência
    """
    if "Matriz" in nome_impl:
        return n * n
    return n + 2 * m


def executar_experimento(repeticoes: int = 3):
    n = 2000
    densidades = [0.001, 0.05, 0.5]

    print("=" * 96)
    print(f" EXPERIMENTO: MEDIR O EFEITO DA REPRESENTAÇÃO (n = {n}, Semente = {SEMENTE}, Repetições = {repeticoes})")
    print("=" * 96)
    header = f"{'Densidade (p)':<15} | {'m obtido':<10} | {'Implementação':<15} | {'Tempo mediano (s)':<18} | {'Espaço (posições)':<18} | {'Triângulos':<12}"
    print(header)
    print("-" * 96)

    resultados = []
    for p in densidades:
        arestas = gerar_arestas_aleatorias(n, p, SEMENTE)
        m_obtido = len(arestas)

        for nome, cls in [("GrafoMatriz", GrafoMatriz), ("GrafoLista", GrafoLista)]:
            print(f"Processando p={p} ({nome})...", end="\r", flush=True)
            g = construir_grafo(cls, n, arestas)
            tempo_med, tri = medir_tempo_mediana(g, repeticoes=repeticoes)
            espaco = calcular_espaco(nome, n, m_obtido)

            linha = f"{p:<15} | {m_obtido:<10} | {nome:<15} | {tempo_med:<18.4f} | {espaco:<18} | {tri:<12}"
            print(linha)
            resultados.append((p, m_obtido, nome, tempo_med, espaco, tri))

    print("=" * 96)
    return resultados


if __name__ == "__main__":
    executar_experimento(repeticoes=3)