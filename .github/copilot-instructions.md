# AI Coding Instructions for miRNA Periodontal Disease Analysis

## Project Overview
This is a biomedical research project analyzing miRNA expression in saliva samples to identify biomarkers for periodontal disease progression (Healthy → Gingivitis → Periodontitis).

## Core Data Structure
- **Primary dataset**: `miRNA-saliva-qPCR-results.csv` contains qPCR Ct values for 6 miRNAs + GAPDH reference
- **Group coding**: `S`=Healthy, `G`=Gingivitis, `P`=Periodontitis (use these exact codes)
- **miRNA targets**: mir146a, mir146b, mir155, mir203, mir223, mir381p
- **Clinical markers**: plaque_index, gingival_index, pocket_depth, bleeding_on_probing, number_of_missing_teeth
- **Demographics**: AGE, SEX (M/F)
- **Prompt aliases**: PPD=pocket_depth, CAL=gingival_index, BoP=bleeding_on_probing

## Analysis Methodology Requirements
1. **Data Transformation Pipeline**:
   - Calculate ΔCt: `Ct(miRNA) - Ct(GAPDH)` for each miRNA
   - Use `S` (Healthy) group as calibrator: calculate mean ΔCt for each miRNA
   - Calculate ΔΔCt: `ΔCt(sample) - mean(ΔCt(S_group))`
   - Calculate RQ: `2^(-ΔΔCt)` for final expression values

2. **Reference Gene Validation**:
   - Always test GAPDH stability across groups before proceeding
   - Document limitation of single reference gene in analysis reports

3. **Statistical Analysis Approach**:
   - Use omnibus tests (ANOVA/Kruskal-Wallis) before pairwise comparisons
   - Apply Benjamini-Hochberg FDR correction for multiple comparisons
   - Calculate effect sizes (Cohen's d) alongside p-values

## Analysis Standards
- **Column naming**: Use `dCt_`, `ddCt_`, `RQ_` prefixes for transformed data
- **Group comparisons**: Always test H vs P, H vs G, G vs P pairwise
- **Clinical expectations**: P group should have higher clinical severity markers than G group
- **Biomarker identification**: Significant miRNAs must meet both q < 0.05 AND |log2FC| > 1

## Technical Environment
- Python 3.11 with virtual environment
- Required packages: pandas, numpy, scipy, sklearn, matplotlib, seaborn
- Statistical focus: Use scipy.stats for all statistical tests
- ML approach: Logistic Regression + Random Forest for binary classification

## Quality Assurance Roles
When performing analysis, embody these roles:
- **Lead Validator**: Check reproducibility, avoid data leakage, document methodology
- **Skeptical Peer Reviewer**: Challenge statistical assumptions, identify limitations
- **Hypothesis Generator**: Use each finding to generate next logical questions
- **Evidence Generator**: Save all plots, tables, and intermediate results

## Data Quality Requirements
- Report data integrity before analysis
- Use median imputation for missing values (document which columns)  
- Check normality with Shapiro-Wilk test before choosing parametric vs non-parametric tests
- Visualize distributions before statistical testing

## Output Standards
- Generate comprehensive results tables with log2FC, p-values, q-values, effect sizes
- Create volcano plots for differential expression with significance thresholds
- Produce candidate biomarkers lists meeting significance criteria
- Use descriptive filenames for all outputs

## Machine Learning Specifics
- Use stratified train-test splits (80/20)
- Fit scalers ONLY on training data, then transform test data
- Perform repeated stratified k-fold cross-validation
- Generate AUC-ROC curves, confusion matrices, and feature importance plots
- Create partial dependence plots for top 3 features

## Validation & Reproducibility
- Document all analytical decisions and assumptions
- Perform sensitivity analyses for key findings
- Generate correlation analyses between demographics and miRNA expression
- Use unsupervised clustering to validate group structure
- Always check that clinical variables align with expected disease progression
