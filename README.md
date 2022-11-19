# Phishing Domain Detection


These project is used to detect whether the given link is phishing or not. 

**What is Phishing** 

Phishing is an type of attack in which an attacker sends a link to the victim and when victim clicks on that link and enter his personal information, 
the attacker gets access to that information. 

**How it Works:** 
```
> User enters a link in the website

> The link will be sent to the django backend

> Seven pre trained Machine learning algorithms(Logistic Regression, Support Vector Machines , K Nearest Neighbours,
  Decision Tree Classifier, Random Forest Classifier Gradient Boosting Classifier and Multi Layer Perceptron) will 
  predict whether the given link is phishing or not.
  
> Based on voting algorithm(majority vote) we will find whether the link is phishing or not.   

> Based on output from ML algorithms, we will print whether given link is phising or not in the website

```

**Tech Stack Used** = Django, HTML, CSS, Machine Learning.

These was deployed on the heroku and you can visit that website by going to "https://thephish.herokuapp.com/"
