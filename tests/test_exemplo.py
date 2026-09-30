import unittest
from src.grafo import GrafoMatriz, GrafoLista
from src.algoritmos import contar_triangulos


class TestGrafosETriangulos(unittest.TestCase):
    def test_grafo_sem_arestas(self):
        for cls in [GrafoMatriz, GrafoLista]:
            with self.subTest(cls=cls.__name__):
                g = cls(5)
                self.assertEqual(g.m, 0)
                self.assertEqual(contar_triangulos(g), 0)

    def test_um_triangulo(self):
        # Triângulo formado por 0, 1, 2
        for cls in [GrafoMatriz, GrafoLista]:
            with self.subTest(cls=cls.__name__):
                g = cls(4)
                g.adicionar_aresta(0, 1)
                g.adicionar_aresta(1, 2)
                g.adicionar_aresta(0, 2)
                self.assertEqual(g.m, 3)
                self.assertEqual(contar_triangulos(g), 1)

    def test_grafo_completo_k4(self):
        # K4 tem C(4, 3) = 4 triângulos
        for cls in [GrafoMatriz, GrafoLista]:
            with self.subTest(cls=cls.__name__):
                g = cls(4)
                for u in range(4):
                    for v in range(u + 1, 4):
                        g.adicionar_aresta(u, v)
                self.assertEqual(g.m, 6)
                self.assertEqual(contar_triangulos(g), 4)

    def test_ciclo_c4_sem_triangulo(self):
        # C4: 0-1-2-3-0 não possui triângulos
        for cls in [GrafoMatriz, GrafoLista]:
            with self.subTest(cls=cls.__name__):
                g = cls(4)
                g.adicionar_aresta(0, 1)
                g.adicionar_aresta(1, 2)
                g.adicionar_aresta(2, 3)
                g.adicionar_aresta(3, 0)
                self.assertEqual(contar_triangulos(g), 0)


    def test_figura_3_1(self):
        """
        Teste exigido no Item 2:
        Grafo da Figura 3.1: n = 6, m = 8.
        Vértices: a=0, b=1, c=2, d=3, e=4, f=5
        Arestas: ab, ac, bc, bd, cd, ce, de, ef
        Sequência de graus em ordem decrescente: (4, 3, 3, 3, 2, 1)
        Soma dos graus: 16 = 2 * m
        """
        arestas = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (4, 5)]
        for cls in [GrafoMatriz, GrafoLista]:
            with self.subTest(cls=cls.__name__):
                g = cls(6)
                for u, v in arestas:
                    g.adicionar_aresta(u, v)

                # Verifica n e m
                self.assertEqual(g.n, 6)
                self.assertEqual(g.m, 8)

                # Verifica sequência de graus em ordem decrescente
                graus = sorted([g.grau(v) for v in range(g.n)], reverse=True)
                self.assertEqual(graus, [4, 3, 3, 3, 2, 1])

                # Verifica o Lema do Aperto de Mão (soma dos graus = 2m)
                self.assertEqual(sum(graus), 2 * g.m)

                # Verifica triângulos (abc, bcd e cde formam 3 triângulos)
                self.assertEqual(contar_triangulos(g), 3)


if __name__ == "__main__":
    unittest.main()

