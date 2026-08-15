"""
Gera a matriz de correlação em formato adequado para inclusão em
trabalho acadêmico (TCC) seguindo as normas ABNT para figuras:

- Fonte legível (Arial ou Times New Roman), tamanho mínimo 10pt no corpo.
- Alto contraste e boa resolução (300 dpi é o mínimo aceito; 600 dpi
  garante nitidez também em impressão).
- Valores numéricos anotados nas células, facilitando a leitura sem
  depender apenas da cor.
- Escala de cores fixa entre -1 e 1, centrada em 0, para que a intensidade
  da cor represente corretamente a força da correlação.
- Legenda ("Fonte: elaborado pelo autor") deve ser inserida no documento,
  logo abaixo da figura, e o título ("Figura X – Matriz de correlação")
  logo acima — a ABNT define a legenda como parte do corpo do texto, não
  da imagem. Por isso, aqui geramos apenas a imagem "limpa"; título e
  fonte devem ser digitados no Word/LaTeX, no padrão:
      Figura 1 – Matriz de correlação entre as variáveis do estudo
      [imagem]
      Fonte: elaborado pelo autor (2026).
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Fonte recomendada pela ABNT (Arial ou Times New Roman)
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10


def plot_matriz_correlacao_grande(corr_df, caminho_saida='matriz_correlacao_tcc.png',
                                   largura_cm=16, so_triangulo=True):
    """
    Versão para matrizes com muitas variáveis (20-40+), como dados de
    estação meteorológica com várias medidas por data/hora.

    Diferente da função `plot_matriz_correlacao`, aqui:
    - o tamanho da figura é definido em CENTÍMETROS (largura_cm), não em
      polegadas soltas — porque o que importa pra ficar legível numa folha
      A4 é o tamanho *impresso*, não a resolução em pixels. Uma figura de
      16x8 polegadas a 600 dpi tem ótima resolução, mas ao ser inserida
      numa página A4 (que tem ~16cm de largura útil) ela é escalada para
      baixo e o texto fica minúsculo do mesmo jeito;
    - `annot=True` é removido — com 30+ variáveis os números se sobrepõem
      e viram ruído visual; a cor + a barra de escala já comunicam a
      informação;
    - a matriz é mascarada para mostrar só o triângulo inferior
      (`so_triangulo=True`), já que corr(A,B) == corr(B,A) — isso libera
      quase o dobro de espaço por célula sem aumentar a figura;
    - a figura é quadrada, porque a matriz é quadrada — um figsize
      retangular (como 16x8) espreme as células na vertical.
    """
    n = corr_df.shape[0]
    lado_pol = largura_cm / 2.54  # cm -> polegadas

    mask = None
    if so_triangulo:
        mask = np.triu(np.ones_like(corr_df, dtype=bool), k=1)

    # tamanho de fonte decresce conforme o número de variáveis aumenta,
    # para o rótulo de cada célula continuar cabendo na largura definida
    tam_fonte = max(5, 11 - 0.12 * n)

    fig, ax = plt.subplots(figsize=(lado_pol, lado_pol), dpi=300)

    sns.heatmap(
        corr_df,
        mask=mask,
        cmap='coolwarm',
        vmin=-1, vmax=1, center=0,
        square=True,
        linewidths=0.2,
        linecolor='white',
        cbar_kws={'shrink': 0.7, 'label': 'Coeficiente de correlação (r)'},
        ax=ax,
    )

    ax.tick_params(axis='both', labelsize=tam_fonte)
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)

    plt.tight_layout()
    # PNG em alta resolução para Word
    plt.savefig(caminho_saida, dpi=600, bbox_inches='tight')
    # versão vetorial (PDF) — não pixeliza em nenhum tamanho de impressão,
    # ideal se o TCC for compilado em LaTeX
    plt.savefig(caminho_saida.rsplit('.', 1)[0] + '.pdf', bbox_inches='tight')
    plt.show()


def plot_matriz_correlacao(corr_df, caminho_saida='matriz_correlacao_tcc.png'):
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)

    sns.heatmap(
        corr_df,
        cmap='coolwarm',
        vmin=-1, vmax=1, center=0,
        square=True,
        linewidths=0.4,
        linecolor='white',
        annot=True, fmt='.2f',
        annot_kws={'size': 8},
        cbar_kws={'shrink': 0.8, 'label': 'Coeficiente de correlação'},
        ax=ax,
    )

    ax.tick_params(axis='both', labelsize=9)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)

    plt.tight_layout()
    plt.savefig(caminho_saida, dpi=600, bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    import pandas as pd

    # Exemplo com poucas variáveis -> usa a versão anotada.
    rng = np.random.default_rng(0)
    dados_pequenos = pd.DataFrame(rng.normal(size=(100, 6)), columns=list('ABCDEF'))
    plot_matriz_correlacao(dados_pequenos.corr())

    # Exemplo com muitas variáveis (caso de dados meteorológicos com várias
    # medidas, tipo o dataset do TCC) -> usa a versão para matriz grande.
    colunas = [f'Var_{i:02d}' for i in range(30)]
    dados_grandes = pd.DataFrame(rng.normal(size=(500, 30)), columns=colunas)
    plot_matriz_correlacao_grande(dados_grandes.corr(), largura_cm=16)
