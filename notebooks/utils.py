import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def get_columns_by_source(df):
    is_phq_column = lambda x: True if (x.find('DPQ') > -1) else False
    phq_cols = [col for col in df.columns if is_phq_column(col)]
    
    is_hei_column = lambda x: True if (x.find('HEI2015') > -1) else False
    hei_cols = [col for col in df.columns if is_hei_column(col)]
    
    demo_cols = ['RIAGENDR', 'RIDAGEYR', 'RIDRETH1', 'DMDEDUC', 'INDFMINC']
    pag_cols = ['PAG_MINW', 'ADHERENCE']
    phq_score_cols = ['PHQ9', 'PHQ_GRP']
    
    return demo_cols, phq_cols, hei_cols, pag_cols, phq_score_cols


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


def get_higher_correlations(df, col='PHQ9'):
#     correlation_thresholds = {
#         'strong': 0.7,  # acima de 0.7
#         'moderate': 0.5,  # entre 0.7 e 0.5
#         'weak': 0.3,  # entre 0.5 e 0.3
#     }
#     correlation_levels = {}
#     for level in correlation_thresholds:
#         correlation_levels[level] = corr[corr > correlation_thresholds[level]] + corr[corr < correlation_thresholds[level] * -1]
        
#     return correlation_levels
    
    correlation_threshold = 0.3
    corr = df.corr().loc[col]
    
    return pd.concat([corr[corr > correlation_threshold], corr[corr < correlation_threshold * -1]])


def plot_for_cols(df, cols, func, kwargs={}, figsize=(20, 12), max_plots_per_row=3, y=None):
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
            func(data=df, x=df[col], **kwargs)


def column_analysis(df, col, normalize=True, kwargs={}):
    print(f'Coluna: {col}')
    
    print(f'\ndescribe():')
    print(df[col].describe())
    
    print(f'\nvalue_counts(normalize={normalize}):')
    print(df[col].value_counts(normalize=normalize))
    
    print(f'\nisnull():')
    print(df[col].isnull().sum())
    
    print(f'\nhistplot():')
    sns.histplot(data=df, x=df[col], discrete=True)
    plt.show()
    print('\n')
    