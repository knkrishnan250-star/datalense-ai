import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Set standard plotting aesthetics
sns.set_theme(style="whitegrid")
plt.rcParams.update({'figure.max_open_warning': 0})

def plot_histogram(df: pd.DataFrame, column: str):
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(df[column], kde=True, ax=ax, color="#4A90E2")
    ax.set_title(f"Distribution Profile: {column}", fontsize=12, fontweight='bold')
    plt.tight_layout()
    return fig

def plot_boxplot(df: pd.DataFrame, column: str):
    fig, ax = plt.subplots(figsize=(8, 3))
    sns.boxplot(x=df[column], ax=ax, color="#50E3C2")
    ax.set_title(f"Box Plot & Outlier Detection: {column}", fontsize=12, fontweight='bold')
    plt.tight_layout()
    return fig

def plot_scatterplot(df: pd.DataFrame, x_col: str, y_col: str):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax, color="#9B51E0", alpha=0.7)
    ax.set_title(f"Scatter Analysis: {x_col} vs {y_col}", fontsize=12, fontweight='bold')
    plt.tight_layout()
    return fig

def plot_heatmap(df: pd.DataFrame):
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.empty:
        return None
    
    corr = numeric_df.corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Generate custom mask for upper triangle matrix
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    sns.heatmap(
        corr, 
        mask=mask, 
        annot=True, 
        fmt=".2f", 
        cmap="coolwarm", 
        vmin=-1, 
        vmax=1, 
        center=0, 
        square=True, 
        linewidths=.5, 
        cbar_kws={"shrink": .7},
        ax=ax
    )
    ax.set_title("Correlation Matrix Heatmap", fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    return fig