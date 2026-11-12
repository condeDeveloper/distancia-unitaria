"""Os numeros do README que nao custam minutos.

A tabela de pares inteira vive no `test_pesados.py`: um dos pares sozinho
custa meio milhao de nos.
"""

from distancia_unitaria.medidas import (
    distancias_validas,
    preve_bipartido,
    tabela_uma_distancia,
)
from distancia_unitaria.nucleo import deslocamentos


def test_quantas_distancias_valem_ate_100():
    assert len(distancias_validas(100)) == 43


def test_as_invalidas_sao_as_que_nao_sao_soma_de_dois_quadrados():
    validas = set(distancias_validas(30))
    assert validas == {d for d in range(1, 31) if deslocamentos(d)}
    for d in (3, 6, 7, 11, 12, 14, 15, 19, 21, 22, 23, 24):
        assert d not in validas


def test_uma_distancia_sozinha_nunca_passa_de_duas_cores():
    """O achado central deste projeto.

    Sao 43 distancias validas ate 100, mas so 33 TEM aresta numa grade 8x8:
    as outras dez sao longas demais para caber. A tabela cobre as 33, e e
    isso que ela diz -- nao as 43.
    """
    linhas = tabela_uma_distancia()
    assert len(linhas) == 33
    assert {k for _, _, k in linhas} == {2}


def test_dez_das_43_nao_cabem_na_grade_8():
    """A diferenca entre "valida" e "mede alguma coisa aqui"."""
    from distancia_unitaria.nucleo import arestas
    validas = distancias_validas(100)
    com_aresta = [d for d in validas if arestas(8, 8, d) > 0]
    assert len(validas) == 43
    assert len(com_aresta) == 33
    assert max(com_aresta) == 98


def test_toda_linha_da_tabela_tem_aresta():
    """Uma linha sem aresta nao provaria nada: o grafo vazio da 1 cor."""
    for _, ar, _ in tabela_uma_distancia():
        assert ar > 0


def test_a_regra_na_distancia_sozinha():
    """Com uma distancia so, a regra sempre diz bipartido -- e esta certa."""
    for d in distancias_validas(100):
        assert preve_bipartido(d)


def test_a_regra_separa_conjuntos():
    """Ela nao diz sim para tudo: misturar par com impar quebra."""
    assert preve_bipartido((1, 5))
    assert preve_bipartido((5, 13))
    assert preve_bipartido((2, 10))      # vira (1, 5) ao dividir por 2
    assert not preve_bipartido((1, 2))
    assert not preve_bipartido((2, 4))   # vira (1, 2)
    assert not preve_bipartido((4, 8))   # vira (1, 2) em dois passos


def test_a_divisao_por_dois_repete_ate_sobrar_impar():
    assert preve_bipartido((4, 20))      # -> (1, 5)
    assert preve_bipartido((8, 40))      # -> (1, 5)
    assert not preve_bipartido((8, 16))  # -> (1, 2)
