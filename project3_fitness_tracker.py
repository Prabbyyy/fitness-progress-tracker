# ============================================================
# PROJECT 3: Fitness Training Tracker & Progress Visualiser
# Tools: Python, Pandas, Matplotlib, NumPy
# Use case: Track and visualise trainee progress over weeks
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from datetime import date, timedelta

# ── 1. Generate Sample Training Log Data ─────────────────
# Simulates 10 trainees tracked over 8 weeks
# Metrics: bodyweight (kg), bench press 1RM (kg), squat 1RM (kg),
#          deadlift 1RM (kg), weekly volume (total sets x reps x kg)

np.random.seed(7)
trainees = [f"Trainee_{i+1}" for i in range(10)]
weeks    = list(range(1, 9))

records = []
for t in trainees:
    bw_start    = np.random.uniform(60, 90)
    bench_start = np.random.uniform(40, 70)
    squat_start = np.random.uniform(50, 90)
    dl_start    = np.random.uniform(60, 100)
    vol_start   = np.random.uniform(8000, 15000)

    for w in weeks:
        records.append({
            "Trainee"      : t,
            "Week"         : w,
            "Bodyweight_kg": round(bw_start    + np.random.uniform(-0.3, 0.5) * w, 1),
            "Bench_1RM_kg" : round(bench_start + np.random.uniform(0.3, 1.2)  * w, 1),
            "Squat_1RM_kg" : round(squat_start + np.random.uniform(0.5, 1.5)  * w, 1),
            "Deadlift_1RM_kg": round(dl_start  + np.random.uniform(0.5, 2.0)  * w, 1),
            "Weekly_Volume": round(vol_start   + np.random.uniform(100, 500)  * w, 0),
        })

df = pd.DataFrame(records)
df.to_csv("fitness_log.csv", index=False)
print("Training log saved as fitness_log.csv")
print(df.head(10).to_string(index=False))

# ── 2. Summary Statistics (Week 1 vs Week 8) ─────────────
w1 = df[df['Week'] == 1].set_index('Trainee')
w8 = df[df['Week'] == 8].set_index('Trainee')

summary = pd.DataFrame({
    "Bench_Gain_kg"   : (w8['Bench_1RM_kg']    - w1['Bench_1RM_kg']).round(1),
    "Squat_Gain_kg"   : (w8['Squat_1RM_kg']    - w1['Squat_1RM_kg']).round(1),
    "Deadlift_Gain_kg": (w8['Deadlift_1RM_kg'] - w1['Deadlift_1RM_kg']).round(1),
    "Volume_Gain"     : (w8['Weekly_Volume']    - w1['Weekly_Volume']).round(0),
})

print("\n── 8-Week Progress Summary ──────────────────────────")
print(summary.to_string())
print(f"\nAverage Bench Gain  : {summary['Bench_Gain_kg'].mean():.1f} kg")
print(f"Average Squat Gain  : {summary['Squat_Gain_kg'].mean():.1f} kg")
print(f"Average Deadlift Gain: {summary['Deadlift_Gain_kg'].mean():.1f} kg")

# ── 3. Visualisation ──────────────────────────────────────

# 3a. Group average strength progress over 8 weeks
avg = df.groupby('Week')[['Bench_1RM_kg','Squat_1RM_kg','Deadlift_1RM_kg']].mean()

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

ax = axes[0]
for col, color, label in zip(
    ['Bench_1RM_kg','Squat_1RM_kg','Deadlift_1RM_kg'],
    ['steelblue','tomato','seagreen'],
    ['Bench Press','Squat','Deadlift']
):
    ax.plot(avg.index, avg[col], marker='o', color=color, label=label, linewidth=2)
ax.set_title("Average 1RM Progress – Group (8 Weeks)")
ax.set_xlabel("Week")
ax.set_ylabel("1RM (kg)")
ax.legend()
ax.grid(alpha=0.3)

# 3b. Individual bench press progress (all 10 trainees)
ax2 = axes[1]
for t in trainees:
    sub = df[df['Trainee'] == t]
    ax2.plot(sub['Week'], sub['Bench_1RM_kg'], alpha=0.6, linewidth=1.2)
ax2.set_title("Individual Bench Press Progression – All Trainees")
ax2.set_xlabel("Week")
ax2.set_ylabel("Bench 1RM (kg)")
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig("fitness_group_progress.png", dpi=150)
plt.show()

# 3c. 8-week gain bar chart per trainee
fig, ax = plt.subplots(figsize=(12, 5))
x = np.arange(len(summary))
w = 0.25
ax.bar(x - w,   summary['Bench_Gain_kg'],    width=w, label='Bench',    color='steelblue')
ax.bar(x,       summary['Squat_Gain_kg'],    width=w, label='Squat',    color='tomato')
ax.bar(x + w,   summary['Deadlift_Gain_kg'], width=w, label='Deadlift', color='seagreen')
ax.set_xticks(x)
ax.set_xticklabels(summary.index, rotation=45, ha='right')
ax.set_title("8-Week Strength Gains per Trainee")
ax.set_ylabel("Gain (kg)")
ax.legend()
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("fitness_individual_gains.png", dpi=150)
plt.show()

print("\nAll plots saved.")

# ── 4. Flag Underperforming Trainees ─────────────────────
threshold = 3.0   # kg — expected minimum bench gain in 8 weeks
underperforming = summary[summary['Bench_Gain_kg'] < threshold]
if not underperforming.empty:
    print("\n⚠ Trainees below expected bench progress threshold:")
    print(underperforming[['Bench_Gain_kg']].to_string())
else:
    print("\nAll trainees met the minimum progress threshold.")
