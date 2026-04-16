# Dental Caries and Childhood Obesity in Denmark
## Urban vs Rural Analysis (2008-2025)

### Overview
This project analyzes the relationship between dental caries and childhood obesity 
in Denmark, with a focus on geographic disparities between urban and rural areas.
The analysis uses national register data from Sundhedsdatastyrelsen.

### Key Findings
- Rural children show significantly higher dental caries rates than urban children
  (def-s/DMF-S: 0.827 vs 0.737, t=4.591, p<0.0001)
- Rural children show significantly higher overweight prevalence than urban children
  (15.6% vs 14.3%, t=7.185, p<0.0001)
- A notable increase in caries scores was observed in 2020, likely reflecting 
  reduced access to dental care during the COVID-19 pandemic
- Correlation between caries and obesity was stronger when excluding pandemic years
  (r=-0.449 vs r=-0.259)

### Data Sources
- **Dental caries data**: SCOR register, Sundhedsdatastyrelsen (2008-2025)
- **Obesity data**: Den Nationale Børnedatabase, Sundhedsdatastyrelsen (2014-2025)

### Methods
- Urban/Rural classification based on municipality size
- Independent samples t-test for group comparisons
- Pearson correlation analysis
- COVID-19 sensitivity analysis

### Technologies
- Python 3
- pandas, matplotlib, seaborn, scipy

### Clinical Implications
Both dental caries and childhood obesity share a common risk factor: 
excessive sugar consumption. Rural areas in Denmark show disproportionately 
higher rates of both conditions, suggesting that dietary interventions 
in rural municipalities could simultaneously address both public health challenges.

### Limitations
- Dental caries data available at subregion level, obesity data at municipality level
- Different time ranges: caries (2008-2025), obesity (2014-2025)
- COVID-19 pandemic acted as a confounding variable (2020-2022)

### Author
Dentist and aspiring Medical Affairs professional