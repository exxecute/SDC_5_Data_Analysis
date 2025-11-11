# Import libraries
library(ggplot2)
library(dplyr)

# Load data sets
data(iris)
data(mtcars)

# View data
head(iris)
head(mtcars)

# Structure of the Iris dataset
str(iris)

# Summary of the Iris dataset
summary(iris)

# Pair plot of the Iris dataset
pairs(iris[, 1:4], main = "Pair plot of Iris Dataset")

# Boxplot of Sepal Length by Species
ggplot(iris, aes(x = Species, y = Sepal.Length)) + 
geom_boxplot(fill = "lightblue") +
ggtitle("Boxplot of Sepal Length by Species") +
xlab("Species") +
ylab("Sepal Length (cm)")

# Structure of the Mtcars dataset
str(mtcars)

# Summary of the Mtcars dataset
summary(mtcars)

# Scatter plot of mpg vs hp
ggplot(mtcars, aes(x = hp, y = mpg)) +
geom_point(color = "blue") +
ggtitle("Miles per Gallon vs Horsepower") +
xlab("Horsepower") +
ylab("Miles per Gallon")

# Bar graph of average mpg by number of cylinders
mtcars %>%
group_by(cyl) %>%
summarise(average_mpg = mean(mpg)) %>%
ggplot(aes(x = as.factor(cyl), y = average_mpg)) +
geom_bar(stat = "identity", fill = "orange") +
ggtitle("Average MPG by Number of Cylinders") +
xlab("Number of Cylinders") +
ylab("Average MPG")

# ANOVA test for Sepal Length
anova_results <- aov(Sepal.Length ~ Species, data = iris)
summary(anova_results)

# Correlation test between hp and mpg
cor.test(mtcars$hp, mtcars$mpg)
