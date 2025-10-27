from reportGenerator.reportGenerator import ReportGenerator
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy.stats import chi2_contingency
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
)

FILE: str = "../TheTask/adult.data.csv"

repGen: ReportGenerator = ReportGenerator()

# Settings
plt.style.use("seaborn-v0_8")
sns.set_palette("Set2")
os.makedirs("plots", exist_ok=True)

# Read data
df = pd.read_csv(FILE)

# Clear data
df.replace("?", np.nan, inplace=True)

## Delete rows with Nones
df.dropna(inplace=True)

# Main Points. Introduction.
## Basic Statistic
numeric_cols = ['age', 'fnlwgt', 'hours-per-week', 'education-num', 'capital-gain', 'capital-loss', 'hours-per-week']

for col in numeric_cols:
    repGen.addBasicStatistic(f"\n- Статистика по признаку '{col}':")
    repGen.addBasicStatistic(f"  - Среднее значение (mean): {df[col].mean():.2f}")
    repGen.addBasicStatistic(f"  - Медиана (median): {df[col].median():.2f}")
    repGen.addBasicStatistic(f"  - (mode): {df[col].mode()[0]}")
    repGen.addBasicStatistic(f"  - Минимум: {df[col].min()}")
    repGen.addBasicStatistic(f"  - Максимум: {df[col].max()}")

## Data Shape
repGen.addDataShape(statistic= df.head().to_string(),
                    shape= str(df.shape))

## Data Types
repGen.addDataTypes(str(df.dtypes))

## Count of Unique Values
categorical_columns = ['workclass', 'education', 'marital-status', 'occupation', 'native-country']

for col in categorical_columns:
    repGen.addUniqData(f"\n- {col}: {df[col].nunique()} уникальных значений")

repGen.addUniqData("\n ## Статистика по уникальным значениям\n")

for col in categorical_columns:
    repGen.addUniqData(f"\n- {col} — уникальные значения:")
    repGen.addUniqData("\n  - " + str(df[col].unique()))

## Value Counts
for col in categorical_columns:
    repGen.addUnicCounts(col=col, statistic=str(df[col].value_counts().sort_values(ascending=False)))

## Simple Filtering
repGen.addSimpleFiltering("Количество людей по уровню дохода:", str(df['salary'].value_counts()))
repGen.addSimpleFiltering("Доход по полу:", str(df.groupby('sex')['salary'].value_counts()))

# Pivot
## Pivot Tables
repGen.addPivotTable("Средний возраст по уровню образования:", str(pd.pivot_table(df, index='education', values='age', aggfunc='mean')))
repGen.addPivotTable("Средние рабочие часы в неделю по полу и образованию:", str(pd.pivot_table(df, index='sex', columns='education', values='hours-per-week', aggfunc='mean')))
repGen.addPivotTable("Количество людей по полу и типу работы:", str(pd.pivot_table(df, index='sex', columns='workclass', values='age', aggfunc='count')))
df['salary_num'] = df['salary'].apply(lambda x: 1 if x == '>50K' else 0)
repGen.addPivotTable("Средний доход (вероятность >50K) по полу и образованию:", str(pd.pivot_table(df, index='sex', columns='education', values='salary_num', aggfunc='mean')))
repGen.addPivotTable("Частота встречаемости workclass по стране и полу:", str(pd.pivot_table(df, index=['native-country', 'sex'], values='workclass', aggfunc='count')))

## Heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(pd.pivot_table(df, index='sex', columns='education', values='hours-per-week', aggfunc='mean'), annot=True, fmt=".1f", cmap="YlGnBu")
plt.title("Средние часы работы по полу и уровню образования")
plt.xlabel("Уровень образования")
plt.ylabel("Пол")
plt.savefig(repGen.getFreqHeatmapPlace(), dpi=300, bbox_inches='tight')

# Avansed
## Data Exploration
for col in numeric_cols:
    mean = df[col].mean()
    median = df[col].median()
    mode = df[col].mode()[0]
    min_val = df[col].min()
    max_val = df[col].max()
    range_val = max_val - min_val
    repGen.addDataEXploration(f"\nСтатистика по {col}:", f"Среднее: {mean:.2f}, Медиана: {median}, Мода: {mode}, Мин: {min_val}, Макс: {max_val}, Диапазон: {range_val}")

plt.figure(figsize=(8,5))
sns.histplot(df['age'], bins=20, kde=True, color='skyblue')
plt.title("Распределение возраста")
plt.xlabel("Возраст")
plt.ylabel("Количество людей")
plt.savefig(repGen.getDataExploration("age", "Распределение возраста"), dpi=300, bbox_inches='tight')

plt.figure(figsize=(8,5))
sns.boxplot(x=df['hours-per-week'], color='lightgreen')
plt.title("Распределение количества рабочих часов в неделю")
plt.xlabel("Часы работы в неделю")
plt.savefig(repGen.getDataExploration("hours_week", "Распределение количества рабочих часов в неделю"), dpi=300, bbox_inches='tight')

plt.figure(figsize=(8,5))
sns.scatterplot(x='age', y='hours-per-week', data=df, alpha=0.5)
plt.title("Возраст vs. Часы работы в неделю")
plt.xlabel("Возраст")
plt.ylabel("Часы работы")
plt.savefig(repGen.getDataExploration("age_hours", "Возраст vs. Часы работы в неделю"), dpi=300, bbox_inches='tight')

plt.figure(figsize=(6,4))
sns.countplot(x='sex', data=df, palette='pastel')
plt.title("Распределение по полу")
plt.xlabel("Пол")
plt.ylabel("Количество")
plt.savefig(repGen.getDataExploration("sex_rasp", "Распределение по полу"), dpi=300, bbox_inches='tight')

plt.figure(figsize=(8,4))
sns.countplot(x='race', data=df, palette='Set2')
plt.title("Распределение по расе")
plt.xlabel("Раса")
plt.ylabel("Количество")
plt.savefig(repGen.getDataExploration("race_rasp", "Распределение по расе"), dpi=300, bbox_inches='tight')

plt.figure(figsize=(10,5))
sns.countplot(y='education', data=df, order=df['education'].value_counts().index, palette='coolwarm')
plt.title("Распределение по уровню образования")
plt.xlabel("Количество людей")
plt.ylabel("Уровень образования")
plt.savefig(repGen.getDataExploration("ackn_rasp", "Распределение по уровню образования"), dpi=300, bbox_inches='tight')

marital_counts = df['marital-status'].value_counts()
plt.figure(figsize=(6,6))
plt.pie(marital_counts, labels=marital_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
plt.title("Распределение по семейному положению")
plt.savefig(repGen.getDataExploration("fam_rasp", "Распределение по семейному положению"), dpi=300, bbox_inches='tight')
