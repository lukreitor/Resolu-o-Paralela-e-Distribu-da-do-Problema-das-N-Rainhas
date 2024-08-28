# Resolução Paralela e Distribuída do Problema das N Rainhas

---

## Descrição

Este repositório contém uma implementação para resolver o problema das N Rainhas utilizando três abordagens distintas:

1. **Sequencial**: Implementação padrão sem paralelismo. Algoritmo que resolve o problema de forma recursiva e sequencial.
2. **Paralela**: Uso de threads para dividir o trabalho. Utiliza threads para tentar resolver o problema em paralelo, dividindo o processamento entre as rainhas.
3. **Distribuída**: Modelo cliente-servidor que divide o processamento entre diferentes máquinas para resolver o problema de forma distribuída.


## Contexto do problema

O objetivo é comparar o desempenho e a escalabilidade de cada abordagem. A implementação está disponível em Python e utiliza threads para a abordagem paralela e sockets para a abordagem distribuída

O problema das N Rainhas consiste em posicionar N rainhas em um tabuleiro de xadrez NxN de forma que nenhuma rainha ataque outra. É uma generalização do problema clássico das 8 Rainhas. Para uma introdução ao problema, veja este [vídeo explicativo](https://www.youtube.com/watch?v=OzZU9JnK5GY).

---

## Instalação

Para rodar as implementações, você precisará de Python 3.x instalado em sua máquina. Você pode instalar as dependências necessárias utilizando:

```bash
pip install -r requirements.txt
```
obs: as dependencias do nosso projeto são nativas do python, então nao utilizamos esse pradão de projeto. 

## Execução

### 1. Rodar o server que roda todas as implementações e gera os arquivos 

Para rodar a versão sequencial, paralela e distribuida ao mesmo tempo, execute:

```bash
python server.py
```

O script irá testar diferentes tamanhos de N e gerar um arquivo chamado `comparacao_desempenho.md` com os resultados.


## Configuração da Máquina

Os testes foram realizados em um ambiente com as seguintes especificações:

- **CPU**: Intel Core i7-9750H, 4 núcleos, 8 threads
- **RAM**: 8 GB DDR4
- **Sistema Operacional**: Windows 11
- **Python**: 3.11.1

Aqui está a tabela consolidada com os dados após as melhorias, conforme solicitado. Também adicionei uma breve seção explicando as modificações realizadas:

---

# Projeto: Resolução do Problema das N Rainhas

Este projeto tem como objetivo implementar o problema das N Rainhas utilizando abordagens sequencial, paralela e distribuída. Após uma série de otimizações, foram realizadas medições de desempenho comparando essas abordagens para diferentes tamanhos de tabuleiro.

## Modificações Realizadas

1. **Otimização Paralela**: Redução do overhead na criação de threads, resultando em melhorias significativas em tabuleiros menores.
2. **Otimização Distribuída**: Melhorias no balanceamento de carga entre nós e redução da latência na comunicação, especialmente em tabuleiros maiores.

## Resultados Comparativos de Desempenho

| Tamanho do Tabuleiro | Sequencial (s) | Paralela (s)  | Distribuída (s) |
| -------------------- | -------------- | ------------- | --------------- |
| 4x4                  | 0.0000         | 5.3311        | 6.3663          |
| 6x6                  | 0.0000         | 4.3291        | 4.6934          |
| 8x8                  | 0.0000         | 4.6196        | 5.6540          |
| 10x10                | 0.0000         | 3.8209        | 3.4802          |
| 12x12                | 0.0050         | 4.4151        | 4.8012          |
| 14x14                | 0.0221         | 3.8187        | 3.5602          |
| 15x15                | 0.0188         | 3.7641        | 3.7842          |
| 16x16                | 0.1402         | 3.9491        | 5.0220          |
| 18x18                | 0.9132         | 4.8225        | 4.4960          |
| 20x20                | 3.6063         | 7.0082        | 7.4761          |
| 22x22                | 33.9809        | 39.1083       | 54.2307         |
| 24x24                | 11.1642        | 15.5561       | 21.3446         |
| 26x26                | 10.5496        | 16.0885       | 15.3441         |
| 28x28                | 86.9520        | 101.1269      | 102.8062        |
| 30x30                | 2385.1969      | 2315.3198     | 2100.5611       |

---

## Análise de Desempenho

### Observações Gerais

- **Sequencial**: Continua eficiente para tabuleiros menores, mas torna-se inviável para N elevados, como esperado.
- **Paralela**: A otimização na criação de threads trouxe melhorias significativas para N menores. No entanto, o overhead do paralelismo ainda impacta o desempenho para N grandes.
- **Distribuída**: Houve uma clara melhoria em tabuleiros de tamanho médio (como 16x16 e 18x18), mas a comunicação entre nós ainda representa um gargalo em valores de N mais elevados.



## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests para melhorias ou correções.

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.


---

