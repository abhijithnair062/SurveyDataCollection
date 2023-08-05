from contextlib import closing

import dropbox as dropbox
import requests
import zipfile
import io
import pandas as pd
def get_qualtrics_survey(dir_save_survey, survey_id):
    """ automatically query the qualtrics survey data
    guide https://community.alteryx.com/t5/Alteryx-Designer-Discussions/Python-Tool-Downloading-Qualtrics-Survey-Data-using-Python-API/td-p/304898 """

    # Setting user Parameters
    api_token = "GacUTFbdoRLuSEI1ni3cIA41k6nF3IZ9pw01REw5"
    file_format = "csv"
    data_center = 'iad1' # "<Organization ID>.<Datacenter ID>"

    # Setting static parameters
    request_check_progress = 0
    progress_status = "in progress"
    base_url = "https://{0}.qualtrics.com/API/v3/responseexports/".format(data_center)
    headers = {
        "content-type": "application/json",
        "x-api-token": api_token,
    }

    # Step 1: Creating Data Export
    download_request_url = base_url
    download_request_payload = '{"format":"' + file_format + '", "useLabels":true,"surveyId":"' + \
                               survey_id + \
                               '"}' # you can set useLabels:True to get responses in text format
    download_request_response = requests.request("POST", download_request_url, data=download_request_payload, headers=headers)
    progress_id = download_request_response.json()["result"]["id"]
    # print(download_request_response.text)

    # Step 2: Checking on Data Export Progress and waiting until export is ready
    while request_check_progress < 100 and progress_status != "complete":
        request_check_url = base_url + progress_id
        request_check_response = requests.request("GET", request_check_url, headers=headers)
        request_check_progress = request_check_response.json()["result"]["percentComplete"]

    # Step 3: Downloading file
    request_download_url = base_url + progress_id + '/file'
    request_download = requests.request("GET", request_download_url, headers=headers, stream=True)

    # Step 4: Unzipping the file
    zipfile.ZipFile(io.BytesIO(request_download.content)).extractall(dir_save_survey)
    print('Downloaded qualtrics survey')

if __name__ == "__main__":



    path = "/Users/abhijithnair/Desktop/RA/CompliedListOfSurveyResponses/Batch 16"

    # Set the below variable True for getting single survey response
    # If needed batch processing set this as False
    onlySingleResponse = False
# SV_djsdRTtkVcQZq2W
    if(onlySingleResponse):
        surveyId = input("Enter survey ID : ")
        get_qualtrics_survey(dir_save_survey = path, survey_id = surveyId)
    else:
        dropboxToken = "sl.BZHIV3pzzYwUzLW8ej_bWZvIdyD1msWUeiFBhLWHddTCrPZ2QWudviHTzcUW4T56AVGQKX" \
                       "dmwZZGk6imACg_rgfvQih8jmeLFt0jtCzuAyiK8E6RuJZ_VdcY_Rz5LO9z-IgY1kkp"
        print("Connect to Dropbox - Initiated")
        conn = dropbox.Dropbox(dropboxToken)
        print("Connect to Dropbox - Completed")
        print("Reading survey details from Dropbox - Initiated")
        # inputFilePath = "/kickImages/Qualtrics/2022_Abhijith/CodedImages2022_Test_Result.csv"
        inputFilePath = "/kickImages/Qualtrics/2022_Abhijith/HIT_To_Publish/Batch16.csv"
        # inputFilePath = "/kickImages/Qualtrics/2022_Abhijith/HIT_Publish_Old/401-411.csv"
        def stream_dropbox_file(path):
            _, res = conn.files_download(path)
            with closing(res) as result:
                byte_data = result.content
                return io.BytesIO(byte_data)

        file_stream = stream_dropbox_file(inputFilePath)
        df = pd.read_csv(file_stream)
        print("Reading survey details from Dropbox - Completed")
        for name, survey_id in zip(df['Survey name'],df['survey_id']):
            print("Export survey data for {0} : Initiated".format(name))
            get_qualtrics_survey(dir_save_survey = path, survey_id = survey_id)
            print("Export survey data : Completed")

