"""Linha de comando.

    python -m distancia_unitaria          tudo
    python -m distancia_unitaria solo     so a tabela de uma distancia
    python -m distancia_unitaria pares    so a tabela de pares
"""

import sys

from .medidas import (
    custo_extremo,
    distancias_validas,
    distribuicao_dos_pares,
    preve_bipartido,
    tabela_pares,
    tabela_uma_distancia,
)


def solo():
    linhas = tabela_uma_distancia()
    print('uma distancia sozinha, grade 8x8')
    print('   %d distancias validas ate 100' % len(distancias_validas()))
    cores = sorted({k for _, _, k in linhas})
    print('   numeros cromaticos encontrados: %s' % cores)
    if cores == [2]:
        print('   TODAS dao 2. Com uma distancia so, a grade nunca sobe.')
    print()


def pares():
    print('pares de distancias, grade 7x7')
    print('   %-12s %-8s %-9s %-6s %s' % ('conjunto', 'arestas', 'piso-teto', 'crom', 'nos'))
    for par, ar, piso, teto, k, nos in tabela_pares():
        print('   %-12s %-8d %-9s %-6d %d'
              % (str(par), ar, '%d-%d' % (piso, teto), k, nos))
    print()
    print('   distribuicao: %s' % distribuicao_dos_pares())
    barato, caro = custo_extremo()
    print('   mais barato: %s com %d nos' % (barato[0], barato[1]))
    print('   mais caro:   %s com %d nos' % (caro[0], caro[1]))
    print()


def regra():
    print('a regra fechada contra a varredura')
    erros = 0
    for par, _, _, _, k, _ in tabela_pares():
        if (k == 2) != preve_bipartido(par):
            erros += 1
            print('   ERRA em %s: cromatico=%d, regra diz %s'
                  % (par, k, preve_bipartido(par)))
    print('   erros: %d' % erros)
    print()


def main():
    alvo = sys.argv[1] if len(sys.argv) > 1 else 'tudo'
    if alvo in ('tudo', 'solo'):
        solo()
    if alvo in ('tudo', 'pares'):
        pares()
    if alvo in ('tudo', 'regra'):
        regra()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
