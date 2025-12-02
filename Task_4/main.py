# ---------------------------------------------------------------
# Lab 4 – Hypothesis Evaluation
# Full Python Script for All 10 Tasks
# ---------------------------------------------------------------

import numpy as np
import scipy.stats as stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# ---------------------------------------------------------------
# 1. One-Sample t-Test
# ---------------------------------------------------------------

data = [32, 28, 30, 29, 31, 35, 33, 27, 29, 28, 30, 34, 31, 29, 30]
t1, p1 = stats.ttest_1samp(data, 30)

print("\n1. ONE-SAMPLE t-TEST")
print("t-statistic:", t1, " p-value:", p1)

# Если p < 0.05 → доставка действительно отличается от 30 минут.
# Если p > 0.05 → нет доказательств отклонения.

# ---------------------------------------------------------------
# 2. Two-Sample Independent t-Test
# ---------------------------------------------------------------

traditional_scores = [78, 85, 88, 92, 76, 80, 84, 75, 83, 89]
new_method_scores = [90, 88, 85, 93, 95, 87, 84, 91, 92, 90]

t2, p2 = stats.ttest_ind(traditional_scores, new_method_scores, equal_var=False)

print("\n2. TWO-SAMPLE INDEPENDENT t-TEST")
print("t-statistic:", t2, " p-value:", p2)

# p < 0.05 → методы дают разные результаты.
# В нашем случае новый метод значимо лучше.

# ---------------------------------------------------------------
# 3. Paired t-Test
# ---------------------------------------------------------------

weights_before = [70, 82, 85, 90, 88, 76, 95, 78, 84, 72, 80, 86]
weights_after  = [68, 80, 83, 85, 86, 74, 90, 76, 82, 70, 78, 85]

t3, p3 = stats.ttest_rel(weights_before, weights_after)

print("\n3. PAIRED t-TEST")
print("t-statistic:", t3, " p-value:", p3)

# p < 0.05 → диета действительно влияет на вес.
# В нашем случае — уменьшает.

# ---------------------------------------------------------------
# 4. One-Sample t-Test with Normally Distributed Data
# ---------------------------------------------------------------

np.random.seed(0)
scores = np.random.normal(500, 30, 30)

t4, p4 = stats.ttest_1samp(scores, 500)

print("\n4. ONE-SAMPLE t-TEST WITH NORMAL DATA")
print("t-statistic:", t4, " p-value:", p4)

# Обычно p > 0.05 → средний результат не отличается от 500.

# ---------------------------------------------------------------
# 5. One-Sample z-Test for Population Mean
# ---------------------------------------------------------------

mu0 = 10
xbar = 9.5
sigma = 1.2
n = 50

z5 = (xbar - mu0) / (sigma / np.sqrt(n))
p5 = 2 * (1 - stats.norm.cdf(abs(z5)))

print("\n5. ONE-SAMPLE z-TEST (MEAN)")
print("z-statistic:", z5, " p-value:", p5)

# p < 0.05 → средняя длительность батареи действительно меньше 10.

# ---------------------------------------------------------------
# 6. Two-Sample z-Test for Means
# ---------------------------------------------------------------

mu1, mu2 = 75, 78
sd1, sd2 = 10, 8
n1, n2 = 80, 100

z6 = (mu1 - mu2) / np.sqrt(sd1**2 / n1 + sd2**2 / n2)
p6 = 2 * (1 - stats.norm.cdf(abs(z6)))

print("\n6. TWO-SAMPLE z-TEST (MEANS)")
print("z-statistic:", z6, " p-value:", p6)

# p < 0.05 → различия значимы.

# ---------------------------------------------------------------
# 7. One-Sample z-Test for Proportion
# ---------------------------------------------------------------

p0 = 0.6
n = 500
phat = 290 / 500

z7 = (phat - p0) / np.sqrt(p0 * (1 - p0) / n)
p7 = 2 * (1 - stats.norm.cdf(abs(z7)))

print("\n7. ONE-SAMPLE z-TEST (PROPORTION)")
print("z-statistic:", z7, " p-value:", p7)

# p > 0.05 → разница статистически незначима.

# ---------------------------------------------------------------
# 8. Two-Sample z-Test for Proportions
# ---------------------------------------------------------------

p1 = 250 / 1000
p2 = 320 / 1200
n1, n2 = 1000, 1200

p_pool = (250 + 320) / (1000 + 1200)

z8 = (p1 - p2) / np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
p8 = 2 * (1 - stats.norm.cdf(abs(z8)))

print("\n8. TWO-SAMPLE z-TEST (PROPORTIONS)")
print("z-statistic:", z8, " p-value:", p8)

# p < 0.05 → пропорции действительно различаются.

# ---------------------------------------------------------------
# 9. ANOVA test + Tukey Post-hoc
# ---------------------------------------------------------------

only_breast = [794.1, 716.9, 993., 724.7, 760.9, 908.2, 659.3, 690.8,
                768.7, 717.3, 630.7, 729.5, 714.1, 810.3, 583.5,
                679.9, 865.1]

only_formula = [898.8, 881.2, 940.2, 966.2, 957.5, 1061.7, 1046.2,
                 980.4, 895.6, 919.7, 1074.1, 952.5, 796.3, 859.6,
                 871.1, 1047.5, 919.1, 1160.5, 996.9]

both = [976.4, 656.4, 861.2, 706.8, 718.5, 717.1, 759.8, 894.6,
         867.6, 805.6, 765.4, 800.3, 789.9, 875.3, 740., 799.4,
         790.3, 795.2, 823.6, 818.7, 926.8, 791.7, 948.3]

f9, p9 = stats.f_oneway(only_breast, only_formula, both)

print("\n9. ANOVA TEST")
print("F-statistic:", f9, " p-value:", p9)

# Tukey post-hoc if ANOVA is significant
if p9 < 0.05:
    data_all = only_breast + only_formula + both
    group_labels = (["breast"] * len(only_breast) +
                    ["formula"] * len(only_formula) +
                    ["both"] * len(both))
    tukey = pairwise_tukeyhsd(data_all, group_labels, 0.05)
    print("\nPOST-HOC TUKEY TEST RESULTS:")
    print(tukey)

# p < 0.05 → хотя бы одна группа отличается.

# ---------------------------------------------------------------
# 10. Chi-Squared Test (User must insert actual table)
# ---------------------------------------------------------------

# p < 0.01 → зависимости есть
# p > 0.01 → пол и риск-аппетит независимы

table = np.array([ 
    [53, 23, 30, 36, 88],       # Male: 
    [71, 48, 51, 57, 203]       # Female: 
])

chi10, p10, dof10, expected10 = stats.chi2_contingency(table)

print("\n10. CHI-SQUARED TEST")
print("Chi-sq statistic:", chi10, " p-value:", p10)
print("\nExpected Frequencies:")
print(expected10)

# ---------------------------------------------------------------
# END OF SCRIPT
# ---------------------------------------------------------------
