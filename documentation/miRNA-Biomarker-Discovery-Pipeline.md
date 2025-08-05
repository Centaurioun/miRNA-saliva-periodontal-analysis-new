# miRNA Biomarker Discovery Pipeline for Periodontal Disease 🧬🦷

This project provides a comprehensive pipeline for analyzing miRNA expression data to identify potential biomarkers for periodontal disease. It encompasses data preprocessing, statistical analysis, machine learning modeling, dimensionality reduction, and report generation. The pipeline aims to facilitate the discovery of miRNAs that can be used for early diagnosis and monitoring of periodontal disease progression.

## 🚀 Key Features

- **Data Preprocessing:** Handles missing values, converts data types, and performs ΔΔCt transformation.
- **Differential Expression Analysis:** Identifies miRNAs with significant expression differences between disease groups using Kruskal-Wallis and Mann-Whitney U tests with multiple testing correction.
- **Correlation Analysis:** Explores the relationships between miRNA expression levels and clinical variables using Spearman and Pearson correlations.
- **Predictive Modeling:** Builds and evaluates machine learning models (Logistic Regression, Random Forest) to classify samples based on miRNA expression.
- **Unsupervised Discovery:** Applies dimensionality reduction (t-SNE, UMAP) and clustering (K-Means) to explore data structure and validate group assignments.
- **GAPDH Sensitivity Analysis:** Assesses the impact of GAPDH normalization on the results.
- **Dimensionality Reduction:** Utilizes PCA, t-SNE, and UMAP for data visualization and feature extraction.
- **Comprehensive Reporting:** Generates reports in HTML, PDF, and DOCX formats, incorporating data, visualizations, and analysis results.
- **Statistical Analysis**: Performs normality tests, group comparisons (ANOVA, t-tests, Mann-Whitney U), and correlation analysis.
- **Visualization**: Generates publication-quality plots, including box plots, scatter plots, heatmaps, volcano plots, and ROC curves.

## 🛠️ Tech Stack

- **Languages:**
    - Python
    - R
- **Python Libraries:**
    - `pandas`: Data manipulation and analysis
    - `numpy`: Numerical operations
    - `matplotlib.pyplot`: Plotting
    - `seaborn`: Statistical data visualization
    - `scipy.stats`: Statistical tests
    - `sklearn`: Machine learning
    - `umap-learn`: UMAP dimensionality reduction
    - `tqdm`: Progress bar
    - `joblib`: Pipelining Python jobs
    - `markdown`: Converting Markdown text into HTML
    - `weasyprint`: Converting HTML into PDF
    - `docx`: Creating and manipulating DOCX files
    - `statsmodels`: Statistical modeling
- **R Packages:**
    - `tidyverse`: Data manipulation and visualization
    - `magrittr`: Pipe operators
    - `broom`: Tidying statistical outputs
    - `effsize`: Effect size calculations
    - `corrplot`: Correlation plots
    - `psych`: Psychological/statistical functions
    - `caret`: Classification and regression training
    - `randomForest`: Random forest implementation
    - `pROC`: ROC analysis
    - `glmnet`: Regularized regression
    - `Rtsne`: t-SNE dimensionality reduction
    - `umap`: UMAP dimensionality reduction
    - `FactoMineR`: PCA
- **Build Tools:**
    - `pytest`: Testing framework
    - `black`: Code formatter
    - `flake8`: Code style checker
    - `sphinx`: Documentation generator
    - `sphinx-rtd-theme`: Read the Docs theme for Sphinx

## 📦 Getting Started

### Prerequisites

- Python 3.6+
- R 4.0+
- Required Python packages (see `requirements.txt`)
- Required R packages (install via `install.packages()`)
- WeasyPrint (for PDF report generation): `pip install WeasyPrint` (may require additional system dependencies)

### Installation

1.  Clone the repository:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  Create a virtual environment (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.  Install R dependencies: Open R and run:
    ```R
    install.packages(c("tidyverse", "magrittr", "broom", "effsize", "corrplot", "psych", "caret", "randomForest", "pROC", "glmnet", "Rtsne", "umap", "FactoMineR"))
    ```

### Running Locally

1.  **Data Preparation:** Ensure your data is in a CSV format and placed in the appropriate input directory.

2.  **Run the Jupyter Notebook:** Execute the `miRNA_Comprehensive_Analysis.ipynb` notebook to perform the core analysis.

    ```bash
    jupyter notebook miRNA_Comprehensive_Analysis.ipynb
    ```

3.  **Run the Python scripts:** Execute the individual python scripts in the `src` directory to perform specific analyses or generate reports.

    ```bash
    python src/miRNA_analysis_part2.py
    python src/miRNA_analysis_part3.py
    python src/miRNA_analysis_part4_corrected.py
    python src/html-pdf-docx-report-generator.py
    ```

4.  **Run the R script:** Execute the `miRNA_Comprehensive_Analysis_Complete.R` script to perform the analysis in R.

    ```bash
    Rscript miRNA_Comprehensive_Analysis_Complete.R
    ```

## 💻 Usage

The pipeline consists of several components that can be run independently or in sequence.

1.  **`miRNA_Comprehensive_Analysis.ipynb`:** The main Jupyter Notebook that performs the core analysis steps.

2.  **`src/miRNA_analysis_part1.py`, `src/miRNA_analysis_part2.py`, `src/miRNA_analysis_part3.py`, `src/miRNA_analysis_part4_corrected.py`:** Python scripts for specific analysis tasks (differential expression, predictive modeling, unsupervised discovery, GAPDH sensitivity).

3.  **`src/html-pdf-docx-report-generator.py`:** Python script to generate comprehensive reports in HTML, PDF, and DOCX formats.

4.  **`miRNA_Comprehensive_Analysis_Complete.R`:** R script that provides an alternative implementation of the analysis.

Adjust the input file paths and parameters within each script or notebook to match your data and analysis requirements.

## 📂 Project Structure

```
├── README.md
├── requirements.txt
├── miRNA_Comprehensive_Analysis.ipynb
├── miRNA_Comprehensive_Analysis_Complete.R
├── src
│   ├── miRNA_analysis.py
│   ├── miRNA_analysis_part2.py
│   ├── miRNA_analysis_part3.py
│   ├── miRNA_analysis_part4_corrected.py
│   ├── generate_enhanced_reports.py
│   ├── html-pdf-docx-report-generator.py
├── outputs
│   ├── python_scripts
│   └── jupyter_notebook
│       └── comprehensive_results
```

## 📸 Screenshots

(Add screenshots of the analysis results, visualizations, and reports here)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them with descriptive messages.
4.  Submit a pull request.

## 📝 License

This project is licensed under the [MIT License](LICENSE).

## 📬 Contact

[Your Name] - [Your Email]

## 💖 Thanks Message

Thank you for your interest in this project! We hope it helps you in your miRNA biomarker discovery research.

This is written by [readme.ai](https://readme-generator-phi.vercel.app/).