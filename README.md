# Regras do Jogo
> Existem 12 regras de movimentação diferentes. Ao fim do nível 12, o jogo volta à regra inicial (em que cada movimento corresponde a apenas ao movimento realmente efetuado), mas aumenta a dificuldade alterando o objetivo da board.

> Não se sabe ao certo quantos tabuleiros diferentes existem.

> Em cima aparece um contador com o tempo do nível atual, o número do nível atual, o counter de moves para o nível atual e um número misterioso.

## Regras de Movimentação
- 1: mover uma coluna ou uma linha corresponde a deslocar uma vez a coluna ou linha selecionada
- 2: igual à regra 1, mas desloca 2 casas de uma vez
- 3: mover uma coluna corresponde a deslocar a linha correspondente e vice-versa (e.g. ao clicar na linha 1, vai mover-se a coluna 1, etc.)
- 4: o movimento é igual à primeira regra, mas existem menos setas, em sítios específicos (primeiras e últimas duas colunas e 3 colunas do meio e primeira linha, últimas duas, e 3 do meio, sendo as linhas e colunas simétricas) (é preciso ter cuidado para o estado inicial não ter peças em sítios impossíveis)
- 5: igual à regra 1, mas a linha/coluna move-se no sentido oposto ao da seta
- 6: como na regra 5, o movimento é oposto, mas agora é também simétrico (mover a coluna n resulta em mover a coluna 9-n+1)
- 7: igual à anterior, mas para além de mover a coluna/linha simétrica, move também a original correspondente à senta onde se clicou
- 8: mover uma coluna/linha resulta em mover também a coluna/linha com número correspondente. Mover para a direita corresponde a mover para cima e mover para a esquerda corresponde a mover para baixo
- 9: o movimento é simétrico: mover a coluna/linha x resulta em mover também uma casa na coluna/linha 9-x+1 (caso se mova a coluna/linha do meio, move apenas essa)
- 10: igual à 8, mas com as setas da 4
- 11: mover uma coluna/linha move também a coluna/linha adjacente. A adjacente é considerada a que está à direta no caso de colunas ou em baixo no caso de linhas. Caso seja a última linha/coluna, o movimento adicional será na primeira
- 12: tipo a 11, mas em vez de mover a adjacente, move a coluna/linha que se situa 2 para a esquerda/baixo. Caso fique fora do tabuleiro aplica-se a regra da 11 

# Correr:
- `pip install -r requirements.txt`
- `python3 main.py`

### Opcional - criar um virtual environment (instala packages apenas localmente no projeto)
- `python -m venv venv`
- `source venv/bin/activate`
- para sair: `deactivate`

