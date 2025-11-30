"""
Critical Analysis of Reformer-Only Data
Chemical Engineering Professor Perspective
"""

import pyodbc
import numpy as np

conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-DRO84HP\\SQLEXPRESS;'
    'DATABASE=BIOOIL;'
    'Trusted_Connection=yes'
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

print('='*80)
print('CRITICAL ANALYSIS - Chemical Engineering Professor Review')
print('REFORMER-ONLY MODEL - Thermodynamic Validity Check')
print('='*80)
print()

# Analysis 1: Temperature Effect on H2 Production
print('1. TEMPERATURE EFFECT ON HYDROGEN PRODUCTION')
print('   Expectation: Higher temp -> More H2 (endothermic reforming)')
print('-'*80)

cursor.execute('''
    SELECT
        s.Temperature_C,
        AVG(o.H2_molpercent) AS Avg_H2,
        AVG(o.CH4_molpercent) AS Avg_CH4,
        AVG(o.CO_molpercent) AS Avg_CO,
        COUNT(*) AS Samples
    FROM ReformerSimulation s
    JOIN ReformerOutput o ON s.SimulationID = o.SimulationID
    WHERE s.Pressure_bar = 15 AND s.SC_Ratio = 4.0
    GROUP BY s.Temperature_C
    ORDER BY s.Temperature_C
''')

print('Temp(C)  H2(%)   CH4(%)  CO(%)   Samples  |  H2 Change  CH4 Change')
prev_h2 = None
prev_ch4 = None
h2_trend = []
ch4_trend = []
for row in cursor.fetchall():
    temp, h2, ch4, co, n = row
    h2_change = '' if prev_h2 is None else f'{h2-prev_h2:+6.2f}%'
    ch4_change = '' if prev_ch4 is None else f'{ch4-prev_ch4:+6.2f}%'
    print(f'{temp:6.0f}   {h2:6.2f}  {ch4:6.2f}  {co:6.2f}  {n:7.0f}   |  {h2_change:8s}  {ch4_change}')
    if prev_h2 is not None:
        h2_trend.append(h2 - prev_h2)
        ch4_trend.append(ch4 - prev_ch4)
    prev_h2 = h2
    prev_ch4 = ch4

print()
print('VERDICT:')
h2_increasing = all(x > 0 for x in h2_trend)
ch4_decreasing = all(x < 0 for x in ch4_trend)
if h2_increasing and ch4_decreasing:
    print('   ✓ [PASS] H2 increases and CH4 decreases with temperature')
    print('   ✓ [PASS] Consistent with Le Chatelier principle (endothermic)')
else:
    print('   ✗ [FAIL] Temperature trend is thermodynamically incorrect')
    print(f'         H2 trend: {h2_trend}')
    print(f'         CH4 trend: {ch4_trend}')
print()

# Analysis 2: Pressure Effect on Methanation
print('2. PRESSURE EFFECT ON METHANE FORMATION')
print('   Reaction: C + 2H2 -> CH4 (favored at HIGH pressure, fewer moles)')
print('-'*80)

cursor.execute('''
    SELECT
        s.Pressure_bar,
        AVG(o.CH4_molpercent) AS Avg_CH4,
        AVG(o.H2_molpercent) AS Avg_H2,
        COUNT(*) AS Samples
    FROM ReformerSimulation s
    JOIN ReformerOutput o ON s.SimulationID = o.SimulationID
    WHERE s.Temperature_C = 750 AND s.SC_Ratio = 4.0
    GROUP BY s.Pressure_bar
    ORDER BY s.Pressure_bar
''')

print('Pressure(bar)  CH4(%)  H2(%)   Samples  |  CH4 Change')
prev_ch4 = None
ch4_vals = []
for row in cursor.fetchall():
    press, ch4, h2, n = row
    ch4_vals.append(ch4)
    ch4_change = '' if prev_ch4 is None else f'{ch4-prev_ch4:+6.2f}%'
    print(f'{press:13.0f}  {ch4:6.2f}  {h2:6.2f}  {n:7.0f}   |  {ch4_change}')
    prev_ch4 = ch4

print()
print('VERDICT:')
ch4_increase = ch4_vals[-1] - ch4_vals[0]
print(f'   CH4 @ 5 bar = {ch4_vals[0]:.2f}%')
print(f'   CH4 @ 30 bar = {ch4_vals[-1]:.2f}%')
print(f'   Increase = {ch4_increase:+.2f} percentage points')
if ch4_increase > 3:
    print('   ✓ [PASS] CH4 increases with pressure (thermodynamically correct)')
else:
    print('   ✗ [FAIL] CH4 should increase significantly with pressure')
print()

# Analysis 3: Steam-to-Carbon Ratio Effect
print('3. STEAM-TO-CARBON RATIO EFFECT')
print('   Higher S/C -> More H2, Less CH4, More H2O')
print('-'*80)

cursor.execute('''
    SELECT
        s.SC_Ratio,
        AVG(o.H2_molpercent) AS Avg_H2,
        AVG(o.CO_molpercent) AS Avg_CO,
        AVG(o.CH4_molpercent) AS Avg_CH4,
        AVG(o.H2O_molpercent) AS Avg_H2O,
        COUNT(*) AS Samples
    FROM ReformerSimulation s
    JOIN ReformerOutput o ON s.SimulationID = o.SimulationID
    WHERE s.Temperature_C = 750 AND s.Pressure_bar = 15
    GROUP BY s.SC_Ratio
    ORDER BY s.SC_Ratio
''')

print('S/C    H2(%)   CO(%)   CH4(%)  H2O(%)  Samples')
h2o_vals = []
ch4_vals_sc = []
for row in cursor.fetchall():
    sc, h2, co, ch4, h2o, n = row
    h2o_vals.append(h2o)
    ch4_vals_sc.append(ch4)
    print(f'{sc:3.1f}   {h2:6.2f}  {co:6.2f}  {ch4:6.2f}  {h2o:6.2f}  {n:7.0f}')

print()
print('VERDICT:')
h2o_increasing = h2o_vals[-1] > h2o_vals[0]
ch4_decreasing_sc = ch4_vals_sc[-1] < ch4_vals_sc[0]
if h2o_increasing and ch4_decreasing_sc:
    print('   ✓ [PASS] H2O increases and CH4 decreases with S/C ratio')
    print('   ✓ [PASS] More steam suppresses methanation (correct)')
else:
    print('   ✗ [FAIL] S/C ratio effect is incorrect')
print()

# Analysis 4: Mass Balance Check
print('4. MASS BALANCE VALIDATION')
print('-'*80)

cursor.execute('''
    SELECT
        MIN(o.H2_molpercent + o.CO_molpercent + o.CO2_molpercent +
            o.CH4_molpercent + o.H2O_molpercent) AS Min_Total,
        MAX(o.H2_molpercent + o.CO_molpercent + o.CO2_molpercent +
            o.CH4_molpercent + o.H2O_molpercent) AS Max_Total,
        AVG(o.H2_molpercent + o.CO_molpercent + o.CO2_molpercent +
            o.CH4_molpercent + o.H2O_molpercent) AS Avg_Total
    FROM ReformerOutput o
''')

row = cursor.fetchone()
min_total, max_total, avg_total = row
print(f'Sum of major species (H2 + CO + CO2 + CH4 + H2O):')
print(f'  Minimum: {min_total:.4f}%')
print(f'  Maximum: {max_total:.4f}%')
print(f'  Average: {avg_total:.4f}%')
print()
if abs(avg_total - 100) < 0.1 and abs(min_total - 100) < 1.0:
    print('   ✓ [PASS] Mass balance closes within acceptable tolerance')
else:
    print('   ✗ [FAIL] Mass balance error too large')
print()

# Analysis 5: H2/CO Ratio Realism
print('5. H2/CO RATIO - SYNGAS QUALITY INDICATOR')
print('-'*80)

cursor.execute('''
    SELECT
        MIN(p.H2_CO_Ratio) AS Min_Ratio,
        MAX(p.H2_CO_Ratio) AS Max_Ratio,
        AVG(p.H2_CO_Ratio) AS Avg_Ratio
    FROM ReformerPerformance p
''')

row = cursor.fetchone()
print(f'H2/CO molar ratio:')
print(f'  Minimum: {row[0]:.2f}')
print(f'  Maximum: {row[1]:.2f}')
print(f'  Average: {row[2]:.2f}')
print()
print('Literature reference for steam reforming:')
print('  Ethanol: H2/CO = 2-4 (typical)')
print('  Glycerol: H2/CO = 2-5')
print('  With high S/C ratio: Can reach 8-12')
print()
if 2 <= row[2] <= 12:
    print('   ✓ [PASS] H2/CO ratios are in realistic range')
else:
    print('   ✗ [WARNING] H2/CO ratios unusual for steam reforming')
print()

# Analysis 6: Composition Range Check
print('6. COMPOSITION RANGES - PHYSICAL VALIDITY')
print('-'*80)

cursor.execute('''
    SELECT
        MIN(H2_molpercent) AS Min_H2,
        MAX(H2_molpercent) AS Max_H2,
        AVG(H2_molpercent) AS Avg_H2,
        MIN(CO_molpercent) AS Min_CO,
        MAX(CO_molpercent) AS Max_CO,
        AVG(CO_molpercent) AS Avg_CO,
        MIN(CO2_molpercent) AS Min_CO2,
        MAX(CO2_molpercent) AS Max_CO2,
        AVG(CO2_molpercent) AS Avg_CO2,
        MIN(CH4_molpercent) AS Min_CH4,
        MAX(CH4_molpercent) AS Max_CH4,
        AVG(CH4_molpercent) AS Avg_CH4
    FROM ReformerOutput
''')

row = cursor.fetchone()
print('Species  Min(%)   Max(%)   Avg(%)   Expected Range  Status')
specs = [
    ('H2', row[0], row[1], row[2], (15, 70)),
    ('CO', row[3], row[4], row[5], (1, 25)),
    ('CO2', row[6], row[7], row[8], (5, 35)),
    ('CH4', row[9], row[10], row[11], (0, 30))
]

all_pass = True
for species, min_val, max_val, avg_val, (exp_min, exp_max) in specs:
    status = 'OK' if exp_min <= avg_val <= exp_max else 'UNUSUAL'
    if status == 'UNUSUAL':
        all_pass = False
    print(f'{species:7s}  {min_val:6.2f}   {max_val:6.2f}   {avg_val:6.2f}   {exp_min:2d}-{exp_max:2d}%        [{status}]')

print()
if all_pass:
    print('   ✓ [PASS] All species within expected ranges for steam reforming')
else:
    print('   ✗ [WARNING] Some species outside typical ranges')
print()

# Analysis 7: Bio-oil Composition Effect
print('7. BIO-OIL COMPOSITION IMPACT')
print('   Does bio-oil composition actually affect H2 production?')
print('-'*80)

cursor.execute('''
    SELECT TOP 5
        b.BiooilId,
        b.aromatics,
        b.alcohols,
        AVG(o.H2_molpercent) AS Avg_H2,
        AVG(o.CH4_molpercent) AS Avg_CH4
    FROM ReformerSimulation s
    JOIN Biooil b ON s.BiooilID = b.BiooilId
    JOIN ReformerOutput o ON s.SimulationID = o.SimulationID
    WHERE s.Temperature_C = 750 AND s.Pressure_bar = 15 AND s.SC_Ratio = 4.0
        AND b.aromatics IS NOT NULL AND b.alcohols IS NOT NULL
    GROUP BY b.BiooilId, b.aromatics, b.alcohols
    ORDER BY b.aromatics DESC
''')

print('BiooilID  Aromatic(%)  Alcohol(%)  Avg_H2(%)  Avg_CH4(%)')
data = cursor.fetchall()
for row in data:
    print(f'{row[0]:8d}  {row[1]:11.2f}  {row[2]:10.2f}  {row[3]:9.2f}  {row[4]:10.2f}')

print()
print('VERDICT:')
if len(data) >= 2:
    h2_varies = abs(data[0][3] - data[-1][3]) > 2  # More than 2% variation
    if h2_varies:
        print('   ✓ [PASS] Bio-oil composition affects H2 production (variance observed)')
    else:
        print('   ✗ [FAIL] H2 production shows no sensitivity to bio-oil composition')
else:
    print('   [INFO] Insufficient data for bio-oil composition analysis')
print()

# Final Summary
print('='*80)
print('OVERALL ASSESSMENT')
print('='*80)
print()
print('Thermodynamic Validity Checks:')
print(f'  Temperature effect:    {"PASS ✓" if h2_increasing and ch4_decreasing else "FAIL ✗"}')
print(f'  Pressure effect:       {"PASS ✓" if ch4_increase > 3 else "FAIL ✗"}')
print(f'  S/C ratio effect:      {"PASS ✓" if h2o_increasing and ch4_decreasing_sc else "FAIL ✗"}')
print(f'  Mass balance:          {"PASS ✓" if abs(avg_total - 100) < 0.1 else "FAIL ✗"}')
print(f'  H2/CO ratio range:     {"PASS ✓" if 2 <= row[2] <= 12 else "WARNING ⚠"}')
print(f'  Species composition:   {"PASS ✓" if all_pass else "WARNING ⚠"}')
print()

cursor.close()
conn.close()

print('='*80)
print('END OF ANALYSIS')
print('='*80)
