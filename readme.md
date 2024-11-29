## Integrantes: João Vitor Martelli, Eduardo Ranzan, Marcelo Savitisk


# Documentação do Projeto IoT: Gerenciador de Lixeira Inteligente
### Este projeto implementa um sistema IoT para gerenciar a ocupação de uma lixeira com feedback visual (LEDs) e comunicação com a API ThingSpeak.

## Arquivos Principais
1. **app.py**

**Descrição**
- Backend em Flask para controlar o hardware e enviar dados para a API.
- Controla os LEDs e monitora a distância utilizando sensores ultrassônicos.
- Oferece rotas para interação com a interface web e controle da lixeira.

#### Funcionalidades
- Monitoramento da Lixeira:
    - Calcula a ocupação da lixeira com base na distância medida pelo sensor ultrassônico.
    - Feedback visual com LEDs para indicar se a lixeira está cheia ou vazia.

- Envio de Dados para ThingSpeak:
- Atualiza a API com o status da tampa e a ocupação da lixeira.
- Rotas Flask:
    - `/`: Exibe o status atual da lixeira.
    - `/lixeira/<action>`: Permite abrir ou fechar a tampa da lixeira e aciona os LEDs.
- Principais Funções
    - `distancia()`: Mede a distância utilizando o sensor ultrassônico.
    - `isEmpty(distancia)`: Determina se a lixeira está vazia.
    - `ocupacaoLixeira()`: Calcula a porcentagem de ocupação.
    - `enviarStatusLixeira(statusLixeira, ocupacao)`: Envia o status para a API.

## Como Executar

- Configure o hardware conforme descrito.
- Execute o Flask App:
```
python app.py
```
- Acesse o sistema no navegador em http://127.0.0.1:8080.
- Interaja com a interface para monitorar e controlar a lixeira.
