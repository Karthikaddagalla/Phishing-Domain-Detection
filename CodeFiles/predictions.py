
import pickle
from CodeFiles import link_tester


with open("Models/mlp_model", "rb") as file:
    mlp = pickle.load(file)


with open("Models/lr_model", "rb") as file:
    lr = pickle.load(file)


with open("Models/knn_model", "rb") as file:
    knn = pickle.load(file)

with open("Models/svm_model", "rb") as file:
    svm = pickle.load(file)

with open("Models/dtc_model", "rb") as file:
    dtc = pickle.load(file)

with open("Models/gbc_model", "rb") as file:
    gbc = pickle.load(file)

with open("Models/rf_model", "rb") as file:
    rfc = pickle.load(file)

# Loading the normalization object

with open("Models/Normalization_objects/normalization_obj", "rb") as file:
    obj = pickle.load(file)


def predictor(link):
    z = link_tester.Url_DataFrame(link)

    http_lin = z.check_http()

    if http_lin == 5:    # It means there is no http
        return 5



    lin_wor = z.check_link()

    # If the given link is not working
    if lin_wor == 0:  
        return 2


    z.df = obj.transform(z.df)


    l = []

    l.append(mlp.predict(z.df)[0])
    l.append(lr.predict(z.df)[0])
    l.append(svm.predict(z.df)[0])
    l.append(dtc.predict(z.df)[0])
    l.append(knn.predict(z.df)[0])
    l.append(gbc.predict(z.df)[0])
    l.append(rfc.predict(z.df)[0])

    sumi = 0

    for i in l:
        if i == 0:
            sumi = sumi + 1
        
        
    print(l)
            
    if sumi >= 3:
        print("The link is Good link")
        return 0
        
    else:
        print("The link is phishing link")
        return 1


