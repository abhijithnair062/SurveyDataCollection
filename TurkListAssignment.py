from datetime import datetime
import boto3
import csv
import dropbox
from contextlib import closing
import io
import pandas as pd

# Establish connection to MTurk
print("Establish connection to MTurk : Initiated")
credentialsFilePath = "/Users/abhijithnair/Desktop/RA/abhijithnair_accessKeys.csv"
with open(credentialsFilePath,'r') as input:
    next(input)
    reader = csv.reader(input)
    for line in reader:
        access_key_id = line[2]
        secret_access_key = line[3]
sandBoxEndpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
# Only use the below url after final testing as it has cost assocaited with it
productionEndpoint_url = 'https://mturk-requester.us-east-1.amazonaws.com'
mtc = boto3.client('mturk',endpoint_url=productionEndpoint_url,aws_access_key_id = access_key_id,
                   aws_secret_access_key = secret_access_key,region_name='us-east-1')

print("Account Balance = "+str(mtc.get_account_balance()))
print("Establish connection to MTurk : Completed")

response = mtc.list_assignments_for_hit(
    HITId='324N5FAHSY2WYLUV1GQ0OGUSVEUKVW'
)
# response = mtc.list_reviewable_hits(
#     NextToken = "p2:c6VzH4548YCSXcHApPtg7B8vGa0petuvBKMj+UVz8xuIXYb/GqsHzhOlaOOwLw=="
# )
# response = mtc.list_reviewable_hits(
# HITId='3LOJFQ4BOY6A44U9AVQ6IUOLVRTKD4',
#     NextToken = "p2:MX83vpfDddK+qQ9k5bRpMYXHlsaJknwkaZWvduUgv4Sm2EPO4LzgBRPn/sTpHQ=="
# )
# response = mtc.list_hits()
# response = mtc.list_hits(
#     NextToken = "p2:DakSjesn+lWR+pCx9f5Bkp5vgTCz9Sc8U+pGpj3DGJBZr8QCItXOduql1z07Fw=="
# )
print(response)
mtc.close()