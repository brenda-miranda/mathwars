import pygame
import random
from sys import exit

# Inicialização do Pygame
pygame.init()

# Dimensões da tela
largura_tela = 800
altura_tela = 600

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)

# Criação da tela
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Meu Jogo")

# Variáveis do jogo
game_over = False
pontuacao = 0
nivel_dificuldade = 1
fase_atual = 1
tempo_restante = 15

# Função para exibir texto na tela
def exibir_texto(texto, tamanho, cor, x, y):
    fonte = pygame.font.SysFont(None, tamanho)
    texto = fonte.render(texto, True, cor)
    tela.blit(texto, (x, y))

def gerar_opcoes_resposta(resposta_correta):
    opcoes = [resposta_correta]

    while len(opcoes) < 4:
        opcao = random.randint(1, 20)
        if opcao != resposta_correta and opcao not in opcoes:
            opcoes.append(opcao)

    random.shuffle(opcoes)
    return opcoes

def verificar_resposta(posicao_mouse, opcoes_resposta):
    x = largura_tela // 2 - 100
    y = altura_tela // 2

    # Verifica se o clique foi em uma das opções de resposta
    for i in range(2):
        retangulo_opcao1 = pygame.Rect(x, y + i * 70, 200, 50)
        retangulo_opcao2 = pygame.Rect(x + 250, y + i * 70, 200, 50)

        if retangulo_opcao1.collidepoint(posicao_mouse):
            return opcoes_resposta[i]
        elif retangulo_opcao2.collidepoint(posicao_mouse):
            return opcoes_resposta[i + 2]

    return None

# Função para exibir a tela de início
def tela_inicio():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Obtenha a posição do clique do mouse
                mouse_pos = pygame.mouse.get_pos()

                # Verifique se o clique está no botão de instrução
                if botao_instrucoes.collidepoint(mouse_pos):
                    # Ação do clique no botão de instrução
                    tela_instrucoes()
                elif botao_iniciar.collidepoint(mouse_pos):
                    tela_jogo()

        tela.fill(preto)
        exibir_texto("Math Wars", 50, branco, largura_tela // 2 - 100, altura_tela // 2 - 50)

        # Criação do botão Iniciar Jogo
        botao_iniciar = pygame.draw.rect(tela, branco, (largura_tela // 2 - 75, altura_tela // 2 + 50, 150, 50))
        exibir_texto("Iniciar Jogo", 30, preto, largura_tela // 2 - 60, altura_tela // 2 + 60)

        # Criação do botão de instruções
        botao_instrucoes = pygame.draw.rect(tela, branco, (largura_tela // 2 - 75, altura_tela // 2 + 120, 150, 50))
        exibir_texto("Instruções", 30, preto, largura_tela // 2 - 55, altura_tela // 2 + 130)

        pygame.display.update()


# Função para exibir a tela de jogo
def tela_jogo():
    global game_over, pontuacao, nivel_dificuldade, fase_atual, tempo_restante

    # Geração da expressão matemática aleatória
    operador = random.choice(['+', '-', '*', '/'])
    numero1 = random.randint(1, 10)
    numero2 = random.randint(1, 10)

    expressao = f"{numero1} {operador} {numero2} = ?"
    resposta_correta = eval(f"{numero1} {operador} {numero2}")

    # Geração de opções de resposta
    opcoes_resposta = gerar_opcoes_resposta(resposta_correta)

    # Tempo restante para responder
    tempo_total = 10
    tempo_inicial = pygame.time.get_ticks()  # Tempo inicial em milissegundos
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Verifica o clique do mouse
                resposta_selecionada = verificar_resposta(pygame.mouse.get_pos(), opcoes_resposta)
                if resposta_selecionada == resposta_correta:  # Verifica se a resposta selecionada está correta
                    pontuacao += 1
                    nivel_dificuldade += 1
                    # Geração de uma nova expressão matemática
                    operador = random.choice(['+', '-', '*', '/'])
                    numero1 = random.randint(1, 10)
                    numero2 = random.randint(1, 10)

                    expressao = f"{numero1} {operador} {numero2} = ?"
                    resposta_correta = eval(f"{numero1} {operador} {numero2}")
                    opcoes_resposta = gerar_opcoes_resposta(resposta_correta)
                    tempo_total += 10  # Tempo em segundos para responder
                else:
                    game_over = True

        tela.fill(preto)

        exibir_texto(expressao, 50, branco, largura_tela // 2 - 100, altura_tela // 2 - 50)

        # Verifica se o tempo de resposta acabou
        tempo_atual = pygame.time.get_ticks()  # Tempo atual em milissegundos
        tempo_decorrido = (tempo_atual - tempo_inicial) // 1000  # Tempo decorrido em segundos
        tempo_restante = max(tempo_total - tempo_decorrido, 0)  # Tempo restante atualizado

        exibir_texto(f"Tempo: {tempo_restante}", 24, branco, largura_tela - 150, 10)

        if tempo_restante <= 0:
            game_over = True

        # Exibição das opções de resposta em duas linhas
        x = largura_tela // 2 - 100
        y = altura_tela // 2
        for i in range(2):
            pygame.draw.rect(tela, preto, (x, y + i * 70, 200, 50))
            exibir_texto(str(opcoes_resposta[i]), 24, branco, x + 10, y + 10 + i * 70)
            pygame.draw.rect(tela, preto, (x + 250, y + i * 70, 200, 50))
            exibir_texto(str(opcoes_resposta[i + 2]), 24, branco, x + 260, y + 10 + i * 70)

        # Atualiza a tela
        pygame.display.update()

    tela_final()


# Função para exibir a tela de finalização do jogo
def tela_final():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Obtenha a posição do clique do mouse
                mouse_pos = pygame.mouse.get_pos()

                if botao_replay.collidepoint(mouse_pos):
                    tela_jogo()
                elif botao_tela_inicial.collidepoint(mouse_pos):
                    tela_inicio()


        tela.fill(preto)
        exibir_texto("Fim de Jogo", 50, branco, largura_tela // 2 - 100, altura_tela // 2 - 50)

        # Criação do botão de jogar novamente
        botao_replay = pygame.draw.rect(tela, branco, (largura_tela // 2 - 130, altura_tela // 2 + 45, 250, 50))
        exibir_texto("Jogar Novamente", 30, preto, largura_tela // 2 - 80, altura_tela // 2 + 60)

        # Criação do botão de tela inicial
        botao_tela_inicial = pygame.draw.rect(tela, branco, (largura_tela // 2 - 85, altura_tela // 2 + 115, 150, 50))
        exibir_texto("Tela Inicial", 30, preto, largura_tela // 2 - 70, altura_tela // 2 + 130)

        pygame.display.update()

# Função para exibir a tela de instruções
def tela_instrucoes():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Verifica o clique do mouse

                # Obtenha a posição do clique do mouse
                mouse_pos = pygame.mouse.get_pos()

                if botao_voltar.collidepoint(mouse_pos):
                    tela_inicio()

        tela.fill(preto)
        exibir_texto("Instruções de Jogabilidade", 40, branco, largura_tela//2-200, altura_tela//2-150)

        # Exibe as instruções
        exibir_texto("Este jogo pode ser usado para melhorar as habilidades matemáticas dos jogadores,", 24, branco, largura_tela//2-300, altura_tela//2-50)
        exibir_texto("como adição, subtração, multiplicação e divisão.", 24, branco, largura_tela//2-180, altura_tela//2-20)
        exibir_texto("O jogo pode ser ambientado no espaço sideral, onde o jogador deve", 24, branco, largura_tela//2-250, altura_tela//2+20)
        exibir_texto("responder a perguntas matemáticas para destruir asteroides ou inimigos alienígenas.", 24, branco, largura_tela//2-310, altura_tela//2+50)
        exibir_texto("O jogador pode ganhar pontos por cada resposta correta e", 24, branco, largura_tela//2-230, altura_tela//2+90)
        exibir_texto("avançar de nível à medida que completam as perguntas corretamente.", 24, branco, largura_tela//2-280, altura_tela//2+120)

        # Criação do botão de voltar
        botao_voltar = pygame.draw.rect(tela, branco, (largura_tela // 2 - 75, altura_tela // 2 + 200, 150, 50))
        exibir_texto("Voltar", 30, preto, largura_tela // 2 - 35, altura_tela // 2 + 220)

        pygame.display.update()

# Loop principal do jogo
def jogo():
    tela_inicio()

# Execução do jogo
jogo()