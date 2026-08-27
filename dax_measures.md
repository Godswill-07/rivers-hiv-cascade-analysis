# DAX Measures

All measures live on `HIV_Cascade_fact`, filtered through `Dim_Indicator`, `Dim_Age`, and `DateTable`.

```dax
Total_Tested = 
CALCULATE(
    SUM(HIV_Cascade_fact[Value]),
    HIV_Cascade_fact[Indicator] = "HTS_TST",
    Dim_Age[Age_Family] = "Narrow"
)

Total_Positive = 
CALCULATE(
    SUM(HIV_Cascade_fact[Value]),
    HIV_Cascade_fact[Indicator] = "HTS_TST_POS",
    Dim_Age[Age_Family] = "Narrow"
)

Total_New_Treatment = 
CALCULATE(
    SUM(HIV_Cascade_fact[Value]),
    HIV_Cascade_fact[Indicator] = "TX_NEW",
    Dim_Age[Age_Family] = "Narrow"
)

Total_Current_Treatment = 
CALCULATE(
    SUM(HIV_Cascade_fact[Value]),
    HIV_Cascade_fact[Indicator] = "TX_CURR",
    Dim_Age[Age_Family] = "Narrow",
    HIV_Cascade_fact[Year] = MAX(HIV_Cascade_fact[Year])
)
-- Note: restricted to the latest year because TX_CURR is a point-in-time
-- snapshot indicator, not a cumulative flow — summing across all years
-- would count the same people repeatedly. See DATA_QUALITY_LOG.md item 5.

Avg_Suppression_Rate = 
CALCULATE(
    AVERAGE(HIV_Cascade_fact[Suppression_Rate]),
    HIV_Cascade_fact[Indicator] = "TX_PVLS_Suppression_Rate"
)

UNAIDS_Target = 95

Gap_to_Target = [Avg_Suppression_Rate] - [UNAIDS_Target]

Positive_to_Treatment_Rate = 
DIVIDE([Total_New_Treatment], [Total_Positive], 0)

Testing_to_Positive_Rate = 
DIVIDE([Total_Positive], [Total_Tested], 0)

Cascade_Value = 
SWITCH(
    SELECTEDVALUE(Dim_Indicator[Cascade_Order]),
    1, [Total_Tested],
    2, [Total_Positive],
    3, [Total_New_Treatment],
    4, [Total_Current_Treatment]
)
-- Used to drive the funnel chart: SWITCH selects the right total
-- based on which indicator's Cascade_Order is currently in context.
```
