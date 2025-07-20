## pip install pandas openpyxl markdown weasyprint python-docx
## ```*   **`markdown`**: Converts the report text to HTML.
## *   **`weasyprint`**: Creates a PDF from the HTML content.
## *   **`python-docx`**: Creates the Microsoft Word `.docx` file.
##
## ---
##
## ### Step 2: Use the Standalone Report Generation Script
##
## The script below is designed to be run *after* you have executed your Jupyter Notebook. It reads the CSV tables and image files ## that the notebook generated and uses them to build the final, comprehensive reports in multiple formats.
##
## 1.  Create a new file named `generate_reports.py` in the same root directory as your Jupyter notebook.
## 2.  Copy and paste the entire code block below into that file.
## 3.  Save the file.
## 4.  Run the script from your terminal: `python generate_reports.py`
##
## You will see detailed output in your terminal, including any errors if they occur, and the final reports will be generated in the `outputs/jupyter_notebook/comprehensive_results/` directory.
##
#### `generate_reports.py`

#!/usr/bin/env python3

# Standalone Report Generation Script for Jupyter Notebook Analysis Results

import pandas as pd
import os
import sys
import base64
from datetime import datetime

# --- Configuration: Match this to your notebook's setup ---
BASE_OUTPUT_DIR = "outputs/jupyter_notebook"
DATA_FILE = "miRNA-saliva-qPCR-results.csv"

# Define output directories
OUTPUT_DIRS = {
    "base": BASE_OUTPUT_DIR,
    "plots": f"{BASE_OUTPUT_DIR}/plots",
    "tables": f"{BASE_OUTPUT_DIR}/tables",
    "reports": f"{BASE_OUTPUT_DIR}/comprehensive_results",
}

# --- Check for required libraries and provide clear instructions if missing ---
try:
    import markdown
    from weasyprint import HTML
    from docx import Document
    from docx.shared import Inches
except ImportError as e:
    print(f"❌ ERROR: A required library is missing: {e.name}")
    print(
        "Please install the necessary packages by running this command in your terminal:"
    )
    print("\npip install pandas openpyxl markdown weasyprint python-docx\n")
    sys.exit(1)


def get_output_path(filename, output_type="plots"):
    """Helper function to get the full path for a given file and type."""
    return os.path.join(OUTPUT_DIRS[output_type], filename)


def get_base64_image(image_path):
    """Encodes an image file into a base64 string for embedding in HTML/Markdown."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except FileNotFoundError:
        print(
            f"⚠️ Warning: Image file not found at {image_path}. It will be omitted from reports."
        )
        return ""
    except Exception as e:
        print(f"Error encoding image {image_path}: {str(e)}")
        return ""


def generate_reports():
    """
    Main function to load analysis results and generate comprehensive reports.
    """
    print("🚀 Starting report generation process...")

    # --- 1. Load all necessary data from files created by the notebook ---
    print("📊 Loading analysis results from CSV files...")
    try:
        demo_stats_df = pd.read_csv(
            get_output_path("Demographic_Clinical_Stats.csv", "tables")
        )
        calibrator_df = pd.read_csv(
            get_output_path("Calibration_Table.csv", "tables"), index_col=0
        )
        h_vs_p_results = pd.read_csv(get_output_path("H_vs_P_Results.csv", "tables"))
        g_vs_p_results = pd.read_csv(get_output_path("G_vs_P_Results.csv", "tables"))
        h_vs_g_results = pd.read_csv(get_output_path("H_vs_G_Results.csv", "tables"))
        model_results_df = pd.read_csv(
            get_output_path("Model_Performance_Metrics.csv", "tables")
        )

        # Combine significant results from pairwise comparisons
        significant_df = pd.concat(
            [
                h_vs_p_results[
                    (h_vs_p_results["FDR_Significant"])
                    & (h_vs_p_results["Log2FC_Threshold"])
                ],
                g_vs_p_results[
                    (g_vs_p_results["FDR_Significant"])
                    & (g_vs_p_results["Log2FC_Threshold"])
                ],
                h_vs_g_results[
                    (h_vs_g_results["FDR_Significant"])
                    & (h_vs_g_results["Log2FC_Threshold"])
                ],
            ]
        ).sort_values("Q_Value")

    except FileNotFoundError as e:
        print(f"❌ FATAL ERROR: Cannot find required input file: {e.filename}")
        print(
            "Please ensure you have run the main Jupyter Notebook first to generate the necessary files."
        )
        return

    # --- 2. Build the Markdown Report Content ---
    print("📝 Building Markdown content...")

    # Define report sections as a list of strings
    embedded_md_content = [
        f"# Comprehensive miRNA Periodontal Disease Analysis Results",
        f"**Date:** {datetime.now().strftime('%B %d, %Y')}  ",
        f"**Dataset:** {DATA_FILE}  ",
        f"**Groups:** S=Healthy, G=Gingivitis, P=Periodontitis  \n",
        "## 1. Demographic & Clinical Characteristics",
        demo_stats_df.to_markdown(index=False),
        "\n## 2. ΔΔCt Transformation & QC",
        "### Calibrator Values (Healthy Group Mean ΔCt)",
        calibrator_df.to_markdown(),
    ]

    # Add volcano plot
    volcano_img_path = get_output_path("Volcano_Plots.png", "plots")
    b64_volcano = get_base64_image(volcano_img_path)
    if b64_volcano:
        embedded_md_content.extend(
            [
                "\n## 3. Differential Expression Analysis",
                "### Volcano Plots",
                f"![Volcano Plots](data:image/png;base64,{b64_volcano})\n",
                "### Significant Differential Expression Results (FDR < 0.05 & |Log2FC| > 1)",
                significant_df[
                    ["miRNA", "Comparison", "Log2_FC", "Q_Value", "Effect_Size"]
                ].to_markdown(index=False, floatfmt=".3f"),
            ]
        )

    # Add machine learning results
    roc_img_path = get_output_path("ROC_Curves.png", "plots")
    b64_roc = get_base64_image(roc_img_path)
    if b64_roc:
        embedded_md_content.extend(
            [
                "\n## 4. Machine Learning Performance",
                model_results_df[["Problem", "Model", "AUC", "Accuracy"]].to_markdown(
                    index=False, floatfmt=".3f"
                ),
                "### ROC Curves",
                f"![ROC Curves](data:image/png;base64,{b64_roc})\n",
            ]
        )

    # Add dimensionality reduction
    dr_img_path = get_output_path("Dimensionality_Reduction.png", "plots")
    b64_dr = get_base64_image(dr_img_path)
    if b64_dr:
        embedded_md_content.extend(
            [
                "\n## 5. Dimensionality Reduction Analysis",
                f"![Dimensionality Reduction Plots](data:image/png;base64,{b64_dr})\n",
            ]
        )

    # Define and add recommendations
    recommendations = [
        "Validate findings with a larger, independent patient cohort.",
        "Investigate the functional roles of mir-203, mir-223, and mir-381p in periodontitis progression using in-vitro studies.",
        "Explore the combined diagnostic potential of miRNA signatures and clinical markers in a longitudinal study to predict disease progression.",
    ]
    embedded_md_content.append("\n## 6. Recommendations")
    embedded_md_content.extend([f"- {rec}" for rec in recommendations])

    # --- 3. Save the Generated Reports ---
    print("💾 Saving reports to multiple formats...")
    os.makedirs(OUTPUT_DIRS["reports"], exist_ok=True)
    report_string = "\n".join(embedded_md_content)

    # Save Markdown (.md)
    md_path = os.path.join(OUTPUT_DIRS["reports"], "Comprehensive_Analysis_Report.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(report_string)
    print(f"  ✅ Markdown report saved to: {md_path}")

    # Generate and save HTML (.html)
    html_path = os.path.join(
        OUTPUT_DIRS["reports"], "Comprehensive_Analysis_Report.html"
    )
    html_content = markdown.markdown(report_string, extensions=["tables"])
    html_full = f"""
       <!DOCTYPE html><html><head><meta charset="utf-8"><title>miRNA Analysis Results</title>
       <style>
           body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 40px; line-height: 1.6; }}
           img {{ max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; padding: 5px; }}
           table {{ border-collapse: collapse; width: auto; margin-bottom: 20px; }}
           th, td {{ border: 1px solid #ddd; padding: 8px; }}
           th {{ background-color: #f2f2f2; }}
       </style></head><body>{html_content}</body></html>
    """
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_full)
    print(f"  ✅ HTML report saved to: {html_path}")

    # Generate and save PDF (.pdf)
    pdf_path = os.path.join(OUTPUT_DIRS["reports"], "Comprehensive_Analysis_Report.pdf")
    HTML(string=html_full).write_pdf(pdf_path)
    print(f"  ✅ PDF report saved to: {pdf_path}")

    print("\n🎉 Report generation complete!")


if __name__ == "__main__":
    generate_reports()
