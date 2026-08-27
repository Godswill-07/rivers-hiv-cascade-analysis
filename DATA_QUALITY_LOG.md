# Data Quality Log

Every data quality issue found during this project, in the order discovered, with root cause and fix.

---

### 1. Floating-point ID corruption (Excel/pandas)
**Found:** Large integer ID values displayed in scientific notation (e.g. `5.635E+17`) after being parsed as float64.
**Root cause:** float64 cannot represent large integers beyond ~15-16 significant digits; values had already been round-tripped through Excel prior to this analysis, permanently losing precision.
**Fix:** Flagged all affected rows (`id_corrupted` column), nulled the unrecoverable ID rather than reconstructing a false value, preserved the row for all other fields.
**Impact:** 1,583 of 12,805 rows in the original practice dataset affected.

### 2. Line breaks embedded in text fields
**Found:** Listing/name fields displaying as multi-line, word-fused text (e.g. "SeptemberGardenHomestayPrince'sCabin").
**Root cause:** Raw scrape data contained literal line-feed/carriage-return characters with no surrounding space.
**Fix:** `SUBSTITUTE(CHAR(10)/CHAR(13), " ")` in Excel; `.str.replace(r'[\r\n]+', ' ')` in Python. Applied before any further text cleaning.

### 3. Age bands corrupted into calendar dates
**Found:** `Fine Age` values like `10-14`, `1-4`, `5-9` appearing as `datetime(2026, 10, 14)`, etc.
**Root cause:** Excel auto-detects "number-dash-number" patterns as dates and silently reformats them on file open/save — original text is unrecoverable once this happens.
**Fix:** Since the corrupted values matched PEPFAR's standard fine-age-band sequence with exactly the expected bands missing, reconstructed original text from the corrupted date's month/day (`f"{val.month}-{val.day}"`).
**Caveat:** This is inference based on a highly consistent pattern, not certain recovery — documented as such.

### 4. Overlapping, non-comparable age-band systems
**Found:** `Fine Age` column contains three non-overlapping "families" of values simultaneously: Narrow (`1-4, 5-9, 10-14...`), Wide (`15-24, 25-34...`), and Other (`Coarse, Retired Age Band, Unknown Age`).
**Root cause:** Different PEPFAR indicators report age at different granularities within the same raw export.
**Fix:** Built `Dim_Age` dimension table tagging every value with its `Age_Family`. All core DAX measures filter to `Age_Family = "Narrow"` to prevent double-counting the same individuals across overlapping bands.
**Impact:** Before this fix, `Total_Tested` measure showed ~12M — implausible for a state with a population of ~7M. After the fix, totals dropped to a realistic figure.

### 5. TX_CURR summed across all time periods (snapshot vs. flow confusion)
**Found:** `Total_Current_Treatment` measure showed a total larger than plausible, inconsistent with other cascade stages.
**Root cause:** TX_CURR is a point-in-time snapshot indicator (same people counted every quarter they remain on treatment), not a flow/event count like TX_NEW or HTS_TST. Summing it across 40 quarters counted the same individuals repeatedly.
**Fix:** Measure restricted to the most recent reporting year only (`HIV_Cascade_fact[Year] = MAX(HIV_Cascade_fact[Year])`), consistent with how PEPFAR defines the indicator.

### 6. TX_RET (retention indicator) absent from dataset
**Found:** Expected indicator not present in filtered data.
**Root cause:** PEPFAR deprecated TX_RET in favor of deriving retention from TX_CURR and TX_NET_NEW in current MER guidance.
**Fix:** No fabricated data; documented explicitly and used TX_CURR/TX_NET_NEW as a stated proxy rather than a direct substitute.

### 7. Suppression rate percentage double-multiplied in Power BI
**Found:** Suppression rate cards displaying values like "896%" instead of "89.6%".
**Root cause:** Power BI's built-in Percentage format assumes the underlying value is a decimal fraction (0.896) and multiplies by 100 on display; the stored value was already a whole-number percentage.
**Fix:** Changed card format to Decimal Number with manual "%" suffix rather than Power BI's automatic Percentage type.

---

*Log maintained as part of this project's commitment to documenting, not hiding, data quality issues.*
