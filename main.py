import pygame
import random
import math
import json

pygame.init()

LARGURA_TELA = 800
ALTURA_TELA  = 600
tela    = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
relogio = pygame.time.Clock()
pygame.display.set_caption("Aventura do Lagarto")

COR_CEU_TOP    = (20,  12,  28)
COR_CEU_BOT    = (50,  30,  80)
COR_CHAO       = (80,  50,  30)
COR_CHAO_TOP   = (60, 100,  30)
COR_LAGARTO    = (34, 180,  60)
COR_LAGARTO_DMG= (255, 80,  80)
COR_INIMIGO    = (180, 30,  30)
COR_INIMIGO_OLH= (255,200,   0)
COR_MOEDA      = (255,210,   0)
COR_MOEDA_BRI  = (255,240, 150)
COR_BRANCO     = (255,255, 255)
COR_AMARELO    = (255,220,  50)
COR_VERMELHO   = (220, 50,  50)
COR_VERDE      = (50, 200,  80)
COR_ROXO       = (100, 60, 160)
COR_ROXO_ESC   = (60,  30, 100)
COR_ESTRELA    = (255,240, 100)
COR_PLAT       = (100, 70, 180)
COR_PLAT_TOP   = (140,100, 220)
COR_ESPINHO    = (200, 50,  50)
COR_ESPINHO_PT = (255, 80,  80)

fonte_grande  = pygame.font.SysFont("Courier New", 48, bold=True)
fonte_media   = pygame.font.SysFont("Courier New", 32, bold=True)
fonte_pequena = pygame.font.SysFont("Courier New", 22, bold=True)
fonte_hud     = pygame.font.SysFont("Courier New", 24, bold=True)

MENU        = "menu"
NOME        = "nome"
JOGANDO     = "jogando"
PAUSADO     = "pausado"
GAME_OVER   = "game_over"
VITORIA     = "vitoria"
LEADERBOARD = "leaderboard"
CHAO_Y      = 500

ARQUIVO_LEADERBOARD = "leaderboard.json"
MAX_LEADERBOARD      = 5
MAX_NICKNAME          = 10

estrelas = [(random.randint(0,800), random.randint(0,400), random.randint(1,3)) for _ in range(60)]
particulas = []
def carregar_leaderboard():
    try:
        with open(ARQUIVO_LEADERBOARD, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        dados.sort(key=lambda item: item["pontos"], reverse=True)
        return dados[:MAX_LEADERBOARD]
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return []
def salvar_leaderboard(lista):
    try:
        with open(ARQUIVO_LEADERBOARD, "w", encoding="utf-8") as arquivo:
            json.dump(lista, arquivo, ensure_ascii=False, indent=2)
    except OSError:
        pass
def adicionar_pontuacao(lista, nome, pontos):
    nome = nome.strip().upper() if nome.strip() else "ANONIMO"
    nova_lista = lista + [{"nome": nome, "pontos": pontos}]
    nova_lista.sort(key=lambda item: item["pontos"], reverse=True)
    nova_lista = nova_lista[:MAX_LEADERBOARD]
    salvar_leaderboard(nova_lista)
    return nova_lista
def adicionar_particulas(x, y, cor, qtd=8):
    for _ in range(qtd):
        particulas.append({
            "x": x, "y": y,
            "vx": random.uniform(-3, 3),
            "vy": random.uniform(-4, -1),
            "vida": random.randint(20, 40),
            "cor": cor,
            "tam": random.randint(3, 7)
        })
def atualizar_particulas():
    for p in particulas[:]:
        p["x"] += p["vx"]; p["y"] += p["vy"]
        p["vy"] += 0.2;     p["vida"] -= 1
        if p["vida"] <= 0:
            particulas.remove(p)
def desenhar_particulas():
    for p in particulas:
        alpha = max(0, min(255, int(255 * p["vida"] / 40)))
        s = pygame.Surface((p["tam"], p["tam"]), pygame.SRCALPHA)
        s.fill((*p["cor"][:3], alpha))
        tela.blit(s, (int(p["x"]), int(p["y"])))
def desenhar_fundo(tick):
    for y in range(500):
        r = int(COR_CEU_TOP[0] + (COR_CEU_BOT[0]-COR_CEU_TOP[0]) * y/500)
        g = int(COR_CEU_TOP[1] + (COR_CEU_BOT[1]-COR_CEU_TOP[1]) * y/500)
        b = int(COR_CEU_TOP[2] + (COR_CEU_BOT[2]-COR_CEU_TOP[2]) * y/500)
        pygame.draw.line(tela, (r,g,b), (0,y), (800,y))
    for (sx,sy,st) in estrelas:
        brilho = int(180 + 70*math.sin(tick*0.05+sx))
        pygame.draw.rect(tela, (brilho,brilho,brilho), (sx,sy,st,st))
    pygame.draw.rect(tela, COR_CHAO,     (0, 500, 800, 100))
    pygame.draw.rect(tela, COR_CHAO_TOP, (0, 500, 800, 8))
def desenhar_fundo_estrelado(tick):
    """Fundo simples (so ceu com estrelas) usado nas telas de menu/nome/ranking."""
    tela.fill(COR_CEU_TOP)
    for (sx,sy,st) in estrelas:
        brilho = int(180+70*math.sin(tick*0.05+sx))
        pygame.draw.rect(tela,(brilho,brilho,brilho),(sx,sy,st,st))
_V=None; _C=(34,180,60); _E=(22,120,40); _O=(220,230,50); _P=(0,0,0); _B=(80,220,100)
LAGARTO_SPRITE=[
    [_V,_V,_V,_V,_V,_V,_V,_V,_C,_C,_C,_V,_V,_V,_V,_V],
    [_V,_V,_V,_V,_V,_V,_V,_C,_E,_C,_C,_C,_V,_V,_V,_V],
    [_C,_C,_V,_V,_V,_V,_C,_E,_C,_C,_C,_C,_C,_C,_V,_V],
    [_V,_C,_C,_V,_V,_C,_E,_C,_C,_C,_C,_C,_C,_C,_C,_V],
    [_V,_V,_C,_C,_C,_E,_C,_C,_B,_B,_C,_C,_C,_C,_O,_V],
    [_V,_V,_V,_C,_C,_C,_C,_B,_B,_B,_B,_C,_C,_C,_P,_V],
    [_V,_V,_V,_C,_C,_C,_C,_B,_B,_B,_B,_C,_C,_C,_C,_V],
    [_V,_V,_C,_C,_E,_C,_C,_C,_B,_B,_C,_C,_C,_C,_C,_V],
    [_V,_C,_C,_E,_C,_C,_C,_C,_C,_C,_C,_C,_C,_C,_V,_V],
    [_V,_C,_E,_C,_C,_C,_E,_C,_C,_C,_E,_C,_C,_V,_V,_V],
    [_C,_E,_C,_C,_C,_E,_C,_C,_C,_E,_C,_C,_V,_V,_V,_V],
    [_C,_C,_C,_C,_C,_C,_C,_C,_C,_C,_C,_V,_V,_V,_V,_V],
    [_V,_C,_C,_V,_C,_C,_V,_C,_C,_V,_V,_V,_V,_V,_V,_V],
    [_V,_C,_C,_V,_C,_C,_V,_C,_C,_V,_V,_V,_V,_V,_V,_V],
    [_C,_E,_V,_V,_C,_E,_V,_C,_E,_V,_V,_V,_V,_V,_V,_V],
    [_C,_C,_V,_V,_C,_C,_V,_C,_C,_V,_V,_V,_V,_V,_V,_V],
]
def _build_lagarto(cor_corpo, escala=3):
    s = pygame.Surface((16*escala, 16*escala), pygame.SRCALPHA)
    mapa = {_C: cor_corpo, _E: _E, _O: _O, _P: _P, _B: _B}
    for row, linha in enumerate(LAGARTO_SPRITE):
        for col, px in enumerate(linha):
            if px is _V: continue
            pygame.draw.rect(s, mapa.get(px, px), (col*escala, row*escala, escala, escala))
    return s
_spr_normal = _build_lagarto(_C)
_spr_dano   = _build_lagarto(COR_LAGARTO_DMG)
def desenhar_lagarto(rect, piscando):
    tela.blit(_spr_dano if piscando else _spr_normal, (rect.x-1, rect.y-1))
def desenhar_inimigo(rect):
    x,y,w,h = rect.x,rect.y,rect.width,rect.height
    pygame.draw.rect(tela, COR_INIMIGO,     (x+2,y+2,w-4,h-4))
    pygame.draw.rect(tela, COR_INIMIGO_OLH, (x+5,y+8,7,7))
    pygame.draw.rect(tela, COR_INIMIGO_OLH, (x+w-12,y+8,7,7))
    pygame.draw.rect(tela, (0,0,0),          (x+7,y+10,4,4))
    pygame.draw.rect(tela, (0,0,0),          (x+w-10,y+10,4,4))
    pygame.draw.rect(tela, (0,0,0),          (x+8,y+h-12,w-16,4))
def desenhar_moeda(rect, tick):
    cx,cy = rect.centerx, rect.centery
    raio = 10 + int(2*math.sin(tick*0.1+cx))
    pygame.draw.circle(tela, COR_MOEDA,    (cx,cy), raio)
    pygame.draw.circle(tela, COR_MOEDA_BRI,(cx,cy), raio-4)
    pygame.draw.circle(tela, COR_MOEDA,    (cx,cy), raio-7)
def desenhar_plataforma(rect):
    pygame.draw.rect(tela, COR_PLAT,    rect)
    pygame.draw.rect(tela, COR_PLAT_TOP,(rect.x, rect.y, rect.width, 6))
    for bx in range(rect.x+8, rect.right-8, 20):
        pygame.draw.rect(tela, COR_ROXO_ESC, (bx, rect.y+8, 2, rect.height-12))
def desenhar_espinhos(lista):
    for e in lista:
        pygame.draw.rect(tela, COR_ESPINHO, (e.x, e.y+8, e.width, 6))
        for i in range(e.width // 10):
            px = e.x + i*10 + 5
            pygame.draw.polygon(tela, COR_ESPINHO_PT, [
                (px-5, e.y+8), (px+5, e.y+8), (px, e.y)
            ])
def desenhar_hud(vidas, pontos, fase, nome):
    hud = pygame.Surface((250,140), pygame.SRCALPHA)
    hud.fill((10,6,20,160))
    tela.blit(hud, (10,10))
    tela.blit(fonte_hud.render(f"{nome[:10]}", True, COR_VERDE), (20,18))
    tela.blit(fonte_hud.render(f"PONTOS: {pontos:04d}", True, COR_AMARELO), (20,48))
    tela.blit(fonte_hud.render(f"FASE:   {fase}/3",     True, COR_BRANCO),  (20,78))
    for i in range(3):
        cor = COR_VERMELHO if i < vidas else (60,30,50)
        hx,hy = 20+i*30, 110
        pygame.draw.rect(tela,cor,(hx+4,hy,10,8))
        pygame.draw.rect(tela,cor,(hx,hy+2,8,6))
        pygame.draw.rect(tela,cor,(hx+10,hy+2,8,6))
        pygame.draw.rect(tela,cor,(hx+2,hy+8,14,6))
        pygame.draw.rect(tela,cor,(hx+5,hy+13,8,4))
def desenhar_menu(tick):
    desenhar_fundo_estrelado(tick)
    for txt,cor,y in [("AVENTURA DO",COR_AMARELO,100),("LAGARTO",COR_VERDE,150)]:
        s = fonte_grande.render(txt, True, COR_ROXO_ESC)
        tela.blit(s,(LARGURA_TELA//2-s.get_width()//2+3, y+3))
        s = fonte_grande.render(txt, True, cor)
        tela.blit(s,(LARGURA_TELA//2-s.get_width()//2, y))
    desenhar_lagarto(pygame.Rect(LARGURA_TELA//2-25, 230, 50,50), False)
    pulso = int(4*math.sin(tick*0.08))
    bw,bh = 260+pulso, 60+pulso//2
    bx,by = LARGURA_TELA//2-bw//2, 320
    pygame.draw.rect(tela, COR_ROXO,   (bx,by,bw,bh), border_radius=4)
    pygame.draw.rect(tela, COR_AMARELO,(bx,by,bw,bh), 3, border_radius=4)
    tb = fonte_media.render("[ JOGAR ]", True, COR_BRANCO)
    tela.blit(tb,(LARGURA_TELA//2-tb.get_width()//2, by+12))
    for i,txt in enumerate(["MOVER:  A/D ou SETAS","PULAR:  W/ESPACO/CIMA",
                             "PAUSE:  ESC","RANKING:  L"]):
        s = fonte_pequena.render(txt, True, (160,140,200))
        tela.blit(s,(LARGURA_TELA//2-s.get_width()//2, 410+i*26))
def desenhar_tela_nome(tick, nome):
    desenhar_fundo_estrelado(tick)
    s = fonte_media.render("QUAL E O SEU NOME?", True, COR_AMARELO)
    tela.blit(s, (LARGURA_TELA//2 - s.get_width()//2, 150))
    desenhar_lagarto(pygame.Rect(LARGURA_TELA//2-25, 200, 50, 50), False)
    bw, bh = 320, 60
    bx, by = LARGURA_TELA//2 - bw//2, 290
    pygame.draw.rect(tela, COR_ROXO_ESC, (bx,by,bw,bh), border_radius=4)
    pygame.draw.rect(tela, COR_AMARELO,  (bx,by,bw,bh), 3, border_radius=4)
    cursor = "_" if (tick//30) % 2 == 0 else " "
    texto_nome = fonte_media.render(nome + cursor, True, COR_BRANCO)
    tela.blit(texto_nome, (LARGURA_TELA//2 - texto_nome.get_width()//2, by+14))
    s = fonte_pequena.render("DIGITE E PRESSIONE ENTER", True, (160,140,200))
    tela.blit(s, (LARGURA_TELA//2 - s.get_width()//2, 390))
    s = fonte_pequena.render("ESC  PARA VOLTAR AO MENU", True, (160,140,200))
    tela.blit(s, (LARGURA_TELA//2 - s.get_width()//2, 420))
def desenhar_leaderboard(tick, lista):
    desenhar_fundo_estrelado(tick)
    s = fonte_grande.render("RANKING", True, COR_VERDE)
    tela.blit(s, (LARGURA_TELA//2 - s.get_width()//2, 60))
    if not lista:
        s = fonte_media.render("NENHUMA PONTUACAO AINDA", True, COR_BRANCO)
        tela.blit(s, (LARGURA_TELA//2 - s.get_width()//2, 260))
    else:
        topo_y = 160
        cores_pos = [COR_AMARELO, (200,200,210), (180,120,60)]
        for i, item in enumerate(lista):
            cor = cores_pos[i] if i < 3 else COR_BRANCO
            linha = f"{i+1}. {item['nome']:<10} {item['pontos']:04d}"
            s = fonte_media.render(linha, True, cor)
            tela.blit(s, (LARGURA_TELA//2 - s.get_width()//2, topo_y + i*50))
    s = fonte_pequena.render("PRESSIONE QUALQUER TECLA PARA VOLTAR", True, (160,140,200))
    tela.blit(s, (LARGURA_TELA//2 - s.get_width()//2, 530))
def desenhar_pausa():
    ov = pygame.Surface((LARGURA_TELA,ALTURA_TELA), pygame.SRCALPHA)
    ov.fill((10,6,20,180)); tela.blit(ov,(0,0))
    s = fonte_grande.render("PAUSADO",True,COR_AMARELO)
    tela.blit(s,(LARGURA_TELA//2-s.get_width()//2,200))
    s = fonte_media.render("ESC  para continuar",True,COR_BRANCO)
    tela.blit(s,(LARGURA_TELA//2-s.get_width()//2,300))
    s = fonte_pequena.render("ENTER  para voltar ao menu",True,(160,140,200))
    tela.blit(s,(LARGURA_TELA//2-s.get_width()//2,360))
def desenhar_game_over(pontos, tick, leaderboard):
    ov = pygame.Surface((LARGURA_TELA,ALTURA_TELA), pygame.SRCALPHA)
    ov.fill((60,0,0,200)); tela.blit(ov,(0,0))
    s = fonte_grande.render("GAME OVER",True,COR_VERMELHO)
    tela.blit(s,(LARGURA_TELA//2-s.get_width()//2,90))
    s = fonte_media.render(f"PONTUACAO FINAL: {pontos:04d}",True,COR_AMARELO)
    tela.blit(s,(LARGURA_TELA//2-s.get_width()//2,180))
    s = fonte_pequena.render("TOP PONTUACOES", True, COR_VERDE)
    tela.blit(s, (LARGURA_TELA//2 - s.get_width()//2, 240))
    for i, item in enumerate(leaderboard[:3]):
        linha = f"{i+1}. {item['nome']:<10} {item['pontos']:04d}"
        s = fonte_pequena.render(linha, True, COR_BRANCO)
        tela.blit(s, (LARGURA_TELA//2 - s.get_width()//2, 268 + i*26))
    pulso = int(3*math.sin(tick*0.08))
    s = fonte_media.render("ESPACO  jogar de novo",True,COR_BRANCO)
    tela.blit(s,(LARGURA_TELA//2-s.get_width()//2,400+pulso))
    s = fonte_pequena.render("ENTER  para menu      L  ranking completo",True,(160,140,200))
    tela.blit(s,(LARGURA_TELA//2-s.get_width()//2,460))
def desenhar_vitoria(pontos, tick, leaderboard):
    ov = pygame.Surface((LARGURA_TELA,ALTURA_TELA), pygame.SRCALPHA)
    ov.fill((0,40,0,200)); tela.blit(ov,(0,0))
    for i in range(5):
        sx=100+i*150; sy=70+int(20*math.sin(tick*0.07+i))
        pygame.draw.polygon(tela,COR_ESTRELA,[
            (sx,sy-15),(sx+5,sy-5),(sx+15,sy-5),(sx+8,sy+3),(sx+10,sy+14),
            (sx,sy+8),(sx-10,sy+14),(sx-8,sy+3),(sx-15,sy-5),(sx-5,sy-5)])
    s = fonte_grande.render("VOCE GANHOU!",True,COR_VERDE)
    tela.blit(s,(LARGURA_TELA//2-s.get_width()//2,100))
    s = fonte_media.render(f"PONTUACAO: {pontos:04d}",True,COR_AMARELO)
    tela.blit(s,(LARGURA_TELA//2-s.get_width()//2,180))
    s = fonte_pequena.render("TOP PONTUACOES", True, COR_VERDE)
    tela.blit(s, (LARGURA_TELA//2 - s.get_width()//2, 240))
    for i, item in enumerate(leaderboard[:3]):
        linha = f"{i+1}. {item['nome']:<10} {item['pontos']:04d}"
        s = fonte_pequena.render(linha, True, COR_BRANCO)
        tela.blit(s, (LARGURA_TELA//2 - s.get_width()//2, 268 + i*26))
    pulso = int(3*math.sin(tick*0.08))
    s = fonte_media.render("ESPACO  jogar de novo",True,COR_BRANCO)
    tela.blit(s,(LARGURA_TELA//2-s.get_width()//2,400+pulso))
    s = fonte_pequena.render("ENTER  para menu      L  ranking completo",True,(160,140,200))
    tela.blit(s,(LARGURA_TELA//2-s.get_width()//2,460))
def iniciar_fase(fase):
    moedas, mobs, vel_mobs, plataformas, espinhos = [], [], [], [], []
    layouts = {
        1: [(200,380,120,16),(500,340,120,16),(650,280,100,16)],
        2: [(150,400,100,16),(350,330,120,16),(560,270,100,16),(700,320,80,16)],
        3: [(120,410,80,16),(280,350,100,16),(450,290,100,16),(620,240,120,16)],
    }
    for px,py,pw,ph in layouts.get(fase,[]):
        plataformas.append(pygame.Rect(px,py,pw,ph))
    posicoes_chao = list(range(170, 760, 80))
    random.shuffle(posicoes_chao)
    for i in range(3):
        moedas.append(pygame.Rect(posicoes_chao[i], CHAO_Y - 28, 20, 20))
    for plat in plataformas[:2]:
        moedas.append(pygame.Rect(plat.centerx - 10, plat.y - 28, 20, 20))
    espinho_xs = {1: [440], 2: [220, 560], 3: [180, 420, 650]}
    for ex in espinho_xs.get(fase, []):
        espinhos.append(pygame.Rect(ex, CHAO_Y - 14, 40, 14))
    qtd = {1: 1, 2: 2, 3: 2}.get(fase, 1)
    opcoes = list(range(300, 680, 80))
    random.shuffle(opcoes)
    for mx in opcoes[:qtd]:
        mobs.append(pygame.Rect(mx, CHAO_Y - 40, 40, 40))
        vel_mobs.append(random.choice([-2, 2]))
    return moedas, mobs, vel_mobs, plataformas, espinhos
def novo_jogo():
    largato = pygame.Rect(100, CHAO_Y-50, 50, 50)
    moedas, mobs, vel_mobs, plataformas, espinhos = iniciar_fase(1)
    return largato, 1, 3, 0, 0, False, True, 0, moedas, mobs, vel_mobs, plataformas, espinhos
estado = MENU
tick   = 0
(largato_player, fase, vidas, pontos, vel_y, no_chao,
 pode_tomar_dano, tempo_ultimo_dano,
 moedas, mobs, vel_mobs, plataformas, espinhos) = novo_jogo()
nickname_atual  = ""
pontuacao_salva = False
leaderboard     = carregar_leaderboard()
rodando = True
while rodando:
    relogio.tick(60)
    tick += 1
    tempo_jogo = pygame.time.get_ticks()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if estado == MENU:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    (largato_player, fase, vidas, pontos, vel_y, no_chao,
                     pode_tomar_dano, tempo_ultimo_dano,
                     moedas, mobs, vel_mobs, plataformas, espinhos) = novo_jogo()
                    pontuacao_salva = False
                    estado = NOME
                elif evento.key == pygame.K_l:
                    estado = LEADERBOARD
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(LARGURA_TELA//2-130,320,260,60).collidepoint(pygame.mouse.get_pos()):
                    (largato_player, fase, vidas, pontos, vel_y, no_chao,
                     pode_tomar_dano, tempo_ultimo_dano,
                     moedas, mobs, vel_mobs, plataformas, espinhos) = novo_jogo()
                    pontuacao_salva = False
                    estado = NOME
        elif estado == NOME:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if nickname_atual.strip() != "":
                        estado = JOGANDO
                elif evento.key == pygame.K_BACKSPACE:
                    nickname_atual = nickname_atual[:-1]
                elif evento.key == pygame.K_ESCAPE:
                    estado = MENU
                elif evento.unicode.isalnum() and len(nickname_atual) < MAX_NICKNAME:
                    nickname_atual += evento.unicode.upper()
        elif estado == LEADERBOARD:
            if evento.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                estado = MENU
        elif estado == JOGANDO:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                estado = PAUSADO
        elif estado == PAUSADO:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE: estado = JOGANDO
                if evento.key == pygame.K_RETURN: estado = MENU
        elif estado in (GAME_OVER, VITORIA):
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    estado = MENU
                elif evento.key == pygame.K_l:
                    estado = LEADERBOARD
                else:
                    (largato_player, fase, vidas, pontos, vel_y, no_chao,
                     pode_tomar_dano, tempo_ultimo_dano,
                     moedas, mobs, vel_mobs, plataformas, espinhos) = novo_jogo()
                    pontuacao_salva = False
                    estado = JOGANDO
    if estado == JOGANDO:
        if not pode_tomar_dano and (tempo_jogo - tempo_ultimo_dano > 1200):
            pode_tomar_dano = True
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]  or teclas[pygame.K_a]: largato_player.x -= 6
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]: largato_player.x += 6
        largato_player.x = max(0, min(largato_player.x, LARGURA_TELA - largato_player.width))
        if (teclas[pygame.K_SPACE] or teclas[pygame.K_w] or teclas[pygame.K_UP]) and no_chao:
            vel_y = -15
            no_chao = False
        vel_y += 0.8
        largato_player.y += int(vel_y)
        no_chao = False
        for plat in plataformas:
            if (largato_player.colliderect(plat) and vel_y >= 0
                    and largato_player.bottom - int(vel_y) <= plat.top + 10):
                largato_player.bottom = plat.top
                vel_y = 0
                no_chao = True
        if largato_player.bottom >= CHAO_Y:
            largato_player.bottom = CHAO_Y
            vel_y = 0
            no_chao = True
        for i in range(len(mobs)):
            mobs[i].x += vel_mobs[i]
            if mobs[i].left <= 150 or mobs[i].right >= 780:
                vel_mobs[i] *= -1
            mobs[i].bottom = CHAO_Y
        for moeda in moedas[:]:
            if largato_player.colliderect(moeda):
                moedas.remove(moeda)
                pontos += 10
                adicionar_particulas(moeda.centerx, moeda.centery, COR_MOEDA)
        if pode_tomar_dano:
            for inimigo in mobs:
                if largato_player.colliderect(inimigo):
                    vidas -= 1
                    largato_player.x = 100
                    pode_tomar_dano = False
                    tempo_ultimo_dano = tempo_jogo
                    adicionar_particulas(largato_player.centerx, largato_player.centery, COR_LAGARTO_DMG, 12)
                    break
        if pode_tomar_dano:
            for e in espinhos:
                if largato_player.colliderect(e):
                    vidas -= 1
                    largato_player.x = 100
                    pode_tomar_dano = False
                    tempo_ultimo_dano = tempo_jogo
                    adicionar_particulas(largato_player.centerx, largato_player.centery, COR_ESPINHO_PT, 12)
                    break
        if vidas <= 0:
            if not pontuacao_salva:
                leaderboard = adicionar_pontuacao(leaderboard, nickname_atual, pontos)
                pontuacao_salva = True
            estado = GAME_OVER
        if largato_player.right >= 790:
            fase += 1
            largato_player.x = 100
            if fase > 3:
                if not pontuacao_salva:
                    leaderboard = adicionar_pontuacao(leaderboard, nickname_atual, pontos)
                    pontuacao_salva = True
                estado = VITORIA
            else:
                moedas, mobs, vel_mobs, plataformas, espinhos = iniciar_fase(fase)
        atualizar_particulas()
    if estado == MENU:
        desenhar_menu(tick)
    elif estado == NOME:
        desenhar_tela_nome(tick, nickname_atual)
    elif estado == LEADERBOARD:
        desenhar_leaderboard(tick, leaderboard)
    elif estado in (JOGANDO, PAUSADO):
        desenhar_fundo(tick)
        for plat in plataformas:
            desenhar_plataforma(plat)
        desenhar_espinhos(espinhos)
        for moeda in moedas:
            desenhar_moeda(moeda, tick)
        for inimigo in mobs:
            desenhar_inimigo(inimigo)
        piscando = (not pode_tomar_dano) and ((tick//4)%2==1)
        desenhar_lagarto(largato_player, piscando)
        desenhar_particulas()
        desenhar_hud(vidas, pontos, fase, nickname_atual)
        if estado == PAUSADO:
            desenhar_pausa()
    elif estado == GAME_OVER:
        desenhar_fundo(tick)
        desenhar_game_over(pontos, tick, leaderboard)
    elif estado == VITORIA:
        desenhar_fundo(tick)
        desenhar_vitoria(pontos, tick, leaderboard)
    pygame.display.flip()
pygame.quit()
