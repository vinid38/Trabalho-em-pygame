import pygame
import random
pygame.init()
LARGURA_TELA = 800
ALTURA_TELA = 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Aventura do Lagarto")
fonte_texto = pygame.font.SysFont("Arial", 28, bold=True)
relogio = pygame.time.Clock()
largato_player = pygame.Rect(100, 450, 50, 50)
vel_y = 0
no_chao = False
vidas = 3
pontos = 0
fase = 1
pode_tomar_dano = True
tempo_ultimo_dano = 0
moedas = []
mobs = []
velocidades_mobs = []
def iniciar_fase(fase):
    global moedas, mobs, velocidades_mobs
    moedas.clear()
    mobs.clear()
    velocidades_mobs.clear()
    for _ in range(5):
        nova_moeda = pygame.Rect(
            random.randint(150, 750),
            random.randint(200, 420),
            20,
            20
        )
        moedas.append(nova_moeda)
    for _ in range(fase):
        novo_inimigo = pygame.Rect(
            random.randint(300, 700),
            460,
            40,
            40
        )
        mobs.append(novo_inimigo)
        velocidades_mobs.append(
            random.choice([-3, -2, 2, 3])
        )
iniciar_fase(fase)
jogando = True
while jogando:
    relogio.tick(60)
    tempo_jogo = pygame.time.get_ticks()
    if not pode_tomar_dano and (tempo_jogo - tempo_ultimo_dano > 1000):
        pode_tomar_dano = True
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogando = False
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        largato_player.x -= 6
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        largato_player.x += 6
    if largato_player.x < 0:
        largato_player.x = 0
    if (teclas[pygame.K_SPACE] or teclas[pygame.K_w] or teclas[pygame.K_UP]) and no_chao:
        vel_y = -15
        no_chao = False
    vel_y += 0.8
    largato_player.y += vel_y
    if largato_player.bottom >= 500:
        largato_player.bottom = 500
        vel_y = 0
        no_chao = True
    for i in range(len(mobs)):
        mobs[i].x += velocidades_mobs[i]
        if mobs[i].left <= 150 or mobs[i].right >= 780:
            velocidades_mobs[i] *= -1
    for moeda in moedas[:]:
        if largato_player.colliderect(moeda):
            moedas.remove(moeda)
            pontos += 10
    if pode_tomar_dano:
        for inimigo in mobs:
            if largato_player.colliderect(inimigo):
                vidas -= 1
                largato_player.x = 100
                pode_tomar_dano = False
                tempo_ultimo_dano = tempo_jogo
                break
    if vidas <= 0:
        print("Fim de Jogo! Você perdeu.")
        jogando = False
    if largato_player.right >= 790:
        fase += 1
        largato_player.x = 100
        if fase > 3:
            print("Parabéns! Você completou o jogo.")
            jogando = False
        else:
            iniciar_fase(fase)
    tela.fill((135, 206, 235))
    pygame.draw.rect(tela, (139, 69, 19), (0, 500, 800, 100))
    if pode_tomar_dano or (tempo_jogo // 150) % 2 == 0:
        pygame.draw.rect(tela, (34, 139, 34), largato_player)
    else:
        pygame.draw.rect(tela, (255, 100, 100), largato_player)
    for moeda in moedas:
        pygame.draw.circle(tela, (255, 215, 0), moeda.center, 10)
    for inimigo in mobs:
        pygame.draw.rect(tela, (178, 34, 34), inimigo)
    txt_pontos = fonte_texto.render(
        f"Pontos: {pontos}",
        True,
        (255, 255, 255)
    )
    txt_vidas = fonte_texto.render(
        f"Vidas: {vidas}",
        True,
        (255, 255, 255)
    )
    txt_fase = fonte_texto.render(
        f"Fase: {fase}/3",
        True,
        (255, 255, 255)
    )
    tela.blit(txt_pontos, (20, 20))
    tela.blit(txt_vidas, (20, 60))
    tela.blit(txt_fase, (20, 100))
    pygame.display.flip()
pygame.quit()
