"""A tabela de pares inteira, e a regra conferida contra ela.

Custa alguns minutos: o par (13, 16) sozinho leva 540.248 nos. Esta separada
porque e o preco de PROVAR, nao de achar -- achar uma coloracao com k cores e
barato, mostrar que k-1 e impossivel exige esgotar.
"""

from itertools import combinations

from distancia_unitaria.medidas import (
    custo_extremo,
    distancias_validas,
    distribuicao_dos_pares,
    preve_bipartido,
    tabela_pares,
)
from distancia_unitaria.busca import cromatico
from distancia_unitaria.nucleo import arestas, coloracao_valida, vizinhanca

DISTRIBUICAO = {2: 7, 3: 20, 4: 9}


def test_todos_os_36_pares():
    linhas = tabela_pares()
    assert len(linhas) == 36


def test_distribuicao_dos_cromaticos():
    assert distribuicao_dos_pares() == DISTRIBUICAO
    assert sum(DISTRIBUICAO.values()) == 36


def test_nenhum_par_chega_a_cinco_cores():
    """Quatro e o teto medido na grade 7x7 com pares."""
    assert max(distribuicao_dos_pares()) == 4


def test_o_exato_fica_dentro_do_intervalo_em_todos():
    for par, _, piso, teto, k, _ in tabela_pares():
        assert piso <= k <= teto, par


def test_custo_varia_dez_mil_vezes():
    """O par mais caro custa 540.248 nos; o mais barato, 50."""
    barato, caro = custo_extremo()
    assert barato[1] == 50
    assert caro == ((13, 16), 540248)
    assert caro[1] // barato[1] > 10000


def test_a_regra_acerta_em_todos_os_pares():
    erros = [(par, k) for par, _, _, _, k, _ in tabela_pares()
             if (k == 2) != preve_bipartido(par)]
    assert erros == []


def test_a_regra_acerta_tambem_nos_trios():
    """Pares mais trios: 71 conjuntos, zero erros."""
    base = distancias_validas()[:7]
    conferidos = 0
    for trio in combinations(base, 3):
        if arestas(7, 7, trio) == 0:
            continue
        adj = vizinhanca(7, 7, trio)
        k, cores, _ = cromatico(adj)
        assert coloracao_valida(adj, cores), trio
        conferidos += 1
        assert (k == 2) == preve_bipartido(trio), (trio, k)
    assert conferidos == 35
    assert conferidos + len(tabela_pares()) == 71
