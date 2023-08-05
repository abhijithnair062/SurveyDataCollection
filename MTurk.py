import boto3
import csv
import dropbox
from contextlib import closing
import io
import pandas as pd

# Before running for Production, make sure the "isProdRun" is set to True, if it's a sandbox run
# then set "isProdRun" to False.
# Also make sure the link is updated in the XML input
isProdRun = True
dropboxToken = "sl.BZHodAT__8GM6G06wgeB0_25O1RNxmTKNHFH0djBl27nvXThV2DX2De4EDp4xwQ-6hJDVcck7J1mZTa" \
               "5DrDjPo-an5vIPQsCQ148fP95Qq-n4d267XGoFFdr3-nWQRKu7ZLdDg23"
print("Connect to Dropbox - Initiated")
conn = dropbox.Dropbox(dropboxToken)
print("Connect to Dropbox - Completed")


print("Reading survey details from Dropbox - Initiated")
# inputFilePath = "/kickImages/Qualtrics/2022_Abhijith/CodedImages2022_Test_Result.csv"
inputFilePath = "/kickImages/Qualtrics/2022_Abhijith/HIT_To_Publish/Batch16.csv"
outputFilePath = "/kickImages/Qualtrics/2022_Abhijith/MTurk_Results/Result_Batch16.csv"
def stream_dropbox_file(path):
    _, res = conn.files_download(path)
    with closing(res) as result:
        byte_data = result.content
        return io.BytesIO(byte_data)

file_stream = stream_dropbox_file(inputFilePath)
df = pd.read_csv(file_stream)
print("Reading survey details from Dropbox - Completed")



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
if isProdRun:
    print("Connecting to production.....")
    mtc = boto3.client('mturk',endpoint_url=productionEndpoint_url,aws_access_key_id = access_key_id,
                      aws_secret_access_key = secret_access_key,region_name='us-east-1')
else:
    print("Connecting to sandbox.....")
    mtc = boto3.client('mturk',endpoint_url=sandBoxEndpoint_url,aws_access_key_id = access_key_id,
                       aws_secret_access_key = secret_access_key,region_name='us-east-1')

print("Account Balance = "+str(mtc.get_account_balance()))
print("Establish connection to MTurk : Completed")

print("Read HIT Layout : Initiated")
if isProdRun:
    question = open('/Users/abhijithnair/Desktop/RA/MTurkIntegration/HITLayoutProduction.xml','r').read()
else:
    question = open('/Users/abhijithnair/Desktop/RA/MTurkIntegration/HITLayoutSandbox.xml','r').read()
print("Read HIT Layout : Completed")

print("Create HIT in MTurk : Initiated")

dfWrite = pd.DataFrame()
datatoappend = {}
hitURL = ""
try:
    for name, link in zip(df['Survey name'],df['Survey link']):
        temp = question.replace("<survey_link>",link)
        response = mtc.create_hit(
            Title = name,
            Description = 'Please observe the image and report your impressions of it.',
            Keywords = 'survey, image evaluation, music',
            Reward = '5.00',
            MaxAssignments = 1,
            LifetimeInSeconds = 432000,
            AssignmentDurationInSeconds = 2700,
            Question = temp,
            QualificationRequirements=[
                # Hit approval rate %
                {"QualificationTypeId": "000000000000000000L0",
                'Comparator':'GreaterThan',
                'IntegerValues':[75]
                },
                # Location
                {
                    'QualificationTypeId':"00000000000000000071",
                    'Comparator':"EqualTo",
                    'LocaleValues':[{
                    'Country':"US",
                }]
                },
                # No of HIT's approved
                {
                    'QualificationTypeId':"00000000000000000040",
                     'Comparator':"GreaterThan",
                     'IntegerValues':[50]
                }
    ]

        )
        # The response included several fields that will be helpful later
        print(response)
        print ("A new HIT has been created. You can preview it here:")
        if isProdRun:
            hitURL = "https://worker.mturk.com/mturk/preview?groupId="
            print ( hitURL+ response['HIT']['HITGroupId'])
        else:
            hitURL = "https://workersandbox.mturk.com/mturk/preview?groupId="
            print (hitURL + response['HIT']['HITGroupId'])
        print ("HITID = " + response['HIT']['HITId'] + " (Use to Get Results)")
        datatoappend = {'Survey name' : name,'Survey link' : link, 'HIT ID' : response['HIT'][
            'HITId'], 'HIT URL' :
            hitURL + response['HIT']['HITGroupId']}
        dfWrite = dfWrite.append(datatoappend,ignore_index=True)
        datatoappend = {}
except Exception as e:
    print(repr(e))
finally:
    #---------------------------------------------Code to append to CSV

    if not dfWrite.empty:
        print("Report write to CSV : Initiated")
        data = dfWrite.to_csv(mode='w', index=False, header=True) # The index parameter is optional

        with io.BytesIO(data.encode()) as stream:
            stream.seek(0)

            conn.files_upload(stream.read(), outputFilePath, mode=dropbox.files.WriteMode.overwrite)
        print("Report write to CSV : Completed")
    mtc.close()