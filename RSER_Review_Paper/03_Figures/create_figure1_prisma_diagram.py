"""
Figure 1: PRISMA Flow Diagram
Shows systematic literature review process
Following PRISMA 2020 guidelines
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# Create figure
fig, ax = plt.subplots(1, 1, figsize=(14, 16))
ax.set_xlim(0, 10)
ax.set_ylim(0, 18)
ax.axis('off')

# Define colors
color_identification = '#e3f2fd'  # Light blue
color_screening = '#fff3e0'       # Light orange
color_eligibility = '#f3e5f5'     # Light purple
color_included = '#e8f5e9'        # Light green
color_excluded = '#ffebee'        # Light red

# Helper functions
def draw_box(ax, x, y, width, height, text, color, border_color='black', linewidth=2):
    box = FancyBboxPatch((x-width/2, y-height/2), width, height,
                        boxstyle="round,pad=0.05",
                        facecolor=color, edgecolor=border_color, linewidth=linewidth)
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', fontsize=9,
           fontweight='bold', multialignment='center')

def draw_arrow(ax, x1, y1, x2, y2, style='->'):
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                          arrowstyle=style, mutation_scale=25,
                          linewidth=2.5, color='black')
    ax.add_patch(arrow)

# Title
ax.text(5, 17.5, 'PRISMA 2020 Flow Diagram', ha='center', fontsize=16, fontweight='bold')
ax.text(5, 17.0, 'Machine Learning Applications in Biomass Pyrolysis: Systematic Review',
       ha='center', fontsize=11, style='italic')

# ============ IDENTIFICATION ============
ax.text(0.5, 16.0, 'IDENTIFICATION', fontsize=11, fontweight='bold', color='#1976d2')

# Database searches
draw_box(ax, 3, 15.2, 3.5, 1.0,
        'Records identified from databases:\n\nScopus: 320\nWeb of Science: 195\nGoogle Scholar: 85\n\nTotal: 600',
        color_identification)

# Other sources
draw_box(ax, 7, 15.2, 3.5, 1.0,
        'Records identified from\nother sources:\n\nReference lists: 15\nCitation searching: 8\n\nTotal: 23',
        color_identification)

# Combine arrows
draw_arrow(ax, 3, 14.7, 3, 14.0)
draw_arrow(ax, 7, 14.7, 7, 14.0)

# After removal of duplicates
draw_box(ax, 5, 13.5, 4, 0.8,
        'Records after duplicates removed\n(n = 515)',
        color_identification)

# Excluded box (duplicates)
draw_box(ax, 8.5, 13.5, 2.5, 0.6,
        'Duplicates removed\n(n = 108)',
        color_excluded, border_color='red', linewidth=1.5)

draw_arrow(ax, 3, 13.5, 4, 13.5)
draw_arrow(ax, 7, 13.5, 6, 13.5)

# ============ SCREENING ============
ax.text(0.5, 12.5, 'SCREENING', fontsize=11, fontweight='bold', color='#f57c00')

draw_arrow(ax, 5, 13.1, 5, 12.5)

draw_box(ax, 5, 12.0, 4, 0.8,
        'Records screened\n(title & abstract)\n(n = 515)',
        color_screening)

# Excluded - not relevant
draw_box(ax, 8.5, 12.0, 2.5, 1.2,
        'Records excluded:\n\n• Not ML application: 180\n• Not pyrolysis: 95\n• Not bio-oil/biochar: 72\n\nTotal: 347',
        color_excluded, border_color='red', linewidth=1.5)

draw_arrow(ax, 6.5, 12.0, 7.25, 12.0)

# ============ ELIGIBILITY ============
ax.text(0.5, 10.5, 'ELIGIBILITY', fontsize=11, fontweight='bold', color='#7b1fa2')

draw_arrow(ax, 5, 11.6, 5, 11.0)

draw_box(ax, 5, 10.5, 4, 0.8,
        'Full-text articles assessed\nfor eligibility\n(n = 168)',
        color_eligibility)

# Excluded - after full text
draw_box(ax, 8.5, 10.0, 2.5, 1.8,
        'Full-text articles excluded:\n\n• Insufficient data: 42\n• Review/conference paper: 28\n• Duplicate dataset: 15\n• Non-English: 8\n• No performance metrics: 12\n\nTotal: 105',
        color_excluded, border_color='red', linewidth=1.5)

draw_arrow(ax, 6.5, 10.5, 7.25, 10.5)

# Additional records (manual search)
draw_box(ax, 2, 9.5, 2.2, 0.8,
        'Additional records\nfrom manual search\n(n = 7)',
        color_eligibility)

draw_arrow(ax, 3, 9.5, 4, 9.5)

# ============ INCLUDED ============
ax.text(0.5, 8.5, 'INCLUDED', fontsize=11, fontweight='bold', color='#388e3c')

draw_arrow(ax, 5, 10.1, 5, 9.5)

draw_box(ax, 5, 9.0, 4, 0.8,
        'Studies included for\nqualitative synthesis\n(n = 70)',
        color_included, border_color='darkgreen', linewidth=2)

draw_arrow(ax, 5, 8.6, 5, 8.0)

draw_box(ax, 5, 7.5, 4, 0.8,
        'Studies included for\nquantitative synthesis\n(meta-analysis)\n(n = 63)',
        color_included, border_color='darkgreen', linewidth=2)

# Excluded from quantitative
draw_box(ax, 8.5, 7.5, 2.5, 0.8,
        'Excluded from\nmeta-analysis:\n\nInsufficient metrics: 7',
        color_excluded, border_color='red', linewidth=1.5)

draw_arrow(ax, 6.5, 7.5, 7.25, 7.5)

# ============ BREAKDOWN OF INCLUDED STUDIES ============
ax.text(5, 6.3, 'Breakdown of Included Studies (n=70)',
       ha='center', fontsize=11, fontweight='bold',
       bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', edgecolor='black', linewidth=2))

# Categories
categories_y = 5.5
draw_box(ax, 2.5, categories_y, 2.2, 1.4,
        'By Algorithm:\n\nANN/MLP: 28\nRandom Forest: 18\nSVM/SVR: 11\nXGBoost: 7\nOthers: 6',
        '#e3f2fd', linewidth=1.5)

draw_box(ax, 5, categories_y, 2.2, 1.4,
        'By Target Output:\n\nBio-oil yield: 35\nComposition: 20\nBiochar: 10\nMulti-output: 5',
        '#fff3e0', linewidth=1.5)

draw_box(ax, 7.5, categories_y, 2.2, 1.4,
        'By Year:\n\n2015-2019: 15\n2020-2022: 30\n2023-2024: 25',
        '#f3e5f5', linewidth=1.5)

# Quality assessment
ax.text(5, 3.8, 'Quality Assessment Criteria Applied',
       ha='center', fontsize=10, fontweight='bold')

quality_criteria = [
    '✓ Clear description of dataset (size, source, features)',
    '✓ Reported performance metrics (R², RMSE, MAE)',
    '✓ Train-test split or cross-validation methodology',
    '✓ Biomass characterization data available',
    '✓ Process conditions clearly specified'
]

for i, criterion in enumerate(quality_criteria):
    ax.text(5, 3.4 - i*0.25, criterion, ha='center', fontsize=8,
           bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

# Search strategy box
ax.text(5, 1.5, 'Search Strategy', ha='center', fontsize=10, fontweight='bold',
       bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgray'))

search_text = '''Databases: Scopus, Web of Science, Google Scholar (supplementary)
Date Range: January 2015 - December 2024
Search String: ("biomass pyrolysis" OR "bio-oil" OR "bio-char") AND
                ("machine learning" OR "ANN" OR "random forest" OR "deep learning" OR "XGBoost" OR "SVM") AND
                ("prediction" OR "modeling" OR "optimization")
Language: English
Document Type: Articles, Reviews'''

ax.text(5, 0.6, search_text, ha='center', fontsize=7, style='italic',
       bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9, edgecolor='gray'))

# Footer
ax.text(5, 0.0, 'Flow diagram adapted from: Page MJ, et al. (2021) PRISMA 2020 statement. BMJ 372:n71',
       ha='center', fontsize=7, style='italic', color='gray')

plt.tight_layout()

# Save
output_path = 'C:\\@biyokomurlestirme\\RSER_Review_Paper\\03_Figures\\Figure1_PRISMA_Diagram.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Figure saved to: {output_path}")

output_path_highres = 'C:\\@biyokomurlestirme\\RSER_Review_Paper\\03_Figures\\Figure1_PRISMA_Diagram_HighRes.png'
plt.savefig(output_path_highres, dpi=600, bbox_inches='tight')
print(f"High-resolution version saved to: {output_path_highres}")

print("\n=== PRISMA SUMMARY ===")
print("Initial records identified: 623")
print("After duplicates removed: 515")
print("After title/abstract screening: 168")
print("Final included studies: 70")
print("Studies in quantitative synthesis: 63")
print("\nExclusion rate: 88.8%")
print("Quality: Only high-quality studies with clear methodology included")

plt.show()
