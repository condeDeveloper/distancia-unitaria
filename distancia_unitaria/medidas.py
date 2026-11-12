"""As tabelas do README.

Duas perguntas, nessa ordem, porque a primeira e que justifica a segunda:

1. Com UMA distancia, de quantas cores a grade precisa? (Resposta medida:
   sempre duas. E por isso que o projeto nao para aqui.)
2. Com CONJUNTOS de distancias, quanto sobe?
"""

from functools import lru_cache

from .busca import cromatico
from .juiz import intervalo
from .nucleo import (
    arestas,
    coloracao_valida,
    deslocamentos,
    normaliza,
    vizinhanca,
)

GRADE_PARES = 7
GRADE_SOLO = 8
TETO_D = 100


@lru_cache(maxsize=None)
def distancias_validas(teto=TETO_D):
    """Os d que tem pelo menos um par de inteiros a essa distancia.

    Nem todo inteiro serve: 3, 6, 7, 11... nao sao soma de dois quadrados, e o
    grafo deles nao tem aresta nenhuma.
    """
    return tuple(d for d in range(1, teto + 1) if deslocamentos(d))


def preve_bipartido(ds):
    """A regra fechada: divide por 2 enquanto todos forem pares, e olha.

    Se o que sobra e todo impar, a paridade de x+y colore o grafo, porque todo
    deslocamento de distancia impar tem dx+dy impar. Se sobra algum par
    misturado com impar, a paridade ja nao separa.

    Isto e uma PREVISAO, e vale zero ate a varredura conferir. O
    `test_medidas.py` confere nos 71 conjuntos.
    """
    ds = list(normaliza(ds))
    while ds and all(d % 2 == 0 for d in ds):
        ds = [d // 2 for d in ds]
    return all(d % 2 == 1 for d in ds)


@lru_cache(maxsize=None)
def tabela_uma_distancia(grade=GRADE_SOLO, teto=TETO_D):
    """(d, arestas, cromatico) para cada distancia valida sozinha."""
    linhas = []
    for d in distancias_validas(teto):
        if arestas(grade, grade, d) == 0:
            continue
        adj = vizinhanca(grade, grade, d)
        k, cores, _ = cromatico(adj)
        if not coloracao_valida(adj, cores):
            raise AssertionError('coloracao invalida em d=%d' % d)
        linhas.append((d, arestas(grade, grade, d), k))
    return tuple(linhas)


@lru_cache(maxsize=None)
def tabela_pares(quantas=9, grade=GRADE_PARES):
    """Todos os pares das primeiras `quantas` distancias validas.

    Devolve (par, arestas, piso, teto, cromatico, nos).
    """
    from itertools import combinations
    base = distancias_validas()[:quantas]
    linhas = []
    for par in combinations(base, 2):
        if arestas(grade, grade, par) == 0:
            continue
        adj = vizinhanca(grade, grade, par)
        piso, teto = intervalo(adj)
        k, cores, nos = cromatico(adj)
        if not coloracao_valida(adj, cores):
            raise AssertionError('coloracao invalida em %s' % (par,))
        if not piso <= k <= teto:
            raise AssertionError('exato fora do intervalo em %s' % (par,))
        linhas.append((par, arestas(grade, grade, par), piso, teto, k, nos))
    return tuple(linhas)


def distribuicao_dos_pares(quantas=9, grade=GRADE_PARES):
    """Quantos pares dao cada numero de cores."""
    d = {}
    for _, _, _, _, k, _ in tabela_pares(quantas, grade):
        d[k] = d.get(k, 0) + 1
    return d


def custo_extremo(quantas=9, grade=GRADE_PARES):
    """O par mais barato e o mais caro de resolver, em nos."""
    linhas = tabela_pares(quantas, grade)
    barato = min(linhas, key=lambda l: l[5])
    caro = max(linhas, key=lambda l: l[5])
    return (barato[0], barato[5]), (caro[0], caro[5])
