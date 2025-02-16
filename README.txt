Como executar o jogo de adivinhação
------------------------------------------------------------------------------------------------------------------------------------

Executar o servidor:

Abra um terminal ou prompt de comando na pasta onde está o arquivo do servidor.

Execute o comando:

python servidor.py

O servidor irá aguardar conexões dos jogadores.
------------------------------------------------------------------------------------------------------------------------------------

Executar o cliente:

Em outro terminal ou prompt de comando, navegue até a pasta onde está o arquivo do cliente.

Execute o comando:

python cliente_Tkinter.py

A interface gráfica do jogo será aberta.
------------------------------------------------------------------------------------------------------------------------------------

Regras do jogo:

O jogador deve adivinhar um número de 3 dígitos distintos.

O servidor fornece feedback baseado no palpite do jogador.

O jogador pode desistir a qualquer momento digitando "desistir" ou clicando no botão.

Após acertar o número, a quantidade de rodadas será exibida.

O jogador pode optar por continuar jogando ou sair.
------------------------------------------------------------------------------------------------------------------------------------

Requisitos

Python 3.x

Biblioteca customtkinter

Socket para comunicação cliente-servidor
