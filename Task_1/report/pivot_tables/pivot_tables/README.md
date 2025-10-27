# Pivot Tables

[<- Back](./../../README.md)

Средний возраст по уровню образования:
```sh
                    age
education              
10th          37.897561
11th          32.363550
12th          32.013263
1st-4th       44.622517
5th-6th       41.649306
7th-8th       47.631957
9th           40.303297
Assoc-acdm    37.286706
Assoc-voc     38.246366
Bachelors     38.641554
Doctorate     47.130667
HS-grad       38.640955
Masters       43.740012
Preschool     41.288889
Prof-school   44.249077
Some-college  36.135370

```

Средние рабочие часы в неделю по полу и образованию:
```sh
education       10th       11th       12th    1st-4th    5th-6th    7th-8th        9th  Assoc-acdm  Assoc-voc  Bachelors  Doctorate    HS-grad    Masters  Preschool  Prof-school  Some-college
sex                                                                                                                                                                                            
Female     32.548000  29.528302  31.524590  31.883721  34.942029  36.901515  34.739496   37.918987  38.542857  39.650460  47.703704  37.128783  41.406680  32.142857    44.896552     35.127643
Male       39.621053  36.750369  37.694118  40.962963  40.013699  41.134118  40.193452   43.288744  43.775822  44.373651  47.867347  42.847045  45.531306  39.000000    48.549451     41.985615

```

Количество людей по полу и типу работы:
```sh
workclass  Federal-gov  Local-gov  Private  Self-emp-inc  Self-emp-not-inc  State-gov  Without-pay
sex                                                                                               
Female             309        824     7642           126               392        484            5
Male               634       1243    14644           948              2107        795            9

```

Средний доход (вероятность >50K) по полу и образованию:
```sh
education   10th      11th      12th   1st-4th   5th-6th   7th-8th       9th  Assoc-acdm  Assoc-voc  Bachelors  Doctorate   HS-grad   Masters  Preschool  Prof-school  Some-college
sex                                                                                                                                                                                
Female     0.008  0.021563  0.016393  0.000000  0.028986  0.007576  0.042017    0.134177   0.134066   0.208279   0.604938  0.068577  0.337917        0.0     0.482759      0.073793
Male       0.100  0.075332  0.105882  0.055556  0.045662  0.080000  0.059524    0.331158   0.332160   0.513629   0.785714  0.208494  0.667263        0.0     0.800000      0.275953

```

Частота встречаемости workclass по стране и полу:
```sh
                       workclass
native-country sex              
Cambodia       Female          2
               Male           16
Canada         Female         34
               Male           73
China          Female         18
...                          ...
United-States  Male        18572
Vietnam        Female         22
               Male           42
Yugoslavia     Female          3
               Male           13

[81 rows x 1 columns]

```
