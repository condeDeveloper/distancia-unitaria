"""Os dois juizes que cercam o numero cromatico por fora.

A busca exata encontra o menor numero de cores que serve. Este arquivo nao
sabe fazer isso. Ele sabe fazer duas coisas mais simples e independentes, que
juntas prendem a resposta num intervalo:

- **clique**: um conjunto de pontos todos vizinhos entre si precisa de uma cor
  cada um. O tamanho da maior clique que se acha e um PISO para o numero
  cromatico.
- **guloso**: colorir na ordem, sempre com a menor cor livre, sempre funciona
  e gasta alguma coisa. Quantas cores ele gastou e um TETO.

Se o piso e o teto se encontram, a resposta esta provada sem a busca exata
precisar rodar. Quando nao se encontram, sobra o intervalo, e ai a busca
decide -- mas tem que cair DENTRO dele. Uma busca que devolve valor fora do
intervalo esta errada, e e isso que a bateria cobra.
"""


def maior_clique(adj, limite_de_nos=200000):
    """O tamanho da maior clique, por busca com retrocesso.

    Devolve (tamanho, nos). O `limite_de_nos` existe porque clique maxima e
    cara: se estourar, o que volta e um piso VALIDO mas talvez nao o melhor,
    e quem chama precisa saber disso -- por isso o contador de nos sai junto.
    """
    n = len(adj)
    vizinhos = [set(v) for v in adj]
    melhor = [0]
    nos = [0]
    estourou = [False]

    def desce(atual, candidatos):
        nos[0] += 1
        if nos[0] > limite_de_nos:
            estourou[0] = True
            return
        if len(atual) > melhor[0]:
            melhor[0] = len(atual)
        if not candidatos:
            return
        if len(atual) + len(candidatos) <= melhor[0]:
            return
        for v in sorted(candidatos):
            if estourou[0]:
                return
            desce(atual + [v], candidatos & vizinhos[v])

    desce([], set(range(n)))
    return melhor[0], nos[0], estourou[0]


def coloracao_gulosa(adj, ordem=None):
    """Colore na ordem dada, sempre com a menor cor livre.

    Devolve (quantas_cores, cores). Nunca falha: no pior caso usa grau+1.
    """
    n = len(adj)
    if ordem is None:
        ordem = range(n)
    cores = [-1] * n
    for v in ordem:
        usadas = {cores[u] for u in adj[v] if cores[u] >= 0}
        c = 0
        while c in usadas:
            c += 1
        cores[v] = c
    return (max(cores) + 1 if n else 0), cores


def guloso_por_grau(adj):
    """O mesmo guloso, visitando os de maior grau primeiro.

    Costuma gastar menos cores, e e um teto diferente do guloso na ordem
    natural. Dois tetos apertam mais que um.
    """
    ordem = sorted(range(len(adj)), key=lambda v: -len(adj[v]))
    return coloracao_gulosa(adj, ordem)


def intervalo(adj):
    """(piso, teto): a resposta exata tem que cair aqui dentro."""
    piso, _, _ = maior_clique(adj)
    teto_natural, _ = coloracao_gulosa(adj)
    teto_grau, _ = guloso_por_grau(adj)
    return piso, min(teto_natural, teto_grau)
