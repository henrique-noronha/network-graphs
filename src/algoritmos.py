"""Módulo contendo algoritmos para análise de grafos."""

from src.grafo import Grafo


def contar_triangulos(grafo: Grafo) -> int:
    """
    Conta o número total de triângulos em um grafo não direcionado.
    
    Um triângulo é formado por um conjunto de três vértices distintos {u, v, w}
    que são mutuamente conectados por arestas.
    
    Para evitar contagens duplicadas e garantir complexidade eficiente,
    iteramos com a ordem u < v < w.
    """
    total = 0
    n = grafo.n

    for u in range(n):
        vizinhos_u = [v for v in grafo.vizinhos(u) if v > u]
        tam = len(vizinhos_u)
        for i in range(tam):
            v = vizinhos_u[i]
            for j in range(i + 1, tam):
                w = vizinhos_u[j]
                if grafo.tem_aresta(v, w):
                    total += 1

    return total
