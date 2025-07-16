# Data & Variable Dictionary

## 1. Data Files

| File                            | Description                |
|---------------------------------|----------------------------|
| `miRNA-saliva-qPCR-results.csv` | Raw qPCR and clinical data |

## 2. Variable Definitions

| Column                  | Description                                             |
|-------------------------|---------------------------------------------------------|
| GROUP                   | Subject group: S=Healthy, G=Gingivitis, P=Periodontitis |
| SEX                     | Biological sex (M/F)                                    |
| AGE                     | Age (years)                                             |
| plaque_index            | Plaque index (clinical)                                 |
| gingival_index          | Gingival index (clinical)                               |
| pocket_depth            | Mean pocket depth (mm)                                  |
| bleeding_on_probing     | Bleeding on probing (%)                                 |
| number_of_missing_teeth | Number of missing teeth                                 |
| mean_mir146a            | Mean Ct for miR-146a                                    |
| mean_mir146b            | Mean Ct for miR-146b                                    |
| mean_mir155             | Mean Ct for miR-155                                     |
| mean_mir203             | Mean Ct for miR-203                                     |
| mean_mir223             | Mean Ct for miR-223                                     |
| mean_mir381p            | Mean Ct for miR-381p                                    |
| mean_GAPDH              | Mean Ct for GAPDH (NOT used for normalization)          |

## 3. Notes

- All analyses use raw and robustly scaled miRNA Ct values.
- GAPDH is assessed for stability but never used for normalization.
