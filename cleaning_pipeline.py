"""
Rivers State HIV Cascade — Full Cleaning Pipeline
===================================================
Transforms raw PEPFAR MER "Clinical Cascade by Fine Age and Sex" export
into a clean, analysis-ready long-format table.

Input:  rivers_state_hiv_cascade.xlsx (raw PEPFAR export, pre-filtered
        to Nigeria / Rivers State in Excel)
Output: rivers_hiv_cascade_final.csv

See DATA_QUALITY_LOG.md for the full explanation of each fix below.
"""

import pandas as pd
import datetime

# ============================================
# STEP 1 — Load
# ============================================
df = pd.read_excel('data/raw/rivers_state_hiv_cascade.xlsx')

# ============================================
# STEP 2 — Separate identity columns from wide quarter/target columns
# ============================================
id_columns = [
    'Operating Unit', 'Country', 'ISO3', 'Sub-National Unit 1',
    'Sub-National Unit 1 UID', 'Indicator', 'Numerator/Denominator',
    'RTRI Result', 'Description', 'Coarse Age', 'Fine Age',
    'Target Age 2024', 'Sex'
]
value_columns = [c for c in df.columns if c not in id_columns]

# ============================================
# STEP 3 — Melt wide -> long (one row per period instead of one column per period)
# ============================================
df_long = pd.melt(
    df,
    id_vars=id_columns,
    value_vars=value_columns,
    var_name='Period',
    value_name='Value'
)

# ============================================
# STEP 4 — Drop unreported (blank) periods
# ============================================
df_clean = df_long.dropna(subset=['Value']).copy()

# ============================================
# STEP 5 — Split Period into Year / Quarter / Type (Result vs Target)
# ============================================
df_clean['Year'] = df_clean['Period'].str.extract(r'(\d{4})')
df_clean['Type'] = df_clean['Period'].apply(lambda x: 'Target' if 'Targets' in x else 'Result')
df_clean['Quarter'] = df_clean['Period'].str.extract(r'Quarter (\d)')

# ============================================
# STEP 6 — Isolate TX_PVLS and pivot Numerator/Denominator onto the same row
# (PEPFAR reports viral suppression as separate N/D rows; we need them
#  side by side to calculate a rate)
# ============================================
pvls = df_clean[df_clean['Indicator'] == 'TX_PVLS'].copy()

pvls_pivot = pvls.pivot_table(
    index=['Year', 'Quarter', 'Sex', 'Fine Age'],
    columns='Numerator/Denominator',
    values='Value',
    aggfunc='sum'
).reset_index()

# ============================================
# STEP 7 — Recover Excel-corrupted age bands
# (Excel silently converts "10-14"-style text into calendar dates;
#  original values are unrecoverable except by inference — see log)
# ============================================
def fix_age(val):
    if isinstance(val, datetime.datetime):
        return f"{val.month}-{val.day}"
    return val

pvls_pivot['Fine Age'] = pvls_pivot['Fine Age'].apply(fix_age)

# ============================================
# STEP 8 — Calculate viral suppression rate
# ============================================
pvls_pivot['Suppression_Rate'] = (pvls_pivot['N'] / pvls_pivot['D']) * 100

# ============================================
# STEP 9 — Reshape suppression rate back to long format for combining
# ============================================
pvls_long = pvls_pivot.melt(
    id_vars=['Year', 'Quarter', 'Sex', 'Fine Age'],
    value_vars=['Suppression_Rate'],
    var_name='Metric',
    value_name='Suppression_Rate_Value'
)
pvls_long = pvls_long.rename(columns={'Suppression_Rate_Value': 'Suppression_Rate'})
pvls_long['Indicator'] = 'TX_PVLS_Suppression_Rate'
pvls_long['Country'] = 'Nigeria'
pvls_long['Sub-National Unit 1'] = 'Rivers'

# ============================================
# STEP 10 — Trim to final column set and combine core indicators + suppression rate
# ============================================
keep_columns = ['Country', 'Sub-National Unit 1', 'Indicator', 'Fine Age', 'Sex', 'Year', 'Quarter']

df_core = df_clean[df_clean['Indicator'] != 'TX_PVLS'][keep_columns + ['Value']].copy()
df_core['Suppression_Rate'] = pd.NA

pvls_final = pvls_long[keep_columns + ['Suppression_Rate']].copy()
pvls_final['Value'] = pd.NA

final_cascade = pd.concat([df_core, pvls_final], ignore_index=True, sort=False)
final_cascade['Suppression_Rate'] = final_cascade['Suppression_Rate'].round(2)
final_cascade = final_cascade.sort_values(['Year', 'Quarter', 'Indicator']).reset_index(drop=True)

# ============================================
# STEP 11 — Export
# ============================================
final_cascade.to_csv('data/cleaned/rivers_hiv_cascade_final.csv', index=False)

print(f"Done. {final_cascade.shape[0]} rows, {final_cascade.shape[1]} columns exported.")
print(f"Indicators: {final_cascade['Indicator'].unique().tolist()}")
