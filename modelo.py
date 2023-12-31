# -*- coding: utf-8 -*-
"""ModeloR_Python_Projeto2 - Export Pickle.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iIDtFwzN1FsdY8pxLiTQzk43ZG21CGcH
"""

#!pip install -q scikit-learn==1.3.1
from sklearn.naive_bayes import GaussianNB
from sklearn import tree
from sklearn import datasets
import pickle#exporta modelo ml
import pandas as pd

base=pd.read_csv('C:/Users/Sander/Documents/exe_IA1/IA1_Semana9_exe/modeloR_python_projeto2/modelo/df.csv')
base.keys()

base.describe()

labels_names = base['STATUS']
pickle.dump(labels_names, open('names.pkl','wb'))
nomesbase = pickle.load(open('names.pkl','rb'))
print(nomesbase)

base.shape

# Remover valores ausentes
base = base.dropna()

base.describe

base.shape

x = base[['SIZE',	'DISTANCE',	'DESIBEL',	'AIRFLOW',	'FREQUENCY']]

y = base[['STATUS']]

#realizando o split da base para teste
from sklearn.model_selection import train_test_split
x_treino,x_teste,y_treino,y_teste = train_test_split(x,y,test_size=0.3)

clf = tree.DecisionTreeClassifier()
clf = clf.fit(x_treino, y_treino)

preditos = clf.predict(x_teste)
print("Preditos:",preditos)
print("Real    :",y_teste)

from sklearn.metrics import accuracy_score
print("Acuracia:", accuracy_score(y_teste,preditos))

pickle.dump(clf, open('model.pkl','wb'))
model = pickle.load(open('model.pkl','rb'))
print (model.predict([ [7,190,86,2.2,5] ]))
#1  gasoline        10       96      0.0         75       0
# 1  gasoline        10      109      4.5         67       1
# 7       lpg       190       86      2.2          5       0

#referencia
#DATASCIENCE- CURSO PESSOAL