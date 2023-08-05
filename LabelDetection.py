import pandas as pd
import csv
import boto3
import os
def main():
    # df = pd.read_excel('/Users/abhijithnair/Desktop/RA/NoRekognition.xlsx')
    # column_name = 'c_id'
    # column_data = df[column_name].tolist()
    # column_data = {str(x)+".jpg" for x in column_data}
    # Input folder path
    imageFolderPath = '/Users/abhijithnair/Desktop/RA/MTurkIntegration/robots_wearables_gadgets'
    destination_csv_folder = \
        '/Users/abhijithnair/Desktop/RA/MTurkIntegration/Image_Analysis_04102023'


    # Read credentials from Credentials csv
    credentialsFilePath = "/Users/abhijithnair/Desktop/RA/abhijithnair_accessKeys.csv"
    with open(credentialsFilePath,'r') as input:
        next(input)
        reader = csv.reader(input)
        for line in reader:
            access_key_id = line[2]
            secret_access_key = line[3]

    client = boto3.client('rekognition',aws_access_key_id = access_key_id,
                          aws_secret_access_key = secret_access_key,region_name='us-east-2')
    imageLabelData = pd.DataFrame(columns=['Image Name','Image Category','Object detected','Confidence'])
    def getLabelDetails(filepath, filename, imageLabelData):
        with open(filepath+"/"+filename,'rb') as source_image:
            source_bytes = source_image.read()
        try:
            response = client.detect_labels(Image={'Bytes': source_bytes},MinConfidence=75)
            if response['Labels']:
                for labeldetails in response['Labels']:
                    imageLabelData = imageLabelData.append({'Image Name': filename,'Image Category': filename,'Object detected': labeldetails['Name'] ,'Confidence': labeldetails['Confidence']}, ignore_index=True)
            else:
                imageLabelData = imageLabelData.append({'Image Name': filename,'Image Category': filename }, ignore_index=True)

        except Exception:
            imageLabelData = imageLabelData.append({'Image Name':filename,'Image Category': filename,'Object detected': 'Image Exception'}, ignore_index=True)
        return imageLabelData
    # for image in column_data:
    #     if(image in os.listdir(imageFolderPath)):
    #         imageLabelData = getLabelDetails(imageFolderPath,image,
    #                                          imageLabelData)
    # for file in os.listdir(imageFolderPath):
    #     imageLabelData = getLabelDetails(imageFolderPath,file,
    #                                      imageLabelData)
    for image in os.listdir(imageFolderPath):
        imageLabelData = getLabelDetails(imageFolderPath,image,imageLabelData)
    imageLabelData.to_csv(destination_csv_folder + '/Image_LabelDetails.csv', index = False,
                          header=True,encoding='utf-8')
if __name__ == "__main__":
    main()