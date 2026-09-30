import random
import time
import tracemalloc
from src.grafo import GrafoMatriz, GrafoLista
from src.algoritmos import contar_triangulos


def gerar_grafo_aleatorio(cls_grafo, n: int, p: float):
    """Gera um grafo aleatório G(n, p) inserindo arestas com probabilidade p."""
    g = cls_grafo(n)
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < p:
                g.adicionar_aresta(u, v)
    return g


def medir_desempenho(cls_grafo, n: int, p: float):
    """Mede o tempo da contagem de triângulos e o pico de consumo de memória RAM."""
    # 1. Medição de Memória RAM na construção
    tracemalloc.start()
    g = gerar_grafo_aleatorio(cls_grafo, n, p)
    _, mem_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    mem_mb = mem_pico / (1024 * 1024)

    # 2. Medição do Tempo do Algoritmo
    inicio = time.perf_counter()
    qtd_triangulos = contar_triangulos(g)
    fim = time.perf_counter()
    tempo_execucao = fim - inicio

    return g.m, qtd_triangulos, tempo_execucao, mem_mb


def executar_experimento():
    n = 2000
    densidades = [0.001, 0.05, 0.5]

    print("=" * 90)
    print(f" EXPERIMENTO DE DESEMPENHO (n = {n})")
    print("=" * 90)
    header = f"{'Densidade (p)':<15} | {'Representação':<15} | {'Arestas (m)':<12} | {'Triângulos':<12} | {'Tempo (s)':<10} | {'Memória (MB)':<12}"
    print(header)
    print("-" * 90)

    for p in densidades:
        for nome, cls in [("Matriz", GrafoMatriz), ("Lista", GrafoLista)]:
            print(f"A processar p={p} ({nome})...", end="\r")
            m, tri, tempo, mem = medir_desempenho(cls, n, p)
            print(f"{p:<15} | {nome:<15} | {m:<12} | {tri:<12} | {tempo:<10.4f} | {mem:<12.2f}")

    print("=" * 90)


if __name__ == "__main__":
    executar_experimento()