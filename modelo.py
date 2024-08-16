# -*- coding: utf-8 -*-
"""Mini_MODELO_ATUAL_13_AGO_2024.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Vc9k4X1BOJL7A08eBjIYoIo52lcO5UJg

**Base de dados do SUAP do IFSULDEMINAS Campus Machado MG**
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,f1_score,precision_score,recall_score

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn import svm


from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import VotingClassifier

"""**1- Carregando dados**"""

#data = pd.read_excel("/content/Relatorio.xls")
data = pd.read_excel("C:/Users/Sander/Documents/modelo_final/Relatorio.xls")

#data.head()

data.info()

"""**1.2 Informações iniciais dos dados**"""

data2 = data
data2.info()

"""**1.3 Checagem de dados nulos ou NaN**"""

data2.isnull().sum()/len(data2)*100
#perceba que o resultado informa 118 colunas do dataframe e seus percentuais de nulos identificados
#as 118 linhas para vc significa as colunas checadas

"""**1.4 - Verificar se existe '-' nos registros e analisar a situação em caso positivo: Ao analisar no Google Sheets e/ou Excel, notou-se a presença desse caracter '-' nos registros. Logo é preciso confirmar a existência deles e tratá-los**"""

for coluna in data2.columns:
  numero_registros_com_hifen = 0
  for valor in data2[coluna]:
    if type(valor) == str and "-" in valor:
      numero_registros_com_hifen += 1
  if numero_registros_com_hifen > 0:
    print(f"Coluna: {coluna}")
    print(f"Número de registros com '-': {numero_registros_com_hifen}")

"""**1.5- O próximo passo, após carregamento e visualização dos dados, identificação dos valores nulos, dos atributos com 'strings' indesejáveis como '-' e suas quantidades, será definido os atributos utilizados para a base de dados, seguido de ajustes nos dados, checagem da correlação, enfim, até a construção dos modelos. A seguir o dicionário de dados:**

ESCOLHENDO ATRIBUTOS por inferencia: (Trabalhos relacionados analisados sugerem que variaveis explicativas de cunho socil, economico e desempenho podem ser relavantes ao modelo). Adaptando a ideia para os dados utilizados do IFSULDEMINAS Campus Machado

DICIONÁRIO DE DADOS

Estado civil: Nao Solteiro = 0/Solteiro = 1
Sexo: 'F' = 0, 'M' = 1
Etnia/Raca: nao bca = 0, bca = 1
Acesso a internet: Tenho acesso no computador em minha própria casa = 1, outros = 0
Tipo origem: nao privada = 0, privada = 1
Forma ingresso:
//
 "Ampla concorrência": 1,
  "Ampla concorrência (ENEM)": 1,
  "Ampla concorrência (SISU)": 1,
  "Ampla concorrência (Vestibular)": 1,
  demais considerar 0
//
Situação no curso: Target:(nao evade = 0 (Matriculado, Concluido, Formado), evade = 1)
I.R.A (se < 6 recebe zero, senao 1)
Frequência no Período: 0-100
Necessidade de auxilio estudantil:(Consigo me manter independentemente de auxílios da instituição = 0, ou seja, não preciso de auxilio/ Nao consigo me manter, preciso de auxilio ou outros correlatos = 1)
//
//Idade: intervalo 17<idade<25 recebe 1, senao 0//

**1.6 -Base de dados carregada com os atributos que serão utilizados, conforme estudos (trabalhos relacionados)**
"""

##
#13 ago 2024
base = data2[['Idade','Sexo', 'Etnia/Raça', 'Estado Civil', 'I.R.A.', 'Forma de Ingresso', 'Tipo de Escola de Origem',
              'Situação no Curso']]

base.head()

"""**2- Ajustando os dados**"""

#Colunas que serão preenchidas com 0 ou 1
colunas_a_preencher = base.select_dtypes(include=['object']).columns

# Verificando se há registros com "-" em cada coluna
for coluna in colunas_a_preencher:
    #Encontrando os índices das linhas com "-"
    indices_com_menos = base[coluna] == "-"

    # Se houver registros com "-", preencha-os com 0 ou 1 aleatoriamente
    if indices_com_menos.any():
      numero_de_linhas_com_menos = indices_com_menos.sum()
      valores_aleatorios = np.random.choice([0, 1], size=numero_de_linhas_com_menos)
      base.loc[indices_com_menos, coluna] = valores_aleatorios

base.head()

# prompt: transforme a coluna Idade que está nesse formato 26 anos, 10 meses, 5 dias em 27 anos.

def extract_age(age_string):
  years = int(age_string.split(' ')[0])
  months = int(age_string.split(' ')[2])
  if months >= 6:
   years += 1
  return years

base['Idade'] = base['Idade'].apply(extract_age)

# prompt: agora trasnforme a nova idade em numero inteiro

base['Idade'] = base['Idade'].astype(int)

#print(base['Idade'])

# prompt: quero checar o tipo da coluna Idade

print(base['Idade'].dtype)

base.head()

# Definindo os dicionários com a lógica adaptada: evade:1 nao evade: 0

estado_civil = {"Solteiro": 1}
sexo = {"M": 1}
etnia_map = {"Branca": 1}
situacao_curso_map = {
    "Matriculado": 0,
    "Formado": 0,
    "Concluído":0
}
# intervalo 17<idade<25 o que resulta mais ou menos em  200 registros
idade = {
    18: 1,
    19: 1,
    20: 1,
    21: 1,
    22: 1,
    23: 1,
    24: 1,
    25: 1

}

tipo_origem_map = {"Privada": 1}
forma_ingresso_map = {
    "Ampla concorrência": 1,
    "Ampla concorrência (ENEM)": 1,
    "Ampla concorrência (SISU)": 1,
    "Ampla concorrência (Vestibular)": 1

}

# Usando o método map do pandas para aplicar a transformação
base['Idade'] = base['Idade'].map(idade).fillna(0).astype(int)

# Substituindo os valores no DataFrame

base["Estado Civil"] = base["Estado Civil"].replace(estado_civil)
base["Sexo"] = base["Sexo"].replace(sexo)
base["Idade"] = base["Idade"].replace(idade)
base["Etnia/Raça"] = base["Etnia/Raça"].replace(etnia_map)
base["Situação no Curso"] = base["Situação no Curso"].replace(situacao_curso_map)
base["Tipo de Escola de Origem"] = base["Tipo de Escola de Origem"].replace(tipo_origem_map)
base["Forma de Ingresso"] = base["Forma de Ingresso"].replace(forma_ingresso_map)

base.head()

#Atualizando os demais valores

base.loc[base["Estado Civil"] != 1, "Estado Civil"] = 0
base.loc[base["Sexo"] != 1, "Sexo"] = 0
base.loc[base["Idade"] != 1, "Idade"] = 0
base.loc[base["Etnia/Raça"] != 1, "Etnia/Raça"] = 0
base.loc[base["Forma de Ingresso"] != 1, "Forma de Ingresso"] = 0
base.loc[base["Situação no Curso"] != 0, "Situação no Curso"] = 1
base.loc[base["Tipo de Escola de Origem"] != 1, "Tipo de Escola de Origem"] = 0

base.head()

base.info()

print(base["Situação no Curso"].unique())

# Converte para string, substitui vírgulas por pontos e depois converte para float
base['I.R.A.'] = base['I.R.A.'].astype(str).str.replace(',', '.').astype(float)

# Conta o número de valores ausentes na coluna 'I.R.A.'
num_missing_values = base['I.R.A.'].isna().sum()
print(f'Número de valores ausentes em "I.R.A.": {num_missing_values}')

# Preenche valores ausentes da coluna 'I.R.A.' com zero
base['I.R.A.'] = base['I.R.A.'].fillna(0)

# Conta o número de valores ausentes na coluna 'I.R.A.'
num_missing_values = base['I.R.A.'].isna().sum()
print(f'Número de valores ausentes em "I.R.A.": {num_missing_values}')

# Converte para string, substitui vírgulas por pontos e depois converte para float
base['I.R.A.'] = base['I.R.A.'].astype(str).str.replace(',', '.').astype(float)

# se media < 6 recebe zero, contrario 1
base['I.R.A.'] = base['I.R.A.'].apply(lambda x: 0 if x < 6 else 1)

"""**2.1 -Transformação completa dos dados**"""

base.head()

"""**2.2- Após a transformação completa dos dados, checar se tem valor negativo decorrente de inserção indevida**"""

# Verificando se o DataFrame contém valores negativos
if any(base[col].min() < 0 for col in base.columns):
    print("O DataFrame contém valores negativos.")
else:
    print("O DataFrame não contém valores negativos.")

"""**2.3- Correlação**"""

base.corr()['Situação no Curso']

base['Situação no Curso'].value_counts()

"""**2.4- Outliers**"""

def detect_outliers(data):
  outliers_dict = {}
  for col in data.columns:
    if data[col].dtype != object:  # Ignore non-numeric columns
      q1 = data[col].quantile(0.25)
      q3 = data[col].quantile(0.75)
      iqr = q3 - q1
      lower_bound = q1 - 1.5 * iqr
      upper_bound = q3 + 1.5 * iqr
      outliers_mask = (data[col] < lower_bound) | (data[col] > upper_bound)
      outliers = data[outliers_mask].index.tolist()
      outliers_dict[col] = len(outliers) if outliers else 0
  return outliers_dict

# Chamada da função
outliers_dict = detect_outliers(base)

# Verificação de outliers
total_outliers = sum(outliers_dict.values())

# Exibição dos resultados
if not total_outliers:
  print("Não foram encontrados outliers no DataFrame.")
else:
  print(f"Total de outliers encontrados: {total_outliers}")
  for col, count in outliers_dict.items():
    if count > 0:
      print(f"  * Coluna '{col}': {count} outliers")

"""**3- Construindo os modelos**"""

basef = base

basef.head()

# Salvando o DataFrame em um arquivo CSV
#basef.to_csv('basef.csv')

"""**3.1- Preparando os modelos preditivos**"""

X = basef.drop(columns=['Situação no Curso'], axis=1)
X.info()

##X = new_data.drop('Target', axis=1)

# os labels: y
y = basef['Situação no Curso']
print(y)

print("Tipo de dados de X_train:", type(X))
print("Tipo de dados de y_train:", type(y))
print("Formato de X_train:", X.shape)
print("Formato de y_train:", y.shape)
#X = X.values
#y = y.values
y = np.array(y, dtype=int)

print(y)

"""**3.2 -Treinando os dados**"""

# treinando os dados
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=0)
print(y_train)

"""**3.3 - Importando o modelo Navy Bayes**"""

from sklearn.naive_bayes import GaussianNB  # Importe a classe GaussianNB
navy = GaussianNB()  # Crie uma instância do classificador GaussianNB

"""**3.4 - Fazendo os ajustes nos modelos com o metodo fit**"""

navy.fit(X_train, y_train)

"""**3.5 - Predição: Acurácia dos modelos**"""

y_pred = navy.predict(X_test)
print("Accuracy :",round(accuracy_score(y_test,y_pred)*100,2),"%")

"""**TESTANDO COM INSERÇÃO DE DADOS**"""

import pickle #do professor: exporta modelo ml
labels_names = basef['Situação no Curso']
pickle.dump(labels_names, open('names.pkl','wb'))
nomesbase = pickle.load(open('names.pkl','rb'))
print(nomesbase)

basef.head(20)

"""ESCOLHENDO ATRIBUTOS por inferencia: (Trabalhos relacionados analisados sugerem que variaveis explicativas de cunho socil, economico e desempenho podem ser relavantes ao modelo). Adaptando a ideia para os dados utilizados do IFSULDEMINAS Campus Machado


DICIONÁRIO DE DADOS

Estado civil: Nao Solteiro = 0/Solteiro = 1
Sexo: 'F' = 0, 'M' = 1
Etnia/Raca: nao bca = 0, bca = 1
Acesso a internet: Tenho acesso no computador em minha própria casa = 1, outros = 0
Tipo origem: nao privada = 0, privada = 1
Forma ingresso:
//
 "Ampla concorrência": 1,
  "Ampla concorrência (ENEM)": 1,
  "Ampla concorrência (SISU)": 1,
  "Ampla concorrência (Vestibular)": 1,
  demais considerar 0
//
Situação no curso: Target:(nao evade = 0 (Matriculado, Concluido, Formado), evade = 1)
I.R.A (se < 6 recebe zero, senao 1)
Frequência no Período: 0-100
Necessidade de auxilio estudantil:(Consigo me manter independentemente de auxílios da instituição = 0, ou seja, não preciso de auxilio/ Nao consigo me manter, preciso de auxilio ou outros correlatos = 1)
//
//Idade: intervalo 17<idade<25 recebe 1, senao zero//

"""

pickle.dump(navy, open('model.pkl','wb'))
model = pickle.load(open('model.pkl','rb'))

#
print (model.predict([ [0,	1,	0,	1,	0,	0,	0	] ]))#1 Evade ok
print (model.predict([ [1,	0,	1,	0,	0,	0,	1 ] ]))#1 Evade ok
print (model.predict([ [0,	1,	1,	1,	1,	0,	0	] ]))#1 Evade ok
print (model.predict([ [1,	1,	1,	1,	0,	1,	0 ] ]))#0 Nao evade ok
print (model.predict([ [1,	0,	1,	1,	0,	1,	0 ] ]))#0 Nao evade ok