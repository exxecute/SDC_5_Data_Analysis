# Multidimensional and Text analysis on titanic data

## 1. PCA (Principal Component Analysis)

- `Данные`: Titanic dataset (891 пассажир)
- `Целевая` переменная: `Survived` (2 уникальных значения: 0 — не выжил, 1 — выжил)
- `Выбранные признаки для анализа`: `Pclass, Age, SibSp, Parch, Fare`
- `Преобработка данных`:
  - Пропущенные значения в `Age` заменены на среднее.
  - Масштабирование данных с использованием `StandardScaler`.
- Результаты PCA:
  - Для сохранения 90% дисперсии необходимо 4 главные компоненты.
- Визуализация проекции на первые две главные компоненты:
  - Диаграмма рассеяния с цветом по Survived
    - ![image](./PCA.png)

## 2. Cluster Analysis (KMeans)
- `Метод`: KMeans с 2 кластерами
- `Данные`: PCA-преобразованные данные (4 компоненты)
- `Результаты`:
  - | Фактический класс | Кластер 0 | Кластер 1 |
    | ----------------- | --------- | --------- |
    | Не выжил (0)      | 445       | 104       |
    | Выжил (1)         | 195       | 147       |
- Визуализация кластеров на первых двух компонентах PCA:
  - ![image](./Cluster.png)

## 3. Text Analysis

- Пример текста для анализа:
  ```txt
  "Natural Language Processing is a field of AI that focuses on the interaction between humans and computers using natural language. Text analysis is essential for extracting insights from textual data."
  ```

- Этапы предобработки:
  - Токенизация: `['natural', 'language', 'processing', 'field', 'ai', 'focuses', ...]`
  - Удаление стоп-слов: Оставлены только значимые слова.
  - Стемминг (Porter, Lancaster, Snowball):
    - | Стеммер   | Результат                                           |
      | --------- | --------------------------------------------------- |
      | Porter    | ['natur', 'languag', 'process', 'field', 'ai', ...] |
      | Lancaster | ['nat', 'langu', 'process', 'field', 'ai', ...]     |
      | Snowball  | ['natur', 'languag', 'process', 'field', 'ai', ...] |
  - Лемматизация (WordNetLemmatizer): `['natural', 'language', 'processing', 'field', 'ai', ...]`

Вывод:
- Стемминг более грубый, может укорачивать слова до нечитабельной формы.
- Лемматизация сохраняет морфологически корректные формы слов, что удобно для семантического анализа.

- Частотный анализ слов:
  - | Слово      | Частота |
    | ---------- | ------- |
    | natural    | 2       |
    | language   | 2       |
    | processing | 1       |
    | field      | 1       |
    | ai         | 1       |
    | focuses    | 1       |

Визуализация наиболее часто встречающихся слов в тексте:
- ![image](./TextAnalysis.png)