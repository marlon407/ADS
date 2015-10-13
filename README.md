# ADS
<h2>Simulação de Sistema com Dois Servidores</h2>
<h3>Prof. Eduardo da Silva</h3>
<h3>Análise e Desempenho de Sistemas – 2015/2</h3>
<h4>Descrição</h4>
<p>Desenvolva uma simulação usando Python com o módulo simPy para um
sistema com uma única fila e dois servidores.
Descrição do Sistema: Os clientes chegam ao sistema e entram em uma
fila para serem atendidos pelo servidor. A figura 1 permite visualizar o cenário do
sistema.</p>
<p>
Nesse sistema, os clientes chegam para serem servidos de acordo com uma
determinada frequência, denominada de Tempo Entre Chegadas (Tabela 1). Esse
intervalo de tempo entre a chegada de duas entidades subsequentes obedece a uma
distribuição de probabilidades empírica.
Quando um cliente toma um servidor (recurso), ele utiliza este recurso por
um período de tempo denominado de Tempo de Serviço (Tabela 2). Assim como o
Tempo Entre Chegadas, o período de tempo relacionado ao Serviço ou Processamento
também será aleatório descrito por distribuições empíricas de probabilidades.</p>

Tabela 1 – Tempo Entre Chegadas de Clientes ao Sistema
Classe (segundos) Probabilidade (%)<br>
0  – 5 35<br>
5  – 10 19<br>
10 – 15 19<br>
15 – 20 13<br>
20 – 25 3<br>
25 – 30 7<br>
30 – 35 1<br>
35 – 40 2<br>
40 – 45 1<br>

Tabela 2 – Tempo de Serviços dos Servidores 1 e 2
Classe (segundos) Servidor 1 (%) Servidor 2 (%)
9,5  – 10 6 5<br>
10   – 10,5 5 4<br>
10,5 – 11 23 15<br>
11   – 11,5 20 16<br>
11,5 – 12 21 23<br>
12   – 12,5 12 20<br>
12,5 – 13 9 10<br>
13   – 13,5 2 5<br>
13,5 – 14 1 2<br>
<p>
Se, ao chegar ao sistema um cliente encontrar os servidores ocupados, ele
deverá aderir a fila de espera. Porém, se os dois servidores estiverem livres, ele deve
admitir que ambos possuem a mesma capacidade de servir, e escolher aleatoriamente
(por sorteio) qual servidor utilizará.
Para medir o desempenho deste sistema, algumas variáveis de respostas devem
ser apresentadas:</p>
1. Número Médio de Clientes na Fila: Ao longo do período simulado, o
número de clientes presentes na fila dos servidores (uma variável de estado
aleatória) se altera, podendo assumir diversos valores discretos. Para obter uma
estatística do valor esperado desta variável é necessário um acompanhamento
(ao longo do período simulado) dos diversos valores assumidos e dos períodos de
tempo ao longo dos quais estes permaneceram constantes. Em outras palavras,
esta é uma variável dependente do tempo. Sua obtenção requer o cálculo de uma
média ponderada, cujos pesos percentuais do tempo total de observação (tempo
simulado) nos quais a variável “número de elementos na fila”, permaneceu em
determinado estado.
2. Taxa Média de Ocupação de cada Servidor: Assim como o Número Médio
de Clientes na Fila, esta também é uma estatística dependente do tempo. Porém,
como se conhece antecipadamente os possíveis estados dos servidores (neste
caso apenas dois: livre ou ocupado), a média ponderada necessária é mais
facilmente calculada.
3. Tempo Médio de um Cliente na Fila: Cada um dos clientes que aderem
a fila dos servidores permanece ali um determinado período de tempo. Este
período é também uma variável aleatória, uma vez que é dependente de TS. O
cálculo desta estatística é mais simples que o anterior, requerendo apenas que
se calcule uma média aritmética simples, considerando os tempos de todos os
clientes que por ali circularam.
4. Tempo Médio no Sistema: Esta estatística deverá ser coletada de forma
semelhante a anterior. O tempo despendido no sistema por um cliente é contado
desde o tempo em que este entra no sistema, até o momento em que, depois
de servido, deixa o sistema.
5. Contador de Clientes: Este é um elemento típico de qualquer programa de
simulação. Trata-se apenas de um simples acumulador. Neste caso, como o
nome pressupõe, deverá incrementar uma variável designada, sempre que for
ativado.
Seu programa deverá permitir que as estatísticas acima descritas sejam
coletadas para que se possa fazer uma análise do desempenho deste sistema sob
diferentes condições de funcionamento. O código deve conter instruções de uso.
