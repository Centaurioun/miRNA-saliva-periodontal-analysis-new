#!/usr/bin/env python3
"""
Update Python scripts to use new organized output structure
"""

import os
import re

# Define the new output structure
output_structure = '''
# Configure output directory structure
BASE_OUTPUT_DIR = "outputs/python_scripts"
OUTPUT_DIRS = {
    'base': BASE_OUTPUT_DIR,
    'plots': f"{BASE_OUTPUT_DIR}/plots",
    'tables': f"{BASE_OUTPUT_DIR}/tables",
    'sensitivity': f"{BASE_OUTPUT_DIR}/sensitivity"
}

# Create output directories
for dir_name, dir_path in OUTPUT_DIRS.items():
    os.makedirs(dir_path, exist_ok=True)

def get_output_path(filename, output_type='plots'):
    """Get standardized output path with Title Case naming"""
    if not filename.endswith(('.png', '.jpg', '.jpeg', '.pdf', '.csv', '.txt')):
        filename += '.png'  # Default to PNG for plots

    return os.path.join(OUTPUT_DIRS[output_type], filename)
'''

# File mappings for Title Case naming
file_mappings = {
    "boxplots_G_vs_P.png": "Boxplots_G_vs_P.png",
    "boxplots_H_vs_G.png": "Boxplots_H_vs_G.png",
    "boxplots_H_vs_P.png": "Boxplots_H_vs_P.png",
    "clinical_variables_by_group.png": "Clinical_Variables_By_Group.png",
    "clustering_results.png": "Clustering_Results.png",
    "confusion_matrices.png": "Confusion_Matrices.png",
    "correlation_heatmap.png": "Correlation_Heatmap.png",
    "correlation_heatmap_mirna_clinical.png": "Correlation_Heatmap_miRNA_Clinical.png",
    "dimensionality_reduction.png": "Dimensionality_Reduction.png",
    "feature_importance.png": "Feature_Importance.png",
    "gapdh_stability_boxplot.png": "GAPDH_Stability_Boxplot.png",
    "partial_dependence_plots.png": "Partial_Dependence_Plots.png",
    "roc_curves.png": "ROC_Curves.png",
    "rq_distributions.png": "RQ_Distributions.png",
    "volcano_plots.png": "Volcano_Plots.png",
    "scatter_plots_significant_correlations.png": "Scatter_Plots_Significant_Correlations.png",
    "processed_data.csv": "Processed_Data.csv",
    "calibration_table.csv": "Calibration_Table.csv",
    "demographic_clinical_stats.csv": "Demographic_Clinical_Stats.csv",
    "normality_test_results.csv": "Normality_Test_Results.csv",
    "overall_correlations.csv": "Overall_Correlations.csv",
    "omnibus_test_results.csv": "Omnibus_Test_Results.csv",
    "H_vs_P_results.csv": "H_vs_P_Results.csv",
    "H_vs_G_results.csv": "H_vs_G_Results.csv",
    "G_vs_P_results.csv": "G_vs_P_Results.csv",
    "candidate_biomarkers_H_vs_P.csv": "Candidate_Biomarkers_H_vs_P.csv",
    "candidate_biomarkers_G_vs_P.csv": "Candidate_Biomarkers_G_vs_P.csv",
    "model_performance_metrics.csv": "Model_Performance_Metrics.csv",
    "feature_importance.csv": "Feature_Importance.csv",
    "detailed_model_results.csv": "Detailed_Model_Results.csv",
    "cluster_composition.csv": "Cluster_Composition.csv",
    "gapdh_clinical_correlations.csv": "GAPDH_Clinical_Correlations.csv",
    "reference_gene_limitation_report.txt": "Reference_Gene_Limitation_Report.txt",
    "sensitivity_analysis_comparison.csv": "Sensitivity_Analysis_Comparison.csv",
    "functional_follow_up_candidates.csv": "Functional_Follow_Up_Candidates.csv",
}

# Update each Python script
python_files = [
    "src/miRNA_analysis.py",
    "src/miRNA_analysis_part2.py",
    "src/miRNA_analysis_part3.py",
    "src/miRNA_analysis_part4_corrected.py",
]

for file_path in python_files:
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Add the output structure at the beginning (after imports)
        if "BASE_OUTPUT_DIR" not in content:
            # Find the end of imports section
            import_end = content.find("# Set")
            if import_end == -1:
                import_end = content.find("def ")
            if import_end == -1:
                import_end = content.find("if __name__")

            if import_end != -1:
                content = (
                    content[:import_end]
                    + output_structure
                    + "\n\n"
                    + content[import_end:]
                )

        # Replace old file saving patterns with new ones
        for old_name, new_name in file_mappings.items():
            # Update savefig calls
            content = re.sub(
                rf'plt\.savefig\(["\']results/plots/{old_name}["\']',
                f'plt.savefig(get_output_path("{new_name}")',
                content,
            )

            # Update to_csv calls
            content = re.sub(
                rf'\.to_csv\(["\']results/tables/{old_name.replace(".png", ".csv")}["\']',
                f'.to_csv(get_output_path("{new_name.replace(".png", ".csv")}", "tables")',
                content,
            )

        # General replacements
        content = re.sub(r"results/plots/", 'get_output_path("', content)
        content = re.sub(r"results/tables/", 'get_output_path("', content)
        content = re.sub(r"results/sensitivity/", 'get_output_path("', content)

        # Write back
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"✅ Updated {file_path}")

print("✅ All Python scripts updated with new organized output structure")
print("📊 Title Case naming applied to all output files")
