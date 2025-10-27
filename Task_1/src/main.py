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
repGen.addSimpleFiltering(str(df['salary'].value_counts()))