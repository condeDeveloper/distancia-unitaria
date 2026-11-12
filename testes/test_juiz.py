"""Os juizes que cercam: clique por baixo, guloso por cima.

O ponto do arquivo e que eles sao INDEPENDENTES da busca exata. Se a busca
devolvesse um valor fora do intervalo que eles prendem, um dos tres estaria
errado.
"""

from distancia_unitaria.busca import cromatico
from distancia_unitaria.juiz import (
    coloracao_gulosa,
    guloso_por_grau,
    intervalo,
    maior_clique,
)
from distancia_unitaria.nucleo import coloracao_valida, vizinhanca


def test_clique_num_grafo_conhecido():
    """Grade 2x2 com d=1 e um quadrado: clique maxima 2, nao 4."""
    adj = vizinhanca(2, 2, 1)
    tamanho, _, estourou = maior_clique(adj)
    assert tamanho == 2
    assert not estourou


def test_clique_do_rei_e_quatro():
    """Com d em {1,2} quatro casas num quadrado 2x2 sao todas vizinhas."""
    adj = vizinhanca(3, 3, (1, 2))
    tamanho, _, _ = maior_clique(adj)
    assert tamanho == 4


def test_guloso_sempre_produz_coloracao_valida():
    for ds in (1, 2, 5, (1, 2), (2, 5), (1, 4, 9)):
        adj = vizinhanca(5, 5, ds)
        for funcao in (coloracao_gulosa, guloso_por_grau):
            k, cores = funcao(adj)
            assert coloracao_valida(adj, cores), ds
            assert max(cores) + 1 == k


def test_nenhuma_ordem_gulosa_domina_a_outra():
    """Medido, nao suposto: as duas ordens perdem uma para a outra.

    Eu tinha escrito que a ordem por grau nunca seria pior -- e a heuristica
    de sempre. Nos 36 pares da grade 6x6 ela perde 5 vezes, ganha 5 e empata
    26. Em (1, 10) ela gasta SEIS cores onde a ordem natural gasta quatro.
    """
    from itertools import combinations
    from distancia_unitaria.medidas import distancias_validas
    from distancia_unitaria.nucleo import arestas

    grau_pior = natural_pior = empate = 0
    for ds in combinations(distancias_validas()[:9], 2):
        if arestas(6, 6, ds) == 0:
            continue
        adj = vizinhanca(6, 6, ds)
        natural, _ = coloracao_gulosa(adj)
        por_grau, _ = guloso_por_grau(adj)
        if por_grau > natural:
            grau_pior += 1
        elif natural > por_grau:
            natural_pior += 1
        else:
            empate += 1
    assert (grau_pior, natural_pior, empate) == (5, 5, 26)


def test_o_caso_em_que_a_heuristica_de_grau_se_da_mal():
    adj = vizinhanca(6, 6, (1, 10))
    natural, _ = coloracao_gulosa(adj)
    por_grau, _ = guloso_por_grau(adj)
    assert (natural, por_grau) == (4, 6)


def test_o_exato_cai_dentro_do_intervalo():
    for ds in (1, 2, 5, (1, 2), (2, 5), (4, 8), (1, 4, 9)):
        adj = vizinhanca(6, 6, ds)
        piso, teto = intervalo(adj)
        k, cores, _ = cromatico(adj)
        assert coloracao_valida(adj, cores), ds
        assert piso <= k <= teto, (ds, piso, k, teto)


def test_grafo_sem_aresta_precisa_de_uma_cor():
    adj = vizinhanca(4, 4, 3)   # d=3 nao tem deslocamento nenhum
    assert all(v == [] for v in adj)
    k, cores, _ = cromatico(adj)
    assert k == 1


def test_clique_avisa_quando_estoura():
    """O limite de nos faz o piso continuar valido, mas talvez nao o melhor."""
    adj = vizinhanca(8, 8, (1, 2))
    tamanho, nos, estourou = maior_clique(adj, limite_de_nos=50)
    assert estourou
    assert nos > 50
    assert tamanho >= 1
