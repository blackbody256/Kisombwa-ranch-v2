# Manager Dashboard - Complete Specification
**KRIS - Kisombwa Ranch Intelligence System**

---

## 🎯 DASHBOARD PURPOSE

**Primary Goal:** Answer the manager's question: *"Why aren't my $40,000 imported animals breeding?"*

**Secondary Goals:**
- Stop guesswork decisions
- Identify financial losses
- Provide actionable recommendations
- Track herd health trends
- Monitor operational efficiency

---

## 📊 DASHBOARD LAYOUT

```
┌─────────────────────────────────────────────────────────────────────┐
│  KISOMBWA RANCH INTELLIGENCE SYSTEM            [Manager Name] [Logout]│
│  Dashboard                                                    Feb 18, 2025│
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  📊 HERD OVERVIEW (KPI Cards)                                        │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐│
│  │ TOTAL    │  │ CATTLE   │  │ GOATS    │  │ SHEEP    │  │ ACTIVE   ││
│  │ ANIMALS  │  │          │  │          │  │          │  │ ALERTS   ││
│  │   127    │  │    100   │  │    20    │  │     7    │  │    8     ││
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘│
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  🚨 ACTIVE ALERTS (Prioritized)                        [View All →] │
├─────────────────────────────────────────────────────────────────────┤
│  🔴 HIGH: 8 animals overdue for vaccination                         │
│  🟠 MEDIUM: 12 animals need pregnancy confirmation check            │
│  🟠 MEDIUM: Breeding success rate down 15% vs. last quarter         │
│  🟡 LOW: 3 animals low weight gain this month                       │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  💰 BREEDING PERFORMANCE ANALYZER (THE KEY INSIGHT)                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Investment Analysis: Imported vs. Local Breeds                     │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐│
│  │ Metric                  │ Imported Bulls (8) │ Local Bulls (15)││
│  ├────────────────────────────────────────────────────────────────┤│
│  │ Investment              │ $40,000            │ $12,000         ││
│  │ Conception Rate         │ 35% ⚠️             │ 75% ✓           ││
│  │ Avg Calving Interval    │ 450 days ⚠️        │ 380 days ✓      ││
│  │ Stillbirth Rate         │ 12% ⚠️             │ 4% ✓            ││
│  │ Calf Survival (6mo)     │ 85% ⚠️             │ 95% ✓           ││
│  │ Calves This Year        │ 12 ⚠️              │ 48 ✓            ││
│  │ Revenue Generated       │ $6,000 ⚠️          │ $24,000 ✓       ││
│  │ ROI                     │ -85% ⚠️            │ +100% ✓         ││
│  └────────────────────────────────────────────────────────────────┤│
│                                                                      │
│  🔍 ROOT CAUSE ANALYSIS (AI-Powered Insights):                      │
│                                                                      │
│  1. VACCINATION ISSUE (High Impact)                                 │
│     • 5 out of 8 imported bulls have incomplete vaccination series  │
│     • Correlation: Incomplete vaccination → 85% lower conception    │
│     • Affected animals: BORAN_IMP_001, 003, 005, 007, 008          │
│                                                                      │
│  2. HEALTH EVENTS (Medium Impact)                                   │
│     • 3 imported bulls had illness within 60 days of breeding       │
│     • Correlation: Recent illness → 40% lower conception            │
│     • Affected animals: BORAN_IMP_002, 004, 006                    │
│                                                                      │
│  3. WEIGHT/NUTRITION (Low Impact)                                   │
│     • 2 bulls below optimal breeding weight (420kg vs 480kg target) │
│     • Correlation: Underweight → 25% lower conception               │
│     • Affected animals: BORAN_IMP_003, 008                         │
│                                                                      │
│  💡 RECOMMENDATIONS (Prioritized by Impact):                        │
│                                                                      │
│  1. ✅ Complete vaccination series for 5 bulls                      │
│     Expected impact: Conception rate 35% → 60% (+$12,500 revenue)  │
│     Cost: $250 (vaccines)                                           │
│     Timeline: 2 weeks                                               │
│                                                                      │
│  2. ✅ Schedule vet checkup for 3 bulls with health history         │
│     Expected impact: Reduce breeding failures                       │
│     Cost: $300 (vet visit)                                          │
│     Timeline: 1 week                                                │
│                                                                      │
│  3. ✅ Increase feed rations for underweight bulls                  │
│     Expected impact: Weight gain 420kg → 480kg in 8 weeks          │
│     Cost: $400 (additional feed)                                    │
│     Timeline: 8 weeks                                               │
│                                                                      │
│  📊 PROJECTED FINANCIAL RECOVERY:                                   │
│  • Implement all recommendations: $950 cost                         │
│  • Expected outcome: Conception rate 35% → 75%                      │
│  • Additional calves per year: 12 → 32 (+20 calves)                │
│  • Revenue increase: $10,000 per year                               │
│  • ROI on interventions: 952% in first year                         │
│                                                                      │
│  [Download Detailed Report] [Share with Vet]                        │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  📈 BREEDING TRENDS (Last 12 Months)                                │
├─────────────────────────────────────────────────────────────────────┤
│  [Line Chart: Conception Rate Over Time]                            │
│   100% ┤                                                             │
│    75% ┤────────●────●────●────●  Local Breeds                      │
│    50% ┤                                                             │
│    25% ┤           ●────●────●────●────●  Imported Breeds           │
│     0% └─┬────┬────┬────┬────┬────┬────┬────┬────┬────┬            │
│          Feb  Apr  Jun  Aug  Oct  Dec  Feb                          │
│                                                                      │
│  Key Observations:                                                   │
│  • Imported conception rate declining since June 2024               │
│  • Local breeds stable at 75% throughout year                       │
│  • Gap widening: Now 40 percentage points difference                │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  🏥 HEALTH VS. BREEDING CORRELATION                                 │
├─────────────────────────────────────────────────────────────────────┤
│  [Bar Chart: Impact of Health Factors on Conception Rate]           │
│                                                                      │
│  Complete Vaccination    ████████████████████ 75%                   │
│  Incomplete Vaccination  ████ 12%                                   │
│                                                                      │
│  No Recent Illness       ███████████████████ 72%                    │
│  Illness in Last 60 Days ██████████ 32%                             │
│                                                                      │
│  Optimal Weight          ████████████████████ 78%                   │
│  Below Target Weight     ████████████ 53%                           │
│                                                                      │
│  Insight: Vaccination status is the strongest predictor             │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  💰 FINANCIAL PERFORMANCE (Current Quarter)                         │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐ │
│  │ TOTAL COSTS      │  │ REVENUE          │  │ NET PROFIT       │ │
│  │ $8,750           │  │ $12,500          │  │ $3,750           │ │
│  │ Feed: $5,200     │  │ Sales: $7,000    │  │ Margin: 30%      │ │
│  │ Medicine: $2,100 │  │ Calves: $5,500   │  │                  │ │
│  │ Labor: $1,450    │  │                  │  │                  │ │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘ │
│                                                                      │
│  Cost Breakdown by Animal Type:                                     │
│  Imported Bulls: $6,200 spent, $6,000 revenue → -$200 loss         │
│  Local Bulls:    $2,550 spent, $6,500 revenue → +$3,950 profit     │
│                                                                      │
│  [View Detailed Cost Analysis]                                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  📊 HERD HEALTH OVERVIEW                                            │
├─────────────────────────────────────────────────────────────────────┤
│  [Pie Chart: Current Health Status]                                 │
│                                                                      │
│    Healthy (90): 71%  ███████████████████████████                   │
│    Under Treatment (8): 6%  ███                                     │
│    Quarantine (2): 2%  █                                            │
│    Observation (27): 21%  ██████████                                │
│                                                                      │
│  Recent Trends:                                                      │
│  • Disease incidents: 4 this month (vs. 7 last month) ↓ Improving   │
│  • Vaccination coverage: 87% (target: 95%) ⚠️ Action needed         │
│  • Mortality rate: 2.3% this quarter (vs. 3.1% last quarter) ↓ Good │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  ⚰️ MORTALITY ANALYSIS (Last 6 Months)                              │
├─────────────────────────────────────────────────────────────────────┤
│  Total Deaths: 4                                                     │
│  Calf Deaths (<12 months): 3 (75% of deaths) ⚠️                     │
│  Adult Deaths: 1                                                     │
│                                                                      │
│  Causes:                                                             │
│  • Pneumonia: 2 deaths                                              │
│  • Unknown: 1 death ⚠️ (Requires investigation)                     │
│  • Injury: 1 death                                                  │
│                                                                      │
│  Estimated Financial Loss: $2,800                                   │
│                                                                      │
│  [View Mortality Details]                                           │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  📅 UPCOMING TASKS & REMINDERS                                      │
├─────────────────────────────────────────────────────────────────────┤
│  This Week:                                                          │
│  • 8 vaccinations due by Friday                                     │
│  • 12 pregnancy checks scheduled                                    │
│  • 3 animals ready for weaning                                      │
│                                                                      │
│  Next 30 Days:                                                       │
│  • 5 expected calvings                                              │
│  • 15 animals due for deworming                                     │
│  • Quarterly vet visit scheduled (Feb 25)                           │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  🐄 RECENT ACTIVITY LOG                                             │
├─────────────────────────────────────────────────────────────────────┤
│  Today:                                                              │
│  • 10:30 AM - BORAN045 vaccinated (FMD) - by John Mugisha           │
│  • 11:15 AM - BORAN023 treated for fever - by Dr. Okello            │
│  • 2:45 PM - BORAN_IMP_003 pregnancy confirmed - by John Mugisha    │
│                                                                      │
│  Yesterday:                                                          │
│  • BORAN089 calving - Live birth (female calf: BORAN127)            │
│  • 15 animals counted at evening check                              │
│  • Herd moved from Pasture A to Pasture C                           │
│                                                                      │
│  [View Full Activity Log]                                           │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  🔢 HERD COUNT TRACKING (RFID Integration)                          │
├─────────────────────────────────────────────────────────────────────┤
│  Last Automated Count: Today at 6:00 PM                             │
│                                                                      │
│  Expected: 127 animals                                              │
│  Scanned:  125 animals  ⚠️                                          │
│  Missing:  2 animals                                                │
│                                                                      │
│  Animals not scanned today:                                         │
│  • BORAN034 (Last seen: Yesterday)                                  │
│  • GOAT012 (Last seen: Yesterday)                                   │
│                                                                      │
│  Action Required: Locate missing animals                            │
│                                                                      │
│  [View Count History] [Generate Report]                             │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  📊 QUICK STATS COMPARISON                                          │
├─────────────────────────────────────────────────────────────────────┤
│                         This Quarter │ Last Quarter │ Change        │
│  Conception Rate             48%    │      52%     │  -4% ↓        │
│  Calf Survival Rate          92%    │      89%     │  +3% ↑        │
│  Vaccination Compliance      87%    │      82%     │  +5% ↑        │
│  Disease Incidents           12     │      18      │  -33% ↑       │
│  Mortality Rate             2.3%    │     3.1%     │  -0.8% ↑      │
│  Avg Daily Weight Gain      0.7kg   │     0.65kg   │  +0.05kg ↑    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📊 DETAILED COMPONENT SPECIFICATIONS

### **1. HERD OVERVIEW KPI CARDS**

**Data Required:**
```sql
-- Total Animals (All Species)
SELECT COUNT(*) 
FROM animals 
WHERE status = 'active';

-- By Species
SELECT species, COUNT(*) 
FROM animals 
WHERE status = 'active' 
GROUP BY species;

-- Active Alerts
SELECT COUNT(*) 
FROM alerts 
WHERE is_resolved = false;
```

**Display:**
- Large number (font-size: 48px)
- Label below (font-size: 14px)
- Color-coded borders (green = good, red = attention needed)
- Icon for each metric

---

### **2. ACTIVE ALERTS SECTION**

**Data Required:**
```sql
-- Overdue Vaccinations
SELECT COUNT(DISTINCT v.animal_tag) 
FROM vaccinations v
WHERE v.next_due_date < CURRENT_DATE 
  AND NOT EXISTS (
    SELECT 1 FROM vaccinations v2 
    WHERE v2.animal_tag = v.animal_tag 
      AND v2.date_administered > v.next_due_date
  );

-- Pregnancy Checks Needed
SELECT COUNT(*) 
FROM breeding_events 
WHERE pregnancy_confirmed = 'pending' 
  AND service_date < CURRENT_DATE - INTERVAL '60 days';

-- Breeding Performance Decline
-- Compare last 3 months vs. previous 3 months
```

**Display:**
- 🔴 Red: High priority (requires immediate action)
- 🟠 Orange: Medium priority (requires attention this week)
- 🟡 Yellow: Low priority (monitor)
- Click to expand for details
- "View All" link to alerts page

---

### **3. BREEDING PERFORMANCE ANALYZER (CRITICAL)**

#### **3A. Investment Analysis Table**

**Data Required:**
```sql
-- Imported Bulls Performance
SELECT 
  'Imported Bulls' as category,
  COUNT(*) as count,
  SUM(purchase_price) as investment,
  
  -- Conception Rate
  (COUNT(CASE WHEN be.pregnancy_confirmed = 'yes' THEN 1 END) * 100.0 / 
   NULLIF(COUNT(be.id), 0)) as conception_rate,
  
  -- Calves This Year
  COUNT(CASE WHEN be.outcome = 'live_birth' 
             AND be.actual_delivery_date >= '2025-01-01' THEN 1 END) as calves_this_year,
  
  -- Stillbirth Rate
  (COUNT(CASE WHEN be.outcome = 'stillbirth' THEN 1 END) * 100.0 / 
   NULLIF(COUNT(CASE WHEN be.outcome IN ('live_birth', 'stillbirth') THEN 1 END), 0)) as stillbirth_rate

FROM animals a
LEFT JOIN breeding_events be ON a.tag_number = be.male_tag
WHERE a.source = 'imported' AND a.sex = 'male'
GROUP BY category;

-- Same query for Local Bulls (WHERE a.source IN ('born', 'purchased'))
```

**Calculated Metrics:**
```python
# ROI Calculation
revenue = calves_this_year * average_calf_price  # e.g., 12 × $500 = $6,000
costs = investment + feed_costs + medicine_costs  # e.g., $40,000 + $2,000 = $42,000
roi = ((revenue - costs) / costs) * 100  # -85%

# Average Calving Interval
avg_days = AVG(
  DATEDIFF(be2.service_date, be1.service_date)
  WHERE be1.outcome = 'live_birth' AND be2.female_tag = be1.female_tag
)
```

**Display:**
- Side-by-side comparison table
- ⚠️ Warning icons for poor metrics
- ✓ Check marks for good metrics
- Color coding: Red (<50%), Yellow (50-70%), Green (>70%)

#### **3B. Root Cause Analysis**

**Data Required:**
```sql
-- Vaccination Impact
WITH vacc_status AS (
  SELECT 
    a.tag_number,
    CASE WHEN COUNT(DISTINCT v.vaccine_type) >= 5 THEN 'complete' 
         ELSE 'incomplete' END as vacc_status
  FROM animals a
  LEFT JOIN vaccinations v ON a.tag_number = v.animal_tag
  WHERE a.source = 'imported' AND a.sex = 'male'
  GROUP BY a.tag_number
)
SELECT 
  vs.vacc_status,
  COUNT(DISTINCT be.id) as breeding_attempts,
  COUNT(CASE WHEN be.pregnancy_confirmed = 'yes' THEN 1 END) as conceptions,
  (COUNT(CASE WHEN be.pregnancy_confirmed = 'yes' THEN 1 END) * 100.0 / 
   NULLIF(COUNT(DISTINCT be.id), 0)) as conception_rate
FROM vacc_status vs
JOIN breeding_events be ON vs.tag_number = be.male_tag
GROUP BY vs.vacc_status;

-- Expected Output:
-- complete:    75% conception rate
-- incomplete:  12% conception rate
-- Correlation: 85% difference (HIGH IMPACT)
```

```sql
-- Health Event Impact
WITH recent_illness AS (
  SELECT 
    t.animal_tag,
    MAX(t.treatment_date) as last_illness
  FROM treatments t
  GROUP BY t.animal_tag
)
SELECT 
  CASE WHEN ri.last_illness > be.service_date - INTERVAL '60 days' 
       THEN 'illness_within_60_days' 
       ELSE 'no_recent_illness' END as health_status,
  (COUNT(CASE WHEN be.pregnancy_confirmed = 'yes' THEN 1 END) * 100.0 / 
   NULLIF(COUNT(be.id), 0)) as conception_rate
FROM breeding_events be
LEFT JOIN recent_illness ri ON be.male_tag = ri.animal_tag
WHERE be.male_tag IN (SELECT tag_number FROM animals WHERE source = 'imported')
GROUP BY health_status;
```

**Display:**
- Numbered list (1, 2, 3)
- Impact level badge (High/Medium/Low)
- Correlation strength (percentage difference)
- List of affected animals (clickable links to animal profiles)
- Visual correlation strength indicator

#### **3C. Recommendations Section**

**Logic:**
```python
def generate_recommendations():
    recommendations = []
    
    # Check vaccination gaps
    incomplete_vacc = get_animals_with_incomplete_vaccination()
    if len(incomplete_vacc) > 0:
        impact = calculate_impact_if_fixed(incomplete_vacc)  # $12,500
        cost = len(incomplete_vacc) * 50  # $50 per animal
        roi = (impact - cost) / cost * 100
        
        recommendations.append({
            'priority': 1,
            'action': f'Complete vaccination series for {len(incomplete_vacc)} bulls',
            'expected_impact': f'Conception rate 35% → 60% (+${impact} revenue)',
            'cost': f'${cost}',
            'timeline': '2 weeks',
            'roi': f'{roi}%'
        })
    
    # Check health history
    animals_with_recent_illness = get_animals_with_illness_last_60_days()
    if len(animals_with_recent_illness) > 0:
        recommendations.append({
            'priority': 2,
            'action': f'Schedule vet checkup for {len(animals_with_recent_illness)} bulls',
            'expected_impact': 'Reduce breeding failures',
            'cost': '$300',
            'timeline': '1 week'
        })
    
    # Check weight
    underweight_animals = get_animals_below_target_weight()
    if len(underweight_animals) > 0:
        recommendations.append({
            'priority': 3,
            'action': f'Increase feed rations for underweight bulls',
            'expected_impact': 'Weight gain 420kg → 480kg in 8 weeks',
            'cost': '$400',
            'timeline': '8 weeks'
        })
    
    return recommendations
```

**Display:**
- Numbered list (1, 2, 3)
- ✅ Checkbox icons
- Bold action text
- Expected impact (quantified)
- Cost and timeline
- Summary financial projection box at bottom

---

### **4. BREEDING TRENDS CHART**

**Data Required:**
```sql
-- Monthly conception rates for last 12 months
SELECT 
  DATE_TRUNC('month', service_date) as month,
  a.source,
  (COUNT(CASE WHEN pregnancy_confirmed = 'yes' THEN 1 END) * 100.0 / 
   NULLIF(COUNT(*), 0)) as conception_rate
FROM breeding_events be
JOIN animals a ON be.male_tag = a.tag_number
WHERE be.service_date >= CURRENT_DATE - INTERVAL '12 months'
  AND a.sex = 'male'
GROUP BY month, a.source
ORDER BY month;
```

**Chart Type:** Line chart  
**X-Axis:** Months (Feb 2024 - Feb 2025)  
**Y-Axis:** Conception Rate %  
**Lines:** 
- Blue line: Imported bulls
- Green line: Local bulls

**Annotations:**
- Point out when imported rate started declining
- Highlight the widening gap

---

### **5. HEALTH VS. BREEDING CORRELATION**

**Data Required:**
```sql
-- Vaccination Status Impact
SELECT 'Complete Vaccination' as factor, 
       AVG(conception_rate) FROM (vaccination_complete_animals);
SELECT 'Incomplete Vaccination' as factor, 
       AVG(conception_rate) FROM (vaccination_incomplete_animals);

-- Illness Impact
SELECT 'No Recent Illness' as factor, 
       AVG(conception_rate) FROM (no_illness_animals);
SELECT 'Illness Last 60 Days' as factor, 
       AVG(conception_rate) FROM (recent_illness_animals);

-- Weight Impact  
SELECT 'Optimal Weight' as factor, 
       AVG(conception_rate) FROM (optimal_weight_animals);
SELECT 'Below Target Weight' as factor, 
       AVG(conception_rate) FROM (underweight_animals);
```

**Chart Type:** Horizontal bar chart  
**X-Axis:** Conception Rate %  
**Y-Axis:** Health factors  
**Colors:**
- Green bars: Positive factors
- Red bars: Negative factors

**Key Insight Box:** "Vaccination status is the strongest predictor"

---

### **6. FINANCIAL PERFORMANCE**

**Data Required:**
```sql
-- Current Quarter Costs
SELECT 
  'Feed' as category, 
  SUM(cost) as amount 
FROM (feed_cost_table) 
WHERE date >= start_of_quarter;

-- Same for medicine, labor, etc.

-- Revenue
SELECT 
  SUM(sale_price) as sales_revenue 
FROM animals 
WHERE status = 'sold' 
  AND updated_at >= start_of_quarter;

SELECT 
  COUNT(*) * 500 as calf_value 
FROM breeding_events 
WHERE outcome = 'live_birth' 
  AND actual_delivery_date >= start_of_quarter;
```

**Display:**
- 3 large KPI cards
- Pie chart or stacked bar for cost breakdown
- Comparison table: Imported vs. Local profitability

---

### **7. HERD HEALTH OVERVIEW**

**Data Required:**
```sql
-- Current Health Status Distribution
SELECT 
  CASE 
    WHEN EXISTS (SELECT 1 FROM treatments WHERE animal_tag = a.tag_number 
                 AND treatment_date > CURRENT_DATE - INTERVAL '7 days') 
      THEN 'Under Treatment'
    WHEN status = 'quarantine' THEN 'Quarantine'
    WHEN status = 'active' AND /* some observation criteria */ THEN 'Observation'
    ELSE 'Healthy'
  END as health_status,
  COUNT(*) as count
FROM animals a
WHERE status = 'active'
GROUP BY health_status;
```

**Chart Type:** Pie chart or donut chart  
**Colors:**
- Green: Healthy
- Yellow: Observation
- Orange: Under Treatment
- Red: Quarantine

**Metrics Below:**
- Disease incidents trend
- Vaccination coverage %
- Mortality rate comparison

---

### **8. MORTALITY ANALYSIS**

**Data Required:**
```sql
-- Mortality in last 6 months
SELECT 
  COUNT(*) as total_deaths,
  COUNT(CASE WHEN age_at_death_months < 12 THEN 1 END) as calf_deaths,
  COUNT(CASE WHEN age_at_death_months >= 12 THEN 1 END) as adult_deaths,
  SUM(estimated_value) as financial_loss
FROM mortality
WHERE death_date >= CURRENT_DATE - INTERVAL '6 months';

-- Causes
SELECT cause, COUNT(*) as count
FROM mortality
WHERE death_date >= CURRENT_DATE - INTERVAL '6 months'
GROUP BY cause
ORDER BY count DESC;
```

**Display:**
- Summary numbers
- Bar chart of causes
- ⚠️ Flag for "Unknown" causes
- Financial loss calculation

---

### **9. UPCOMING TASKS & REMINDERS**

**Data Required:**
```sql
-- Vaccinations Due
SELECT COUNT(*) 
FROM vaccinations 
WHERE next_due_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days';

-- Pregnancy Checks
SELECT COUNT(*) 
FROM breeding_events 
WHERE pregnancy_confirmed = 'pending' 
  AND service_date < CURRENT_DATE - INTERVAL '60 days';

-- Expected Calvings
SELECT COUNT(*) 
FROM breeding_events 
WHERE expected_delivery_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '30 days';
```

**Display:**
- "This Week" section
- "Next 30 Days" section
- Clickable items linking to detailed views

---

### **10. RECENT ACTIVITY LOG**

**Data Required:**
```sql
-- Recent events (last 48 hours)
SELECT 
  'vaccination' as type,
  v.date_administered as timestamp,
  v.animal_tag,
  v.vaccine_type as detail,
  s.name as performed_by
FROM vaccinations v
JOIN staff s ON v.administered_by_id = s.id
WHERE v.created_at >= CURRENT_DATE - INTERVAL '2 days'

UNION ALL

SELECT 
  'treatment' as type,
  t.treatment_date as timestamp,
  t.animal_tag,
  t.diagnosis as detail,
  s.name as performed_by
FROM treatments t
JOIN staff s ON t.treated_by_id = s.id
WHERE t.created_at >= CURRENT_DATE - INTERVAL '2 days'

ORDER BY timestamp DESC
LIMIT 10;
```

**Display:**
- Reverse chronological list
- Grouped by day (Today, Yesterday)
- Icon for each event type
- "View Full Activity Log" link

---

### **11. HERD COUNT TRACKING (RFID)**

**Data Required:**
```sql
-- Today's scan summary
SELECT 
  COUNT(DISTINCT rfid_code) as scanned_count,
  MAX(scan_timestamp) as last_scan
FROM rfid_scan_logs
WHERE DATE(scan_timestamp) = CURRENT_DATE;

-- Expected count
SELECT COUNT(*) 
FROM animals 
WHERE status = 'active';

-- Missing animals
SELECT a.tag_number, MAX(rsl.scan_timestamp) as last_seen
FROM animals a
LEFT JOIN rfid_scan_logs rsl ON a.rfid_code = rsl.rfid_code
WHERE a.status = 'active'
  AND (rsl.scan_timestamp IS NULL 
       OR DATE(rsl.scan_timestamp) < CURRENT_DATE)
GROUP BY a.tag_number;
```

**Display:**
- Large numbers: Expected vs. Scanned
- ⚠️ Warning if discrepancy
- List of missing animals with last seen date
- "Action Required" prompt if difference > 2

---

### **12. QUICK STATS COMPARISON**

**Data Required:**
```sql
-- This Quarter vs. Last Quarter
WITH current_quarter AS (
  SELECT /* metrics */ FROM breeding_events 
  WHERE service_date >= start_of_current_quarter
),
last_quarter AS (
  SELECT /* metrics */ FROM breeding_events 
  WHERE service_date >= start_of_last_quarter 
    AND service_date < start_of_current_quarter
)
SELECT 
  cq.conception_rate as current,
  lq.conception_rate as last,
  cq.conception_rate - lq.conception_rate as change
FROM current_quarter cq, last_quarter lq;
```

**Display:**
- 3-column table
- Green ↑ for improvements
- Red ↓ for declines
- Percentage or absolute change

---

## 🎨 DESIGN PRINCIPLES

### **Visual Hierarchy:**
1. **Most Important First:** Breeding Performance Analyzer at top
2. **Actionable Alerts:** High visibility for items needing attention
3. **Supporting Data:** Trends and details below
4. **Historical Context:** Comparison charts at bottom

### **Color Coding:**
- 🟢 **Green:** Good/Healthy/On-track (>70%)
- 🟡 **Yellow:** Warning/Needs Attention (50-70%)
- 🔴 **Red:** Critical/Action Required (<50%)
- 🔵 **Blue:** Neutral/Informational

### **Data Freshness:**
- Real-time: Alerts, counts
- Daily: Activity log, RFID scans
- Weekly: Health trends
- Monthly: Financial reports, breeding trends

### **Interactivity:**
- Click KPI cards → Detailed view
- Click animal tags → Animal profile
- Click recommendations → Implementation guide
- Hover charts → Tooltips with exact values

---

## 📱 MOBILE RESPONSIVENESS

Dashboard should work on:
- Desktop (primary): Full dashboard
- Tablet: Stacked layout
- Mobile: Most critical KPIs only (breeding analyzer + alerts)

---

## 🔄 DATA REFRESH

- **Page Load:** All data fetched
- **Auto-refresh:** Every 5 minutes (for alerts and counts)
- **Manual refresh:** Button in header
- **Real-time updates:** WebSocket for activity log (optional)

---

## 🎯 SUCCESS METRICS FOR DASHBOARD

Manager should be able to answer these questions in <30 seconds:
1. ✅ Why aren't my imported animals breeding? (Root Cause Analysis)
2. ✅ What's the financial impact? (ROI calculation)
3. ✅ What should I do about it? (Recommendations)
4. ✅ Is my herd healthy overall? (Health Overview)
5. ✅ Are any animals missing? (RFID Count)
6. ✅ What's happening today? (Activity Log)

---

## 💻 TECHNICAL IMPLEMENTATION

### **Backend (Django Views):**
```python
def manager_dashboard(request):
    context = {
        'kpis': get_herd_kpis(),
        'alerts': get_active_alerts(),
        'breeding_analyzer': get_breeding_performance_analysis(),
        'health_correlation': get_health_breeding_correlation(),
        'financial': get_financial_performance(),
        'mortality': get_mortality_analysis(),
        'upcoming_tasks': get_upcoming_tasks(),
        'activity_log': get_recent_activity(),
        'rfid_count': get_rfid_count_summary(),
        'quick_stats': get_quarter_comparison(),
    }
    return render(request, 'dashboard/manager.html', context)
```

### **Frontend (Chart.js Examples):**
```javascript
// Breeding Trends Line Chart
new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb'],
        datasets: [
            {
                label: 'Imported Bulls',
                data: [45, 42, 38, 35, 32, 35, 33, 35, 36, 34, 35, 35, 35],
                borderColor: 'rgb(220, 38, 38)',
                backgroundColor: 'rgba(220, 38, 38, 0.1)'
            },
            {
                label: 'Local Bulls',
                data: [75, 76, 74, 75, 77, 75, 76, 74, 75, 76, 75, 75, 75],
                borderColor: 'rgb(34, 197, 94)',
                backgroundColor: 'rgba(34, 197, 94, 0.1)'
            }
        ]
    }
});

// Health Correlation Bar Chart
new Chart(ctx, {
    type: 'bar',
    data: {
        labels: [
            'Complete Vaccination',
            'Incomplete Vaccination',
            'No Recent Illness',
            'Illness (60 days)',
            'Optimal Weight',
            'Below Target Weight'
        ],
        datasets: [{
            data: [75, 12, 72, 32, 78, 53],
            backgroundColor: [
                'rgb(34, 197, 94)',
                'rgb(220, 38, 38)',
                'rgb(34, 197, 94)',
                'rgb(220, 38, 38)',
                'rgb(34, 197, 94)',
                'rgb(220, 38, 38)'
            ]
        }]
    },
    options: {
        indexAxis: 'y'  // Horizontal bars
    }
});
```

---

## ✅ DASHBOARD COMPLETION CHECKLIST

- [ ] All 12 sections implemented
- [ ] Data queries optimized (<2s page load)
- [ ] Charts render correctly
- [ ] Responsive on mobile
- [ ] Color coding applied
- [ ] Links/buttons functional
- [ ] Auto-refresh working
- [ ] Error handling (no data states)
- [ ] Export functionality (PDF reports)
- [ ] Tested with real data

---

**This dashboard transforms the manager from guessing to KNOWING. It's not just data visualization—it's decision intelligence.** 🎯