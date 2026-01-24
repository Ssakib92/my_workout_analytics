# visuals.py
import numpy as np
import matplotlib.pyplot as plt

BODYWEIGHT_KG = 63

def radar_plot(tier1_df, title="Muscle Balance"):
    labels = tier1_df["Muscle Group"].tolist()
    values = (tier1_df["Intensity Score"] / BODYWEIGHT_KG).tolist()

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
    values += values[:1]
    angles = np.append(angles, angles[0])

    plt.figure(figsize=(6, 6))
    ax = plt.subplot(111, polar=True)
    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.25)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.set_title(title)
    plt.show()
