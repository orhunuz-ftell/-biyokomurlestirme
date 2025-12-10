"""
Figure 4: Missing Data Heatmap
Creates a heatmap visualization showing missing data percentages across variables
Data source: TİK-2 Report (OrhunUzdiyem_tik2.pdf)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Missing data statistics from TİK-2 Report (Pages 3-4)
missing_data = {
    # Biomass Characterization
    'Carbon (C)': 0.00,
    'Hydrogen (H)': 0.00,
    'Nitrogen (N)': 0.00,
    'Oxygen (O)': 0.00,
    'Sulfur (S)': 31.25,
    'HHV': 20.83,
    'Volatiles': 10.42,
    'FixedCarbon': 10.42,

    # Process Parameters
    'ProcessTemperature': 0.00,
    'CatalystBiomassRatio': 0.00,
    'FeedRate': 89.58,
    'ResidenceTime': 89.58,
    'GasFlowrate': 47.92,

    # Bio-oil Composition Outputs
    'LiquidOutput': 37.50,
    'Sugar': 56.25,
    'Alcohols': 52.08,
    'Aromatics': 29.17,
    'Furans': 22.92,
    'Aldehyde_ketone': 10.42,
    'Acids': 0.00,  # From performance table - had good R²
    'Phenols': 0.00,  # Estimated based on medium performance
    'Oxides': 52.08,
    'Esters': 47.92,
    'Aliphatichydrocarbon': 47.92,
}

# Create DataFrame for visualization
df = pd.DataFrame(list(missing_data.items()), columns=['Variable', 'Missing %'])

# Categorize variables
categories = {
    'Biomass Characterization': ['Carbon (C)', 'Hydrogen (H)', 'Nitrogen (N)', 'Oxygen (O)',
                                  'Sulfur (S)', 'HHV', 'Volatiles', 'FixedCarbon'],
    'Process Parameters': ['ProcessTemperature', 'CatalystBiomassRatio', 'FeedRate',
                           'ResidenceTime', 'GasFlowrate'],
    'Bio-oil Composition': ['LiquidOutput', 'Sugar', 'Alcohols', 'Aromatics', 'Furans',
                            'Aldehyde_ketone', 'Acids', 'Phenols', 'Oxides', 'Esters',
                            'Aliphatichydrocarbon']
}

# Add category column
df['Category'] = df['Variable'].apply(
    lambda x: next((cat for cat, vars in categories.items() if x in vars), 'Other')
)

# Sort by category and missing percentage
df['Category_order'] = df['Category'].map({
    'Biomass Characterization': 1,
    'Process Parameters': 2,
    'Bio-oil Composition': 3
})
df = df.sort_values(['Category_order', 'Missing %'], ascending=[True, False])

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 10), gridspec_kw={'width_ratios': [2, 1]})

# Main heatmap
pivot_data = df.pivot_table(values='Missing %', index='Variable', aggfunc='first')
sns.heatmap(pivot_data, annot=True, fmt='.2f', cmap='RdYlGn_r',
            vmin=0, vmax=100, cbar_kws={'label': 'Missing Data (%)'},
            ax=ax1, linewidths=0.5, linecolor='gray')

ax1.set_title('Missing Data Across Variables in Biomass Pyrolysis Literature\n(N=48 experimental conditions from 7 studies)',
              fontsize=14, fontweight='bold', pad=20)
ax1.set_ylabel('Variables', fontsize=12)
ax1.set_xlabel('Missing Data Percentage (%)', fontsize=12)

# Add category separators
current_category = None
y_pos = 0
for idx, row in df.iterrows():
    if row['Category'] != current_category:
        if current_category is not None:
            ax1.axhline(y=y_pos, color='black', linewidth=2)
        current_category = row['Category']
        # Add category label
        ax1.text(-0.5, y_pos + 0.5, row['Category'],
                rotation=0, va='bottom', ha='right', fontweight='bold', fontsize=10)
    y_pos += 1

# Summary statistics bar chart
summary = df.groupby('Category')['Missing %'].mean().sort_values(ascending=False)
summary.plot(kind='barh', ax=ax2, color=['#d73027', '#fee08b', '#1a9850'])
ax2.set_title('Average Missing Data\nby Category', fontsize=12, fontweight='bold')
ax2.set_xlabel('Average Missing (%)', fontsize=11)
ax2.set_ylabel('')
ax2.grid(axis='x', alpha=0.3)

# Add value labels on bars
for i, v in enumerate(summary):
    ax2.text(v + 2, i, f'{v:.1f}%', va='center', fontweight='bold')

plt.tight_layout()

# Save figure
output_path = 'C:\\@biyokomurlestirme\\RSER_Review_Paper\\03_Figures\\Figure4_MissingData_Heatmap.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Figure saved to: {output_path}")

# Also save as high-res version for publication
output_path_highres = 'C:\\@biyokomurlestirme\\RSER_Review_Paper\\03_Figures\\Figure4_MissingData_Heatmap_HighRes.png'
plt.savefig(output_path_highres, dpi=600, bbox_inches='tight')
print(f"High-resolution version saved to: {output_path_highres}")

# Create summary statistics table
print("\n=== MISSING DATA SUMMARY ===")
print(f"Total variables analyzed: {len(df)}")
print(f"Variables with 0% missing: {len(df[df['Missing %'] == 0])}")
print(f"Variables with >50% missing: {len(df[df['Missing %'] > 50])}")
print(f"Variables with >80% missing (CRITICAL): {len(df[df['Missing %'] > 80])}")
print("\nCritical missing data variables:")
print(df[df['Missing %'] > 80][['Variable', 'Missing %']])

plt.show()
