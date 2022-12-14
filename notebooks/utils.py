import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def plot_phq9_correlation(df, columns, ignore_blank_phq9_rows=True, decimal_cases=2):
    segmented_df = df[columns + ['PHQ9']]
    if ignore_blank_phq9_rows:
        segmented_df = segmented_df[segmented_df.PHQ9.notna()]
        
    sns.heatmap(
        segmented_df.corr(),
        annot=True,
        fmt=f'.{decimal_cases}f',
        cmap='PuBu',
        mask=np.triu(np.ones_like(segmented_df.corr()))
    )


def get_higher_correlations(df, col='PHQ9', corr_threshold = 0.3):
    corr = df.corr().loc[col]
    return pd.concat([corr[corr > corr_threshold], corr[corr < corr_threshold * -1]])


def plot_for_cols(df, cols, func, y=None, figsize=(20, 12), max_plots_per_row=3, kwargs={}):
    """
    Plota as colunas `cols` do dataframe `df` usando a função de plot `func`.
    
    Uma forma mais genérica e flexível de:
    df[cols].hist(layout=(5, 3), figsize=(15,12))
    plt.suptitle('Cols Histograms')
    """
    
    n_cols = len(cols)
    plot_cols = max_plots_per_row
    plot_rows = math.ceil(n_cols / plot_cols)
    
    fig, ax = plt.subplots(plot_rows, plot_cols, figsize=figsize, squeeze=False)
    
    for i, col in enumerate(cols):
        plot_y = i % plot_cols
        plot_x = math.floor(i / plot_cols)
        kwargs["ax"] = ax[plot_x][plot_y]
        
        if y:
            func(data=df, x=col, y=y, **kwargs)
        else:
            func(data=df, x=col, **kwargs)


def column_descriptive_analysis(df, col, plot_kwargs={}):
    description = df[col].describe().reset_index().rename(
        columns = {'index':'describe'}
    )
    value_counts = df[col].value_counts(dropna=False).reset_index().rename(
        columns = {'index':'value counts'}
    )
    norm_value_counts = df[col].value_counts(dropna=False, normalize=True).reset_index().rename(
        columns = {'index':'value percents'}
    )
    
    analysis = pd.concat([description, value_counts, norm_value_counts], ignore_index=False, axis=1)
    analysis = analysis.rename(columns = {col: ''})
    
    plot = sns.histplot(data=df, x=df[col], **plot_kwargs)
    
    print(f'Coluna: {col}')
    plt.show()
    print(analysis.to_string(index=False))
    
    return analysis, plot


def validate_derived_category_columns(df, orig_col, cols):
    """
    Testa se a soma dos valores de colunas derivadas de uma categoria bate com os valores não nulos da coluna original
    """
    non_null = df[orig_col].notna().sum()
    
    cols_sum = 0
    for col in cols:
        cols_sum += df[df[col] == 1][col].sum()
        
    return non_null == cols_sum


def validate_score_columns(df, score_col, cols, decimals=5):
    calc_score = df[cols].sum(axis=1)
    
    # Devido às diferenças de ponto flutuante, é necessário arredondar as casas decimais mais distantes
    rounded_calc_score = np.round(calc_score, decimals=decimals)
    rounded_score_col = np.round(df[score_col], decimals=decimals)
    
    return rounded_score_col.equals(rounded_calc_score)
