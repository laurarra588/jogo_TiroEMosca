import socket
import customtkinter as ctk
import threading

HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 65432        # Porta do servidor

class JogoClient(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Jogo de Adivinhação")
        self.geometry("900x900")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((HOST, PORT))

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        self.tab_jogo = self.tabview.add("Jogo")
        self.tab_historico = self.tabview.add("Histórico")

        # Aba do jogo
        self.label_mensagem = ctk.CTkLabel(
            self.tab_jogo, text="Aguardando mensagem do servidor...",
            wraplength=900, font=("Arial", 20, "bold"), text_color="#FFD700"
        )
        self.label_mensagem.pack(pady=20)

        self.entry_input = ctk.CTkEntry(self.tab_jogo, width=600, font=("Arial", 18), corner_radius=10)
        self.entry_input.pack(pady=10)

        self.button_frame = ctk.CTkFrame(self.tab_jogo, corner_radius=10)
        self.button_frame.pack(pady=10)

        self.button_enviar = ctk.CTkButton(
            self.button_frame, text="Enviar", command=self.enviar_mensagem,
            fg_color="#1e90ff", hover_color="#0073e6", corner_radius=10
        )
        self.button_enviar.pack(side="left", padx=10)

        self.button_desistir = ctk.CTkButton(
            self.button_frame, text="Desistir", command=self.desistir_do_jogo,
            fg_color="#FFA500", hover_color="#CC8400", corner_radius=10
        )
        self.button_desistir.pack(side="left", padx=10)

        self.button_sair = ctk.CTkButton(
            self.button_frame, text="Sair", command=self.sair_do_jogo,
            fg_color="#ff4d4d", hover_color="#cc0000", corner_radius=10
        )
        self.button_sair.pack(side="right", padx=10)

        self.button_continuar = ctk.CTkButton(
            self.button_frame, text="Continuar", command=self.continuar_jogo,
            fg_color="#32CD32", hover_color="#228B22", corner_radius=10
        )
        self.button_continuar.pack(side="left", padx=10)

        # Aba do histórico
        self.label_historico = ctk.CTkLabel(self.tab_historico, text="Histórico de Tentativas e Rodadas", font=("Arial", 18, "bold"))
        self.label_historico.pack(pady=10)

        self.texto_historico = ctk.CTkTextbox(self.tab_historico, height=500, width=900, font=("Arial", 16), corner_radius=10)
        self.texto_historico.pack(pady=10)
        self.texto_historico.configure(state="disabled")

        self.historico_tentativas = []
        self.rodadas = 0
        self.tentativas = 0

        self.thread_receber = threading.Thread(target=self.receber_mensagem_continuamente, daemon=True)
        self.thread_receber.start()

    def receber_mensagem_continuamente(self):
        while True:
            try:
                dados = self.client_socket.recv(4096)
                if not dados:
                    raise ConnectionResetError
                mensagem = dados.decode()
                self.label_mensagem.configure(text=mensagem)
                self.atualizar_historico(mensagem)
                self.verificar_parabens(mensagem)
            except ConnectionResetError:
                self.label_mensagem.configure(text="Conexão perdida com o servidor.")
                break

    def atualizar_historico(self, mensagem):
        self.historico_tentativas.append(mensagem)
        self.texto_historico.configure(state="normal")
        self.texto_historico.insert("end", mensagem + "\n")
        self.texto_historico.see("end")
        self.texto_historico.configure(state="disabled")

    def verificar_parabens(self, mensagem):
        if "Parabéns!" in mensagem:
            self.mostrar_mensagem_parabens(self.rodadas)
            self.tentativas = 0

    def mostrar_mensagem_parabens(self, rodadas):
        popup = ctk.CTkToplevel(self)
        popup.geometry("500x250")
        popup.title("Vitória!")
        popup.grab_set()
        popup.configure(fg_color="#2E8B57")
        
        label = ctk.CTkLabel(
            popup, text=f"🎉 PARABÉNS! VOCÊ ACERTOU O NÚMERO EM {self.tentativas} TENTATIVAS! 🎉",
            font=("Arial", 24, "bold"), wraplength=480, text_color="white"
        )
        label.pack(pady=40)
        
        btn = ctk.CTkButton(popup, text="OK", command=popup.destroy, fg_color="#FFD700", hover_color="#DAA520")
        btn.pack()

    def continuar_jogo(self):
        self.client_socket.sendall("continuar".encode())
        self.label_mensagem.configure(text="Novo jogo iniciado! Faça seu palpite.")
        self.entry_input.delete(0, "end")
        self.historico_tentativas.clear()
        self.tentativas = 0

    def enviar_mensagem(self):
        mensagem = self.entry_input.get().strip()
        if mensagem:
            self.client_socket.sendall(mensagem.encode())
            self.atualizar_historico(f"Você: {mensagem}")  # Adiciona ao histórico
            self.entry_input.delete(0, "end")
            self.tentativas += 1

    def desistir_do_jogo(self):
        self.client_socket.sendall("desistir".encode())
        self.atualizar_historico("Você desistiu do jogo.")

    def sair_do_jogo(self):
        self.client_socket.sendall("sair".encode())
        self.client_socket.close()
        self.destroy()

if __name__ == "__main__":
    app = JogoClient()
    app.mainloop()
