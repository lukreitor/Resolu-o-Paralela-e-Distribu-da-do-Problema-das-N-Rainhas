import time
import threading
import socket
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('Agg')  # Usa um backend não interativo, seguro para threads
import matplotlib.pyplot as plt


# Função para verificar se a rainha pode ser colocada na posição (row, col) sem ser atacada
def is_safe(board, row, col, n):
    for i in range(row):
        if board[i] == col or \
           board[i] - i == col - row or \
           board[i] + i == col + row:
            return False
    return True

# Função recursiva para resolver o problema das N Rainhas de forma sequencial
def solve_n_queens_sequential(board, row, n):
    if row == n:
        return True  # Solução encontrada
    for col in range(n):
        if is_safe(board, row, col, n):
            board[row] = col
            if solve_n_queens_sequential(board, row + 1, n):
                return True
            board[row] = -1  # Backtracking
    return False

# Função que inicializa o problema das N Rainhas de forma sequencial
def n_queens_sequential(n):
    board = [-1] * n
    if solve_n_queens_sequential(board, 0, n):
        return board  # Retorna o tabuleiro completo com as posições das rainhas
    return None

# Classe para resolver o problema das N Rainhas utilizando threads
class NQueensThread(threading.Thread):
    def __init__(self, n, board, row):
        threading.Thread.__init__(self)
        self.n = n
        self.board = board[:]
        self.row = row
        self.solved = False

    def run(self):
        self.solved = self.solve_n_queens_parallel(self.board, self.row, self.n)

    def is_safe(self, board, row, col):
        for i in range(row):
            if board[i] == col or \
               board[i] - i == col - row or \
               board[i] + i == col + row:
                return False
        return True

    def solve_n_queens_parallel(self, board, row, n):
        if row == n:
            return True
        for col in range(n):
            if self.is_safe(board, row, col):
                board[row] = col
                if self.solve_n_queens_parallel(board, row + 1, n):
                    return True
                board[row] = -1  # Backtracking
        return False

# Função para inicializar o problema das N Rainhas de forma paralela
def n_queens_parallel(n):
    threads = []
    solved_board = None
    for i in range(n):
        board = [-1] * n
        thread = NQueensThread(n, board, 0)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
        if thread.solved:
            solved_board = thread.board
            break

    if solved_board:
        save_board_image(solved_board, n, f"tabuleiro_paralelo_n_{n}.png")
        print(f"Imagem do tabuleiro de N={n} salva como 'tabuleiro_paralelo_n_{n}.png'.")

    return solved_board

# Função para lidar com o cliente no modelo distribuído
def handle_client(client_socket, n):
    board = [-1] * n
    if solve_n_queens_sequential(board, 0, n):
        client_socket.send(str(board).encode())
        save_board_image(board, n, f"tabuleiro_distribuido_n_{n}.png")
        print(f"Imagem do tabuleiro de N={n} salva como 'tabuleiro_distribuido_n_{n}.png'.")
    else:
        client_socket.send("Solução não encontrada".encode())
    client_socket.close()

def server_program(n):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(5)
    print("Servidor aguardando conexões...")

    client_socket, _ = server.accept()
    handle_client(client_socket, n)  # Passar o valor correto de n
    server.close()


def client_program():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 9999))
    resposta = client.recv(4096).decode()
    print(f"Resposta do servidor: {resposta}")
    client.close()

def n_queens_distributed(n):
    server_thread = threading.Thread(target=server_program, args=(n,))
    server_thread.start()
    time.sleep(1)  # Esperar o servidor iniciar
    client_program()
    server_thread.join()


# Função para salvar o tabuleiro em uma imagem
def save_board_image(board, n, filename):
    fig, ax = plt.subplots(figsize=(n, n))
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(True)
    ax.set_aspect('equal')

    # Corrigir o posicionamento das rainhas no tabuleiro NxN
    for row, col in enumerate(board):
        ax.add_patch(plt.Circle((col + 0.5, n - row - 0.5), 0.4, color='black'))

    # Ajustar os limites do tabuleiro corretamente
    ax.set_xlim(0, n)
    ax.set_ylim(0, n)

    plt.savefig(filename)
    plt.close()


# Função para realizar o benchmark e salvar os resultados incrementais
def benchmark_n_queens(n):
    start_time = time.time()
    board_seq = n_queens_sequential(n)
    sequential_time = time.time() - start_time

    start_time = time.time()
    solved_parallel = n_queens_parallel(n)
    parallel_time = time.time() - start_time

    start_time = time.time()
    n_queens_distributed(n)
    distributed_time = time.time() - start_time

    # Atualizar o arquivo .md sem sobrescrever os benchmarks anteriores
    with open("comparacao_desempenho.md", "a") as f:
        f.write(f"## Tamanho do Tabuleiro: {n}x{n}\n\n")
        f.write("| Implementação | Tempo de Execução (segundos) |\n")
        f.write("| ------------- | --------------------------- |\n")
        f.write(f"| Sequencial    | {sequential_time:.4f} segundos |\n")
        f.write(f"| Paralela      | {parallel_time:.4f} segundos |\n")
        f.write(f"| Distribuída   | {distributed_time:.4f} segundos |\n")
        f.write("\n---\n")

    print(f"Benchmark para N={n} salvo no arquivo 'comparacao_desempenho.md'.")

    if board_seq:
        save_board_image(board_seq, n, f"tabuleiro_n_{n}.png")
        print(f"Imagem do tabuleiro de N={n} salva como 'tabuleiro_n_{n}.png'.")

if __name__ == "__main__":
    for n in [4, 8, 6, 12, 10, 15, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 35, 40]:
        print(f"Rodando testes para N={n}")
        benchmark_n_queens(n)
