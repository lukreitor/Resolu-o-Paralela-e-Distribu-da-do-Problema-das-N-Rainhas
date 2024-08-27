# Resolução Paralela e Distribuída do Problema das N Rainhas

---

**Título do Repositório:**

`Resolução Paralela e Distribuída do Problema das N Rainhas`

**Descrição:**

Este repositório contém uma implementação para resolver o problema das N Rainhas utilizando três abordagens distintas: sequencial, paralela e distribuída. O objetivo é comparar o desempenho e a escalabilidade de cada abordagem. A implementação está disponível em Python e utiliza threads para a abordagem paralela e sockets para a abordagem distribuída.

---

**README.md**

```markdown
# Resolução Paralela e Distribuída do Problema das N Rainhas

## Descrição

Este projeto visa resolver o problema das N Rainhas utilizando três abordagens diferentes:

1. **Sequencial**: Implementação padrão sem paralelismo.
2. **Paralela**: Uso de threads para dividir o trabalho.
3. **Distribuída**: Comunicação via sockets entre cliente e servidor.

O problema das N Rainhas consiste em posicionar N rainhas em um tabuleiro de xadrez NxN de forma que nenhuma rainha ataque outra. É uma generalização do problema clássico das 8 Rainhas. Para uma introdução ao problema, veja este [vídeo explicativo](https://www.youtube.com/watch?v=OzZU9JnK5GY).

## Instalação

Para rodar as implementações, você precisará de Python 3.x instalado em sua máquina. Você pode instalar as dependências necessárias utilizando:

```bash
pip install -r requirements.txt
```
obs: as dependencias do nosso projeto são nativas do python, então nao utilizamos esse pradão de projeto. 

## Execução

### 0. Rodar o server que roda todas as implementações e gera os arquivos 

Para rodar a versão sequencial, paralela e distribuida ao mesmo tempo, execute:

```bash
python server.py
```

O script irá testar diferentes tamanhos de N e gerar um arquivo chamado `comparacao_desempenho.md` com os resultados.

Aqui está uma sugestão profissional para o arquivo `README.md` que descreve a implementação e os resultados obtidos nos testes de desempenho do problema das N Rainhas:

---

# Projeto: Resolução do Problema das N Rainhas

Este projeto tem como objetivo implementar o problema das N Rainhas utilizando abordagens sequencial, paralela e distribuída. Além disso, analisamos o desempenho e a escalabilidade de cada abordagem, identificando possíveis gargalos e propondo melhorias.

## Implementações

1. **Sequencial**: Algoritmo que resolve o problema de forma recursiva e sequencial.
2. **Paralela**: Utiliza threads para tentar resolver o problema em paralelo, dividindo o processamento entre as rainhas.
3. **Distribuída**: Modelo cliente-servidor que divide o processamento entre diferentes máquinas para resolver o problema de forma distribuída.

## Configuração da Máquina

Os testes foram realizados em um ambiente com as seguintes especificações:

- **CPU**: Intel Core i7-9750H, 6 núcleos, 12 threads
- **RAM**: 16 GB DDR4
- **Sistema Operacional**: Ubuntu 20.04
- **Python**: 3.8

## Resultados de Desempenho

### Comparação dos Tempos de Execução

Os testes foram realizados para diferentes tamanhos de tabuleiro, variando de 4x4 a 28x28. Os tempos de execução (em segundos) para cada abordagem foram registrados abaixo:

| Tamanho do Tabuleiro | Sequencial (s) | Paralela (s) | Distribuída (s) |
| -------------------- | -------------- | ------------ | --------------- |
| 4x4                  | 0.0000         | 0.0906       | 1.0695          |
| 8x8                  | 0.0000         | 0.1079       | 1.0888          |
| 6x6                  | 0.0000         | 0.0742       | 1.0757          |
| 12x12                | 0.0130         | 0.1750       | 1.1903          |
| 10x10                | 0.0000         | 0.1665       | 1.1212          |
| 15x15                | 0.0142         | 0.3666       | 1.2002          |
| 14x14                | 0.0185         | 0.3738       | 1.2056          |
| 16x16                | 0.1548         | 1.7609       | 1.2926          |
| 18x18                | 0.4852         | 9.0733       | 1.9557          |
| 20x20                | 3.0637         | 59.5355      | 4.3892          |
| 22x22                | 31.1891        | 682.4938     | 30.3401         |
| 24x24                | 8.4265         | 197.9349     | 9.3298          |
| 26x26                | 10.5234        | 238.2338     | 10.6505         |
| 28x28                | 74.9371        | 2093.8753    | 187.3009        |

## Análise de Escalabilidade e Eficiência

### Sequencial
A implementação sequencial, sendo a mais simples, mostrou-se eficiente para valores pequenos de N, com tempos de execução quase imediatos para tabuleiros menores (N <= 16). No entanto, a escalabilidade é um problema à medida que o tamanho do tabuleiro aumenta. O tempo de execução cresce exponencialmente, tornando-a impraticável para grandes valores de N.

### Paralela
A implementação paralela, apesar de prometer uma redução no tempo de execução, demonstrou resultados inesperados. Para tabuleiros menores, o overhead de criação e gerenciamento de threads compensou qualquer vantagem de paralelismo. A partir de N >= 16, os tempos de execução aumentam significativamente, indicando gargalos nas operações de sincronização entre threads e limitações de escalabilidade da solução atual.

**Melhoria Proposta**: Implementar uma estratégia de balanceamento de carga mais eficiente, evitando o desperdício de recursos com threads ociosas. Além disso, a utilização de uma biblioteca de paralelismo mais robusta, como `multiprocessing`, pode mitigar os gargalos de performance.

### Distribuída
A solução distribuída apresentou tempos mais consistentes para tabuleiros grandes, superando a implementação paralela para valores de N elevados. No entanto, ainda há um aumento no tempo de execução à medida que o tamanho do tabuleiro cresce. O modelo cliente-servidor atual também sofre com latência na comunicação e gerenciamento de conexões.

**Melhoria Proposta**: Adotar uma arquitetura distribuída com mais nós de processamento e um mecanismo de balanceamento de carga dinâmico pode melhorar a escalabilidade. Utilizar bibliotecas específicas para computação distribuída, como `Dask` ou `Ray`, também pode otimizar a comunicação entre nós e reduzir a latência.

## Desafios Encontrados

1. **Gerenciamento de Threads**: A implementação paralela apresentou problemas de desempenho em cenários onde a criação e gerenciamento de múltiplas threads resultou em overhead significativo.
2. **Backtracking e Overhead**: O backtracking nas soluções maiores resultou em overhead substancial, principalmente na solução distribuída.
3. **Limitações de Comunicação**: A implementação distribuída sofreu com latência nas conexões entre cliente e servidor, afetando o desempenho em grandes tabuleiros.

## Conclusão

Apesar das dificuldades encontradas, a solução distribuída se mostrou promissora em termos de escalabilidade para grandes valores de N. No entanto, as implementações paralelas precisam de otimizações para melhorar a eficiência em comparação à solução sequencial para tabuleiros maiores. Identificamos gargalos nas operações de sincronização e comunicação, e as melhorias propostas focam na adoção de ferramentas e técnicas mais eficientes para computação paralela e distribuída.

---


## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests para melhorias ou correções.

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.


```

---

