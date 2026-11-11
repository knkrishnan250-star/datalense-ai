import pandas as pd
import numpy as np

class DatasetAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_overview(self) -> dict:
        """Calculates high-level metrics of the dataframe."""
        memory_usage_bytes = self.df.memory_usage(deep=True).sum()
        
        # Human readable file size conversion
        if memory_usage_bytes < 1024 * 1024:
            size_str = f"{memory_usage_bytes / 1024:.2f} KB"
        else:
            size_str = f"{memory_usage_bytes / (1024 * 1024):.2f} MB"

        return {
            "num_rows": self.df.shape[0],
            "num_cols": self.df.shape[1],
            "memory_usage": size_str,
        }

    def get_column_summary(self) -> pd.DataFrame:
        """Generates detailed statistics per column."""
        summary_data = []
        for col in self.df.columns:
            summary_data.append({
                "Column": col,
                "Data Type": str(self.df[col].dtype),
                "Missing Values": self.df[col].isnull().sum(),
                "Unique Values": self.df[col].nunique()
            })
        return pd.DataFrame(summary_data)

    def get_numeric_stats(self) -> pd.DataFrame:
        """Returns fundamental statistical dispersion for numeric types."""
        numeric_df = self.df.select_dtypes(include=[np.number])
        if numeric_df.empty:
            return pd.DataFrame()
        
        stats = numeric_df.describe().T
        # Renaming to align with explicit requirements
        stats = stats.rename(columns={
            "mean": "Mean",
            "50%": "Median",
            "std": "Standard Deviation",
            "min": "Min",
            "max": "Max"
        })
        return stats[["Mean", "Median", "Standard Deviation", "Min", "Max"]]

    def detect_outliers_iqr(self) -> dict:
        """Identifies outliers using the Interquartile Range technique."""
        numeric_df = self.df.select_dtypes(include=[np.number])
        outlier_summary = {}
        
        for col in numeric_df.columns:
            q1 = numeric_df[col].quantile(0.25)
            q3 = numeric_df[col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            
            outliers = numeric_df[(numeric_df[col] < lower_bound) | (numeric_df[col] > upper_bound)]
            if len(outliers) > 0:
                outlier_summary[col] = len(outliers)
                
        return outlier_summary