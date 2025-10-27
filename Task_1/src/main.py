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

plt.figure(figsize=(10, 6))
sns.heatmap(pd.pivot_table(df, index='sex', columns='education', values='hours-per-week', aggfunc='mean'), annot=True, fmt=".1f", cmap="YlGnBu")
plt.title("Средние часы работы по полу и уровню образования")
plt.xlabel("Уровень образования")
plt.ylabel("Пол")
plt.savefig(repGen.getFreqHeatmapPlace(), dpi=300, bbox_inches='tight')
