# Relatório Acadêmico: Representações de Grafos e Algoritmos de Redes Complexas

**Disciplina:** Redes Complexas / Teoria dos Grafos  
**Repositório:** `network-graphs`  

---

## 1. Decisões de Projeto

Para a implementação da interface base `Grafo` e das classes concretas `GrafoMatriz` e `GrafoLista` em Python, adotamos as seguintes premissas:

* **Estrutura da Lista de Adjacência:** Utilização de `list` contendo `set` (`List[Set[int]]`). O uso de `set` garante checagem de existência de aresta `tem_aresta(u, v)` em tempo esperado $O(1)$.
* **Arestas Repetidas:** Se uma aresta $(u, v)$ for adicionada novamente, a operação é ignorada e o contador de arestas $m$ não é alterado.
* **Laços:** Não são permitidos (grafos simples). Convites para arestas do tipo $(u, u)$ são descartados sem incrementar $m$.

---

## 2. Validação do Grafo da Figura 3.1

O grafo de exemplo ($n=6, m=8$) foi implementado no módulo de testes `tests/test_exemplo.py`.

* **Vértices ($n$):** 6
* **Arestas ($m$):** 8
* **Sequência de Graus:** $(4, 3, 3, 3, 2, 1)$
* **Lema do Aperto de Mão:** $\sum_{v \in V} d(v) = 4 + 3 + 3 + 3 + 2 + 1 = 16 = 2 \times 8 = 2m$
* **Contagem de Triângulos:** 2 triângulos.

---

## 3. Resultados dos Experimentos de Desempenho ($n = 2000$)

Experimento realizado com grafos aleatórios $G(n, p)$ em três níveis de densidade:

| Densidade ($p$) | Representação | Arestas ($m$) | Triângulos | Tempo (s) | Memória (MB) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **0.001** | Matriz | ~2.000 | 1 | 0.0010 s | 30.64 MB |
| **0.001** | Lista | 1.989 | 1 | 0.0010 s | 0.57 MB |
| **0.05** | Matriz | 99.280 | 163.084 | 0.3687 s | 30.64 MB |
| **0.05** | Lista | 99.750 | 165.112 | 0.2519 s | 19.04 MB |
| **0.50** | Matriz | 999.362 | 166.362.488 | 26.6316 s | 30.64 MB |
| **0.50** | Lista | 1.000.134 | 166.740.817 | 29.2549 s | 93.00 MB |

---

## 4. Análise e Discussão dos Resultados

1. **Complexidade Teórica vs. Empírica:**
   * O algoritmo `contar_triangulos` utilizando **Matriz de Adjacência** possui complexidade $O(n(n+m))$, pois para cada par de vértices vizinhos é necessário percorrer uma linha inteira da matriz de tamanho $n$.
   * Utilizando **Lista de Adjacência**, a complexidade é $O(n + \sum_{v \in V} d(v)^2)$. Para grafos esparsos onde $d(v) \ll n$, esta abordagem reduz drasticamente as iterações desnecessárias.

2. **Trade-off Espaço-Tempo:**
   * A **Lista de Adjacência** é significativamente superior para a imensa maioria das redes do mundo real (que são tipicamente esparsas), economizando até 98% de memória.
   * A **Matriz de Adjacência** apresenta consumo de espaço pré-alocado constante $O(n^2)$, tornando-se competitiva em tempo apenas para grafos extremamente densos ($p \ge 0.5$).
