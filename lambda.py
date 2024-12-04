import json
import boto3 # type: ignore

def lambda_handler(event, context):
    print("Evento recibido:", json.dumps(event))  
    
    input_text = ""

  
    if event.get("httpMethod") == "POST":
        if isinstance(event.get("body"), str):
            body = json.loads(event["body"])  
        elif isinstance(event.get("body"), dict):
            body = event["body"]  
        else:
            body = {}
        input_text = body.get("inputText", "")
    elif event.get("httpMethod") == "GET":
        input_text = event.get("queryStringParameters", {}).get("inputText", "")

  
    if not input_text:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "inputText es requerido"})
        }

    
    client = boto3.client('bedrock-runtime', region_name='us-east-1')
    model_id = 'amazon.titan-text-lite-v1'
    payload = {"inputText": input_text}

    try:
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(payload),
            contentType='application/json',
            accept='application/json'
        )
        response_body = json.loads(response['body'].read())
        return {
            "statusCode": 200,
            "body": json.dumps({"response": response_body})
        }
    except Exception as e:
        print(f"Error al invocar el modelo: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }