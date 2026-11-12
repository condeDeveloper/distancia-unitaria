"""A busca exata: o menor numero de cores que serve.

Tenta k = 1, 2, 3, ... e para no primeiro que da. Para cada k, uma busca com
retrocesso tenta colorir vertice por vertice.

Duas podas, e as duas sao de simetria, nao de forca bruta:

- **cor nova so na ordem**: trocar o nome das cores nao muda nada, entao o
  primeiro vertice sempre recebe a cor 0, e um vertice so pode estrear uma
  cor se todas as menores ja estiverem em uso. Isso corta o fatorial das
  renomeacoes.
- **ordem por grau**: colorir primeiro quem tem mais vizinhos faz o conflito
  aparecer cedo, quando ainda ha pouco trabalho jogado fora.

O comecar em k = piso (vindo da clique) em vez de k = 1 nao e poda: e nao
repetir pergunta que ja tem resposta.
"""

from .juiz import maior_clique


def colorivel_com(adj, k, contar_nos=False):
    """Da para colorir com exatamente k cores disponiveis?

    Devolve (da, cores, nos).
    """
    n = len(adj)
    if n == 0:
        return True, [], 0
    if k <= 0:
        return False, None, 0

    ordem = sorted(range(n), key=lambda v: -len(adj[v]))
    posicao = {v: i for i, v in enumerate(ordem)}
    vizinhos_antes = [[u for u in adj[v] if posicao[u] < posicao[v]] for v in range(n)]

    cores = [-1] * n
    nos = [0]

    def desce(i, usadas):
        nos[0] += 1
        if i == n:
            return True
        v = ordem[i]
        proibidas = {cores[u] for u in vizinhos_antes[v]}
        # Uma cor ainda nao usada e intercambiavel com qualquer outra ainda
        # nao usada: basta tentar a PRIMEIRA delas.
        teto = min(usadas + 1, k)
        for c in range(teto):
            if c in proibidas:
                continue
            cores[v] = c
            if desce(i + 1, max(usadas, c + 1)):
                return True
            cores[v] = -1
        return False

    deu = desce(0, 0)
    return deu, (list(cores) if deu else None), nos[0]


def cromatico(adj):
    """O numero cromatico exato, e quantos nos custou prova-lo.

    Devolve (k, cores, nos_totais). Comeca do piso dado pela clique: abaixo
    dele a resposta ja e nao, e perguntar seria desperdicio.
    """
    if not adj:
        return 0, [], 0
    piso, _, _ = maior_clique(adj)
    total = 0
    k = max(1, piso)
    while True:
        deu, cores, nos = colorivel_com(adj, k)
        total += nos
        if deu:
            return k, cores, total
        k += 1


def custo_de_provar(adj, k):
    """Quantos nos para mostrar que k-1 nao basta e que k basta.

    E a medida honesta do "quanto custa provar", separada do "quanto custa
    achar": achar uma coloracao com k cores e barato; mostrar que k-1 e
    impossivel exige esgotar.
    """
    _, _, nos_falha = colorivel_com(adj, k - 1)
    _, _, nos_sucesso = colorivel_com(adj, k)
    return nos_falha, nos_sucesso
