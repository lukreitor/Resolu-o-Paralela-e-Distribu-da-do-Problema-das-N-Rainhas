import time
import multiprocessing
import socket
import dask.distributed as dask_dist
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('Agg')  # Usa um backend não interativo, seguro para multiprocessamento

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

# Função para resolver as N rainhas em paralelo usando multiprocessing
def parallel_worker(n, row):
    board = [-1] * n
    if solve_n_queens_sequential(board, row, n):
        return board
    return None

# Função para inicializar o problema das N Rainhas de forma paralela usando multiprocessing
def n_queens_parallel(n):
    with multiprocessing.Pool() as pool:
        results = pool.starmap(parallel_worker, [(n, row) for row in range(n)])
        
    # Filtrar o primeiro tabuleiro solucionado
    solved_board = next((result for result in results if result), None)
    
    if solved_board:
        save_board_image(solved_board, n, f"tabuleiro_paralelo_n_{n}.png")
        print(f"Imagem do tabuleiro de N={n} salva como 'tabuleiro_paralelo_n_{n}.png'.")
    
    return solved_board

# Função distribuída usando Dask
def dask_worker(n):
    board = [-1] * n
    if solve_n_queens_sequential(board, 0, n):
        return board
    return None

def n_queens_distributed(n):
    cluster = dask_dist.LocalCluster()
    client = dask_dist.Client(cluster)
    
    futures = client.map(dask_worker, [n] * n)
    results = client.gather(futures)
    
    solved_board = next((result for result in results if result), None)
    
    if solved_board:
        save_board_image(solved_board, n, f"tabuleiro_distribuido_n_{n}.png")
        print(f"Imagem do tabuleiro de N={n} salva como 'tabuleiro_distribuido_n_{n}.png'.")
    
    client.close()
    cluster.close()

    return solved_board

# Função para salvar o tabuleiro em uma imagem
def save_board_image(board, n, filename):
    fig, ax = plt.subplots(figsize=(n, n))
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(True)
    ax.set_aspect('equal')

    for row, col in enumerate(board):
        ax.add_patch(plt.Circle((col + 0.5, n - row - 0.5), 0.4, color='black'))

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
    solved_distributed = n_queens_distributed(n)
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
