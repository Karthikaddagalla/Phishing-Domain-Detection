
import requests








def predictor(url):

    request_url = f'https://wds80hjjn5.execute-api.ap-south-1.amazonaws.com/phishingStage/phishingResource?url={url}'

# Send a GET request to the URL
    response = requests.get(request_url)
    print(response)

# Check if the request was successful (status code 200)
    if response.status_code == 200:
    # Parse the JSON response
        data = response.json()

    # Access the 'output' key from the JSON response
        output = data.get('output')

    # Print the value of the 'output' key
        print("Output:", output)

        return int(output)
    else:
    # Print an error message if the request was not successful
        print("Error:", response.status_code)


            
    # if y_pred==1:
    #     print("The link is Good link")
    #     return 0
        
    # else:
    #     print("The link is phishing link")
    #     return 1

# predictor("h")

