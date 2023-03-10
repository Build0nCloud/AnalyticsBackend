import boto3
import json
import requests
from requests_aws4auth import AWS4Auth

region = 'us-east-1' # For example, us-west-1
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

host = 'https://search-my-test-domain-4omoj2lfbqwcwklilkzjbmyiza.us-east-1.es.amazonaws.com'




# Lambda execution starts here
def lambda_handler(event, context):

    #load request body 
    myBody = json.loads(event["body"])
    
    print("Index Found :" + myBody["indexName"] )
    
    # Form search URL
    url = host + '/' + myBody["indexName"] + myBody["openSearchAPIEndpoint"]
    print("Final url:" + url)
    # Put the user query into the query DSL for more accurate search results.
    # Note that certain fields are boosted (^).

#   Test Query    
#    query = {
#        "size": 25,
#        "query": {
#            "multi_match": {
#                "query": event['queryStringParameters']['q'],
#                "query" : "q=mars",
#                "fields": ["title^4", "plot^2", "actors", "directors"]
#            }
#        }
#    }
    
# load query from request    
    query = myBody["queryBody"]
    
    
    # Elasticsearch 6.x requires an explicit Content-Type header
    headers = { "Content-Type": "application/json" }
    
#   Basic Authentication    
#   awsauth = ('osroot', 'OSroot@01')


    # Make the signed HTTP request
    r = requests.get(url, auth=awsauth, headers=headers, data=json.dumps(query))

    # Create the response and add some extra content to support CORS
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": '*'
        },
        "isBase64Encoded": False
    }

    # Add the search results to the response
    response['body'] = r.text
    return response

