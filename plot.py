import matplotlib.pyplot as plt
import numpy as np

# Data
tasks = ["BLINK Spatial", "BLINK Depth", "BLINK Jigsaw", "Math Parity", "Math Convexity"]
models = [
    "GPT-4o",
    "Sketchpad + GPT-4o",
    "LLaVA 1.5",
    "Reported: GPT-4o",
    "Reported: Sketchpad + GPT-4o",
    "Reported: LLaVA 1.5"
]
scores = [
    [76.9, 75.0, 62.0, 86.5, 92.6],  # GPT-4o
    [79.7, 83.9, 70.0, 91.7, 93.8],  # Sketchpad + GPT-4o
    [59.4, 58.0, 52.7, 0.0, 0.0],  # LLaVA 1.5
    [72.0, 71.8, 64.0, 84.4, 87.2],  # Reported: GPT-4o
    [81.1, 83.9, 70.7, 94.7, 94.9],  # Reported: Sketchpad + GPT-4o
    [61.5, 52.4, 11.3, 0.0, 0.0]  # Reported: LLaVA 1.5
]

# Colors for the bars
colors = [
    "#1f77b4",  # GPT-4o
    "#ff7f0e",  # Sketchpad + GPT-4o
    "#2ca02c",  # LLaVA 1.5 (green)
    "#a1c4f4",  # Reported: GPT-4o (lighter blue)
    "#ffbb78",  # Reported: Sketchpad + GPT-4o (lighter orange)
    "#98df8a"  # Reported: LLaVA 1.5 (lighter green)
]

# Bar positions
x = np.arange(len(tasks))
width = 0.13

fig, ax = plt.subplots(figsize=(15, 5))

# Plot bars for each model
bars = []
for i, (model, score) in enumerate(zip(models, scores)):
    position = x + (i - len(models) / 2 + 0.5) * width
    bars.append(ax.bar(position, score, width, label=model, color=colors[i]))

# Adding text labels for scores
for bar_group, model_scores in zip(bars, scores):
    for bar, score in zip(bar_group, model_scores):
        if score > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5, f"{score:.1f}",
                    ha='center', va='bottom', fontsize=11, color="black")

# Adding deltas
# Deltas for Sketchpad and LLaVA
sketchpad_delta = np.array(scores[1]) - np.array(scores[0])  # Sketchpad + GPT-4o vs GPT-4o
reported_sketchpad_delta = np.array(scores[4]) - np.array(scores[3])  # Reported Sketchpad vs Reported GPT-4o
llava_delta = np.array(scores[2]) - np.array(scores[0])  # LLaVA 1.5 vs Reported LLaVA 1.5
reported_llava_delta = np.array(scores[5]) - np.array(scores[3])

# Add delta annotations for each relevant bar
for bar_group, delta, color in zip(
        [bars[1], bars[4], bars[2], bars[5]],
        [sketchpad_delta, reported_sketchpad_delta, llava_delta, reported_llava_delta],
        ["green", "green", "red", "red"]
):
    for bar, d in zip(bar_group, delta):
        if not np.isnan(d) and d != 0 and d > -80:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 8, f"({d:+.1f})",
                    ha='center', va='bottom', fontsize=12, color=color)
        # elif not np.isnan(d) and d != 0 and d<0:
        #     ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 8, f"({d:-.1f})",
        #             ha='center', va='bottom', fontsize=12, color=color)

# Adjust legend position (on top)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=6, fontsize=11)

# Labels and ticks
ax.set_xlabel("Tasks", fontsize=15)
ax.set_ylabel("Accuracy (%)", fontsize=15)
ax.set_xticks(x)
ax.set_xticklabels(tasks)

# Set y-axis range
ax.set_ylim(0, 100)

plt.tight_layout()
plt.show()