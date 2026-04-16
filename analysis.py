"""
Dental Caries and Childhood Obesity in Denmark
Urban vs Rural Analysis (2008-2025)
Author: Kasia
Data sources: Sundhedsdatastyrelsen (SCOR register), Den Nationale Børnedatabase
"""

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os
import glob
from scipy import stats

matplotlib.use('Agg')  # Non-interactive backend for saving plots without displaying

# =============================================================================
# PART 1: DENTAL CARIES DATA (SCOR register, 2008-2025)
# =============================================================================

print("=" * 60)
print("PART 1: Loading dental caries data")
print("=" * 60)

folder = 'caries_data_raw'
all_caries = []

for year in range(2008, 2026):
    file = f'{folder}/scor_{year}.csv'
    if os.path.exists(file):
        df = pd.read_csv(file, sep=',', encoding='utf-8',
                         decimal=',', quotechar='"')
        df['year'] = year
        all_caries.append(df)
        print(f"✅ Loaded: {year}")
    else:
        print(f"❌ Missing: {year}")

df_caries = pd.concat(all_caries, ignore_index=True)
df_caries.to_csv('caries_all_years.csv', index=False)
print(f"\nCaries data shape: {df_caries.shape}")

# Calculate yearly trend
caries_trend = df_caries.groupby('year')['def-s/DMF-S'].mean()

# =============================================================================
# PART 2: OBESITY DATA (Den Nationale Børnedatabase, 2014-2025)
# =============================================================================

print("\n" + "=" * 60)
print("PART 2: Loading obesity data")
print("=" * 60)

df_obesity = pd.read_excel('obesity_kommuner.xlsx',
                            sheet_name='Udskoling fordelt på kommuner',
                            skiprows=7)

# Clean data
df_obesity = df_obesity.drop(columns=['Unnamed: 0', 'Unnamed: 1'])
df_obesity = df_obesity.dropna(subset=['Kommune'])

# Convert to numeric
df_obesity['Procentdel moderat overvægt'] = pd.to_numeric(
    df_obesity['Procentdel moderat overvægt'], errors='coerce')
df_obesity['Procentdel svær overvægt'] = pd.to_numeric(
    df_obesity['Procentdel svær overvægt'], errors='coerce')

# Urban/Rural classification based on municipality size
urban_municipalities = [
    'København', 'Aarhus', 'Odense', 'Aalborg',
    'Esbjerg', 'Randers', 'Kolding', 'Horsens',
    'Vejle', 'Roskilde', 'Helsingør', 'Fredericia'
]

df_obesity['urban_rural'] = df_obesity['Kommune'].apply(
    lambda x: 'Urban' if x in urban_municipalities else 'Rural'
)

df_obesity.to_csv('obesity_all_years.csv', index=False)
print(f"Obesity data shape: {df_obesity.shape}")
print(f"Municipalities: {df_obesity['Kommune'].nunique()}")

# Calculate yearly obesity trend
obesity_trend = df_obesity.groupby('Opgørelsesår')['Procentdel moderat overvægt'].mean()
obesity_urban_rural = df_obesity.groupby('urban_rural')['Procentdel moderat overvægt'].mean()

# =============================================================================
# PART 3: SUBREGION DATA (SCOR per subregion)
# =============================================================================

print("\n" + "=" * 60)
print("PART 3: Loading subregion data")
print("=" * 60)

files = glob.glob('subregions_data/scor_*.csv')
print(f"Found {len(files)} subregion files")

subregions = []
for file in files:
    name = os.path.basename(file).replace('scor_', '').replace('.csv', '')
    df_temp = pd.read_csv(file, sep=',', encoding='utf-8',
                          decimal=',', quotechar='"')
    df_temp['subregion'] = name
    subregions.append(df_temp)

df_sub = pd.concat(subregions, ignore_index=True)
print(f"Subregion data shape: {df_sub.shape}")

# Urban/Rural classification for subregions
urban_subregions = [
    'HS-Kobenhavn', 'HS-Frederiksberg', 'MJ-Aarhus',
    'HS-Gentofte', 'HS-Gladsaxe', 'HS-Lyngby',
    'HS-Hvidovre', 'HS-Brondby', 'HS-Ballerup'
]

df_sub['urban_rural'] = df_sub['subregion'].apply(
    lambda x: 'Urban' if x in urban_subregions else 'Rural'
)

caries_urban_rural = df_sub.groupby('urban_rural')['Målvariabel'].mean()

# =============================================================================
# PART 4: STATISTICAL ANALYSIS
# =============================================================================

print("\n" + "=" * 60)
print("PART 4: Statistical analysis")
print("=" * 60)

# T-test for caries Urban vs Rural
rural_caries = df_sub[df_sub['urban_rural'] == 'Rural']['Målvariabel']
urban_caries = df_sub[df_sub['urban_rural'] == 'Urban']['Målvariabel']
t_stat1, p_val1 = stats.ttest_ind(rural_caries, urban_caries)

print(f"Caries - Rural: {rural_caries.mean():.3f}, Urban: {urban_caries.mean():.3f}")
print(f"Caries - t={t_stat1:.3f}, p={p_val1:.4f}")

# T-test for obesity Urban vs Rural
rural_obesity = df_obesity[df_obesity['urban_rural'] == 'Rural']['Procentdel moderat overvægt'].dropna()
urban_obesity = df_obesity[df_obesity['urban_rural'] == 'Urban']['Procentdel moderat overvægt'].dropna()
t_stat2, p_val2 = stats.ttest_ind(rural_obesity, urban_obesity)

print(f"Obesity - Rural: {rural_obesity.mean():.3f}%, Urban: {urban_obesity.mean():.3f}%")
print(f"Obesity - t={t_stat2:.3f}, p={p_val2:.4f}")

# Correlation analysis
trend_df = caries_trend.reset_index()
trend_df.columns = ['year', 'caries']
obesity_df2 = obesity_trend.reset_index()
obesity_df2.columns = ['year', 'obesity']
merged = pd.merge(trend_df, obesity_df2, on='year')

corr_all = merged['caries'].corr(merged['obesity'])
merged_no_covid = merged[~merged['year'].isin([2020, 2021, 2022])]
corr_no_covid = merged_no_covid['caries'].corr(merged_no_covid['obesity'])

print(f"\nCorrelation (all years): {corr_all:.3f}")
print(f"Correlation (excluding COVID years): {corr_no_covid:.3f}")

# =============================================================================
# PART 5: VISUALIZATIONS
# =============================================================================

print("\n" + "=" * 60)
print("PART 5: Creating visualizations")
print("=" * 60)

# Plot 1: Caries trend 2008-2025
plt.figure(figsize=(12, 6))
plt.plot(caries_trend.index, caries_trend.values,
         marker='o', color='steelblue', linewidth=2)
plt.axvline(x=2020, color='red', linestyle='--', label='COVID-19 pandemic')
plt.title('Dental Caries Trend in Danish Children (def-s/DMF-S)\n2008-2025', fontsize=14)
plt.xlabel('Year')
plt.ylabel('def-s/DMF-S')
plt.xticks(range(2008, 2026), rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('caries_trend_2008_2025.png', dpi=150)
print("✅ Saved: caries_trend_2008_2025.png")

# Plot 2: Caries vs Obesity over time
fig, ax1 = plt.subplots(figsize=(12, 6))
ax2 = ax1.twinx()
ax1.plot(caries_trend.index, caries_trend.values,
         color='steelblue', marker='o', label='Dental Caries (def-s/DMF-S)')
ax2.plot(obesity_trend.index, obesity_trend.values,
         color='coral', marker='s', label='Childhood Overweight (%)')
ax1.set_ylabel('def-s/DMF-S', color='steelblue')
ax2.set_ylabel('Overweight prevalence (%)', color='coral')
ax1.set_xlabel('Year')
plt.title('Dental Caries vs Childhood Obesity in Denmark')
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2)
ax1.set_xticks(range(2008, 2026))
ax1.set_xticklabels(range(2008, 2026), rotation=45)
plt.tight_layout()
plt.savefig('caries_vs_obesity_over_time.png', dpi=150)
print("✅ Saved: caries_vs_obesity_over_time.png")

# Plot 3: Scatter plot correlation
plt.figure(figsize=(8, 6))
plt.scatter(merged['obesity'], merged['caries'], color='steelblue', s=100)
for i, row in merged.iterrows():
    plt.annotate(str(int(row['year'])),
                 (row['obesity'], row['caries']),
                 textcoords="offset points", xytext=(5, 5))
plt.xlabel('Childhood Overweight (%)')
plt.ylabel('Dental Caries (def-s/DMF-S)')
plt.title('Correlation: Dental Caries vs Childhood Obesity\nDenmark 2014-2025')
plt.tight_layout()
plt.savefig('caries_obesity_scatter.png', dpi=150)
print("✅ Saved: caries_obesity_scatter.png")

# Plot 4: Urban vs Rural comparison
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

caries_urban_rural.plot(kind='bar', ax=ax1,
                         color=['coral', 'steelblue'], edgecolor='black')
ax1.set_title('Dental Caries (def-s/DMF-S)\nUrban vs Rural')
ax1.set_xlabel('Area type')
ax1.set_ylabel('def-s/DMF-S')
ax1.set_xticklabels(['Rural', 'Urban'], rotation=0)

obesity_urban_rural.plot(kind='bar', ax=ax2,
                          color=['coral', 'steelblue'], edgecolor='black')
ax2.set_title('Childhood Overweight (%)\nUrban vs Rural')
ax2.set_xlabel('Area type')
ax2.set_ylabel('Overweight prevalence (%)')
ax2.set_xticklabels(['Rural', 'Urban'], rotation=0)

plt.suptitle("Children's Health: Urban vs Rural in Denmark (2014-2025)",
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('caries_obesity_urban_rural_comparison.png', dpi=150)
print("✅ Saved: caries_obesity_urban_rural_comparison.png")

print("\n✅ All done!")
