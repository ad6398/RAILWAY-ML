#departments predicting
import numpy as np
import csv
import pickle

#loading prepared training body
def l oad_train_data():
    d=open("trainig_body.txt")
    data=[]
    for line in d.readlines():
        data.append(line)
    return data
#loading training lebels of training body

def load_train_target():
    d=open("training_labels.txt")
    data=[]
    for line in d.readlines():
        data.append(int(line))
    return data
 #load testing body and labels
def load_test_data():
    d=open("testing_body.txt")
    data=[]
    for line in d.readlines():
        data.append(line)
    return data

def load_test_target():
    d=open("target_train_2.txt")
    data=[]
    for line in d.readlines():
        data.append(int(line))
    return data
test_data=load_test_data()
train_data=load_train_data()
train_target=load_train_target()

test_target=load_test_target()


from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier

# groups in which we have classified
dict={1:"Commercial",2:"Maintainence",3:"Safety And Lost and Found",4:"Traffic",5:"Financial",6:"Unclassified"}

# cleaning, stop word removal, vectorizing text 
text_clf_svm = Pipeline([('vect', CountVectorizer(stop_words='english')),('tfidf', TfidfTransformer()),('clf-svm', SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, n_iter=5, random_state=42)),])
_ = text_clf_svm.fit(train_data,train_target)
predicted_svm = text_clf_svm.predict(test_data)
#print(predicted_svm)
#for i in predicted_svm:
    #print(dict[i])

#classifing and storing in file
print(np.mean(predicted_svm == test_target)*100)
depart=[]
for i in range(0,len(predicted_svm)):
	depart.append(str(dict[predicted_svm[i]]))
with open('department_list.txt', 'wb') as fp:
    pickle.dump(depart, fp)
#print(test_target))
#text="Indian Railways — failed air conditioning in rajdhani first class-As writing this message, 22nd March 2018, time 1030hrs I am on board Train no. 22824 Coach H1, C cabin vide PNR No. [protected], have been repeatedly asking attendant to fix the A/c as it's too warm / hot. The response is pathetic.Can't really believe the standard of Rajdhani First class.Suresh Prabhu ji, let me see what standard we can expect under Modi ji and your words and promises. .Regards / Pruthijit Mohanty"
#v=text_clf_svm.predict(text)
#print(str(dict[v]))