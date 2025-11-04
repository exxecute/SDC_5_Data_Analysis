import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# Import plotting modules and set up
import seaborn as sns

sns.set()
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker

DPI = 100

df = pd.read_csv("mlbootcamp5.csv", sep=';')
print("Dataset size: ", df.shape)

print("1. Single variable shape and distribution")
print(df.head())
print()

df["age_years"] = (df["age"] / 365).astype(int)

df["BMI"] = df["weight"] / (df["height"] / 100) ** 2

print("1.1 Age is given here in days. Please create a new field containing age in years")
print(df.head())
print()

print("1.2 Put down the general statistics information about this dataset")
print(df.describe())
print()

print("1.3 Put down type of each column in the dataset")
print(df.info())
print()

print("### 1.4 Histogram")
features = ["weight", "height", "age_years"]
iterator: int = 0

for feature in features:
    plt.figure()
    sns.histplot(df[feature], kde=True, stat="density", binwidth=1)
    plt.title(f"Distribution of {feature}")
    plt.savefig(str(iterator) + ".png", dpi=DPI, bbox_inches='tight')
    iterator += 1
print()

plt.figure()
sns.boxplot(x="weight", data=df)
plt.savefig(str(iterator) + ".png", dpi=DPI, bbox_inches='tight')
iterator += 1
print()

plt.figure()
sns.boxplot(x="height", data=df)
plt.savefig(str(iterator) + ".png", dpi=DPI, bbox_inches='tight')
iterator += 1
print()

plt.figure()
plt.scatter(df["weight"], df["BMI"], color='steelblue', alpha=0.7)
plt.xlabel("Weight (kg)")
plt.ylabel("BMI (Body Mass Index)")
plt.title("Relationship between Weight and BMI")
plt.grid(True)
plt.savefig(str(iterator) + ".png", dpi=DPI, bbox_inches='tight')
iterator += 1

plt.figure()
plt.scatter(df["weight"], df["height"], color='green', alpha=0.6)
plt.xlabel("Weight (kg)")
plt.ylabel("Height (cm)")
plt.title("Scatter Plot of Weight vs Height")
plt.grid(True)
plt.savefig(str(iterator) + ".png", dpi=DPI, bbox_inches='tight')
iterator += 1

df_melt = pd.melt(frame=df, value_vars=["height"], id_vars=["gender"])
plt.figure(figsize=(12, 10))
ax = sns.violinplot(
    x="variable",
    y="value",
    hue="gender",
    palette="muted",
    split=True,
    data=df_melt,
    scale="count",
    scale_hue=False,
)
plt.savefig(str(iterator) + ".png", dpi=DPI, bbox_inches='tight')
iterator += 1

plt.figure(figsize=(12,6))
sns.countplot(x="age_years", hue="cardio", data=df, palette="Set1")
plt.xlabel("Age (years)")
plt.ylabel("Number of People")
plt.title("Count of People by Age and Cardiovascular Disease")
plt.legend(title="Cardio")
plt.savefig(str(iterator) + ".png", dpi=DPI, bbox_inches='tight')
iterator += 1

plt.figure(figsize=(8,6))
ax = sns.countplot(x="gender", hue="alco", data=df, palette="Set2")
plt.xlabel("Gender")
plt.ylabel("Number of People")
plt.title("Alcohol Consumption by Gender")
plt.legend(title="Alcohol (0=No, 1=Yes)")

for p in ax.patches:
    height = p.get_height()
    ax.annotate(f'{int(height)}', 
                (p.get_x() + p.get_width() / 2., height),
                ha='center', va='bottom', fontsize=10, color='black')
plt.savefig(str(iterator) + ".png", dpi=DPI, bbox_inches='tight')
iterator += 1

smoking_old_men = df[
    (df["gender"] == 2)
    & (df["age_years"] >= 60)
    & (df["age_years"] < 65)
    & (df["smoke"] == 1)
].reset_index()
group_1 = smoking_old_men[(smoking_old_men["cholesterol"] == 1) & (smoking_old_men["ap_hi"] < 120)]
group_2 = smoking_old_men[(smoking_old_men["cholesterol"] == 3) & (smoking_old_men["ap_hi"] >= 160) & (smoking_old_men["ap_hi"] < 180)]
plt.figure(figsize=(8,6))

ax = sns.countplot(
    x="cardio",
    hue=pd.concat([group_1.assign(group="Low risk"), group_2.assign(group="High risk")])["group"],
    data=pd.concat([group_1.assign(group="Low risk"), group_2.assign(group="High risk")]),
    stat="percent",
    palette=["skyblue","salmon"]
)

plt.xlabel("Cardiovascular Disease (0=No, 1=Yes)")
plt.ylabel("Percentage (%)")
plt.title("Fraction of CVD in Low and High Risk Groups")

for p in ax.patches:
    height = p.get_height()
    ax.annotate(f'{height:.1f}%', 
                (p.get_x() + p.get_width() / 2., height),
                ha='center', va='bottom', fontsize=10, color='black')

plt.legend(title="Group")
plt.tight_layout()
plt.savefig(str(iterator) + ".png", dpi=DPI, bbox_inches='tight')
iterator += 1

df_uniques = pd.melt(
    frame=df,
    value_vars=["gender", "cholesterol", "gluc", "smoke", "alco", "active", "cardio"],
)
df_uniques = (
    pd.DataFrame(df_uniques.groupby(["variable", "value"])["value"].count())
    .sort_index(level=[0, 1])
    .rename(columns={"value": "count"})
    .reset_index()
)

g = sns.catplot(
    x="variable",
    y="count",
    hue="value",
    data=df_uniques,
    kind="bar",
    palette="Set2",
    height=6,
    aspect=1.5
)

g.set_xticklabels(rotation=45)
g.set_axis_labels("Feature", "Number of People")
g.fig.suptitle("Distribution of Binary and Categorical Features", fontsize=16)

ax = g.facet_axis(0, 0)
for p in ax.patches:
    height = p.get_height()
    ax.annotate(f'{int(height)}', 
                (p.get_x() + p.get_width() / 2., height),
                ha='center', va='bottom', fontsize=10, color='black')

plt.tight_layout()
plt.savefig(str(iterator) + ".png", dpi=DPI, bbox_inches='tight')
iterator += 1
