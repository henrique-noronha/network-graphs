# Atividade do Capítulo 3: Medir o Efeito da Representação Computacional

**Disciplina:** Teoria dos Grafos / Redes Complexas  
**Instituição:** Universidade Federal do Tocantins (UFT)  
**Professor:** Jackson Gomes  
**Repositório:** [https://github.com/henrique-noronha/network-graphs](https://github.com/henrique-noronha/network-graphs)  
**Integrantes do Grupo (até 3 participantes):**
1. Henrique Noronha
2. Laurinda Nhaga Mona
3. *(Nome do 3º integrante / ou individual/dupla)*

---

## 1. Decisões de Projeto (Item 1)

As classes `GrafoMatriz` e `GrafoLista` foram implementadas em [`src/grafo.py`](src/grafo.py) herdando da classe abstrata `Grafo`. As decisões formais de projeto são:

1. **Coleção de cada posição na lista:** Foi utilizado `List[Set[int]]` (conjuntos/tabelas de dispersão). Essa escolha garante que a operação `tem_aresta(u, v)` (teste de pertinência) seja executada em tempo esperado $O(1)$, além de permitir que `vizinhos(u)` itere estritamente sobre os vizinhos reais sem duplicações.
2. **Tratamento de arestas repetidas:** Ao tentar reinserir uma aresta $(u, v)$ já existente, a operação não altera o estado da estrutura e mantém o contador de arestas $m$ inalterado tanto na matriz quanto na lista, evitando qualquer divergência de contagem entre as duas representações.
3. **Tratamento de laços:** Em conformidade com a definição de grafo simples, laços do tipo $(u, u)$ são estritamente rejeitados em ambas as estruturas (`if u == v: return`), não incrementando $m$ nem afetando os graus dos vértices.

---

## 2. Validação do Grafo de Exemplo da Figura 3.1 (Item 2)

O grafo da Figura 3.1 do livro texto possui:
* **Ordem ($n$):** 6 vértices ($a, b, c, d, e, f \implies 0, 1, 2, 3, 4, 5$).
* **Tamanho ($m$):** 8 arestas ($ab, ac, bc, bd, cd, ce, de, ef$).
* **Sequência de Graus:** Ordenada de forma não crescente, resulta em $(4, 3, 3, 3, 2, 1)$, com $d(c)=4$, $d(b)=d(d)=d(e)=3$, $d(a)=2$ e $d(f)=1$.
* **Lema do Aperto de Mão:** $\sum_{v \in V} d(v) = 4 + 3 + 3 + 3 + 2 + 1 = 16 = 2 \times 8 = 2m$.
* **Contagem de Triângulos:** 3 triângulos ($abc$, $bcd$, $cde$).

Essa verificação foi formalizada como teste unitário automatizado em [`tests/test_exemplo.py`](tests/test_exemplo.py), sendo validada identicamente para `GrafoMatriz` e `GrafoLista`:

```bash
python -m unittest tests/test_exemplo.py
```

---

## 3. Matriz de Incidência à Mão para $G - ce$ (Item 3)

O grafo $G - ce$ (remoção da aresta entre os vértices $c$ e $e$) preserva os 6 vértices e possui as 7 arestas restantes em ordem: $ab, ac, bc, bd, cd, de, ef$.

A matriz de incidência $B(G - ce)$ ($6 \times 7$), com linhas indexadas pelos vértices $a, b, c, d, e, f$ e colunas pelas arestas, é dada por:

$$
B(G - ce) =
\begin{pmatrix}
1 & 1 & 0 & 0 & 0 & 0 & 0 \\
1 & 0 & 1 & 1 & 0 & 0 & 0 \\
0 & 1 & 1 & 0 & 1 & 0 & 0 \\
0 & 0 & 0 & 1 & 1 & 1 & 0 \\
0 & 0 & 0 & 0 & 0 & 1 & 1 \\
0 & 0 & 0 & 0 & 0 & 0 & 1
\end{pmatrix}
$$

### Conferência das Propriedades:
* **Soma de cada coluna:** Exatamente 2 (cada coluna registra as duas extremidades da respectiva aresta).
* **Soma das linhas (graus):**
  * Linha $a$: $1 + 1 = 2$
  * Linha $b$: $1 + 1 + 1 = 3$
  * Linha $c$: $1 + 1 + 1 = 3$ (reduzido de 4 para 3)
  * Linha $d$: $1 + 1 + 1 = 3$
  * Linha $e$: $1 + 1 = 2$ (reduzido de 3 para 2)
  * Linha $f$: $1$
  * **Soma total:** $2 + 3 + 3 + 3 + 2 + 1 = 14 = 2 \times 7 = 2m$.
* **Linhas que mudaram em relação a $G$:** Apenas as linhas dos vértices **$c$** e **$e$**, que perderam o valor $1$ da coluna da aresta $ce$, refletindo diretamente a diminuição de seus graus. As demais linhas permaneceram inalteradas.

---

## 4. Geração dos Grafos Aleatórios (Item 4)

Os grafos aleatórios $G(n, p)$ foram gerados percorrendo todos os pares $u < v$ e inserindo cada aresta com probabilidade $\rho$:
* **Número de vértices ($n$):** 2.000.
* **Semente do gerador pseudoaleatório:** `SEMENTE = 42` (registrada para assegurar estrita reprodutibilidade).
* **Controle experimental:** A lista de arestas gerada para cada probabilidade foi repassada de forma idêntica para instanciar tanto a `GrafoMatriz` quanto a `GrafoLista`.
* **Arestas obtidas ($m$):**
  * Para $p = 0{,}001 \implies m = 1.910$ arestas.
  * Para $p = 0{,}05 \implies m = 99.819$ arestas.
  * Para $p = 0{,}5 \implies m = 999.109$ arestas.

---

## 5. Medição de Desempenho: Tempo e Espaço (Item 5)

A medição de tempo considerou a **mediana de 3 execuções independentes** da função `contar_triangulos` (medida com `time.perf_counter`).  
O espaço foi contabilizado conforme a especificação do capítulo: **$n^2$** posições para matriz de adjacência e **$n + 2m$** posições para lista de adjacência.

### Tabela de Desempenho ($n = 2.000$, Semente = 42, Mediana de 3 repetições)

| Densidade ($p$) | $m$ obtido | Implementação | Tempo mediano (s) | Espaço (posições) | Triângulos |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **0.001** | 1.910 | GrafoMatriz | 0.1784 s | 4.000.000 | 2 |
| **0.001** | 1.910 | GrafoLista | 0.0006 s | 5.820 | 2 |
| **0.05** | 99.819 | GrafoMatriz | 5.2304 s | 4.000.000 | 165.360 |
| **0.05** | 99.819 | GrafoLista | 0.4504 s | 201.638 | 165.360 |
| **0.50** | 999.109 | GrafoMatriz | 98.5428 s | 4.000.000 | 166.216.758 |
| **0.50** | 999.109 | GrafoLista | 39.9542 s | 2.000.218 | 166.216.758 |

> **Nota metodológica:** A quantidade de triângulos contados é rigorosamente idêntica entre as duas implementações em todas as densidades, comprovando a correção algorítmica e a equivalência das estruturas.

---

## 6. Análise e Discussão dos Resultados (Item 6)

### 6.1. Composição de Custo Teórico
Conforme deduzido na Seção 3.12.1 do livro texto, o custo de `contar_triangulos` é governado por:
* **Lista de Adjacência:** $O\left(n + \sum_{v \in V} d(v)^2\right)$
* **Matriz de Adjacência:** $\Theta\left(n(n + m)\right)$

A diferença fulcral reside no comportamento do método `vizinhos(u)`:
* Na **Lista de Adjacência**, `vizinhos(u)` itera unicamente sobre os $d(u)$ vértices adjacentes.
* Na **Matriz de Adjacência**, `vizinhos(u)` é obrigado a inspecionar todas as $n$ entradas da linha $u$, independentemente de quantas arestas incidentes realmente existem.

### 6.2. Comparação por Densidade
1. **Regime Esparso ($p = 0{,}001$, $m \approx 2.000$):**
   * O grau médio é $\approx 1{,}91$. Na lista, cada iteração examina pouquíssimos nós vizinhos. O tempo foi de apenas **0,0006 s** contra **0,1784 s** da matriz (**a lista foi ~300 vezes mais rápida**).
   * Em termos de memória, a lista consumiu apenas 5.820 posições contra as 4.000.000 posições alocadas pela matriz (economia de **99,85%** de espaço).

2. **Regime Intermediário ($p = 0{,}05$, $m \approx 100.000$):**
   * O grau médio sobe para $\approx 100$. A lista completou em **0,4504 s**, enquanto a matriz necessitou de **5,2304 s** (**a lista permaneceu ~11,6 vezes mais rápida**).
   * No espaço, a lista ocupou 201.638 posições contra 4.000.000 da matriz (economia de **94,96%**).

3. **Regime Denso ($p = 0{,}5$, $m \approx 1.000.000$):**
   * O grafo atinge 1 milhão de arestas e 166 milhões de triângulos. O tempo de execução da matriz saltou para **98,54 s**, enquanto a lista realizou a contagem em **39,95 s** (**a lista continuou ~2,5 vezes mais rápida**).
   * No espaço, mesmo em densidade 50%, a lista requereu 2.000.218 posições, o que equivale a metade das 4.000.000 posições ocupadas pela matriz.

### 6.3. Conclusão
Em todas as faixas avaliadas, a **Lista de Adjacência** superou a Matriz de Adjacência tanto em tempo quanto em consumo de memória. Conforme a densidade se aproxima de 1 (grafo quase completo), a vantagem temporal da lista reduz progressivamente devido ao custo de dispersão das tabelas `set`, enquanto a matriz amortiza o custo de varredura fixa de suas linhas. No entanto, para redes reais — que são eminentemente esparsas ($p \ll 0{,}01$) —, a Lista de Adjacência com conjuntos é amplamente superior.

---

## 7. Instruções para Reprodução

Para reproduzir os testes e experimentos localmente:

```bash
# 1. Ativar o ambiente virtual
source venv/bin/activate

# 2. Executar os testes unitários (inclui o grafo da Figura 3.1)
python -m unittest tests/test_exemplo.py

# 3. Executar o experimento completo de medição (3 repetições com semente 42)
python -m src.experimento
```
