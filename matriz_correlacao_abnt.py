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

import matplotlib.pyplot as plt
import seaborn as sns

# Fonte recomendada pela ABNT (Arial ou Times New Roman)
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10

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
    import numpy as np

    # Exemplo apenas para demonstrar o uso da função acima.
    rng = np.random.default_rng(0)
    dados = pd.DataFrame(rng.normal(size=(100, 6)), columns=list('ABCDEF'))
    plot_matriz_correlacao(dados.corr())
