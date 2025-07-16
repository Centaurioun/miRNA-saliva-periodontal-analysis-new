#!/usr/bin/env python3
"""
miRNA Periodontal Disease Analysis - Part 3: Predictive Power & Model Assessment
===============================================================================

Machine learning analysis to assess diagnostic power of candidate miRNA biomarkers.

Author: AI-driven Analytical Scientist
Date: July 16, 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    roc_auc_score,
    roc_curve,
    confusion_matrix,
    classification_report,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.inspection import permutation_importance, partial_dependence
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


def predictive_modeling_analysis(df, candidate_biomarkers):
    """
    Comprehensive predictive modeling analysis
    Acting as Lead Validator: Ensure no data leakage and proper validation
    """
    print("=" * 80)
    print("PART 3: PREDICTIVE POWER & MODEL ASSESSMENT")
    print("=" * 80)
    print("\n6. PREDICTIVE MODELING")
    print("-" * 30)

    # Extract all unique candidate miRNAs
    all_candidates = set()
    for comp_candidates in candidate_biomarkers.values():
        for candidate in comp_candidates:
            all_candidates.add(candidate["miRNA"])

    candidate_features = [f"RQ_{mirna}" for mirna in all_candidates]

    print(f"Using {len(candidate_features)} candidate biomarkers as features:")
    print(f"Features: {list(all_candidates)}")

    # Define binary classification problem: Periodontitis vs Healthy
    print(f"\nBinary Classification Problem: Periodontitis (P) vs Healthy (S)")
    print("-" * 55)

    # Filter data for binary classification
    binary_df = df[df["GROUP"].isin(["S", "P"])].copy()

    # Create binary target variable
    binary_df["target"] = (binary_df["GROUP"] == "P").astype(int)

    print(f"Dataset for binary classification:")
    print(f"- Total samples: {len(binary_df)}")
    print(f"- Healthy (S): {sum(binary_df['target'] == 0)}")
    print(f"- Periodontitis (P): {sum(binary_df['target'] == 1)}")

    # Prepare features and target
    X = binary_df[candidate_features].values
    y = binary_df["target"].values

    print(f"\nFeature matrix shape: {X.shape}")
    print(f"Target vector shape: {y.shape}")

    # Acting as Lead Validator: Ensure proper data splitting
    print(f"\n🔒 DATA SPLITTING & SCALING (AVOIDING DATA LEAKAGE)")
    print("-" * 50)

    # Stratified train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Training set: {X_train.shape[0]} samples")
    print(f"- Healthy: {sum(y_train == 0)}")
    print(f"- Periodontitis: {sum(y_train == 1)}")

    print(f"Test set: {X_test.shape[0]} samples")
    print(f"- Healthy: {sum(y_test == 0)}")
    print(f"- Periodontitis: {sum(y_test == 1)}")

    # Feature scaling - CRITICALLY fit only on training data
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)  # Transform, not fit_transform!

    print(f"\n✓ StandardScaler fitted on training data only")
    print(f"✓ Both training and test sets transformed")

    # Model training with repeated stratified cross-validation
    print(f"\n🤖 MODEL TRAINING & VALIDATION")
    print("-" * 35)

    # Define models
    models = {
        "Logistic Regression": LogisticRegression(random_state=42, max_iter=1000),
        "Random Forest": RandomForestClassifier(random_state=42, n_estimators=100),
    }

    # Repeated stratified k-fold cross-validation
    cv_results = {}
    n_repeats = 5

    for model_name, model in models.items():
        print(f"\n{model_name}:")
        print("-" * len(model_name))

        # Perform repeated cross-validation
        cv_scores = []
        for repeat in range(n_repeats):
            cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42 + repeat)
            scores = cross_val_score(
                model, X_train_scaled, y_train, cv=cv, scoring="roc_auc"
            )
            cv_scores.extend(scores)

        cv_results[model_name] = {
            "cv_scores": cv_scores,
            "mean_cv_score": np.mean(cv_scores),
            "std_cv_score": np.std(cv_scores),
        }

        print(
            f"Cross-validation AUC: {np.mean(cv_scores):.3f} ± {np.std(cv_scores):.3f}"
        )

        # Train final model on full training set
        model.fit(X_train_scaled, y_train)

        # Evaluate on test set
        y_pred = model.predict(X_test_scaled)
        y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]

        # Calculate metrics
        test_auc = roc_auc_score(y_test, y_pred_proba)
        test_accuracy = accuracy_score(y_test, y_pred)
        test_precision = precision_score(y_test, y_pred)
        test_recall = recall_score(y_test, y_pred)
        test_f1 = f1_score(y_test, y_pred)

        cv_results[model_name].update(
            {
                "test_auc": test_auc,
                "test_accuracy": test_accuracy,
                "test_precision": test_precision,
                "test_recall": test_recall,
                "test_f1": test_f1,
                "y_pred": y_pred,
                "y_pred_proba": y_pred_proba,
            }
        )

        print(f"Test AUC: {test_auc:.3f}")
        print(f"Test Accuracy: {test_accuracy:.3f}")
        print(f"Test Precision: {test_precision:.3f}")
        print(f"Test Recall: {test_recall:.3f}")
        print(f"Test F1-Score: {test_f1:.3f}")

    # Create comprehensive results table
    results_data = []
    for model_name, results in cv_results.items():
        results_data.append(
            {
                "Model": model_name,
                "CV_AUC_Mean": results["mean_cv_score"],
                "CV_AUC_Std": results["std_cv_score"],
                "Test_AUC": results["test_auc"],
                "Test_Accuracy": results["test_accuracy"],
                "Test_Precision": results["test_precision"],
                "Test_Recall": results["test_recall"],
                "Test_F1": results["test_f1"],
            }
        )

    results_df = pd.DataFrame(results_data)
    results_df = results_df.round(3)
    results_df.to_csv(get_output_path("Model_Performance_Metrics.csv", "tables"), index=False)

    print(f"\n📊 COMPREHENSIVE MODEL PERFORMANCE")
    print("-" * 35)
    print(results_df.to_string(index=False))

    # ROC Curves
    print(f"\n📈 ROC CURVES")
    print("-" * 12)

    plt.figure(figsize=(10, 8))

    for model_name, results in cv_results.items():
        # Calculate ROC curve
        fpr, tpr, _ = roc_curve(y_test, results["y_pred_proba"])
        auc = results["test_auc"]

        plt.plot(fpr, tpr, linewidth=2, label=f"{model_name} (AUC = {auc:.3f})")

    # Add diagonal line
    plt.plot([0, 1], [0, 1], "k--", alpha=0.5, label="Random (AUC = 0.5)")

    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curves: Periodontitis vs Healthy Classification", fontweight="bold")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(get_output_path("ROC_Curves.png"), dpi=300, bbox_inches="tight")
    plt.show()

    # Confusion Matrices
    print(f"\n📊 CONFUSION MATRICES")
    print("-" * 20)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Confusion Matrices", fontsize=16, fontweight="bold")

    for i, (model_name, results) in enumerate(cv_results.items()):
        ax = axes[i]

        # Calculate confusion matrix
        cm = confusion_matrix(y_test, results["y_pred"])

        # Create heatmap
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            ax=ax,
            xticklabels=["Healthy", "Periodontitis"],
            yticklabels=["Healthy", "Periodontitis"],
        )

        ax.set_title(f"{model_name}")
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")

    plt.tight_layout()
    plt.savefig(get_output_path("Confusion_Matrices.png"), dpi=300, bbox_inches="tight")
    plt.show()

    # Feature Importance Analysis
    print(f"\n🔍 FEATURE IMPORTANCE ANALYSIS")
    print("-" * 30)

    # Random Forest feature importance
    rf_model = models["Random Forest"]
    rf_importance = rf_model.feature_importances_

    # Create feature importance plot
    plt.figure(figsize=(10, 6))

    # Sort features by importance
    importance_df = pd.DataFrame(
        {"Feature": list(all_candidates), "Importance": rf_importance}
    ).sort_values("Importance", ascending=True)

    plt.barh(range(len(importance_df)), importance_df["Importance"])
    plt.yticks(range(len(importance_df)), importance_df["Feature"])
    plt.xlabel("Feature Importance")
    plt.title("Random Forest Feature Importance", fontweight="bold")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(get_output_path("Feature_Importance.png"), dpi=300, bbox_inches="tight")
    plt.show()

    # Get top 3 features for partial dependence plots
    top_features = importance_df.tail(3)["Feature"].tolist()
    top_feature_indices = [
        list(all_candidates).index(feature) for feature in top_features
    ]

    print(f"Top 3 most important features: {top_features}")

    # Partial Dependence Plots
    print(f"\n📊 PARTIAL DEPENDENCE PLOTS")
    print("-" * 25)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(
        "Partial Dependence Plots - Top 3 Features", fontsize=16, fontweight="bold"
    )

    for i, (feature, feature_idx) in enumerate(zip(top_features, top_feature_indices)):
        ax = axes[i]

        # Calculate partial dependence
        pdp_result = partial_dependence(
            rf_model,
            X_train_scaled,
            features=[feature_idx],
            kind="average",
            grid_resolution=50,
        )

        # Plot partial dependence
        ax.plot(pdp_result["grid_values"][0], pdp_result["average"][0], linewidth=2)
        ax.set_xlabel(f"{feature} (scaled)")
        ax.set_ylabel("Partial Dependence")
        ax.set_title(f"{feature}")
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(
        "get_output_path("partial_dependence_plots.png", dpi=300, bbox_inches="tight"
    )
    plt.show()

    # Acting as Hypothesis-Generating Engine: Interpret results
    print(f"\n🔬 HYPOTHESIS GENERATION & INTERPRETATION")
    print("-" * 40)

    # Model performance interpretation
    best_model = max(cv_results.items(), key=lambda x: x[1]["test_auc"])
    best_model_name, best_results = best_model

    print(
        f"Best performing model: {best_model_name} (AUC = {best_results['test_auc']:.3f})"
    )

    # Performance interpretation
    if best_results["test_auc"] > 0.9:
        performance_level = "Excellent"
    elif best_results["test_auc"] > 0.8:
        performance_level = "Good"
    elif best_results["test_auc"] > 0.7:
        performance_level = "Fair"
    else:
        performance_level = "Poor"

    print(f"Diagnostic performance: {performance_level}")

    # Feature importance interpretation
    most_important_feature = top_features[-1]
    print(f"Most important biomarker: {most_important_feature}")

    # Clinical utility assessment
    print(f"\n💡 CLINICAL UTILITY ASSESSMENT:")
    print(f"- Sensitivity (Recall): {best_results['test_recall']:.3f}")
    print(f"- Specificity: {1 - (1 - best_results['test_precision']):.3f}")
    print(f"- Positive Predictive Value: {best_results['test_precision']:.3f}")

    # Save comprehensive results
    cv_results_df = pd.DataFrame(cv_results).T
    cv_results_df.to_csv(get_output_path("Detailed_Model_Results.csv", "tables"))

    # Save feature importance
    importance_df.to_csv(get_output_path("Feature_Importance.csv", "tables"), index=False)

    return cv_results, top_features


def main():
    """Main function for Part 3 analysis"""
    # Load processed data and candidate biomarkers
    df = pd.read_csv("results/processed_data.csv")

    # Reconstruct candidate biomarkers from saved files
    candidate_biomarkers = {}

    # Try to load candidate biomarker files
    import os

    for filename in os.listdir("results/tables"):
        if filename.startswith("candidate_biomarkers_") and filename.endswith(".csv"):
            comp_name = filename.replace("candidate_biomarkers_", "").replace(
                ".csv", ""
            )
            try:
                comp_df = pd.read_csv(f"get_output_path("{filename}")
                candidate_biomarkers[comp_name] = comp_df.to_dict("records")
            except:
                pass

    # If no candidate files found, use all miRNAs that showed significance
    if not candidate_biomarkers:
        print("⚠️  No candidate biomarker files found, using all miRNAs")
        all_mirnas = ["mir146a", "mir146b", "mir155", "mir203", "mir223", "mir381p"]
        candidate_biomarkers = {
            "H_vs_P": [
                {"miRNA": mirna, "log2FC": 1.5, "q_value": 0.001, "effect_size": 0.8}
                for mirna in all_mirnas
            ]
        }

    print("🧬 CONTINUING miRNA ANALYSIS - PART 3")
    print(f"Loaded processed data: {df.shape[0]} samples")
    print(f"Candidate biomarkers loaded from {len(candidate_biomarkers)} comparisons")

    # Part 3: Predictive Modeling
    cv_results, top_features = predictive_modeling_analysis(df, candidate_biomarkers)

    print("\n" + "=" * 80)
    print("PART 3 COMPLETED - PREDICTIVE POWER & MODEL ASSESSMENT")
    print("=" * 80)

    # Summary statistics
    best_model = max(cv_results.items(), key=lambda x: x[1]["test_auc"])
    best_model_name, best_results = best_model

    print(f"✓ Binary classification model trained and validated")
    print(f"✓ Best model: {best_model_name} (AUC = {best_results['test_auc']:.3f})")
    print(f"✓ Feature importance analysis completed")
    print(f"✓ Top 3 features: {top_features}")
    print(f"✓ Partial dependence plots generated")

    print("\nModel Performance Summary:")
    for model_name, results in cv_results.items():
        print(
            f"  - {model_name}: AUC = {results['test_auc']:.3f}, "
            f"Accuracy = {results['test_accuracy']:.3f}"
        )

    print("\nReady for Part 4: Proactive & Unforeseen Analyses")


if __name__ == "__main__":
    main()
