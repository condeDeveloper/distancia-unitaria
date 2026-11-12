# distancia-unitaria

Grafos de distância na **grade inteira**, varridos em Python 3.10+ sem dependência nenhuma:
número cromático exato por busca com retrocesso, cercado por cima e por baixo por dois
juízes independentes, e toda conta feita com inteiros.

## O que é

Hadwiger-Nelson pergunta de quantas cores o plano precisa para que dois pontos a distância
1 nunca dividam a cor. A resposta está entre 5 e 7 e o problema segue aberto. Pior para
quem quer **medir**: as coordenadas que interessam no plano envolvem raízes que nenhum
computador representa exato.

Aqui a mesma pergunta é feita onde tudo fecha. Os pontos são pares `(x, y)` de inteiros, e
"estar a distância 1" vira "estar a distância **ao quadrado** igual a `d`", com `d` inteiro
fixo. Nenhum arredondamento entra, o domínio é finito, e dá para provar em vez de estimar.

## Os quatro achados

- **Com uma distância só, a grade nunca passa de duas cores.** Das 43 distâncias válidas
  até 100, as **33** que têm aresta numa grade 8×8 dão **todas** número cromático 2. No
  plano uma distância já força pelo menos 5; na grade inteira ela nunca força mais que 2.
  A tabela saiu chapada, e a tabela chapada *era* o achado.
- **A razão é um teorema de paridade, e a varredura entregou ele.** De
  `(dx+dy)² = dx² + dy² + 2·dx·dy = d + 2·dx·dy` sai que `dx+dy ≡ d (mod 2)`: a paridade da
  soma é propriedade de **d**, não do vetor. Com `d` ímpar, a paridade de `x+y` já é uma
  coloração própria. Com `d` par, o grafo se parte em duas sublattices e a pergunta
  recomeça menor.
- **Uma regra fechada decide bipartição para conjuntos de distâncias:** divida todas por 2
  enquanto todas forem pares, e veja se o que sobrou é todo ímpar. Conferida contra a busca
  exata em **71 conjuntos** — 36 pares e 35 trios — com **zero erros**.
- **A heurística padrão de colorir pelos vértices de maior grau não domina.** Nos 36 pares
  da grade 6×6 ela perde 5 vezes, ganha 5 e empata 26. Em `{1, 10}` ela gasta **seis** cores
  onde a ordem natural gasta **quatro**.

## Uma distância sozinha

| medida | valor |
|---|---|
| distâncias válidas até 100 | 43 |
| com aresta numa grade 8×8 | 33 |
| maior `d` que ainda cabe | 98 |
| números cromáticos encontrados | **{2}** |

"Válida" e "mede alguma coisa aqui" não são a mesma coisa: dez das 43 são longas demais
para caber numa grade 8×8, e a linha delas não provaria nada.

Nem todo inteiro é uma distância válida. `d` precisa ser soma de dois quadrados, então
3, 6, 7, 11, 12, 14, 15, 19, 21, 22, 23 e 24 não têm **nenhuma** aresta — o grafo deles é
poeira solta.

## Pares de distâncias (grade 7×7)

É aqui que a pergunta fica viva. Das primeiras nove distâncias válidas saem 36 pares:

| cores | pares |
|---|---|
| 2 | 7 |
| 3 | 20 |
| 4 | 9 |

Nenhum par chega a 5 cores nesta grade. Os sete bipartidos são `{1,5}`, `{1,9}`, `{1,13}`,
`{5,9}`, `{5,13}`, `{9,13}` — todos pares de ímpares — e `{2,10}`, que vira `{1,5}` ao ser
dividido por 2. A regra fechada acerta os sete.

## Achar é barato, provar é caro

| par | nós |
|---|---|
| mais barato | 50 |
| `{13, 16}` | **540.248** |

Mais de dez mil vezes de diferença entre o par mais fácil e o mais difícil **da mesma
tabela**. A assimetria tem explicação: achar uma coloração com `k` cores é barato — basta
uma dar certo. Mostrar que `k-1` é impossível exige esgotar o espaço inteiro.

## Os três caminhos para o mesmo número

A busca exata não anda sozinha. Dois juízes independentes prendem a resposta num intervalo
antes de ela existir:

- **clique** dá o piso: um conjunto de pontos todos vizinhos entre si precisa de uma cor
  para cada um.
- **guloso** dá o teto: colorir na ordem com a menor cor livre sempre funciona, e o que
  gastou é um limite superior.

Quando piso e teto se encontram, a resposta está provada sem a busca exata precisar rodar.
Quando não se encontram, a busca decide — mas **tem que cair dentro do intervalo**, e a
bateria cobra isso nos 36 pares. Uma busca que respondesse fora dele estaria errada.

## O que as medidas me corrigiram

- **Minha primeira tabela veio toda com o valor 2 e eu quase a dei por boa.** Treze
  distâncias, treze vezes "cromático 2". Tabela chapada é sinal de pergunta mal feita, e
  era: com uma distância só o grafo é sempre bipartido. Em vez de trocar o projeto, medi
  **por quê** — e saiu o teorema de paridade, que virou o segundo achado. A pergunta certa
  era sobre conjuntos.
- **Escrevi no teste que a ordem por grau nunca seria pior.** É a heurística que todo mundo
  usa, e eu a tratei como garantida dentro do arquivo que existe para impedir chute. Ela
  perde em 5 dos 36 pares, e em `{1, 10}` perde feio: 6 cores contra 4.
- **Confundi "distância válida" com "distância que mede algo nesta grade".** Prendi 43 no
  teste quando a tabela tem 33 linhas: as outras dez não cabem numa grade 8×8. São duas
  perguntas diferentes e eu as escrevi como se fossem uma.
- **O caminho do Git Bash quebrou um script de varredura.** `/c/Projetos/...` não é caminho
  que o Python do Windows resolva, e o erro saiu como `ModuleNotFoundError` num módulo que
  existia o tempo todo.

## Rodar

```bash
pip install -e ".[dev]"
pytest                                    # a bateria inteira
pytest --ignore=testes/test_pesados.py    # sem a tabela de pares (minutos)
python -m distancia_unitaria              # tudo
python -m distancia_unitaria solo         # uma distância sozinha
python -m distancia_unitaria regra        # a regra fechada contra a varredura
python ferramentas/medidor.py
```

## Mapa

| arquivo | o que faz |
|---|---|
| `distancia_unitaria/nucleo.py` | pontos, deslocamentos, o grafo, a paridade forçada |
| `distancia_unitaria/juiz.py` | clique por baixo, guloso por cima |
| `distancia_unitaria/busca.py` | o cromático exato, com poda de simetria de cores |
| `distancia_unitaria/medidas.py` | as tabelas, e a regra fechada |
| `testes/test_pesados.py` | os 36 pares e os 35 trios |

34 testes. MIT.
