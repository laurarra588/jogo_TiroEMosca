import socket

HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 65432        # Porta do servidor

def receber_mensagem(client_socket):
    """Recebe mensagens do servidor garantindo que mensagens longas sejam completamente recebidas."""
    try:
        dados = client_socket.recv(4096)
        if not dados:
            raise ConnectionResetError
        return dados.decode()
    except ConnectionResetError:
        print("Conexão perdida com o servidor.")
        return None

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((HOST, PORT))
            mensagem_inicial = receber_mensagem(client_socket)
            if not mensagem_inicial:
                return
            print(mensagem_inicial)  # Mensagem de boas-vindas ou escolha de jogo
            

            continuar_jogando = True

            while continuar_jogando:
                jogo_ativo = True
                while jogo_ativo:
                    palpite = input("Digite seu palpite (3 dígitos distintos) ou 'desistir' para sair:")

                    if palpite.lower() == 'desistir':
                        client_socket.sendall(palpite.encode())
                        mensagem = receber_mensagem(client_socket)
                        if mensagem:
                            print(mensagem)
                        print("Reiniciando o jogo...")
                        continue

                    if len(palpite) != 3 or len(set(palpite)) != 3:
                        print("Palpite inválido! Digite um número de 3 dígitos distintos.")
                        continue
                    
                    client_socket.sendall(palpite.encode())
                    resultado = receber_mensagem(client_socket)
                    if not resultado:
                        return
                    print(resultado)
                    
                    if "Parabéns!" in resultado:
                        historico = receber_mensagem(client_socket)
                        if historico:
                            print(historico)
                    
                        break
                
                # Agora a pergunta só aparece depois do fim do jogo

                jogar_novamente = input("")
                if jogar_novamente.lower() != 's':
                    print("Obrigado por jogar! Encerrando conexão.")
                    client_socket.sendall("sair".encode())  # Informar o servidor que o jogador saiu
                    continuar_jogando = False
                else:
                    client_socket.sendall("continuar".encode())  # Informar ao servidor que deseja continuar
                    
                    # Esperar a confirmação do novo jogo antes de exibir a mensagem
                    mensagem_inicio = receber_mensagem(client_socket)
                    if not mensagem_inicio:
                        return
                    print("\nNovo jogo iniciado!", mensagem_inicio)
        except (ConnectionResetError, BrokenPipeError):
            print("A conexão com o servidor foi perdida. Fechando o cliente.")
        except Exception as e:
            print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    main()
