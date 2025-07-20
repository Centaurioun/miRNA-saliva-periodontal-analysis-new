# miRNA Periodontal Disease Analysis - R Script Results

**Analysis Date:** 2025-07-20 13:23:39
**R Version:** R version 4.5.1 (2025-06-13 ucrt)

## Analysis Summary

- **Dataset:** 108 samples across 3 groups
- **miRNAs analyzed:** 6
- **Statistical tests:** 11 variables
- **ML models:** 6 evaluations
- **Best AUC:** 1

## Session Information

```r
R version 4.5.1 (2025-06-13 ucrt)
Platform: x86_64-w64-mingw32/x64
Running under: Windows 11 x64 (build 22631)

Matrix products: default
  LAPACK version 3.12.1

locale:
[1] LC_COLLATE=Turkish_Türkiye.utf8  LC_CTYPE=Turkish_Türkiye.utf8   
[3] LC_MONETARY=Turkish_Türkiye.utf8 LC_NUMERIC=C                    
[5] LC_TIME=Turkish_Türkiye.utf8    

time zone: Europe/Istanbul
tzcode source: internal

attached base packages:
[1] stats     graphics  grDevices utils     datasets  methods   base     

other attached packages:
 [1] rlang_1.1.6          mclust_6.1.1         cluster_2.1.8.1     
 [4] jsonlite_2.0.0       here_1.0.1           patchwork_1.3.1     
 [7] scales_1.4.0         RColorBrewer_1.1-3   pheatmap_1.0.13     
[10] factoextra_1.0.7     umap_0.2.10.0        Rtsne_0.17          
[13] glmnet_4.1-9         Matrix_1.7-3         pROC_1.18.5         
[16] randomForest_4.7-1.2 caret_7.0-1          lattice_0.22-7      
[19] psych_2.5.6          corrplot_0.95        effsize_0.8.1       
[22] broom_1.0.8          magrittr_2.0.3       lubridate_1.9.4     
[25] forcats_1.0.0        stringr_1.5.1        dplyr_1.1.4         
[28] purrr_1.1.0          readr_2.1.5          tidyr_1.3.1         
[31] tibble_3.3.0         ggplot2_3.5.2        tidyverse_2.0.0     

loaded via a namespace (and not attached):
 [1] mnormt_2.1.1         compiler_4.5.1       png_0.1-8           
 [4] systemfonts_1.2.3    vctrs_0.6.5          reshape2_1.4.4      
 [7] pkgconfig_2.0.3      shape_1.4.6.1        crayon_1.5.3        
[10] backports_1.5.0      labeling_0.4.3       utf8_1.2.6          
[13] promises_1.3.3       prodlim_2025.04.28   tzdb_0.5.0          
[16] ragg_1.4.0           bit_4.6.0            httpgd_2.0.4        
[19] recipes_1.3.1        later_1.4.2          parallel_4.5.1      
[22] R6_2.6.1             stringi_1.8.7        reticulate_1.42.0   
[25] parallelly_1.45.0    rpart_4.1.24         Rcpp_1.1.0          
[28] iterators_1.0.14     future.apply_1.20.0  httpuv_1.6.16       
[31] splines_4.5.1        nnet_7.3-20          timechange_0.3.0    
[34] tidyselect_1.2.1     timeDate_4041.110    codetools_0.2-20    
[37] listenv_0.9.1        plyr_1.8.9           withr_3.0.2         
[40] askpass_1.2.1        unigd_0.1.3          future_1.58.0       
[43] survival_3.8-3       pillar_1.11.0        foreach_1.5.2       
[46] stats4_4.5.1         generics_0.1.4       vroom_1.6.5         
[49] rprojroot_2.1.0      hms_1.1.3            globals_0.18.0      
[52] class_7.3-23         glue_1.8.0           tools_4.5.1         
[55] data.table_1.17.8    RSpectra_0.16-2      ModelMetrics_1.2.2.2
[58] gower_1.0.2          grid_4.5.1           ipred_0.9-15        
[61] nlme_3.1-168         cli_3.6.5            textshaping_1.0.1   
[64] lava_1.8.1           gtable_0.3.6         digest_0.6.37       
[67] ggrepel_0.9.6        farver_2.1.2         lifecycle_1.0.4     
[70] hardhat_1.4.1        openssl_2.3.3        bit64_4.6.0-1       
[73] MASS_7.3-65         
```

## Warnings Summary

```r
No warnings generated
```

