import pygame, random

pygame.init()
pygame.mixer.init()

LARG, ALT = 800, 350
TELA = pygame.display.set_mode((LARG, ALT))
pygame.display.set_caption("Ozzy vs morcego")

clock = pygame.time.Clock()
vel = 20
pontos = 0
vidas = 3
fonte = pygame.font.SysFont("arial", 20, True)

# CORES DO LABIRINTO
PRETO = (0,0,0)
AZUL = (0,155,150)

# MAPA DO LABIRINTO
# 0 = caminho / 1 = parede
mapa = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,0,1,0,1,1,0,1,0,1,1,1,0,0,1],
    [1,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],
    [1,1,1,0,1,1,0,1,0,1,0,1,0,1,1,0,1,1,1,1],
    [1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,0,1,0,1,0,1,0,1,1,1,1,0,0,1],
    [1,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

TAM = 40
linhas = len(mapa)
colunas = len(mapa[0])

# IMAGENS
player_img = pygame.image.load("./imagens/ozzy.png")
alvo_img = pygame.image.load("./imagens/morcego.png")
player_img = pygame.transform.scale(player_img, (60, 60))
alvo_img = pygame.transform.scale(alvo_img, (50, 50))

# POSIÇÕES
player_linha, player_coluna = 1, 1
livres = [(l,c) for l in range(linhas) for c in range(colunas) if mapa[l][c] == 0]
alvo_linha, alvo_coluna = random.choice(livres)

#  SOM
try:
    som_pegar = pygame.mixer.Sound("./sounds/ozzysom.mp3")
except:
    som_pegar = None

# LOOP
rodando = True
while rodando:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()
    nova_linha, nova_coluna = player_linha, player_coluna
    if teclas[pygame.K_LEFT]:  nova_coluna -= 1
    if teclas[pygame.K_RIGHT]: nova_coluna += 1
    if teclas[pygame.K_UP]:    nova_linha -= 1
    if teclas[pygame.K_DOWN]:  nova_linha += 1

    # Move só se for caminho
    if 0 <= nova_linha < linhas and 0 <= nova_coluna < colunas:
        if mapa[nova_linha][nova_coluna] == 0:
            player_linha, player_coluna = nova_linha, nova_coluna

    # Colisão com o morcego
    if (player_linha, player_coluna) == (alvo_linha, alvo_coluna):
        pontos += 1
        if som_pegar: som_pegar.play()
        alvo_linha, alvo_coluna = random.choice(livres)


    TELA.fill(PRETO)
    for l in range(linhas):
        for c in range(colunas):
            x, y = c * TAM, l * TAM
            if mapa[l][c] == 1:
                pygame.draw.rect(TELA, AZUL, (x, y, TAM, TAM))
    TELA.blit(alvo_img, (alvo_coluna*TAM, alvo_linha*TAM))
    TELA.blit(player_img, (player_coluna*TAM, player_linha*TAM))

    texto = fonte.render(f"Pontos: {pontos}", True, (255,255,255))
    TELA.blit(texto, (10, ALT-30))

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
print("Pontuação final:", pontos)
