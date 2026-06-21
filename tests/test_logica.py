"test_arquivo_inexistente_retorna_lista_vazia  Arquivo"
"test_arquivo_invalido_retorna_lista_vazia  Validação"
"test_carrega_e_ordena_por_pontos  Ordenação"
"test_limita_a_cinco_entradas  Limite"
"test_adiciona_nova_pontuacao  Inserção"
"test_nome_convertido_para_maiusculo  Maiúsculas"
"test_nome_vazio_vira_anonimo  Anonimização"
"test_lista_mantém_ordem_decrescente  Classificação"
"test_maximo_cinco_entradas  Capacidade"
"test_entrada_baixa_nao_entra_com_lista_cheia  Filtragem"
"TestRect"
"test_colliderect_sobrepostos  Colisão"
"test_colliderect_sem_sobreposicao  Separação"
"test_colliderect_adjacentes_nao_colidem  Adjacência"
"test_propriedades_geometricas  Geometria"
"test_setter_bottom  Posicionamento"
"TestIniciarFase"
"test_fase_1  Fase"
"test_fase_2  Fase"
"test_fase_3  Fase"
"test_moedas_minimo_tres  Moedas"
"test_velocidade_mob_valida  Velocidade"
"test_espinhos_no_chao  Espinhos"
"test_fase_invalida_sem_erro  Robustez"
"TestColisoes"
"test_coleta_moeda  Coleta"
"test_sem_coleta_quando_longe  Distância"
"test_colisao_inimigo  Inimigo"
"test_sem_colisao_inimigo_longe  Segurança"
"test_colisao_espinho  Espinho"
"test_aterrissagem_plataforma  Plataforma"

import json
import os
import random
import tempfile
import unittest

MAX_LEADERBOARD = 5
MAX_NICKNAME    = 10
CHAO_Y          = 500

def carregar_leaderboard(caminho):
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
        dados.sort(key=lambda i: i["pontos"], reverse=True)
        return dados[:MAX_LEADERBOARD]
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return []
def salvar_leaderboard(caminho, lista):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=2)
def adicionar_pontuacao(lista, nome, pontos):
    nome = nome.strip().upper() if nome.strip() else "ANONIMO"
    nova = lista + [{"nome": nome, "pontos": pontos}]
    nova.sort(key=lambda i: i["pontos"], reverse=True)
    return nova[:MAX_LEADERBOARD]
class Rect:
    def __init__(self, x, y, w, h):
        self.x, self.y, self.width, self.height = x, y, w, h
    @property
    def right(self):  return self.x + self.width
    @property
    def bottom(self): return self.y + self.height
    @property
    def top(self):    return self.y
    @property
    def left(self):   return self.x
    @bottom.setter
    def bottom(self, v): self.y = v - self.height
    def colliderect(self, other):
        return (self.x < other.right  and self.right  > other.x and
                self.y < other.bottom and self.bottom > other.y)
def iniciar_fase(fase):
    moedas, mobs, vel_mobs, plataformas, espinhos = [], [], [], [], []
    layouts = {
        1: [(200,380,120,16),(500,340,120,16),(650,280,100,16)],
        2: [(150,400,100,16),(350,330,120,16),(560,270,100,16),(700,320,80,16)],
        3: [(120,410,80,16),(280,350,100,16),(450,290,100,16),(620,240,120,16)],
    }
    for px,py,pw,ph in layouts.get(fase,[]):
        plataformas.append(Rect(px,py,pw,ph))
    posicoes = list(range(170, 760, 80))
    random.shuffle(posicoes)
    for i in range(3):
        moedas.append(Rect(posicoes[i], CHAO_Y-28, 20, 20))
    for plat in plataformas[:2]:
        moedas.append(Rect(plat.x+plat.width//2-10, plat.y-28, 20, 20))
    espinho_xs = {1:[440], 2:[220,560], 3:[180,420,650]}
    for ex in espinho_xs.get(fase,[]):
        espinhos.append(Rect(ex, CHAO_Y-14, 40, 14))
    qtd = {1:1, 2:2, 3:2}.get(fase, 1)
    opcoes = list(range(300, 680, 80))
    random.shuffle(opcoes)
    for mx in opcoes[:qtd]:
        mobs.append(Rect(mx, CHAO_Y-40, 40, 40))
        vel_mobs.append(random.choice([-2, 2]))
    return moedas, mobs, vel_mobs, plataformas, espinhos
class TestLeaderboard(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        self.path = self.tmp.name
    def tearDown(self):
        os.unlink(self.path)
    def test_arquivo_inexistente_retorna_lista_vazia(self):
        resultado = carregar_leaderboard("arquivo_que_nao_existe.json")
        self.assertEqual(resultado, [])
    def test_arquivo_invalido_retorna_lista_vazia(self):
        with open(self.path, "w") as f:
            f.write("isso nao e json valido")
        self.assertEqual(carregar_leaderboard(self.path), [])
    def test_carrega_e_ordena_por_pontos(self):
        dados = [{"nome": "B", "pontos": 10}, {"nome": "A", "pontos": 50}]
        salvar_leaderboard(self.path, dados)
        resultado = carregar_leaderboard(self.path)
        self.assertEqual(resultado[0]["nome"], "A")
        self.assertEqual(resultado[1]["nome"], "B")
    def test_limita_a_cinco_entradas(self):
        dados = [{"nome": str(i), "pontos": i*10} for i in range(8)]
        salvar_leaderboard(self.path, dados)
        self.assertLessEqual(len(carregar_leaderboard(self.path)), MAX_LEADERBOARD)
    def test_adiciona_nova_pontuacao(self):
        lista = adicionar_pontuacao([], "mario", 100)
        self.assertEqual(len(lista), 1)
        self.assertEqual(lista[0]["nome"], "MARIO")
        self.assertEqual(lista[0]["pontos"], 100)
    def test_nome_convertido_para_maiusculo(self):
        lista = adicionar_pontuacao([], "joao", 50)
        self.assertEqual(lista[0]["nome"], "JOAO")
    def test_nome_vazio_vira_anonimo(self):
        lista = adicionar_pontuacao([], "   ", 30)
        self.assertEqual(lista[0]["nome"], "ANONIMO")
    def test_lista_mantém_ordem_decrescente(self):
        lista = []
        lista = adicionar_pontuacao(lista, "B", 20)
        lista = adicionar_pontuacao(lista, "A", 80)
        lista = adicionar_pontuacao(lista, "C", 50)
        pontos = [e["pontos"] for e in lista]
        self.assertEqual(pontos, sorted(pontos, reverse=True))
    def test_maximo_cinco_entradas(self):
        lista = []
        for i in range(8):
            lista = adicionar_pontuacao(lista, f"J{i}", i*10)
        self.assertLessEqual(len(lista), MAX_LEADERBOARD)
    def test_entrada_baixa_nao_entra_com_lista_cheia(self):
        lista = [{"nome": f"P{i}", "pontos": (i+1)*100} for i in range(5)]
        nova = adicionar_pontuacao(lista, "FRACO", 1)
        nomes = [e["nome"] for e in nova]
        self.assertNotIn("FRACO", nomes)
class TestRect(unittest.TestCase):
    def test_colliderect_sobrepostos(self):
        a = Rect(0, 0, 50, 50)
        b = Rect(25, 25, 50, 50)
        self.assertTrue(a.colliderect(b))
    def test_colliderect_sem_sobreposicao(self):
        a = Rect(0, 0, 50, 50)
        b = Rect(60, 0, 50, 50)
        self.assertFalse(a.colliderect(b))
    def test_colliderect_adjacentes_nao_colidem(self):
        a = Rect(0, 0, 50, 50)
        b = Rect(50, 0, 50, 50)
        self.assertFalse(a.colliderect(b))
    def test_propriedades_geometricas(self):
        r = Rect(10, 20, 30, 40)
        self.assertEqual(r.right,  40)
        self.assertEqual(r.bottom, 60)
        self.assertEqual(r.top,    20)
        self.assertEqual(r.left,   10)
    def test_setter_bottom(self):
        r = Rect(0, 0, 40, 40)
        r.bottom = 500
        self.assertEqual(r.y, 460)
class TestIniciarFase(unittest.TestCase):
    def _verificar_fase(self, fase, qtd_plat, qtd_espinhos, qtd_mobs):
        moedas, mobs, vel_mobs, plataformas, espinhos = iniciar_fase(fase)
        self.assertEqual(len(plataformas), qtd_plat,    f"fase {fase}: plataformas")
        self.assertEqual(len(espinhos),    qtd_espinhos, f"fase {fase}: espinhos")
        self.assertEqual(len(mobs),        qtd_mobs,     f"fase {fase}: mobs")
        self.assertEqual(len(vel_mobs),    qtd_mobs,     f"fase {fase}: vel_mobs")
    def test_fase_1(self):  self._verificar_fase(1, 3, 1, 1)
    def test_fase_2(self):  self._verificar_fase(2, 4, 2, 2)
    def test_fase_3(self):  self._verificar_fase(3, 4, 3, 2)
    def test_moedas_minimo_tres(self):
        for fase in (1, 2, 3):
            moedas, *_ = iniciar_fase(fase)
            self.assertGreaterEqual(len(moedas), 3, f"fase {fase}")
    def test_velocidade_mob_valida(self):
        for fase in (1, 2, 3):
            _, _, vel_mobs, *_ = iniciar_fase(fase)
            for v in vel_mobs:
                self.assertIn(v, (-2, 2))
    def test_espinhos_no_chao(self):
        for fase in (1, 2, 3):
            _, _, _, _, espinhos = iniciar_fase(fase)
            for e in espinhos:
                self.assertEqual(e.bottom, CHAO_Y, f"espinho fora do chão na fase {fase}")
    def test_fase_invalida_sem_erro(self):
        moedas, mobs, vel_mobs, plataformas, espinhos = iniciar_fase(99)
        self.assertEqual(plataformas, [])
class TestColisoes(unittest.TestCase):
    """Simula as verificações de colisão do loop principal."""
    def test_coleta_moeda(self):
        player = Rect(100, CHAO_Y-50, 50, 50)
        moedas = [Rect(110, CHAO_Y-40, 20, 20)] 
        coletadas = [m for m in moedas if player.colliderect(m)]
        self.assertEqual(len(coletadas), 1)
    def test_sem_coleta_quando_longe(self):
        player = Rect(100, CHAO_Y-50, 50, 50)
        moedas = [Rect(400, CHAO_Y-28, 20, 20)]
        coletadas = [m for m in moedas if player.colliderect(m)]
        self.assertEqual(len(coletadas), 0)
    def test_colisao_inimigo(self):
        player  = Rect(200, CHAO_Y-50, 50, 50)
        inimigo = Rect(210, CHAO_Y-40, 40, 40)
        self.assertTrue(player.colliderect(inimigo))
    def test_sem_colisao_inimigo_longe(self):
        player  = Rect(100, CHAO_Y-50, 50, 50)
        inimigo = Rect(500, CHAO_Y-40, 40, 40)
        self.assertFalse(player.colliderect(inimigo))
    def test_colisao_espinho(self):
        player  = Rect(440, CHAO_Y-50, 50, 50)
        espinho = Rect(440, CHAO_Y-14, 40, 14)
        self.assertTrue(player.colliderect(espinho))
    def test_aterrissagem_plataforma(self):
        """Player caindo sobre plataforma deve ter bottom fixado no topo dela."""
        plat   = Rect(200, 380, 120, 16)
        player = Rect(220, 325, 50, 50)   
        vel_y  = 8.0
        player.y += int(vel_y)          
        if (player.colliderect(plat) and vel_y >= 0
                and player.bottom - int(vel_y) <= plat.top + 10):
            player.bottom = plat.top
            vel_y = 0
        self.assertEqual(player.bottom, plat.top)
        self.assertEqual(vel_y, 0)
if __name__ == "__main__":
    unittest.main(verbosity=2)
