import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix, accuracy_score
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, LancasterStemmer, SnowballStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
from collections import Counter
from wordcloud import WordCloud

DPI = 100

## PCA

# Load Titanic dataset
titanic = pd.read_csv('./files/titanic_train.csv')

# Inspect dataset
print(titanic.head())
print(titanic.info())

# Target variable
y = titanic['Survived']

# Count unique values
num_classes = y.nunique()
print("Number of unique labels in target:", num_classes)

# Features selection (numerical features for PCA)
features = ['Pclass', 'Age', 'SibSp', 'Parch', 'Fare']
X = titanic[features].fillna(titanic[features].mean())  # Fill missing values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply PCA
pca = PCA(n_components=0.90)  # retain 90% variance
X_pca = pca.fit_transform(X_scaled)

print("Number of components to cover 90% variance:", pca.n_components_)

plt.figure(figsize=(8,6))
plt.scatter(X_pca[:,0], X_pca[:,1], c=y, cmap='viridis', alpha=0.6)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('PCA Projection of Titanic Dataset')
plt.colorbar(label='Survived')
plt.savefig("PCA" + ".png", dpi=DPI, bbox_inches='tight')

## Cluster analysis

# Assume 2 clusters (Survived / Not Survived)
kmeans = KMeans(n_clusters=2, random_state=42)
clusters = kmeans.fit_predict(X_pca)

# Visualize clusters
plt.figure(figsize=(8,6))
plt.scatter(X_pca[:,0], X_pca[:,1], c=clusters, cmap='coolwarm', alpha=0.6)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('KMeans Clustering on PCA-reduced Titanic Data')
plt.savefig("Cluster" + ".png", dpi=DPI, bbox_inches='tight')

# Compare cluster labels with actual labels

print(confusion_matrix(y, clusters))


## Text analysis
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

text = """Natural Language Processing is a field of AI that focuses on the interaction between humans and computers using natural language. Text analysis is essential for extracting insights from textual data."""

# Tokenization
tokens = word_tokenize(text.lower())

# Remove stop words
stop_words = set(stopwords.words('english'))
tokens_filtered = [word for word in tokens if word.isalpha() and word not in stop_words]

print("Filtered Tokens:", tokens_filtered)

porter = PorterStemmer()
lancaster = LancasterStemmer()
snowball = SnowballStemmer('english')

print("Porter:", [porter.stem(word) for word in tokens_filtered])
print("Lancaster:", [lancaster.stem(word) for word in tokens_filtered])
print("Snowball:", [snowball.stem(word) for word in tokens_filtered])

lemmatizer = WordNetLemmatizer()
lemmas = [lemmatizer.lemmatize(word) for word in tokens_filtered]
print("Lemmatized:", lemmas)

# Frequency count
freq = Counter(tokens_filtered)
print(freq.most_common(10))

# Word Cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(freq)

plt.figure(figsize=(10,5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.savefig("TextAnalysis" + ".png", dpi=DPI, bbox_inches='tight')

