import socket
import random

HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 65432        # Porta para escutar as conexões

def gerar_numero_secreto():
    """Gera um número secreto de 3 dígitos distintos."""
    digitos = random.sample(range(0, 10), 3)
    return ''.join(map(str, digitos))

def analisar_palpite(numero, palpite):
    """Analisa um palpite e retorna a quantidade de tiros e moscas."""
    tiros = moscas = 0
    for i in range(3):
        if palpite[i] == numero[i]:
            moscas += 1
        elif palpite[i] in numero:
            tiros += 1
    return tiros, moscas

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print("Servidor aguardando conexões...")
        
        try:
            conn1, addr1 = server_socket.accept()
            print(f"Jogador conectado: {addr1}")
            
            historico = []
            
            
            while True:
                numero_secreto = gerar_numero_secreto()
                conn1.sendall("Tente adivinhar o número! (ou digite 'desistir' para pular)".encode())

                print(f"Número secreto gerado: {numero_secreto} (não revele durante testes!)")
                    
                rodadas = 0
                historico.clear()
                jogo_ativo = True

                while jogo_ativo:
                    palpite = conn1.recv(1024).decode()
                    if palpite.lower() == 'desistir':
                        print("Recomeçando o jogo")
                        break
                        
                    rodadas += 1
                    tiros, moscas = analisar_palpite(numero_secreto, palpite)
                    historico.append(f"{rodadas}. {palpite} - {tiros}t{moscas}m")
                        
                        
                    if palpite == numero_secreto:
                        conn1.sendall(f"Parabéns! Você acertou o número em {rodadas} rodadas!".encode())
                        conn1.sendall(f"Histórico:\n{chr(10).join(historico)}".encode())
                        conn1.sendall("\nDeseja jogar novamente?(s/n)".encode())
                        resposta = conn1.recv(1024).decode().strip().lower()
                        if resposta != 's':
                            jogo_ativo = False
                            break

                        else: 
                            break
                            
                    else:
                        conn1.sendall(f"Seu resultado: {tiros}T{moscas}M. Tente novamente.".encode())
                
        
        except Exception as e:
            print(f"Erro inesperado: {e}")
        finally:
            conn1.close()

if __name__ == "__main__":
    main()
