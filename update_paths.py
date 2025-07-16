#!/usr/bin/env python3
"""
Update image paths in comprehensive analysis results document
"""

import re

# Read the file
with open("docs/COMPREHENSIVE_ANALYSIS_RESULTS_EMBEDDED.md", "r") as f:
    content = f.read()

# Define path mappings (old -> new)
path_mappings = {
    "results/plots/clinical_variables_by_group.png": "outputs/python_scripts/plots/Clinical_Variables_By_Group.png",
    "results/plots/gapdh_stability_boxplot.png": "outputs/python_scripts/plots/GAPDH_Stability_Boxplot.png",
    "results/plots/rq_distributions.png": "outputs/python_scripts/plots/RQ_Distributions.png",
    "results/plots/boxplots_H_vs_G.png": "outputs/python_scripts/plots/Boxplots_H_vs_G.png",
    "results/plots/boxplots_H_vs_P.png": "outputs/python_scripts/plots/Boxplots_H_vs_P.png",
    "results/plots/boxplots_G_vs_P.png": "outputs/python_scripts/plots/Boxplots_G_vs_P.png",
    "results/plots/volcano_plots.png": "outputs/python_scripts/plots/Volcano_Plots.png",
    "results/plots/correlation_heatmap.png": "outputs/python_scripts/plots/Correlation_Heatmap.png",
    "results/plots/correlation_heatmap_mirna_clinical.png": "outputs/python_scripts/plots/Correlation_Heatmap_miRNA_Clinical.png",
    "results/plots/scatter_plots_significant_correlations.png": "outputs/python_scripts/plots/Scatter_Plots_Significant_Correlations.png",
    "results/plots/roc_curves.png": "outputs/python_scripts/plots/ROC_Curves.png",
    "results/plots/confusion_matrices.png": "outputs/python_scripts/plots/Confusion_Matrices.png",
    "results/plots/feature_importance.png": "outputs/python_scripts/plots/Feature_Importance.png",
    "results/plots/partial_dependence_plots.png": "outputs/python_scripts/plots/Partial_Dependence_Plots.png",
    "results/plots/dimensionality_reduction.png": "outputs/python_scripts/plots/Dimensionality_Reduction.png",
    "results/plots/clustering_results.png": "outputs/python_scripts/plots/Clustering_Results.png",
    # Add other paths as needed
    "results/tables/": "outputs/python_scripts/tables/",
    "results/plots/": "outputs/python_scripts/plots/",
}

# Update the content
updated_content = content
for old_path, new_path in path_mappings.items():
    updated_content = updated_content.replace(old_path, new_path)

# Write back to file
with open("docs/COMPREHENSIVE_ANALYSIS_RESULTS_EMBEDDED.md", "w") as f:
    f.write(updated_content)

print("✅ Image paths updated in comprehensive analysis results document")
print("📊 Updated path mappings:")
for old, new in path_mappings.items():
    if old != new:
        print(f"  {old} -> {new}")
