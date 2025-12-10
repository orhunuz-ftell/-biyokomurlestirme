"""
Figure 5: Data Preprocessing Workflow
Creates a flowchart showing the systematic data preprocessing approach
Based on TİK-2 and TİK-3 methodologies
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Create figure
fig, ax = plt.subplots(1, 1, figsize=(16, 12))
ax.set_xlim(0, 10)
ax.set_ylim(0, 14)
ax.axis('off')

# Define colors for different process types
color_input = '#e8f4f8'      # Light blue - input
color_process = '#fff4e6'    # Light orange - processing
color_decision = '#ffe6f0'   # Light pink - decision
color_output = '#e6f9e6'     # Light green - output
color_imputation = '#f3e5f5' # Light purple - imputation methods

# Helper function to draw boxes
def draw_box(ax, x, y, width, height, text, color, style='round'):
    if style == 'round':
        box = FancyBboxPatch((x-width/2, y-height/2), width, height,
                            boxstyle="round,pad=0.1",
                            facecolor=color, edgecolor='black', linewidth=2)
    elif style == 'diamond':
        # Diamond for decision boxes
        points = np.array([[x, y+height/2], [x+width/2, y],
                          [x, y-height/2], [x-width/2, y]])
        box = mpatches.Polygon(points, facecolor=color, edgecolor='black', linewidth=2)
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', fontsize=9,
           fontweight='bold', wrap=True)

# Helper function to draw arrows
def draw_arrow(ax, x1, y1, x2, y2, label='', style='->'):
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                          arrowstyle=style, mutation_scale=20,
                          linewidth=2, color='black')
    ax.add_patch(arrow)
    if label:
        mid_x, mid_y = (x1+x2)/2, (y1+y2)/2
        ax.text(mid_x+0.3, mid_y, label, fontsize=8,
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

# Title
ax.text(5, 13.5, 'Data Preprocessing Workflow for Bio-oil Composition Prediction',
       ha='center', fontsize=14, fontweight='bold')
ax.text(5, 13.0, 'Systematic Missing Data Handling Strategy (TİK-2 & TİK-3 Methodology)',
       ha='center', fontsize=11, style='italic', color='gray')

# Step 1: Raw Data Input
draw_box(ax, 5, 11.5, 3, 0.8, 'Raw Data from Literature\n(70 samples, 14 studies)', color_input)

# Arrow down
draw_arrow(ax, 5, 11.1, 5, 10.5)

# Step 2: Missing Data Detection
draw_box(ax, 5, 10.0, 3.5, 0.8, 'Missing Data Detection\n(10% to 90% missing across variables)', color_process)

# Arrow down
draw_arrow(ax, 5, 9.6, 5, 9.0)

# Step 3: Decision - Can be calculated?
draw_box(ax, 5, 8.5, 2.5, 0.8, 'Can be calculated\nfrom other variables?', color_decision, style='diamond')

# Branch 1: YES - Calculation-based imputation (LEFT)
draw_arrow(ax, 3.75, 8.5, 2.5, 8.5, label='YES')

draw_box(ax, 1.8, 7.5, 2.2, 1.5,
        'Calculation-Based\nImputation:\n\n• O/C = O% / C%\n• H/C = H% / C%\n• Holocellulose =\n  Cellulose + Hemicellulose\n• Duration synthesis',
        color_imputation)

# Branch 2: NO - Continue to next decision (RIGHT)
draw_arrow(ax, 6.25, 8.5, 7.5, 8.5, label='NO')

# Step 4: Decision - High correlation with other features?
draw_box(ax, 8.5, 7.5, 2.5, 0.8, 'High correlation\nwith other features?', color_decision, style='diamond')

# Branch 2a: YES - KNN Imputation
draw_arrow(ax, 8.5, 7.1, 8.5, 6.5, label='YES')

draw_box(ax, 8.5, 5.5, 2.5, 1.5,
        'KNN Imputation:\n\n• Volatiles, FixedCarbon\n  (predictors: O/C, H/C, S, Ash)\n\n• HHV\n  (predictors: composition +\n   structural features)\n\n• Cellulose, Hemicellulose\n  (with constraint scaling)',
        color_imputation)

# Branch 2b: NO - Mean/Median Imputation
draw_arrow(ax, 9.75, 7.5, 10.5, 7.5, label='NO')

draw_box(ax, 11.5, 7.5, 1.8, 1.2,
        'Mean/Median\nImputation:\n\n• Nitrogen (N)\n• Low variance\n  variables',
        color_imputation)

# Converge all branches
draw_arrow(ax, 1.8, 6.7, 1.8, 5.5)
draw_arrow(ax, 1.8, 5.5, 5, 5.5)

draw_arrow(ax, 8.5, 4.7, 8.5, 4.0)
draw_arrow(ax, 8.5, 4.0, 5, 4.0)
draw_arrow(ax, 5, 5.5, 5, 4.5)

draw_arrow(ax, 11.5, 6.9, 11.5, 4.0)
draw_arrow(ax, 11.5, 4.0, 5, 4.0)

# Step 5: Combined imputed dataset
draw_box(ax, 5, 3.5, 3, 0.6, 'Combined Imputed Dataset', color_output)

# Arrow down
draw_arrow(ax, 5, 3.2, 5, 2.8)

# Step 6: Feature Engineering
draw_box(ax, 5, 2.3, 3.5, 0.8,
        'Feature Engineering & Scaling\n(StandardScaler for normalization)',
        color_process)

# Arrow down
draw_arrow(ax, 5, 1.9, 5, 1.5)

# Step 7: Train-Test Split
draw_box(ax, 5, 1.0, 3, 0.6, 'Train-Test Split (80-20)', color_process)

# Final outputs (two branches)
draw_arrow(ax, 3.5, 0.7, 2.5, 0.2)
draw_arrow(ax, 6.5, 0.7, 7.5, 0.2)

draw_box(ax, 2.0, -0.3, 1.8, 0.6, 'Training Set\n(56 samples)', color_output)
draw_box(ax, 8.0, -0.3, 1.8, 0.6, 'Test Set\n(14 samples)', color_output)

# Add legend box
legend_y = 0.5
legend_elements = [
    ('Input Data', color_input),
    ('Processing', color_process),
    ('Decision Point', color_decision),
    ('Imputation Method', color_imputation),
    ('Output', color_output)
]

ax.text(0.5, legend_y+1.3, 'Legend:', fontsize=10, fontweight='bold')
for i, (label, color) in enumerate(legend_elements):
    y_pos = legend_y - i*0.25
    rect = mpatches.Rectangle((0.3, y_pos-0.1), 0.3, 0.15,
                              facecolor=color, edgecolor='black', linewidth=1)
    ax.add_patch(rect)
    ax.text(0.75, y_pos, label, fontsize=8, va='center')

# Add key statistics box
stats_box_y = 11.5
ax.text(9.5, stats_box_y+0.3, 'Key Statistics:', fontsize=9, fontweight='bold',
       bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', edgecolor='black', linewidth=2))
ax.text(9.5, stats_box_y-0.1, '• 89.58% missing:\n  FeedRate, ResidenceTime', fontsize=7, va='top')
ax.text(9.5, stats_box_y-0.6, '• 56.25% missing: Sugar', fontsize=7, va='top')
ax.text(9.5, stats_box_y-0.9, '• 47-52% missing:\n  Alcohols, Esters,\n  Aliphatics, Oxides', fontsize=7, va='top')

# Add methodology notes
ax.text(5, -1.0, 'Notes: (1) Calculation-based methods preserve chemical relationships exactly\n' +
                 '(2) KNN imputation (k=5) preserves inter-variable correlations\n' +
                 '(3) Constraint-based scaling ensures physical consistency (e.g., Cellulose + Hemicellulose ≤ Holocellulose)',
       ha='center', fontsize=8, style='italic', color='dimgray',
       bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8, edgecolor='gray'))

plt.tight_layout()

# Save figure
output_path = 'C:\\@biyokomurlestirme\\RSER_Review_Paper\\03_Figures\\Figure5_Preprocessing_Workflow.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Figure saved to: {output_path}")

# High-resolution version
output_path_highres = 'C:\\@biyokomurlestirme\\RSER_Review_Paper\\03_Figures\\Figure5_Preprocessing_Workflow_HighRes.png'
plt.savefig(output_path_highres, dpi=600, bbox_inches='tight')
print(f"High-resolution version saved to: {output_path_highres}")

print("\n=== PREPROCESSING WORKFLOW SUMMARY ===")
print("Three-tier imputation strategy implemented:")
print("1. Calculation-based (exact, no estimation error)")
print("2. KNN imputation (preserves correlations, k=5)")
print("3. Mean/median (simple, for low-variance variables)")
print("\nFinal dataset: 70 samples, 80-20 train-test split")

plt.show()
