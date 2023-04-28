import boto3
import json
import requests
from requests_aws4auth import AWS4Auth

print('Loading function')
region = 'us-east-1'
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
#url = 'https://search-my-test-domain-4omoj2lfbqwcwklilkzjbmyiza.us-east-1.es.amazonaws.com/movies/_search?q=mars'
#url = "https://search-movies-ldtvltos5bscc2xeck6fhp4erq.us-east-1.es.amazonaws.com/movies/_search?q=mars"

host = 'https://search-my-test-domain-4omoj2lfbqwcwklilkzjbmyiza.us-east-1.es.amazonaws.com'

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
   
    #For Basic OpenSearch Authentication
    #awsauth = ('osroot', 'OSroot@01')
    
    headers = { "Content-Type": "application/json" }
    myBody = json.loads(event["body"])
    #myBody=event["body"]
    print("Index Found : " + myBody["indexName"])
    
    #create url
    if (myBody["additionalOpts"]["doc_as_upsert"]) :
        url = host +'/' + myBody["indexName"] + '/' + '_update' + '/'+ myBody['indexDocumentID']
        myPayload = {
            "doc" : myBody["doc"],
            "doc_as_upsert" : True
        }
    else :
        url = host +'/' + myBody["indexName"] + '/' + '_doc' + '/'+ myBody['indexDocumentID']
        myPayload=myBody["doc"]
    
    print("Final url: " + url)
    
    print("sending payload " + json.dumps(myPayload))
    
    r = requests.post(url, auth=awsauth, json=myPayload, headers=headers)
#  r = requests.post(url, auth=awsauth, json=myBody["doc"], headers=headers)

    response = {
        "statusCode": r.status_code,
        "headers": {
            "Access-Control-Allow-Origin": '*'
        },
        "body": "Reason: " + r.reason + "***" + r.text,
        "isBase64Encoded": False
    }

    # Add the update results to the response
    # response['body'] = r.text
    return response
    
    
    raise Exception('Something went wrong')

