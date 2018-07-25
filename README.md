# Grammar-Parser
Simplificação de GLC's, Forma Normal de Chomsky e Parsing de Linguagem Natural com CYK

Como executar o programa:

O programa pode ser rodado diretamente (dando dois cliques em cima do arquivo 'trabFormais.pyw') apenas se houver o Python 3.6 no Path do computador.

Caso haja problemas para iniciar o programa (que não é executado pelo terminal, mas sim criada uma janela), o programa pode ser aberto na IDLE do próprio Python 3.6 
e a partir dele, rodar.


LEITURA: o arquivo de entrada é passado para o programa no espaço dado, e para realizar a leitura, deve-se apertar no botão 'Ler', logo ao lado.
O nome do arquivo pode ou não ser passado com o final '.txt', caso não tenha nenhuma extensão, ele irá adicionar o '.txt' e ler o arquivo assim que o usuário pedir.
Outro método para abrir o arquivo é indo em 'File'->'Open' nas abas do menu do programa. Ao utilizar essa opção será possível escolher um diretório para selecionar o arquivo TXT
desejado. Note que apertando o botão 'Ler' com o espaço de escrita do nome do arquivo em branco, também será possível entrar nos diretórios para procurar o arquivo.

A janela não é redimensionável para não haver problemas visuais durante a execução.


FORMATAÇÃO: O arquivo de leitura deve conter descritores do que se segue, isto é, nome da informação seguido pela informação. Por exemplo:
OBS: Importante manter os nomes abaixo, pois serão palavras chave para o programa saber exatamente o que está lendo.

#Terminais
...
#Variaveis
...
#Inicial
...
#Regras
... (Regras devem ser formatadas na forma '[ X ] > [ Y ]...')
(qualquer comentário não deve ser feito em uma linha sozinha, deve ser feita como está apresentada em 'gramatica_exemplo1', de onde foi tirada a formatação padrão)


Após realizar a leitura do arquivo, o usuário poderá apertar no botão 'Simplificar/FNC' logo abaixo da tela onde é mostrado o conteúdo, o qual realiza
o algoritmo de Simplificação e, logo em seguida, da Forma Normal de Chomksy.

Apenas após aplicar a Simplificação/FNC o botão de verificação de palavra será liberado para ser clicado. Nesse momento o usuário poderá verificar diversas palavras, e o programa
vai colocar na janela a matriz gerada a partir do algoritmo CYK e todas as árvores de derivações geradas. Sempre abaixo do espaço de escrita, depois de clicar para verificar uma
palavra, será mostrada em forma de texto se a palavra foi aceita ou não.


O programa ainda tem a opção de salvar o conteúdo da janela, onde tem as simplificações, etc, em um arquivo TXT em um diretório escolhido pelo usuário, o que pode ser útil
dependendo as intenções do usuário.

-verifique se o icone ('icon8.ico') da janela está presente na pasta contendo o programa, caso não esteja pode haver problema na execução.
-Estamos enviando alguns arquivos de teste que podem ser utilizados, até para poder verificar a formatação do arquivo de entrada.
