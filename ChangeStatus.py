from contextlib import closing
from datetime import datetime, date

import boto3
import csv
import dropbox
import io
import pandas as pd


# dropboxToken = "sl.BXN5UNvpXxIX0m8IGsT_UlooKd6naBnbgfeCsVoaxLvBTMIFSWOwlD5_2Df9mYV7sOGvwdN8tBg4" \
#                "f85meyd9aCG9LCbbR0_Xipl7veMYTE2M2zawLFM8K2XFjWehXhK0CtCyyf-N"
# print("Connect to Dropbox - Initiated")
# conn = dropbox.Dropbox(dropboxToken)
# print("Connect to Dropbox - Completed")


# print("Reading survey details from Dropbox - Initiated")
# # inputFilePath = "/kickImages/Qualtrics/2022_Abhijith/CodedImages2022_Test_Result.csv"
# inputFilePath = "/kickImages/Qualtrics/2022_Abhijith/MTurk_Results/Result_Batch15.csv"
# def stream_dropbox_file(path):
#     _, res = conn.files_download(path)
#     with closing(res) as result:
#         byte_data = result.content
#         return io.BytesIO(byte_data)
#
# file_stream = stream_dropbox_file(inputFilePath)
# df = pd.read_csv(file_stream)
# print("Reading survey details from Dropbox - Completed")

print("Establish connection to MTurk : Initiated")
credentialsFilePath = "/Users/abhijithnair/Desktop/RA/abhijithnair_accessKeys.csv"
with open(credentialsFilePath,'r') as input:
    next(input)
    reader = csv.reader(input)
    for line in reader:
        access_key_id = line[2]
        secret_access_key = line[3]
productionEndpoint_url = 'https://mturk-requester.us-east-1.amazonaws.com'
sandBoxEndpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

print("Connecting to production.....")
mtc = boto3.client('mturk',endpoint_url=productionEndpoint_url,aws_access_key_id = access_key_id,
                   aws_secret_access_key = secret_access_key,region_name='us-east-1')


# for hit_id in df['HIT ID']:
#     try:
#         response = mtc.update_hit_review_status(
#             HITId= hit_id
#         )
#         print(response)
#     except Exception as e:
#         print(repr(e))

response = mtc.update_hit_review_status(
    HITId= "37ZQELHEQ1PEG4LPK1HPTCSJYA6NMU"
)
print(response)