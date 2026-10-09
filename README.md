# DataLens AI — Intelligent Dataset Explorer

DataLens AI is a modular data-profiling workspace engineered to ingest, parse, clean-validate, and extract statistical structures dynamically out of unstructured or tabular CSV flat files.

## High-Performance Architectural Blueprints
- **Automated Data Profile Mapping:** Structural matrix maps row counts, variable type constraints, and deep-RAM allocations instantly.
- **Parametric Descriptive Statistics:** Central tendencies measurements ($\mu$, median, $\sigma$) automatically isolated per continuous column.
- **Anomalous Signatures Profiling:** Evaluates structural null values and implements deterministic **IQR outbounding ($1.5 \times IQR$)** computations.
- **Multivariate Analytical Graphics:** Embedded declarative Matplotlib and Seaborn visualization pipes mapping feature relationships cleanly.

## Quick-Start Setup Guide

### 1. Requirements Allocation
Create an isolated environment context using Python 3.10+:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate