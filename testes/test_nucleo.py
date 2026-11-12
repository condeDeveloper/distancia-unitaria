"""Pontos, deslocamentos e o grafo."""

from distancia_unitaria.nucleo import (
    arestas,
    coloracao_valida,
    deslocamentos,
    deslocamentos_do_conjunto,
    distancia2,
    normaliza,
    paridade_forcada,
    pontos,
    tem_representacao,
    vizinhanca,
)


def test_distancia_e_inteira_e_exata():
    assert distancia2((0, 0), (3, 4)) == 25
    assert distancia2((0, 0), (0, 0)) == 0
    assert distancia2((-2, 1), (1, -3)) == 25


def test_pontos_em_ordem_de_leitura():
    assert pontos(2, 2) == [(0, 0), (1, 0), (0, 1), (1, 1)]
    assert len(pontos(5, 4)) == 20


def test_deslocamentos_de_d_conhecidos():
    assert sorted(deslocamentos(1)) == [(-1, 0), (0, -1), (0, 1), (1, 0)]
    assert len(deslocamentos(2)) == 4
    assert len(deslocamentos(5)) == 8
    assert len(deslocamentos(25)) == 12


def test_d_sem_representacao():
    """3 nao e soma de dois quadrados: o grafo fica sem aresta."""
    assert deslocamentos(3) == []
    assert not tem_representacao(3)
    for d in (3, 6, 7, 11, 12, 14, 15, 19, 21, 22, 23, 24):
        assert not tem_representacao(d), d


def test_todo_deslocamento_tem_mesmo_a_distancia():
    for d in (1, 2, 5, 10, 25, 50):
        for dx, dy in deslocamentos(d):
            assert dx * dx + dy * dy == d


def test_paridade_e_propriedade_de_d_nao_do_vetor():
    """(dx+dy)^2 = d + 2*dx*dy, entao dx+dy tem a paridade de d. Sempre."""
    for d in range(1, 101):
        for dx, dy in deslocamentos(d):
            assert (dx + dy) % 2 == paridade_forcada(d), (d, dx, dy)


def test_normaliza_aceita_int_e_conjunto():
    assert normaliza(5) == (5,)
    assert normaliza([2, 1, 2]) == (1, 2)
    assert normaliza((3, 1)) == (1, 3)


def test_deslocamentos_do_conjunto_junta_sem_repetir():
    um = set(deslocamentos(1))
    dois = set(deslocamentos(2))
    junto = set(deslocamentos_do_conjunto([1, 2]))
    assert junto == um | dois
    assert len(junto) == 8


def test_grafo_e_simetrico():
    adj = vizinhanca(4, 4, 1)
    for i, vs in enumerate(adj):
        for j in vs:
            assert i in adj[j]


def test_arestas_conta_cada_par_uma_vez():
    """Grade 3x3 com d=1: 12 arestas (6 horizontais e 6 verticais)."""
    assert arestas(3, 3, 1) == 12


def test_coloracao_valida_reprova():
    adj = vizinhanca(2, 2, 1)
    assert not coloracao_valida(adj, [0, 0, 0, 0])
    assert coloracao_valida(adj, [0, 1, 1, 0])
