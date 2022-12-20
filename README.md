# Trabalho 1 (2022-2)
Trabalho 1 da disciplina de Fundamentos de Sistemas Embarcados (2022/2)

## Objetivo
Este trabalho tem por objetivo a criação de um sistema distribuído de automação predial para monitoramento e acionamento de sensores e dispositivos de um prédio com múltiplas salas. O sistema deve ser desenvolvido para funcionar em um conjunto de placas Raspberry Pi com um servidor central responsável pelo controle e interface com o usuário e servidores distribuídos para leitura e acionamento dos dispositivos. Dentre os dispositivos envolvidos estão o monitoramento de temperatura e umidade, sensores de presença, sensores de fumaça, sensores de contagem de pessoas, sensores de abertura e fechamento de portas e janelas, acionamento de lâmpadas, aparelhos de ar-condicionado, alarme e aspersores de água em caso de incêndio.

Veja mais detalhes clicando [aqui](https://gitlab.com/fse_fga/trabalhos-2022_2/trabalho-1-2022-2#trabalho-1-2022-2).

## Dependências
Este trabalho foi desenvolvido usando a linguagem [Python](https://www.python.org/downloads/) em sua versão 3.
- Bibliotecas auxiliares:
    - [RPI.GPIO](https://pypi.org/project/RPi.GPIO/): Responsável por permitir acesso a placa.
    - [Adafruit-DHT](https://pypi.org/project/Adafruit-DHT/): Responsável por acessar os sensores de temperatura. 

## Detalhes da implementação
- O projeto conta com a implementação de um servidor central e um distribuído que usam o protocolo de comunicação TCP/IP.
- O projeto conta com a implementação de Threads para recebimento e envio de mensagens entre servidores. 
- O projeto realiza o consumo das informações de configuração a partir de um arquivo json.
- O projeto tem as seguintes funcionalidades:
    - Visualizar estado dos dispositivos de saída (Lâmpadas, Projetores e Ar-condicionado)
    - Visualizar estado dos disposivitos de entrada (Sensores de presença, fumaça, porta, janela e contagem de pessoas )
    - Visualizar a temperatura e humidade atual a cada 2 segundos.
    - Acionar dispositivos de saída (Lâmpadas, Projetores e Ar-condicionado) individualmente. 
    - Acionar/Desativar todos os dispositivos de entrada (Lâmpadas, Projetores e Ar-condicionado).
    - Salvar comandos em arquivo CSV com dia e hora, alêm de disponibilizar a visualização deles no prompt de comando. 
    - Visualizar número de pessoas na sala escolhida. 
    - Acionamento do alarme por meio da ativação dos sensores de presença, porta ou janela. 
## Possíveis melhorias
- O servidor central está se conectando somente a um servidor distribuído (Conectando somente a uma sala por vez). 
- As rotinas de acionamento do alarme não estão sendo retornadas ao servidor central em tempo real, somente é exibida no distribuído (para visualizar no servidor central é necessário acionar o comando de ver o estado dos dispositivos. 

## Instruções/Como rodar 
- Acessar a placa
- Ter as dependências devidamente instaladas no ambiente de teste
- Acessar a pasta services
- Rodar o servidor central:
```bash
    python3 centralServer.py
```
- Selecionar a sala desejada selecionando digitando 1 ou 2
- Rodar o servidor ditribuido:
```bash
    python3 ditriServer.py
```
- Selecionar a sala desejada selecionando digitando 1 ou 2 (A mesma selecionada no servidor central)
- Digitar algum dos comando exibidos no menu.

## Screenshots 

## Vídeo de apresentação
