# Nome do Jogo
Lizard Adventure 

Projeto final da disciplina de Introdução a Algoritmos/Programação, desenvolvido com Python e Pygame.

Este repositório é um template para os grupos da disciplina. A proposta é começar com uma base funcional e evoluir o jogo ao longo do semestre.

## Integrantes do grupo

- Nome do integrante 1: Daniel Ischaber Xavier
- Nome do integrante 2: William Augusto Lobo Freire
- Nome do integrante 3: Vinicius Daniel Santos
- Nome do integrante 4: 

## Estrutura do projeto

- `main.py`: ponto de entrada da aplicação.
- `src/`: código-fonte principal do jogo (loop, regras, sprites e dados).
- `assets/`: imagens, fontes e sons.
- `data/`: arquivos persistentes (recorde/ranking).
- `tests/`: testes unitários com `pytest`.
- `docs/`: documentação do projeto, incluindo proposta inicial.

## Descrição do jogo

>O Lizard Adventure é um jogo de plataforma 2D inspirado em clássicos do gênero. O jogador controla um pequeno lagarto que deve atravessar obstáculos, inimigos e desafios para alcançar seu objetivo final. Durante a jornada, será possível coletar itens espalhados pelo cenário para aumentar a sua pontuação. O jogo termina quando o jogador conclui todas as fases ou perde todas as suas vidas.

## Objetivo do jogador
> O objetivo do jogador é controlar o lagarto e atgravessar as três fases do jogo, evitando inimigos e obstáculos. Para vencer, o jogador deve chegar ao final da última fase sem perder todas as suas vidas


## Regras do jogo
-O jogador controla um lagarto que pode se mover e pular.
-O jogador deve chegar ao final de cada fase para avançar.
-Itens podem ser coletados para aumentar  a pontuação.
-Inimigos e armadilhas causam dano ao jogador quando há colisão.
-Ao perder todas as vidas, o jogo termina.
-O jogador vence ao completar as três fases.


## Controles
-A/Seta Esquerda: mover para a esquerda
-D/Seta Direita: mover para a direita
-Espaço/W: pular
-J: Usar poder
-ESC: pausar ou sair do jogo

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone LINK_DO_REPOSITORIO
cd NOME_DA_PASTA
pip install -r requirements.txt
python main.py
```

## Como executar os testes

```bash
python -m pytest
```

## Checklist mínimo para entrega

- Preencher este README com nome final, descrição real, regras e controles do jogo.
- Atualizar `docs/proposta.MD` com a proposta do grupo.
- Garantir que o jogo executa com `python main.py`.
- Garantir que os testes passam com `pytest`.

## Observações para os alunos

- Mantenham o código organizado em módulos pequenos e com responsabilidade clara.
- Comentem partes importantes da lógica, principalmente regras do jogo.
- Registrem decisões técnicas no README do grupo ao longo do desenvolvimento.
