import json
import io
import pickle

with io.open("qald-6-train-multilingual.json", 'r', encoding='utf-8') as data_file:
    trainDataset=json.load(data_file)

#with open("qald-6-test-multilingual.json", 'r', encoding='utf-8') as data_file:
#    testDataset=json.load(data_file)

trainData = []

for i in trainDataset['questions']:
    #print("id:", i['id']) 
    for question in i['question']:
        if question['language'] == "en":
            #print("question:", question['string'])
            element = [i['id'], question['string']]
            #print(element)
            trainData.append(element)

print(trainData)



#file = open("train.txt", "w+")

#content = str(trainData) 
#file.write(content) 
#file.close()



# Writing a object file with trainData 
file = open("trainData.pickle", "wb") 
pickle.dump(trainData, file, 2)
file.close()

print("\n")

file = open("trainData.pickle", "rb")
trainData2 = pickle.load(file)
file.close()
print(trainData2)
