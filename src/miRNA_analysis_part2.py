#!/usr/bin/env python3
"""
miRNA Periodontal Disease Analysis - Part 2: Core Biomarker Discovery
=====================================================================

Continuation of comprehensive miRNA analysis focusing on differential expression
and correlation analysis with clinical variables.

Author: AI-driven Analytical Scientist
Date: July 16, 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import mannwhitneyu, kruskal, spearmanr, pearsonr
from statsmodels.stats.multitest import multipletests
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


def calculate_effect_size(group1, group2, test_type="mann_whitney"):
    """Calculate effect size for non-parametric tests"""
    if test_type == "mann_whitney":
        # Rank-biserial correlation (effect size for Mann-Whitney U)
        n1, n2 = len(group1), len(group2)
        u_stat, _ = mannwhitneyu(group1, group2, alternative="two-sided")
        r = 1 - (2 * u_stat) / (n1 * n2)
        return r
    return None


def log2_fold_change(group1_mean, group2_mean):
    """Calculate log2 fold change"""
    return np.log2(group2_mean / group1_mean)


def differential_expression_analysis(df, rq_cols):
    """
    Comprehensive differential expression analysis
    Acting as Lead Validator: Ensure proper statistical methodology
    """
    print("=" * 80)
    print("PART 2: CORE BIOMARKER DISCOVERY")
    print("=" * 80)
    print("\n4. DIFFERENTIAL miRNA EXPRESSION ANALYSIS")
    print("-" * 50)

    # Step 1: Omnibus test for each miRNA
    print("Step 1: Omnibus testing (Kruskal-Wallis) across all groups")
    print("-" * 55)

    omnibus_results = {}
    groups = ["S", "G", "P"]

    for rq_col in rq_cols:
        mirna_name = rq_col.replace("RQ_", "")

        # Extract data for each group
        group_data = [df[df["GROUP"] == group][rq_col].values for group in groups]

        # Kruskal-Wallis test (non-parametric omnibus test)
        h_stat, p_value = kruskal(*group_data)

        omnibus_results[mirna_name] = {
            "h_statistic": h_stat,
            "p_value": p_value,
            "significant": p_value < 0.05,
        }

        print(
            f"{mirna_name}: H={h_stat:.3f}, p={p_value:.3f} {'*' if p_value < 0.05 else ''}"
        )

    # Create omnibus results table
    omnibus_df = pd.DataFrame(omnibus_results).T
    omnibus_df.to_csv(get_output_path("Omnibus_Test_Results.csv", "tables"))

    # Identify significant miRNAs for post-hoc analysis
    significant_mirnas = [
        mirna for mirna, result in omnibus_results.items() if result["significant"]
    ]

    print(
        f"\n✓ {len(significant_mirnas)}/{len(rq_cols)} miRNAs significant in omnibus test"
    )
    print(f"Significant miRNAs: {significant_mirnas}")

    # Step 2: Post-hoc pairwise comparisons
    print(f"\nStep 2: Post-hoc pairwise comparisons for significant miRNAs")
    print("-" * 55)

    comparisons = [("S", "P"), ("S", "G"), ("G", "P")]
    comparison_names = ["H_vs_P", "H_vs_G", "G_vs_P"]

    all_results = {}

    for comp_idx, (group1, group2) in enumerate(comparisons):
        comp_name = comparison_names[comp_idx]
        print(f"\n{comp_name} comparison:")
        print("-" * 20)

        results = {}
        p_values = []

        for mirna in significant_mirnas:
            rq_col = f"RQ_{mirna}"

            # Extract group data
            g1_data = df[df["GROUP"] == group1][rq_col].values
            g2_data = df[df["GROUP"] == group2][rq_col].values

            # Mann-Whitney U test (non-parametric)
            u_stat, p_value = mannwhitneyu(g1_data, g2_data, alternative="two-sided")

            # Calculate effect size (rank-biserial correlation)
            effect_size = calculate_effect_size(g1_data, g2_data)

            # Calculate log2 fold change
            g1_mean = np.mean(g1_data)
            g2_mean = np.mean(g2_data)
            log2fc = log2_fold_change(g1_mean, g2_mean)

            results[mirna] = {
                "group1_mean": g1_mean,
                "group2_mean": g2_mean,
                "log2FC": log2fc,
                "u_statistic": u_stat,
                "p_value": p_value,
                "effect_size": effect_size,
            }

            p_values.append(p_value)

        # Apply Benjamini-Hochberg FDR correction
        if p_values:
            rejected, q_values, _, _ = multipletests(p_values, method="fdr_bh")

            # Add q-values to results
            for i, mirna in enumerate(significant_mirnas):
                results[mirna]["q_value"] = q_values[i]
                results[mirna]["significant_fdr"] = rejected[i]

        all_results[comp_name] = results

        # Create results table for this comparison
        results_df = pd.DataFrame(results).T
        results_df = results_df.round(4)
        results_df.to_csv(f"get_output_path("{comp_name}_results.csv")

        print(
            results_df[
                ["log2FC", "p_value", "q_value", "effect_size", "significant_fdr"]
            ]
        )

    # Step 3: Create volcano plots
    print(f"\nStep 3: Creating volcano plots")
    print("-" * 25)

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle(
        "Volcano Plots: miRNA Differential Expression", fontsize=16, fontweight="bold"
    )

    for i, (comp_name, results) in enumerate(all_results.items()):
        ax = axes[i]

        # Extract data for plotting
        log2fc_vals = [results[mirna]["log2FC"] for mirna in results.keys()]
        neg_log10_q = [-np.log10(results[mirna]["q_value"]) for mirna in results.keys()]
        mirna_names = list(results.keys())

        # Create scatter plot
        colors = [
            (
                "red"
                if (
                    abs(results[mirna]["log2FC"]) > 1
                    and results[mirna]["q_value"] < 0.05
                )
                else "gray"
            )
            for mirna in mirna_names
        ]

        ax.scatter(log2fc_vals, neg_log10_q, c=colors, alpha=0.7, s=60)

        # Add significance thresholds
        ax.axhline(
            y=-np.log10(0.05), color="blue", linestyle="--", alpha=0.5, label="q=0.05"
        )
        ax.axvline(x=1, color="green", linestyle="--", alpha=0.5, label="log2FC=1")
        ax.axvline(x=-1, color="green", linestyle="--", alpha=0.5)

        # Label significant points
        for j, mirna in enumerate(mirna_names):
            if abs(results[mirna]["log2FC"]) > 1 and results[mirna]["q_value"] < 0.05:
                ax.annotate(
                    mirna,
                    (log2fc_vals[j], neg_log10_q[j]),
                    xytext=(5, 5),
                    textcoords="offset points",
                    fontsize=8,
                )

        ax.set_xlabel("log2 Fold Change")
        ax.set_ylabel("-log10(q-value)")
        ax.set_title(f"{comp_name}")
        ax.legend()
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(get_output_path("Volcano_Plots.png"), dpi=300, bbox_inches="tight")
    plt.show()

    # Step 4: Generate candidate biomarkers lists
    print(f"\nStep 4: Generating candidate biomarkers")
    print("-" * 35)

    candidate_biomarkers = {}

    for comp_name, results in all_results.items():
        candidates = []
        for mirna, data in results.items():
            if abs(data["log2FC"]) > 1 and data["q_value"] < 0.05:
                candidates.append(
                    {
                        "miRNA": mirna,
                        "log2FC": data["log2FC"],
                        "q_value": data["q_value"],
                        "effect_size": data["effect_size"],
                    }
                )

        candidate_biomarkers[comp_name] = candidates

        print(f"{comp_name}: {len(candidates)} candidate biomarkers")
        if candidates:
            candidates_df = pd.DataFrame(candidates)
            candidates_df.to_csv(
                f"get_output_path("candidate_biomarkers_{comp_name}.csv", index=False
            )
            print(candidates_df)

    # Step 5: Boxplots for top significant miRNAs
    print(f"\nStep 5: Creating boxplots for top significant miRNAs")
    print("-" * 45)

    for comp_name, results in all_results.items():
        # Get top 3-5 most significant miRNAs
        sorted_mirnas = sorted(results.keys(), key=lambda x: results[x]["q_value"])
        top_mirnas = sorted_mirnas[: min(5, len(sorted_mirnas))]

        if top_mirnas:
            group1, group2 = comp_name.split("_vs_")
            comparison_groups = [group1, group2] if group1 == "H" else [group1, group2]

            fig, axes = plt.subplots(
                1, len(top_mirnas), figsize=(4 * len(top_mirnas), 6)
            )
            if len(top_mirnas) == 1:
                axes = [axes]

            fig.suptitle(f"Top miRNAs: {comp_name}", fontsize=16, fontweight="bold")

            for i, mirna in enumerate(top_mirnas):
                ax = axes[i]
                rq_col = f"RQ_{mirna}"

                # Create boxplot data
                plot_data = []
                plot_labels = []

                for group in comparison_groups:
                    group_data = df[df["GROUP"] == group][rq_col].values
                    plot_data.append(group_data)
                    plot_labels.append(group)

                # Create boxplot
                bp = ax.boxplot(plot_data, labels=plot_labels, patch_artist=True)

                # Color boxes
                colors = ["lightblue", "lightcoral"]
                for patch, color in zip(bp["boxes"], colors):
                    patch.set_facecolor(color)

                ax.set_ylabel("RQ Value")
                ax.set_title(f'{mirna}\nq={results[mirna]["q_value"]:.3f}')
                ax.grid(True, alpha=0.3)

            plt.tight_layout()
            plt.savefig(
                f"get_output_path("boxplots_{comp_name}.png", dpi=300, bbox_inches="tight"
            )
            plt.show()

    return all_results, candidate_biomarkers


def correlation_analysis(df, candidate_biomarkers):
    """
    Correlation analysis between candidate biomarkers and clinical variables
    Acting as Hypothesis-Generating Engine: Connect molecular and clinical findings
    """
    print("\n5. CORRELATION ANALYSIS WITH CLINICAL VARIABLES")
    print("-" * 50)

    # Clinical variables (using prompt aliases)
    clinical_vars = {
        "pocket_depth": "PPD",
        "gingival_index": "CAL",
        "bleeding_on_probing": "BoP",
    }

    # Collect all unique candidate biomarkers
    all_candidates = set()
    for comp_candidates in candidate_biomarkers.values():
        for candidate in comp_candidates:
            all_candidates.add(candidate["miRNA"])

    all_candidates = list(all_candidates)

    if not all_candidates:
        print("⚠️  No candidate biomarkers found for correlation analysis")
        return {}

    print(f"Analyzing correlations for {len(all_candidates)} candidate biomarkers")
    print(f"Candidates: {all_candidates}")

    # Overall correlation analysis
    print("\n📊 OVERALL CORRELATION ANALYSIS")
    print("-" * 30)

    overall_correlations = {}

    for mirna in all_candidates:
        rq_col = f"RQ_{mirna}"
        mirna_correlations = {}

        for clinical_var, alias in clinical_vars.items():
            # Test for normality
            mirna_normal = stats.shapiro(df[rq_col])[1] > 0.05
            clinical_normal = stats.shapiro(df[clinical_var])[1] > 0.05

            # Choose correlation method
            if mirna_normal and clinical_normal:
                corr, p_val = stats.pearsonr(df[rq_col], df[clinical_var])
                method = "Pearson"
            else:
                corr, p_val = stats.spearmanr(df[rq_col], df[clinical_var])
                method = "Spearman"

            mirna_correlations[alias] = {
                "correlation": corr,
                "p_value": p_val,
                "method": method,
            }

        overall_correlations[mirna] = mirna_correlations

    # Within-group correlation analysis
    print("\n📊 WITHIN-GROUP CORRELATION ANALYSIS")
    print("-" * 35)

    group_correlations = {}

    for group in ["S", "G", "P"]:
        group_df = df[df["GROUP"] == group]
        group_correlations[group] = {}

        print(f"\n{group} group (n={len(group_df)}):")

        for mirna in all_candidates:
            rq_col = f"RQ_{mirna}"
            mirna_correlations = {}

            for clinical_var, alias in clinical_vars.items():
                if len(group_df) < 5:  # Skip if too few samples
                    mirna_correlations[alias] = {
                        "correlation": np.nan,
                        "p_value": np.nan,
                        "method": "insufficient_data",
                    }
                    continue

                # Test for normality
                mirna_normal = stats.shapiro(group_df[rq_col])[1] > 0.05
                clinical_normal = stats.shapiro(group_df[clinical_var])[1] > 0.05

                # Choose correlation method
                if mirna_normal and clinical_normal:
                    corr, p_val = stats.pearsonr(
                        group_df[rq_col], group_df[clinical_var]
                    )
                    method = "Pearson"
                else:
                    corr, p_val = stats.spearmanr(
                        group_df[rq_col], group_df[clinical_var]
                    )
                    method = "Spearman"

                mirna_correlations[alias] = {
                    "correlation": corr,
                    "p_value": p_val,
                    "method": method,
                }

            group_correlations[group][mirna] = mirna_correlations

            # Print correlations for this miRNA in this group
            corr_str = ", ".join(
                [
                    f"{alias}: r={data['correlation']:.3f}(p={data['p_value']:.3f})"
                    for alias, data in mirna_correlations.items()
                    if not np.isnan(data["correlation"])
                ]
            )
            print(f"  {mirna}: {corr_str}")

    # Apply FDR correction to overall correlations
    print("\n📊 FDR CORRECTION FOR OVERALL CORRELATIONS")
    print("-" * 40)

    all_p_values = []
    correlation_pairs = []

    for mirna in all_candidates:
        for alias in clinical_vars.values():
            all_p_values.append(overall_correlations[mirna][alias]["p_value"])
            correlation_pairs.append((mirna, alias))

    if all_p_values:
        rejected, q_values, _, _ = multipletests(all_p_values, method="fdr_bh")

        # Add q-values to results
        for i, (mirna, alias) in enumerate(correlation_pairs):
            overall_correlations[mirna][alias]["q_value"] = q_values[i]
            overall_correlations[mirna][alias]["significant_fdr"] = rejected[i]

    # Create correlation heatmap
    print("\n📊 CORRELATION HEATMAP")
    print("-" * 20)

    # Prepare data for heatmap
    heatmap_data = []
    for mirna in all_candidates:
        row = []
        for alias in clinical_vars.values():
            corr = overall_correlations[mirna][alias]["correlation"]
            row.append(corr)
        heatmap_data.append(row)

    heatmap_df = pd.DataFrame(
        heatmap_data, index=all_candidates, columns=list(clinical_vars.values())
    )

    # Create heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        heatmap_df,
        annot=True,
        cmap="RdBu_r",
        center=0,
        square=True,
        linewidths=0.5,
        fmt=".3f",
    )
    plt.title("miRNA-Clinical Variable Correlations", fontweight="bold")
    plt.tight_layout()
    plt.savefig(
        "get_output_path("correlation_heatmap_mirna_clinical.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.show()

    # Create scatter plots for significant correlations
    print("\n📊 SCATTER PLOTS FOR SIGNIFICANT CORRELATIONS")
    print("-" * 45)

    significant_correlations = []

    for mirna in all_candidates:
        for alias in clinical_vars.values():
            if overall_correlations[mirna][alias]["significant_fdr"]:
                significant_correlations.append((mirna, alias))

    if significant_correlations:
        n_plots = len(significant_correlations)
        n_cols = min(3, n_plots)
        n_rows = (n_plots + n_cols - 1) // n_cols

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(6 * n_cols, 5 * n_rows))
        if n_plots == 1:
            axes = [axes]
        elif n_rows == 1:
            axes = axes.reshape(1, -1)

        fig.suptitle(
            "Significant miRNA-Clinical Correlations", fontsize=16, fontweight="bold"
        )

        for i, (mirna, alias) in enumerate(significant_correlations):
            ax = axes[i // n_cols, i % n_cols] if n_rows > 1 else axes[i]

            # Get actual column name
            clinical_col = [k for k, v in clinical_vars.items() if v == alias][0]
            rq_col = f"RQ_{mirna}"

            # Create scatter plot
            x = df[rq_col]
            y = df[clinical_col]

            ax.scatter(
                x,
                y,
                alpha=0.6,
                c=df["GROUP"].map({"S": "blue", "G": "orange", "P": "red"}),
            )

            # Add regression line
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            ax.plot(x, p(x), "black", alpha=0.8, linestyle="--")

            # Labels and title
            ax.set_xlabel(f"{mirna} RQ")
            ax.set_ylabel(alias)

            corr_data = overall_correlations[mirna][alias]
            ax.set_title(
                f'{mirna} vs {alias}\nr={corr_data["correlation"]:.3f}, q={corr_data["q_value"]:.3f}'
            )

            ax.grid(True, alpha=0.3)

        # Hide empty subplots
        for i in range(n_plots, n_rows * n_cols):
            if n_rows > 1:
                axes[i // n_cols, i % n_cols].set_visible(False)
            else:
                axes[i].set_visible(False)

        plt.tight_layout()
        plt.savefig(
            "get_output_path("scatter_plots_significant_correlations.png",
            dpi=300,
            bbox_inches="tight",
        )
        plt.show()

        print(
            f"✓ Created scatter plots for {len(significant_correlations)} significant correlations"
        )
    else:
        print("No significant correlations found after FDR correction")

    # Generate "Top Candidates for Functional Follow-up"
    print("\n🔬 TOP CANDIDATES FOR FUNCTIONAL FOLLOW-UP")
    print("-" * 45)

    functional_candidates = []

    for mirna in all_candidates:
        # Check if this miRNA was significant in differential expression
        diff_expr_significant = any(
            any(candidate["miRNA"] == mirna for candidate in comp_candidates)
            for comp_candidates in candidate_biomarkers.values()
        )

        # Check if this miRNA has significant correlations
        corr_significant = any(
            overall_correlations[mirna][alias]["significant_fdr"]
            for alias in clinical_vars.values()
        )

        if diff_expr_significant and corr_significant:
            # Get correlation details
            corr_details = {}
            for alias in clinical_vars.values():
                if overall_correlations[mirna][alias]["significant_fdr"]:
                    corr_details[alias] = overall_correlations[mirna][alias][
                        "correlation"
                    ]

            functional_candidates.append(
                {
                    "miRNA": mirna,
                    "differential_expression": diff_expr_significant,
                    "significant_correlations": corr_details,
                }
            )

    if functional_candidates:
        print(
            f"✓ {len(functional_candidates)} miRNAs qualify for functional follow-up:"
        )

        for candidate in functional_candidates:
            mirna = candidate["miRNA"]
            corr_str = ", ".join(
                [
                    f"{alias}(r={corr:.3f})"
                    for alias, corr in candidate["significant_correlations"].items()
                ]
            )
            print(f"  - {mirna}: {corr_str}")

        # Save functional candidates
        functional_df = pd.DataFrame(functional_candidates)
        functional_df.to_csv(
            "get_output_path("functional_follow_up_candidates.csv", index=False
        )
    else:
        print("⚠️  No miRNAs meet both differential expression and correlation criteria")

    # Save all correlation results
    overall_corr_df = pd.DataFrame(
        {
            (mirna, alias): overall_correlations[mirna][alias]
            for mirna in all_candidates
            for alias in clinical_vars.values()
        }
    ).T
    overall_corr_df.to_csv(get_output_path("Overall_Correlations.csv", "tables"))

    return {
        "overall_correlations": overall_correlations,
        "group_correlations": group_correlations,
        "functional_candidates": functional_candidates,
    }


def main():
    """Main function for Part 2 analysis"""
    # Load processed data
    df = pd.read_csv("results/processed_data.csv")
    rq_cols = [col for col in df.columns if col.startswith("RQ_")]

    print("🧬 CONTINUING miRNA ANALYSIS - PART 2")
    print(f"Loaded processed data: {df.shape[0]} samples, {len(rq_cols)} RQ columns")

    # Part 2: Core Biomarker Discovery
    all_results, candidate_biomarkers = differential_expression_analysis(df, rq_cols)
    correlation_results = correlation_analysis(df, candidate_biomarkers)

    print("\n" + "=" * 80)
    print("PART 2 COMPLETED - CORE BIOMARKER DISCOVERY")
    print("=" * 80)

    # Summary statistics
    total_candidates = sum(
        len(candidates) for candidates in candidate_biomarkers.values()
    )
    functional_candidates = len(correlation_results["functional_candidates"])

    print(f"✓ Differential expression analysis completed")
    print(
        f"✓ {total_candidates} candidate biomarkers identified across all comparisons"
    )
    print(f"✓ Correlation analysis with clinical variables completed")
    print(f"✓ {functional_candidates} miRNAs qualify for functional follow-up")

    print("\nCandidate biomarkers by comparison:")
    for comp_name, candidates in candidate_biomarkers.items():
        print(f"  - {comp_name}: {len(candidates)} candidates")

    if correlation_results["functional_candidates"]:
        print("\nTop functional candidates:")
        for candidate in correlation_results["functional_candidates"]:
            print(f"  - {candidate['miRNA']}")

    print("\nReady for Part 3: Predictive Power & Model Assessment")


if __name__ == "__main__":
    main()
