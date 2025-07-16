#!/bin/bash

echo "Monitoring file creation in repository root..."
echo "Current files in root directory:"
ls -la

echo -e "\nWatching for file creation events..."
echo "Press Ctrl+C to stop monitoring"

# Monitor file creation in the current directory
while true; do
    sleep 1
    
    # Check for the problematic files
    if [ -f "COMPREHENSIVE_ANALYSIS_RESULTS_EMBEDDED.md" ] || 
       [ -f "COMPREHENSIVE_ANALYSIS_RESULTS_REPORT.md" ] || 
       [ -f "FINAL_ANALYSIS_REPORT.md" ] || 
       [ -f "fix_columns.py" ] || 
       [ -f "miRNA_analysis.py" ] || 
       [ -f "miRNA_analysis_part2.py" ] || 
       [ -f "miRNA_analysis_part3.py" ] || 
       [ -f "miRNA_analysis_part4.py" ] || 
       [ -f "miRNA_analysis_part4_corrected.py" ] || 
       [ -f "rename_files.py" ]; then
        
        echo "$(date): FILES DETECTED! The following files were created:"
        for file in "COMPREHENSIVE_ANALYSIS_RESULTS_EMBEDDED.md" "COMPREHENSIVE_ANALYSIS_RESULTS_REPORT.md" "FINAL_ANALYSIS_REPORT.md" "fix_columns.py" "miRNA_analysis.py" "miRNA_analysis_part2.py" "miRNA_analysis_part3.py" "miRNA_analysis_part4.py" "miRNA_analysis_part4_corrected.py" "rename_files.py"; do
            if [ -f "$file" ]; then
                echo "  - $file ($(stat -c %Y "$file" | xargs -I {} date -d @{}))"
            fi
        done
        
        echo "Removing files..."
        rm -f COMPREHENSIVE_ANALYSIS_RESULTS_EMBEDDED.md COMPREHENSIVE_ANALYSIS_RESULTS_REPORT.md FINAL_ANALYSIS_REPORT.md fix_columns.py miRNA_analysis.py miRNA_analysis_part*.py rename_files.py
        echo "Files removed."
    fi
done
