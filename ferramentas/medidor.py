"""Medidor: as tabelas do README em markdown.

    python ferramentas/medidor.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from distancia_unitaria.medidas import (  # noqa: E402
    custo_extremo,
    distancias_validas,
    distribuicao_dos_pares,
    preve_bipartido,
    tabela_pares,
    tabela_uma_distancia,
)


def main():
    t0 = time.time()

    print('## Uma distancia sozinha (grade 8x8)')
    print()
    linhas = tabela_uma_distancia()
    cores = sorted({k for _, _, k in linhas})
    print('- distancias validas ate 100: %d' % len(distancias_validas()))
    print('- grafos com aresta na grade: %d' % len(linhas))
    print('- numeros cromaticos encontrados: %s' % cores)
    print()

    print('## Pares de distancias (grade 7x7)')
    print()
    print('| conjunto | arestas | piso-teto | cromatico | nos |')
    print('|---|---|---|---|---|')
    for par, ar, piso, teto, k, nos in tabela_pares():
        print('| %s | %d | %d-%d | %d | %d |' % (str(par), ar, piso, teto, k, nos))

    print()
    print('distribuicao: %s' % distribuicao_dos_pares())
    barato, caro = custo_extremo()
    print('mais barato: %s com %d nos' % (barato[0], barato[1]))
    print('mais caro: %s com %d nos' % (caro[0], caro[1]))

    print()
    print('## A regra fechada contra a varredura')
    print()
    erros = sum(1 for par, _, _, _, k, _ in tabela_pares()
                if (k == 2) != preve_bipartido(par))
    print('pares conferidos: %d, erros da regra: %d' % (len(tabela_pares()), erros))

    print()
    print('medido em %.1f s' % (time.time() - t0))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
