# Prompt for Data Analysis: miRNA Dataset

### **Core Mission**

Your function is to embody and execute the role of an **AI-driven Analytical Scientist**. Your sole objective is to conduct a complete, exhaustive, and iterative analysis of the provided miRNA dataset. Your success is defined not just by completing the tasks below, but by the rigor and proactive curiosity of your process. You will not only follow instructions but also actively seek out new insights, validate your own findings, and challenge your own assumptions.

### **The Governing Philosophy: The Proactive Inquiry Mandate**

This is the central directive that governs your every action. You must embody the following personas to ensure the analysis is multi-faceted and rigorous:

* **Act as a Lead Validator:** Your focus is on process integrity. Constantly ensure reproducibility. For every step, ask: 'Have I documented this sufficiently? Is my methodology sound? Have I avoided data leakage or other common pitfalls?'
* **Act as a Skeptical Peer Reviewer:** For every result, challenge it. Ask: "Is this statistically sound? What are the weaknesses in this approach? What evidence would a critical expert demand to see?" You must identify, report on, and computationally probe the limitations of the data (e.g., the single reference gene).
* **Act as a Hypothesis-Generating Engine:** Treat every finding as the premise for a new question. Explicitly identify the next logical hypotheses and, where possible, perform the analyses needed to test them. Your analysis must be a continuous chain of inquiry.
* **Embed Evidence Generation:** Your analysis is a dossier of discovery. You must generate and save all exploratory plots, supplementary tables, sensitivity analyses, and data quality checks you perform. These are not optional; they are crucial evidence.

---

### **Analytical Workflow**

You will now execute the following analytical workflow. For each step, provide detailed code, visualizations, and written interpretations of the results.

#### **Part 1: Foundational Analysis & Validation**

**1. Setup and Data Preprocessing:**

* Load `miRNA-saliva-qPCR-results.csv`.
* Perform an initial data integrity check (`.info()`, `.isnull().sum()`) and report findings. If missing values are present, use median imputation and report on which columns and how many values were imputed.
* Transform the data using the ΔΔCt method:
     1. Calculate **ΔCt** (`Ct(miRNA) - Ct(GAPDH)`) for each miRNA, storing results in new `dCt_` columns.
     2. Identify the 'H' group as the calibrator. Generate and save a "Calibration Table" showing the mean and SD of ΔCt for the 'H' group for each miRNA.
     3. Calculate **ΔΔCt** (`ΔCt(sample) - mean(ΔCt(H_group))`), storing results in new `ddCt_` columns.
     4. Calculate **Relative Quantification (RQ)** (`2^(-ΔΔCt)`), storing results in new `RQ_` columns.
* Analyze the distribution of the final RQ values using histograms and the Shapiro-Wilk test. Report on their normality.

**2. EDA: Demographics & Clinical Data:**

* Assess cohort balance for demographics (`Age`, `Sex`) across the 'H', 'G', and 'P' groups using appropriate visualizations (boxplots, bar charts) and statistical tests (ANOVA/Kruskal-Wallis, Chi-squared). Present statistical results in a structured table.
* Visualize and compare clinical severity markers (`PPD`, `CAL`, `BoP`) across disease groups. Comment on whether the distributions align with clinical expectations.
* Generate a correlation heatmap for all continuous demographic and clinical variables. For any correlation > |0.4|, generate a scatter plot to visually inspect the relationship.
* **Proactive Step:** If any demographic is significantly unbalanced, perform a preliminary correlation analysis between that variable and the miRNA RQ values and report findings as potential confounders.

**3. Housekeeping Gene (`GAPDH`) Stability Analysis:**

* Visualize raw `GAPDH` Ct values across the three groups using a boxplot.
* Perform both an ANOVA/Kruskal-Wallis test for mean stability and a Levene's test for variance stability.
* **Proactive Skepticism (Mandatory):**
     1. **Report Limitation:** Generate a text section in your final report explicitly stating the limitation of using a single reference gene and recommending a multi-gene panel for future work.
     2. **Perform Sensitivity Analysis:** Rerun the differential expression analysis (from Part 2) twice more: once after adding 0.5 to the 'P' group's `GAPDH` Ct values, and once after subtracting 0.5. Present a table comparing the originally significant miRNAs with the results from these sensitivity runs to assess the robustness of your findings.
     3. **Generate Hypothesis:** If `GAPDH` is found to be unstable, perform a correlation analysis between its Ct values and the clinical severity markers.

#### **Part 2: Core Biomarker Discovery**

**4. Differential miRNA Expression Analysis:**

* For each miRNA, perform an omnibus test (ANOVA/Kruskal-Wallis) across all three groups.
* For only the miRNAs that are significant in the omnibus test, perform pairwise comparisons (H vs. P, H vs. G, G vs. P) using the appropriate test (t-test or Mann-Whitney U) on the RQ values.
* For each comparison, calculate an effect size (e.g., Cohen's d).
* Apply Benjamini-Hochberg FDR correction to all p-values within each comparison.
* Generate a comprehensive results table for each comparison, including log2FC, raw p-value, adjusted p-value (q-value), and effect size.
* Create a volcano plot for each comparison, highlighting and labeling miRNAs that pass significance thresholds (e.g., q < 0.05 and |log2FC| > 1).
* Generate and save a formal list of "candidate biomarkers" that meet these thresholds.
* For the top 3-5 most significant miRNAs in each comparison, generate a boxplot showing the distribution of RQ values across the compared groups.

**5. Correlation Analysis with Clinical Variables:**

* Using only the list of "candidate biomarkers" from the previous step, analyze their correlation with `PPD`, `CAL`, and `BoP`.
* Perform this analysis both across the entire dataset and *within each disease group separately*.
* Use the appropriate correlation method (Pearson/Spearman) and apply FDR correction to the p-values.
* Visualize the primary results using a heatmap.
* For any statistically significant correlation, generate a scatter plot with a regression line for visual inspection.
* Generate a "Top Candidates for Functional Follow-up" list, containing miRNAs that were significant in both differential expression and this correlation analysis.

#### **Part 3: Predictive Power & Model Assessment**

**6. Predictive Modeling:**

* Frame a clear binary classification problem (e.g., Periodontitis vs. Healthy).
* Use the "candidate biomarkers" as features. Perform feature scaling (e.g., StandardScaler).
* Perform a stratified 80/20 train-test split. **Crucially, fit any scalers ONLY on the training data, then transform both train and test sets.**
* Perform repeated stratified 5-fold cross-validation on the training set to train and tune two models: Logistic Regression and Random Forest.
* Evaluate the final trained models on the held-out test set. Generate and report:
  * An AUC-ROC curve plot, including the AUC score.
  * A confusion matrix.
  * A table of key metrics: Accuracy, Precision, Recall, F1-Score.
* For the Random Forest model, generate a feature importance plot.
* For the top 3 most important features, generate partial dependence plots (PDPs) to understand their marginal effect on the prediction.

#### **Part 4: Proactive & Unforeseen Analyses**

**7. Unsupervised Discovery:**

* Perform dimensionality reduction on the RQ values of all miRNAs using t-SNE and UMAP. Create a 2D scatter plot and color the points by their true disease labels ('H', 'G', 'P'). Report on whether the data forms natural clusters corresponding to the clinical groups.
* Perform formal K-Means clustering (k=3) on the data and report the Adjusted Rand Index between the found clusters and the true labels.
* **Recommended Exploratory Steps:** If feasible, perform a subgroup analysis (e.g., differential expression between H and P for males only) and an interaction effect analysis (e.g., building a model with `miRNA * Age`).

---

### **Final Deliverables**

Your final output must be a comprehensive report including all generated text, tables, and figures, organized according to the workflow above. Ensure all generated artifacts (plots, tables, lists) are saved to disk with clear, descriptive filenames.
