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


if __name__ == "__main__":
    unittest.main()
