# ===============================================================
# LAB WORK: Analysis of the Adult Income Dataset (adult.data.csv)
# ===============================================================

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

# ---------- Настройки ----------
plt.style.use("seaborn-v0_8")
sns.set_palette("Set2")
os.makedirs("plots", exist_ok=True)

# ---------- 1. Загрузка данных ----------
print("=" * 70)
print("📘 ЗАГРУЗКА ДАННЫХ")
print("=" * 70)
df = pd.read_csv("../../TheTask/adult.data.csv")

print(f"✅ Датасет загружен: {df.shape[0]} строк, {df.shape[1]} столбцов")
print("\n🔹 Первые 5 строк:")
print(df.head())

# ---------- 2. Очистка данных ----------
print("\n" + "=" * 70)
print("🧹 ОЧИСТКА ДАННЫХ")
print("=" * 70)

# Заменяем '?' на NaN
df.replace("?", np.nan, inplace=True)
print("\nКоличество пропусков по столбцам:")
print(df.isna().sum())

# Удаляем строки с пропусками
df.dropna(inplace=True)
print(f"\n✅ После очистки: {df.shape[0]} строк осталось.")

# Преобразуем категориальные переменные
for col in df.select_dtypes("object").columns:
    df[col] = df[col].astype("category")

print("\nТипы данных после преобразования:")
print(df.dtypes)

# ---------- 3. Исследовательский анализ ----------
print("\n" + "=" * 70)
print("🔍 ИССЛЕДОВАТЕЛЬСКИЙ АНАЛИЗ")
print("=" * 70)

print("\n🔹 Описательная статистика числовых переменных:")
print(df[["age", "fnlwgt", "hours-per-week"]].describe())

# Гистограммы
for col in ["age", "hours-per-week"]:
    plt.figure(figsize=(6, 4))
    sns.histplot(df[col], kde=True, bins=20)
    plt.title(f"Distribution of {col}")
    plt.savefig(f"plots/{col}_hist.png")
    plt.close()

# Boxplot: часы работы по уровню дохода
plt.figure(figsize=(7, 5))
sns.boxplot(x="salary", y="hours-per-week", data=df)
plt.title("Work Hours by Income Level")
plt.savefig("plots/hours_by_income.png")
plt.close()

# Распределение образования
plt.figure(figsize=(10, 5))
sns.countplot(y="education", data=df, order=df["education"].value_counts().index)
plt.title("Education Distribution")
plt.savefig("plots/education_distribution.png")
plt.close()

# ---------- 4. Простая фильтрация ----------
print("\n" + "=" * 70)
print("🔎 ПРОСТАЯ ФИЛЬТРАЦИЯ")
print("=" * 70)

print("\nДоходное распределение:")
print(df["salary"].value_counts())

print("\nДоход по полу:")
income_by_gender = df.groupby(["sex", "salary"]).size().unstack(fill_value=0)
print(income_by_gender)

# ---------- 5. Анализ категориальных переменных ----------
print("\n" + "=" * 70)
print("🧾 АНАЛИЗ КАТЕГОРИАЛЬНЫХ ПЕРЕМЕННЫХ")
print("=" * 70)

cat_cols = ["workclass", "education", "marital-status", "occupation", "native-country"]
for col in cat_cols:
    print(f"{col}: {df[col].nunique()} уникальных значений")

# ---------- 6. Проверка гипотез ----------
print("\n" + "=" * 70)
print("📊 СТАТИСТИЧЕСКИЕ ТЕСТЫ")
print("=" * 70)

# Пример: связь между полом и доходом
contingency = pd.crosstab(df["sex"], df["salary"])
chi2, p, dof, expected = chi2_contingency(contingency)
print("\nChi-square test (sex vs salary):")
print(f"chi2 = {chi2:.3f}, p-value = {p:.6f}")

if p < 0.05:
    print("✅ Разница статистически значима (p < 0.05)")
else:
    print("❌ Разница незначима (p >= 0.05)")

# ---------- 7. Моделирование дохода ----------
print("\n" + "=" * 70)
print("🤖 МОДЕЛИРОВАНИЕ ДОХОДА (>50K)")
print("=" * 70)

# Разделяем данные
X = df.drop("salary", axis=1)
y = df["salary"]

cat_features = X.select_dtypes("category").columns
num_features = X.select_dtypes("number").columns

# Препроцессор
preprocessor = ColumnTransformer(
    transformers=[("cat", OneHotEncoder(handle_unknown="ignore"), cat_features)],
    remainder="passthrough",
)

# Разделение train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# --- Модель 1: Логистическая регрессия ---
log_model = Pipeline(
    steps=[("preprocess", preprocessor), ("model", LogisticRegression(max_iter=500))]
)
log_model.fit(X_train, y_train)
y_pred = log_model.predict(X_test)

print("\n🔹 Logistic Regression Report:")
print(classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# --- Модель 2: Случайный лес ---
rf_model = Pipeline(
    steps=[
        ("preprocess", preprocessor),
        ("model", RandomForestClassifier(n_estimators=200, random_state=42)),
    ]
)
rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)

print("\n🔹 Random Forest Report:")
print(classification_report(y_test, rf_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, rf_pred))
print(f"Accuracy: {accuracy_score(y_test, rf_pred):.3f}")

# ---------- 8. Анализ важности признаков ----------
print("\n" + "=" * 70)
print("🎯 ВАЖНОСТЬ ПРИЗНАКОВ (Random Forest)")
print("=" * 70)

# Извлекаем признаки после One-Hot Encoding
ohe = rf_model.named_steps["preprocess"].named_transformers_["cat"]
cat_feature_names = ohe.get_feature_names_out(cat_features)
all_features = np.concatenate([cat_feature_names, num_features])

importances = rf_model.named_steps["model"].feature_importances_
feat_imp = pd.Series(importances, index=all_features).sort_values(ascending=False)[:15]
print(feat_imp)

plt.figure(figsize=(8, 5))
sns.barplot(x=feat_imp.values, y=feat_imp.index)
plt.title("Top 15 Feature Importances")
plt.savefig("plots/feature_importance.png")
plt.close()

# ---------- 9. Анализ разрыва доходов ----------
print("\n" + "=" * 70)
print("💰 АНАЛИЗ ДОХОДНЫХ РАЗРЫВОВ")
print("=" * 70)

income_gap = df.groupby(["sex", "race"])["salary"].value_counts(normalize=True).unstack()
print(income_gap)

# ---------- 10. Предсказание для нового примера ----------
print("\n" + "=" * 70)
print("🔮 ПРЕДСКАЗАНИЕ ДЛЯ НОВЫХ ДАННЫХ")
print("=" * 70)

new_data = pd.DataFrame({
    "age": [29],
    "workclass": ["Private"],
    "fnlwgt": [190000],
    "education": ["Bachelors"],
    "education-num": [13],
    "marital-status": ["Never-married"],
    "occupation": ["Tech-support"],
    "relationship": ["Not-in-family"],
    "race": ["White"],
    "sex": ["Female"],
    "capital-gain": [0],
    "capital-loss": [0],
    "hours-per-week": [40],
    "native-country": ["United-States"]
})
print("Новая запись:")
print(new_data)
print("Предсказанный доход:", rf_model.predict(new_data)[0])

print("\n✅ Лабораторная работа успешно выполнена!")
print("Все графики сохранены в папку: plots/")
