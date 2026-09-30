from abc import ABC, abstractmethod
from typing import List, Set

class Grafo(ABC):
    def __init__(self, n: int):
        self.n = n
        self.m = 0

    def ordem(self) -> int:
        return self.n

    def tamanho(self) -> int:
        return self.m

    def vertices(self):
        return range(self.n)

    def inserir_aresta(self, u: int, v: int) -> None:
        self.adicionar_aresta(u, v)

    @abstractmethod
    def adicionar_aresta(self, u: int, v: int) -> None:
        pass

    @abstractmethod
    def tem_aresta(self, u: int, v: int) -> bool:
        pass

    @abstractmethod
    def vizinhos(self, u: int):
        pass

    @abstractmethod
    def grau(self, u: int) -> int:
        pass


class GrafoMatriz(Grafo):
    def __init__(self, n: int):
        super().__init__(n)
        self.matriz = [[0] * n for _ in range(n)]

    def adicionar_aresta(self, u: int, v: int) -> None:
        if u == v:
            return  # Rejeita laços
        if not self.matriz[u][v]:
            self.matriz[u][v] = 1
            self.matriz[v][u] = 1
            self.m += 1

    def tem_aresta(self, u: int, v: int) -> bool:
        return self.matriz[u][v] == 1

    def vizinhos(self, u: int) -> List[int]:
        return [v for v in range(self.n) if self.matriz[u][v] == 1]

    def grau(self, u: int) -> int:
        return sum(self.matriz[u])


class GrafoLista(Grafo):
    def __init__(self, n: int):
        super().__init__(n)
        self.adj: List[Set[int]] = [set() for _ in range(n)]

    def adicionar_aresta(self, u: int, v: int) -> None:
        if u == v:
            return  # Rejeita laços
        if v not in self.adj[u]:
            self.adj[u].add(v)
            self.adj[v].add(u)
            self.m += 1

    def tem_aresta(self, u: int, v: int) -> bool:
        return v in self.adj[u]

    def vizinhos(self, u: int) -> Set[int]:
        return self.adj[u]

    def grau(self, u: int) -> int:
        return len(self.adj[u])