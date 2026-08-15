import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10


def plot_matriz_correlacao_grande(corr_df, caminho_saida='matriz_correlacao_tcc.png',
                                   largura_cm=16, renomear=None):
    if renomear:
        corr_df = corr_df.rename(index=renomear, columns=renomear)

    n = corr_df.shape[0]
    lado_pol = largura_cm / 2.54

    tam_fonte = max(5, 11 - 0.12 * n)

    fig, ax = plt.subplots(figsize=(lado_pol, lado_pol), dpi=300)

    sns.heatmap(
        corr_df,
        cmap='coolwarm',
        vmin=-1, vmax=1, center=0,
        square=True,
        linewidths=0.2,
        linecolor='white',
        cbar_kws={'shrink': 0.7, 'label': 'Coeficiente de correlação (r)'},
        xticklabels=True,
        yticklabels=True,
        ax=ax,
    )

    ax.tick_params(axis='both', labelsize=tam_fonte)
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)

    plt.tight_layout()
    plt.savefig(caminho_saida, dpi=600, bbox_inches='tight')
    plt.savefig(caminho_saida.rsplit('.', 1)[0] + '.pdf', bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    import pandas as pd

    rng = np.random.default_rng(0)
    colunas = [f'Var_{i:02d}' for i in range(30)]
    dados = pd.DataFrame(rng.normal(size=(500, 30)), columns=colunas)
    plot_matriz_correlacao_grande(dados.corr(), largura_cm=16)
