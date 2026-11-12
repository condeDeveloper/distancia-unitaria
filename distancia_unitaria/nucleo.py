"""Grafos de distancia na grade inteira.

Hadwiger-Nelson pergunta de quantas cores o plano precisa para que dois pontos
a distancia 1 nunca tenham a mesma cor. A resposta esta entre 5 e 7 e o
problema segue aberto -- e, pior para quem quer medir, as coordenadas que
interessam no plano envolvem raizes que nenhum computador representa exato.

Aqui a mesma pergunta e feita num lugar onde tudo fecha: a **grade inteira**.
Os pontos sao pares (x, y) de inteiros e "estar a distancia 1" vira "estar a
distancia ao quadrado igual a d", com d inteiro fixo. Toda conta e inteira,
nenhum arredondamento entra, e o dominio e finito -- entao da para varrer e
provar, nao estimar.

Trocar `d` troca o grafo inteiro: d=1 liga vizinhos de aresta, d=2 liga
diagonais, d=25 liga tanto (3,4) quanto (5,0). E e essa troca que faz a
pergunta render.
"""


def distancia2(a, b):
    """Distancia ao quadrado. Inteira, exata, sem raiz."""
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def pontos(largura, altura):
    """Os pontos da grade, em ordem fixa."""
    return [(x, y) for y in range(altura) for x in range(largura)]


def deslocamentos(d):
    """Os vetores (dx, dy) com dx^2 + dy^2 == d.

    Sao eles que definem o grafo: dois pontos sao vizinhos exatamente quando
    um esta no outro mais um destes.
    """
    saida = []
    limite = int(d ** 0.5) + 1
    for dx in range(-limite, limite + 1):
        for dy in range(-limite, limite + 1):
            if dx * dx + dy * dy == d:
                saida.append((dx, dy))
    return saida


def tem_representacao(d):
    """Existe algum par de inteiros a distancia ao quadrado d?

    Nem todo d serve: 3 nao e soma de dois quadrados, entao o grafo de d=3 nao
    tem aresta nenhuma e a pergunta fica vazia.
    """
    return len(deslocamentos(d)) > 0


def normaliza(d):
    """Aceita uma distancia ou um conjunto delas, e devolve sempre tupla.

    Com UMA distancia a grade inteira nunca passa de duas cores (ver o README).
    A pergunta so fica viva com CONJUNTOS, entao tudo aqui trabalha com tupla
    e o inteiro solto e so um atalho de escrita.
    """
    if isinstance(d, int):
        return (d,)
    return tuple(sorted(set(d)))


def deslocamentos_do_conjunto(ds):
    """Todos os vetores que alguma distancia do conjunto autoriza."""
    saida = []
    for d in normaliza(ds):
        saida.extend(deslocamentos(d))
    return sorted(set(saida))


def vizinhanca(largura, altura, ds):
    """O grafo, como lista de adjacencia indexada pela ordem de `pontos`."""
    ps = pontos(largura, altura)
    indice = {p: i for i, p in enumerate(ps)}
    desl = deslocamentos_do_conjunto(ds)
    adj = [[] for _ in ps]
    for i, (x, y) in enumerate(ps):
        for dx, dy in desl:
            j = indice.get((x + dx, y + dy))
            if j is not None:
                adj[i].append(j)
    return adj


def arestas(largura, altura, ds):
    """Quantas arestas o grafo tem (cada par contado uma vez)."""
    adj = vizinhanca(largura, altura, ds)
    return sum(len(v) for v in adj) // 2


def paridade_forcada(d):
    """A paridade de dx+dy que a distancia d obriga.

    De (dx+dy)^2 = dx^2 + dy^2 + 2*dx*dy = d + 2*dx*dy sai que (dx+dy)^2 tem a
    paridade de d, e portanto dx+dy tambem. Nenhum deslocamento escapa: a
    paridade e propriedade de d, nao do vetor.
    """
    return d % 2


def coloracao_valida(adj, cores):
    """Nenhum par vizinho divide a cor?"""
    for i, vizinhos in enumerate(adj):
        for j in vizinhos:
            if cores[i] == cores[j]:
                return False
    return True
