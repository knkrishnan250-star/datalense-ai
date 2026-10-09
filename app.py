import streamlit as str
import pandas as pd
from utils.analyzer import DatasetAnalyzer
from utils import visualizer

str.set_page_config(
    page_title="DataLens AI - Intelligent Dataset Explorer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Application Header Design
str.title("📊 DataLens AI")
str.subheader("Intelligent Dataset Explorer & Automated Reporter")
str.markdown("---")

# File Upload Processing
uploaded_file = str.sidebar.file_uploader("Upload target CSV dataset", type=["csv"])

if uploaded_file is not None:
    try:
        # Load dataset into memory
        df = pd.read_csv(uploaded_file)
        analyzer = DatasetAnalyzer(df)
        
        # Tabs system initialization
        tab1, tab2, tab3, tab4 = str.tabs([
            "📋 Metadata Overview", 
            "🔢 Statistical Matrix", 
            "🔍 Integrity & Outliers", 
            "📈 Interactive Visualizations"
        ])
        
        with tab1:
            str.header("Dataset Metadata Overview")
            overview = analyzer.get_overview()
            
            # KPI display metrics
            col1, col2, col3 = str.columns(3)
            col1.metric("Total Rows", f"{overview['num_rows']:,}")
            col2.metric("Total Columns", f"{overview['num_cols']:,}")
            col3.metric("Estimated Memory Alloc", overview['memory_usage'])
            
            str.markdown("### Structural Breakdown")
            column_summary = analyzer.get_column_summary()
            str.dataframe(column_summary, use_container_width=True, hide_index=True)
            
        with tab2:
            str.header("Descriptive Descriptive Statistics")
            stats_df = analyzer.get_numeric_stats()
            
            if not stats_df.empty:
                str.dataframe(stats_df, use_container_width=True)
            else:
                str.warning("No operational numeric columns identified inside this dataset.")
                
        with tab3:
            str.header("Data Integrity & Validation Profiles")
            
            col_left, col_right = str.columns(2)
            
            with col_left:
                str.subheader("Missing Value Density Matrix")
                missing_counts = df.isnull().sum()
                missing_df = pd.DataFrame({"Column": missing_counts.index, "Missing Records": missing_counts.values})
                missing_df = missing_df[missing_df["Missing Records"] > 0]
                
                if not missing_df.empty:
                    str.dataframe(missing_df, use_container_width=True, hide_index=True)
                else:
                    str.success("Data validation clean. Zero missing records detected.")
            
            with col_right:
                str.subheader("Outlier Footprints (IQR Anomaly Method)")
                outliers = analyzer.detect_outliers_iqr()
                if outliers:
                    outlier_df = pd.DataFrame(list(outliers.items()), columns=["Column", "Outlier Count"])
                    str.dataframe(outlier_df, use_container_width=True, hide_index=True)
                else:
                    str.success("No absolute structural outliers detected matching standard $1.5 \\times IQR$ bounds.")

        with tab4:
            str.header("Visual Data Exploration Engines")
            
            # Select target plot features
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            all_cols = df.columns.tolist()
            
            if numeric_cols:
                str.subheader("Univariate Profiles")
                selected_col = str.selectbox("Choose feature to map profile:", numeric_cols)
                
                c1, c2 = str.columns(2)
                with c1:
                    fig_hist = visualizer.plot_histogram(df, selected_col)
                    str.pyplot(fig_hist)
                with c2:
                    fig_box = visualizer.plot_boxplot(df, selected_col)
                    str.pyplot(fig_box)
                
                str.markdown("---")
                str.subheader("Multivariate Profiles")
                
                if len(numeric_cols) >= 2:
                    cx, cy = str.columns(2)
                    with cx:
                        x_axis = str.selectbox("X-Axis Feature", all_cols, index=0)
                    with cy:
                        y_axis = str.selectbox("Y-Axis Feature", all_cols, index=min(1, len(all_cols)-1))
                    
                    fig_scatter = visualizer.plot_scatterplot(df, x_axis, y_axis)
                    str.pyplot(fig_scatter)
                
                str.markdown("---")
                str.subheader("Global Association Engine")
                fig_heat = visualizer.plot_heatmap(df)
                if fig_heat:
                    str.pyplot(fig_heat)
            else:
                str.warning("Visual features disabled: Numerical data is missing.")
                
    except Exception as e:
        str.error(f"Critical execution fault during runtime file ingestion parser: {e}")
else:
    # Landing State UI
    str.info("Waiting for data engine instantiation... Feed an unencrypted CSV flat-file via the control panel sidebar.")