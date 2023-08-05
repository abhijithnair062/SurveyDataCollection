import io
import json
from contextlib import closing
import requests
import dropbox
import pandas as pd
import py_qualtrics_api.tools as pq
import random

dropboxToken = "sl.BZHodAT__8GM6G06wgeB0_25O1RNxmTKNHFH0djBl27nvXThV2DX2De4EDp4xwQ-6hJDVcck7J1mZTa" \
               "5DrDjPo-an5vIPQsCQ148fP95Qq-n4d267XGoFFdr3-nWQRKu7ZLdDg23"
#
#  Establish a connection  and read Config file
print("Connect to Dropbox - Initiated")
conn = dropbox.Dropbox(dropboxToken)
print("Connect to Dropbox - Completed")
print("Reading credentials - Initiated")
q = pq.QualtricsAPI('config.yml')
print("Reading credentials - Completed")
# # Iterate through all the files in input file and add it to a set. This
# # ensures only unique images are included for processing

print("Reading images from Dropbox - Initiated")
inputFilePath = "/kickImages/Qualtrics/2022_Abhijith/ImagesToCodeFeb1723.csv"
def stream_dropbox_file(path):
    _, res = conn.files_download(path)
    with closing(res) as result:
        byte_data = result.content
        return io.BytesIO(byte_data)

file_stream = stream_dropbox_file(inputFilePath)
df = pd.read_csv(file_stream)
imagesToCode = list()
for column in df['c_id']:
    column = str(column).strip().replace(".jpg","")
    imagesToCode.append(int(column))


print("Reading images from Dropbox - Completed")



dropbox_path = '/kickImages/Music/All Images'
imageFolderpath = []
temparray = []
publishedSurveyList = list()
publishledSurveyURL = "https://neu.co1.qualtrics.com/jfe/form/"

print("Create embed links for images - Initiated")
for image_item in imagesToCode:
    path = conn.files_search(dropbox_path, str(image_item)+".jpg").matches
    imageFolderpath.append(path[0].metadata.path_lower)
    temparray.append(image_item)
uncodedImagesTempLink = []
for x in imageFolderpath:
    uncodedImagesTempLink.append(str(conn.sharing_create_shared_link(x).url).replace("dl=0","raw=1"))
uncodedImagesTempLink = list(uncodedImagesTempLink)
print("Create embed links for images - Completed")


count = 1
surveynameCode = 679
jsondata_Array = []
successfulCodedImages = []
datatoappend = {}
dfWrite = pd.DataFrame()
imagesInaSurvey = ""
surveyName = ""
mTurkVerificationCode = ""
try:
    for i,j in zip(uncodedImagesTempLink,temparray):
        successfulCodedImages.append(j)
        jsonData_Inner = {}
        st = (uncodedImagesTempLink.index(i))%5 + 1
        jsonData_Inner["key"] = "link" + str(st)
        jsonData_Inner["value"] = i
        jsondata_Array.append(jsonData_Inner)
        jsonData_Inner = {}
        jsonData_Inner["key"] = "image" + str(st)
        jsonData_Inner["value"] = j
        jsondata_Array.append(jsonData_Inner)
        imagesInaSurvey += str(j)+" | "
        if count % 5 == 0 :
            jsonData_Inner["key"] = "mTurkCode"
            mTurkVerificationCode = str(random.randint(0,100000000))
            jsonData_Inner["value"] = mTurkVerificationCode
            jsondata_Array.append(jsonData_Inner)
            jsonData_Inner = {}
            imagesInaSurvey = imagesInaSurvey[:-2]
            jsonData_Outer = {}
            dataCenter = "iad1"
            surveyName = "ImageCoding_UvA_{0}".format(surveynameCode)
            jsonData_Outer['projectName'] = surveyName
            jsonData_Outer['embeddedDataFields'] = jsondata_Array
            baseUrl = "https://{0}.qualtrics.com/API/v3/surveys".format(dataCenter)
            surveyId = "SV_6mSPoElpum7lbZY"
            data = jsonData_Outer
            apiToken = "GacUTFbdoRLuSEI1ni3cIA41k6nF3IZ9pw01REw5"
            userId = "UR_8nRsd76ECZEMVIF"
            headers = {
                "Content-Type": "application/json",
                "x-api-token": apiToken,
                "x-copy-source": surveyId,
                "x-copy-destination-owner": userId
            }
            print(data)
            try:
                response = requests.post(baseUrl, headers=headers, data=json.dumps(data))
            except:
                print("Error creating survey")

            print("Survey" +response.text)
            jsondata_Array = []
            surveynameCode += 1
            resJsonString = response.json()
            newlyCreatedSurveyId = resJsonString['result']['id']
            baseUrl = "https://{0}.qualtrics.com/API/v3/surveys/{1}/embeddeddatafields".format(
                dataCenter,newlyCreatedSurveyId)
            data = jsonData_Outer
            headers = {
                "Content-Type": "application/json",
                "x-api-token": apiToken
            }
            try:
                response = requests.post(baseUrl, headers=headers, data=json.dumps(data))
                success = q.activate_survey(newlyCreatedSurveyId)
                if success:
                    print("Survey {0} published successfully".format(newlyCreatedSurveyId))
                    publishedSurveyList.append(publishledSurveyURL+newlyCreatedSurveyId)
                    datatoappend = {'Survey name' : surveyName,'c_id' : imagesInaSurvey,
                                    'survey_id' :
                        newlyCreatedSurveyId, 'Survey link' :
                        publishledSurveyURL+newlyCreatedSurveyId, 'MTurk Verification Code' :
                    mTurkVerificationCode }
                    dfWrite = dfWrite.append(datatoappend,ignore_index=True)
                    datatoappend = {}
                else:
                    print("Survey {0} not published".format(newlyCreatedSurveyId))
            except:
                del successfulCodedImages[len(successfulCodedImages) - 5:]
            imagesInaSurvey = ""
            jsondata_Array = []
            # raise ValueError('A very specific bad thing happened.')
        count+=1
except Exception as e:
    print(repr(e))
finally:
    #---------------------------------------------Code to append to CSV

    if not dfWrite.empty:
        print("Report write to CSV : Initiated")
        outputFilePath = \
            "/kickImages/Qualtrics/2022_Abhijith/CodedImages2023_Test_Result_Feb1723" \
                         ".csv"
        data = dfWrite.to_csv(mode='w', index=False, header=True) # The index parameter is optional

        with io.BytesIO(data.encode()) as stream:
            stream.seek(0)

            conn.files_upload(stream.read(), outputFilePath, mode=dropbox.files.WriteMode.overwrite)
        print("Report write to CSV : Completed")

print(publishedSurveyList)





