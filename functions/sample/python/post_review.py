import sys 
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict): 
    authenticator = IAMAuthenticator("HmeG7P8FwEkUYNYPxNyYSww5uzGd4cI4PkBKlor-GIE7")
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url("https://5f8b49ed-9f92-4248-ba7d-af4618075e6d-bluemix.cloudantnosqldb.appdomain.cloud")
    response = service.post_document(
                db='reviews',
                document=dict["review"]).get_result()
    try: 
        # result_by_filter=my_database.get_query_result(selector,raw_result=True) 
        result= {
            'headers': {'Content-Type':'application/json'}, 
            'body': {'data':response} 
            }        
        return result
    except:  
        return { 
            'statusCode': 404, 
            'message': 'Something went wrong'
            }
