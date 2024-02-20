# Phishing Domain Detection


These project is used to detect whether the given link is phishing or not. It is the second version of the already built model with more clean UI and improved accuracy.

**What is Phishing** 

Phishing is an type of attack in which an attacker sends a link to the victim and when victim clicks on that link and enters his personal information, 
the attacker gets access to that information. 

**How it Works:** 
```
> User enters a link in the website

> The link will be sent to the django backend

> Django will call the phishing api hosted by myself on AWS lambda.
  
> Api will make predictions based on the provided URL and return the response.   

> Based on Response, we will print whether given link is phishing or not in the website

```

**[API Repo Link](https://github.com/Karthikaddagalla/AWS-Lambda-Phishing-Api)**

**Tech Stack Used:** Django, HTML, CSS, Machine Learning.

These project is deployed on vercel and you can visit that website by going [here](https://phishing-domain-detection-gz559ebq4-karthikaddagallas-projects.vercel.app/)


![image](https://github.com/Karthikaddagalla/Phishing-Domain-Detection/assets/75205632/4f4d095a-45d3-4e10-bd9f-ed528f6180af)

