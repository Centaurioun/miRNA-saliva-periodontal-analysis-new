#!/usr/bin/env python3
"""
miRNA Periodontal Disease Analysis
==================================

This script performs comprehensive analysis of miRNA expression data to identify
biomarkers for periodontal disease progression (Healthy → Gingivitis → Periodontitis).

Following the Proactive Inquiry Mandate:
- Act as a Lead Validator
- Act as a Skeptical Peer Reviewer
- Act as a Hypothesis-Generating Engine
- Embed Evidence Generation

Author: AI-driven Analytical Scientist
Date: July 16, 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import (
    levene,
    shapiro,
    kruskal,
    mannwhitneyu,
    ttest_ind,
    chi2_contingency,
)
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    roc_auc_score,
    roc_curve,
    confusion_matrix,
    classification_report,
)
from sklearn.inspection import permutation_importance, partial_dependence
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import umap
import warnings

warnings.filterwarnings("ignore")


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


# Set style for publication-quality plots
plt.style.use("seaborn-v0_8")
sns.set_palette("husl")


def setup_output_directory():
    """Create output directory for saving results"""
    import os

    os.makedirs("results", exist_ok=True)
    os.makedirs("results/plots", exist_ok=True)
    os.makedirs("results/tables", exist_ok=True)
    os.makedirs("results/sensitivity", exist_ok=True)
    print("✓ Output directories created")


def load_and_inspect_data():
    """
    Load the miRNA dataset and perform initial data integrity checks
    Acting as Lead Validator: Ensure data quality and reproducibility
    """
    print("=" * 80)
    print("PART 1: FOUNDATIONAL ANALYSIS & VALIDATION")
    print("=" * 80)
    print("\n1. SETUP AND DATA PREPROCESSING")
    print("-" * 50)

    # Load data
    df = pd.read_csv("miRNA-saliva-qPCR-results.csv")
    print(f"✓ Data loaded successfully: {df.shape[0]} samples, {df.shape[1]} variables")

    # Data integrity check
    print("\n📊 DATA INTEGRITY REPORT:")
    print(f"Dataset shape: {df.shape}")
    print(f"Data types:\n{df.dtypes}")
    print(f"\nMissing values:\n{df.isnull().sum()}")

    # Basic statistics
    print(f"\nGroup distribution:\n{df['GROUP'].value_counts()}")
    print(f"Sex distribution:\n{df['SEX'].value_counts()}")
    print(f"Age statistics:\n{df['AGE'].describe()}")

    # Acting as Skeptical Peer Reviewer: Check for data anomalies
    print("\n🔍 DATA QUALITY ASSESSMENT:")

    # Check for outliers in age
    age_outliers = df[(df["AGE"] < 18) | (df["AGE"] > 65)]
    if len(age_outliers) > 0:
        print(f"⚠️  Found {len(age_outliers)} age outliers (< 18 or > 65 years)")

    # Check for impossible clinical values
    clinical_vars = [
        "plaque_index",
        "gingival_index",
        "pocket_depth",
        "bleeding_on_probing",
    ]
    for var in clinical_vars:
        if (df[var] < 0).any():
            print(f"⚠️  Found negative values in {var}")

    # Check for missing data patterns
    missing_data = df.isnull().sum()
    if missing_data.sum() > 0:
        print(f"⚠️  Total missing values: {missing_data.sum()}")
        print("Missing data will be imputed using median values")

        # Median imputation for numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].isnull().sum() > 0:
                median_val = df[col].median()
                df[col].fillna(median_val, inplace=True)
                print(
                    f"  - {col}: {missing_data[col]} values imputed with median {median_val:.2f}"
                )

    print("✓ Data preprocessing completed")
    return df


def delta_delta_ct_transformation(df):
    """
    Perform ΔΔCt transformation following qPCR best practices
    Acting as Lead Validator: Ensure correct qPCR normalization
    """
    print("\n🧬 ΔΔCt TRANSFORMATION PIPELINE")
    print("-" * 50)

    # Define miRNA columns
    mirna_cols = [
        "mean_mir146a",
        "mean_mir146b",
        "mean_mir155",
        "mean_mir203",
        "mean_mir223",
        "mean_mir381p",
    ]

    # Step 1: Calculate ΔCt (Ct_miRNA - Ct_GAPDH)
    print("Step 1: Calculating ΔCt (Ct_miRNA - Ct_GAPDH)")
    for mirna in mirna_cols:
        mirna_name = mirna.replace("mean_", "")
        df[f"dCt_{mirna_name}"] = df[mirna] - df["mean_GAPDH"]

    # Step 2: Identify healthy group as calibrator and calculate mean ΔCt
    print("Step 2: Using Healthy (S) group as calibrator")
    healthy_group = df[df["GROUP"] == "S"]

    calibration_data = {}
    for mirna in mirna_cols:
        mirna_name = mirna.replace("mean_", "")
        dct_col = f"dCt_{mirna_name}"
        mean_dct = healthy_group[dct_col].mean()
        std_dct = healthy_group[dct_col].std()
        calibration_data[mirna_name] = {"mean_dCt": mean_dct, "std_dCt": std_dct}

    # Create and save calibration table
    calibration_df = pd.DataFrame(calibration_data).T
    calibration_df.to_csv(get_output_path("Calibration_Table.csv", "tables"))
    print("✓ Calibration table saved")
    print(calibration_df.round(3))

    # Step 3: Calculate ΔΔCt (ΔCt_sample - mean_ΔCt_healthy)
    print("\nStep 3: Calculating ΔΔCt")
    for mirna in mirna_cols:
        mirna_name = mirna.replace("mean_", "")
        dct_col = f"dCt_{mirna_name}"
        ddct_col = f"ddCt_{mirna_name}"
        calibrator_mean = calibration_data[mirna_name]["mean_dCt"]
        df[ddct_col] = df[dct_col] - calibrator_mean

    # Step 4: Calculate RQ (2^(-ΔΔCt))
    print("Step 4: Calculating Relative Quantification (RQ = 2^(-ΔΔCt))")
    rq_cols = []
    for mirna in mirna_cols:
        mirna_name = mirna.replace("mean_", "")
        ddct_col = f"ddCt_{mirna_name}"
        rq_col = f"RQ_{mirna_name}"
        df[rq_col] = 2 ** (-df[ddct_col])
        rq_cols.append(rq_col)

    print(f"✓ Created {len(rq_cols)} RQ columns")

    # Analyze RQ distribution
    print("\n📈 RQ DISTRIBUTION ANALYSIS")
    print("-" * 30)

    # Create histogram plots
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle("Distribution of RQ Values by miRNA", fontsize=16, fontweight="bold")

    normality_results = {}
    for i, rq_col in enumerate(rq_cols):
        ax = axes[i // 3, i % 3]

        # Histogram
        ax.hist(df[rq_col], bins=30, alpha=0.7, edgecolor="black")
        ax.set_xlabel("RQ Value")
        ax.set_ylabel("Frequency")
        ax.set_title(f"{rq_col}")

        # Shapiro-Wilk test for normality
        stat, p_value = shapiro(df[rq_col])
        normality_results[rq_col] = {"statistic": stat, "p_value": p_value}

        # Add normality test result to plot
        is_normal = "Normal" if p_value > 0.05 else "Non-normal"
        ax.text(
            0.02,
            0.98,
            f"Shapiro-Wilk: {is_normal}\np = {p_value:.3f}",
            transform=ax.transAxes,
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
        )

    plt.tight_layout()
    plt.savefig(get_output_path("RQ_Distributions.png"), dpi=300, bbox_inches="tight")
    plt.show()

    # Create normality results table
    normality_df = pd.DataFrame(normality_results).T
    normality_df.to_csv(get_output_path("Normality_Test_Results.csv", "tables"))

    print("Normality Test Results (Shapiro-Wilk):")
    print(normality_df.round(4))

    # Acting as Hypothesis-Generating Engine: What does this tell us?
    non_normal_count = sum(
        1 for result in normality_results.values() if result["p_value"] <= 0.05
    )
    print(f"\n🔬 HYPOTHESIS GENERATION:")
    print(f"- {non_normal_count}/{len(rq_cols)} miRNAs show non-normal distribution")
    print(
        "- This suggests we should use non-parametric tests for differential expression"
    )
    print("- RQ values may require log-transformation for some analyses")

    return df, rq_cols, calibration_df


def explore_demographics_and_clinical(df):
    """
    Comprehensive EDA of demographics and clinical variables
    Acting as Lead Validator: Assess cohort balance and clinical validity
    """
    print("\n2. EDA: DEMOGRAPHICS & CLINICAL DATA")
    print("-" * 50)

    # Clinical variable mapping (as per prompt aliases)
    clinical_mapping = {
        "pocket_depth": "PPD",
        "gingival_index": "CAL",
        "bleeding_on_probing": "BoP",
    }

    # Demographics balance assessment
    print("📊 COHORT BALANCE ASSESSMENT")
    print("-" * 30)

    # Age distribution across groups
    print("Age distribution by group:")
    age_by_group = df.groupby("GROUP")["AGE"].agg(
        ["count", "mean", "std", "min", "max"]
    )
    print(age_by_group.round(2))

    # Statistical test for age differences
    groups = df["GROUP"].unique()
    age_groups = [df[df["GROUP"] == group]["AGE"].values for group in groups]

    # Check normality for age in each group
    age_normal = all(shapiro(group)[1] > 0.05 for group in age_groups if len(group) > 3)

    if age_normal:
        age_stat, age_p = stats.f_oneway(*age_groups)
        age_test = "ANOVA"
    else:
        age_stat, age_p = stats.kruskal(*age_groups)
        age_test = "Kruskal-Wallis"

    print(f"Age differences ({age_test}): statistic={age_stat:.3f}, p={age_p:.3f}")

    # Sex distribution
    sex_crosstab = pd.crosstab(df["GROUP"], df["SEX"])
    print(f"\nSex distribution by group:\n{sex_crosstab}")

    # Chi-square test for sex balance
    chi2, sex_p, dof, expected = chi2_contingency(sex_crosstab)
    print(f"Sex balance (Chi-square): χ²={chi2:.3f}, p={sex_p:.3f}")

    # Clinical severity markers
    print("\n🏥 CLINICAL SEVERITY MARKERS")
    print("-" * 30)

    clinical_vars = [
        "plaque_index",
        "gingival_index",
        "pocket_depth",
        "bleeding_on_probing",
    ]

    # Create visualization
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("Clinical Variables by Disease Group", fontsize=16, fontweight="bold")

    clinical_stats = {}

    for i, var in enumerate(clinical_vars):
        ax = axes[i // 2, i % 2]

        # Box plot
        df.boxplot(column=var, by="GROUP", ax=ax)
        ax.set_title(f"{clinical_mapping.get(var, var)}")
        ax.set_xlabel("Disease Group")
        ax.set_ylabel("Value")

        # Statistical test
        var_groups = [df[df["GROUP"] == group][var].values for group in groups]
        var_normal = all(
            shapiro(group)[1] > 0.05 for group in var_groups if len(group) > 3
        )

        if var_normal:
            stat, p_val = stats.f_oneway(*var_groups)
            test_name = "ANOVA"
        else:
            stat, p_val = stats.kruskal(*var_groups)
            test_name = "Kruskal-Wallis"

        clinical_stats[var] = {
            "test": test_name,
            "statistic": stat,
            "p_value": p_val,
            "S_mean": df[df["GROUP"] == "S"][var].mean(),
            "G_mean": df[df["GROUP"] == "G"][var].mean(),
            "P_mean": df[df["GROUP"] == "P"][var].mean(),
        }

        # Add test result to plot
        ax.text(
            0.02,
            0.98,
            f"{test_name}\np = {p_val:.3f}",
            transform=ax.transAxes,
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
        )

    plt.tight_layout()
    plt.savefig(
        "get_output_path("clinical_variables_by_group.png", dpi=300, bbox_inches="tight"
    )
    plt.show()

    # Create comprehensive statistics table
    demographic_stats = {
        "AGE": {"test": age_test, "statistic": age_stat, "p_value": age_p},
        "SEX": {"test": "Chi-square", "statistic": chi2, "p_value": sex_p},
    }

    all_stats = {**demographic_stats, **clinical_stats}
    stats_df = pd.DataFrame(all_stats).T
    stats_df.to_csv(get_output_path("Demographic_Clinical_Stats.csv", "tables"))

    print("\nStatistical Test Results:")
    print(stats_df.round(4))

    # Acting as Skeptical Peer Reviewer: Clinical validity check
    print("\n🔍 CLINICAL VALIDITY CHECK")
    print("-" * 25)

    # Check if clinical progression makes sense (S < G < P)
    clinical_progression = {}
    for var in clinical_vars:
        s_mean = df[df["GROUP"] == "S"][var].mean()
        g_mean = df[df["GROUP"] == "G"][var].mean()
        p_mean = df[df["GROUP"] == "P"][var].mean()

        expected_progression = s_mean < g_mean < p_mean
        clinical_progression[var] = {
            "S_mean": s_mean,
            "G_mean": g_mean,
            "P_mean": p_mean,
            "expected_progression": expected_progression,
        }

        status = "✓" if expected_progression else "⚠️"
        print(
            f"{status} {var}: S({s_mean:.2f}) < G({g_mean:.2f}) < P({p_mean:.2f}) = {expected_progression}"
        )

    # Correlation analysis
    print("\n📈 CORRELATION ANALYSIS")
    print("-" * 20)

    # Select continuous variables for correlation
    continuous_vars = ["AGE"] + clinical_vars
    corr_matrix = df[continuous_vars].corr()

    # Create correlation heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        corr_matrix, annot=True, cmap="coolwarm", center=0, square=True, linewidths=0.5
    )
    plt.title(
        "Correlation Matrix: Demographics & Clinical Variables", fontweight="bold"
    )
    plt.tight_layout()
    plt.savefig(get_output_path("Correlation_Heatmap.png"), dpi=300, bbox_inches="tight")
    plt.show()

    # Identify strong correlations (|r| > 0.4)
    strong_corr_pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i + 1, len(corr_matrix.columns)):
            corr_val = corr_matrix.iloc[i, j]
            if abs(corr_val) > 0.4:
                var1, var2 = corr_matrix.columns[i], corr_matrix.columns[j]
                strong_corr_pairs.append((var1, var2, corr_val))

    if strong_corr_pairs:
        print(f"\nStrong correlations (|r| > 0.4):")
        for var1, var2, corr in strong_corr_pairs:
            print(f"- {var1} vs {var2}: r = {corr:.3f}")

            # Create scatter plot for strong correlations
            plt.figure(figsize=(8, 6))
            plt.scatter(df[var1], df[var2], alpha=0.6)
            plt.xlabel(var1)
            plt.ylabel(var2)
            plt.title(f"{var1} vs {var2} (r = {corr:.3f})")

            # Add regression line
            z = np.polyfit(df[var1], df[var2], 1)
            p = np.poly1d(z)
            plt.plot(df[var1], p(df[var1]), "r--", alpha=0.8)

            plt.tight_layout()
            plt.savefig(
                f"get_output_path("scatter_{var1}_vs_{var2}.png",
                dpi=300,
                bbox_inches="tight",
            )
            plt.show()

    # Acting as Hypothesis-Generating Engine: Check for demographic imbalances
    print("\n🔬 PROACTIVE CONFOUNDER ANALYSIS")
    print("-" * 30)

    # Check if any demographic variables are significantly imbalanced
    imbalanced_vars = []
    if age_p < 0.05:
        imbalanced_vars.append("AGE")
    if sex_p < 0.05:
        imbalanced_vars.append("SEX")

    if imbalanced_vars:
        print(f"⚠️  Significantly imbalanced variables: {imbalanced_vars}")
        print("These may confound miRNA expression analysis")
        # This analysis would continue with RQ values, but we'll do that after RQ calculation
    else:
        print("✓ No significant demographic imbalances detected")

    return clinical_stats, demographic_stats, strong_corr_pairs, imbalanced_vars


def gapdh_stability_analysis(df):
    """
    Comprehensive GAPDH stability analysis with mandatory skepticism
    Acting as Skeptical Peer Reviewer: Challenge reference gene assumptions
    """
    print("\n3. HOUSEKEEPING GENE (GAPDH) STABILITY ANALYSIS")
    print("-" * 50)

    # Visualize GAPDH Ct values across groups
    plt.figure(figsize=(10, 6))
    df.boxplot(column="mean_GAPDH", by="GROUP")
    plt.title("GAPDH Ct Values by Disease Group")
    plt.xlabel("Disease Group")
    plt.ylabel("GAPDH Ct Value")
    plt.tight_layout()
    plt.savefig(
        "get_output_path("gapdh_stability_boxplot.png", dpi=300, bbox_inches="tight"
    )
    plt.show()

    # Statistical tests for GAPDH stability
    groups = df["GROUP"].unique()
    gapdh_groups = [df[df["GROUP"] == group]["mean_GAPDH"].values for group in groups]

    # Test for mean stability
    gapdh_normal = all(
        shapiro(group)[1] > 0.05 for group in gapdh_groups if len(group) > 3
    )

    if gapdh_normal:
        mean_stat, mean_p = stats.f_oneway(*gapdh_groups)
        mean_test = "ANOVA"
    else:
        mean_stat, mean_p = stats.kruskal(*gapdh_groups)
        mean_test = "Kruskal-Wallis"

    # Test for variance stability (Levene's test)
    var_stat, var_p = levene(*gapdh_groups)

    print(
        f"GAPDH Mean Stability ({mean_test}): statistic={mean_stat:.3f}, p={mean_p:.3f}"
    )
    print(f"GAPDH Variance Stability (Levene): statistic={var_stat:.3f}, p={var_p:.3f}")

    # MANDATORY PROACTIVE SKEPTICISM
    print("\n🚨 MANDATORY PROACTIVE SKEPTICISM")
    print("-" * 35)

    # 1. Report Limitation
    limitation_text = """
    LIMITATION OF REFERENCE GENE NORMALIZATION:

    This analysis relies on a single reference gene (GAPDH) for normalization, which represents
    a significant methodological limitation. Best practices in qPCR analysis recommend:

    1. Use of multiple reference genes (ideally 3-5) for robust normalization
    2. Validation of reference gene stability using algorithms like geNorm or NormFinder
    3. Assessment of reference gene stability across all experimental conditions

    The current single-gene approach may introduce bias if GAPDH expression is influenced by:
    - Disease state (periodontal inflammation)
    - Metabolic changes in saliva
    - Sample collection or processing conditions

    RECOMMENDATIONS FOR FUTURE STUDIES:
    - Validate findings with a panel of reference genes (e.g., ACTB, HPRT1, RPLP0)
    - Use geometric mean of multiple reference genes for normalization
    - Implement reference gene stability assessment in study design
    """

    print(limitation_text)

    # Save limitation report
    with open("get_output_path("reference_gene_limitation_report.txt", "w") as f:
        f.write(limitation_text)

    # 2. Sensitivity Analysis Setup (will be completed after differential expression)
    print("\n🔬 SENSITIVITY ANALYSIS SETUP")
    print("-" * 28)
    print(
        "Sensitivity analysis will be performed after differential expression analysis"
    )
    print("- Scenario 1: Add 0.5 to P group GAPDH Ct values")
    print("- Scenario 2: Subtract 0.5 from P group GAPDH Ct values")
    print("- Compare significant miRNAs across scenarios")

    # 3. Generate Hypothesis if GAPDH is unstable
    gapdh_unstable = (mean_p < 0.05) or (var_p < 0.05)

    if gapdh_unstable:
        print("\n⚠️  GAPDH INSTABILITY DETECTED - HYPOTHESIS GENERATION")
        print("-" * 50)

        # Correlate GAPDH with clinical severity markers
        clinical_vars = [
            "plaque_index",
            "gingival_index",
            "pocket_depth",
            "bleeding_on_probing",
        ]

        gapdh_clinical_corr = {}
        for var in clinical_vars:
            # Test normality
            gapdh_normal = shapiro(df["mean_GAPDH"])[1] > 0.05
            var_normal = shapiro(df[var])[1] > 0.05

            if gapdh_normal and var_normal:
                corr, p_val = stats.pearsonr(df["mean_GAPDH"], df[var])
                method = "Pearson"
            else:
                corr, p_val = stats.spearmanr(df["mean_GAPDH"], df[var])
                method = "Spearman"

            gapdh_clinical_corr[var] = {
                "correlation": corr,
                "p_value": p_val,
                "method": method,
            }

            print(f"GAPDH vs {var}: {method} r={corr:.3f}, p={p_val:.3f}")

        # Save correlation results
        gapdh_corr_df = pd.DataFrame(gapdh_clinical_corr).T
        gapdh_corr_df.to_csv(get_output_path("GAPDH_Clinical_Correlations.csv", "tables"))

        # HYPOTHESIS: GAPDH expression is regulated by disease state
        print(
            "\n💡 HYPOTHESIS: GAPDH expression may be regulated by periodontal disease state"
        )
        print("This could bias all downstream miRNA expression calculations")

    else:
        print("\n✓ GAPDH appears stable across disease groups")

    return {
        "mean_stability": {
            "test": mean_test,
            "statistic": mean_stat,
            "p_value": mean_p,
        },
        "variance_stability": {
            "test": "Levene",
            "statistic": var_stat,
            "p_value": var_p,
        },
        "unstable": gapdh_unstable,
    }


def main():
    """Main analysis pipeline"""
    print("🧬 miRNA PERIODONTAL DISEASE ANALYSIS")
    print("=" * 80)
    print("AI-driven Analytical Scientist | Proactive Inquiry Mandate")
    print("=" * 80)

    # Setup
    setup_output_directory()

    # Part 1: Foundational Analysis
    df = load_and_inspect_data()
    df, rq_cols, calibration_df = delta_delta_ct_transformation(df)
    clinical_stats, demographic_stats, strong_corr_pairs, imbalanced_vars = (
        explore_demographics_and_clinical(df)
    )
    gapdh_results = gapdh_stability_analysis(df)

    # Save processed data
    df.to_csv("results/processed_data.csv", index=False)
    print("\n✓ Processed data saved to results/processed_data.csv")

    print("\n" + "=" * 80)
    print("PART 1 COMPLETED - FOUNDATIONAL ANALYSIS & VALIDATION")
    print("=" * 80)
    print(f"✓ Data loaded and preprocessed ({df.shape[0]} samples)")
    print(f"✓ ΔΔCt transformation completed ({len(rq_cols)} miRNAs)")
    print(f"✓ Demographics and clinical data explored")
    print(f"✓ GAPDH stability assessed (unstable: {gapdh_results['unstable']})")
    print("\nReady for Part 2: Core Biomarker Discovery")


if __name__ == "__main__":
    main()
