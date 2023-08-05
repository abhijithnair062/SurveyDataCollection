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
    imageFaceData = pd.DataFrame(columns=['Image Name','Image Category','Is Face present',
                                          'AgeRange-Low','AgeRange-High','Smile','Smile Confidence',
                                          'Eyeglasses','Eyeglasses Confidence','Sunglasses',
                                          'Sunglasses Confidence','Gender','Gender Confidence',
                                          'Beard','Beard Confidence','Mustache','Mustache Confidence',
                                          'EyesOpen','EyesOpen Confidence','MouthOpen',
                                          'MouthOpen Confidence','Emotion-SAD','Emotion-ANGRY',
                                          'Emotion-CONFUSED','Emotion-HAPPY','Emotion-CALM',
                                          'Emotion-DISGUSTED','Emotion-SURPRISED','Emotion-FEAR'])
    def getFaceDetails(filepath, filename, imageFaceData):
        with open(filepath+"/"+filename,'rb') as source_image:
            source_bytes = source_image.read()
        try:
            response = client.detect_faces(Image={'Bytes': source_bytes},Attributes=['ALL'])
            Emotion_SAD,Emotion_ANGRY,Emotion_CONFUSED,Emotion_HAPPY,Emotion_DISGUSTED,Emotion_SURPRISED,Emotion_FEAR,Emotion_CALM = '','','','','','','',''
            if response['FaceDetails']:
                for faceDetails in response['FaceDetails']:
                    for faceEmotions in faceDetails['Emotions']:
                        if(faceEmotions['Type']=='SAD'):
                            Emotion_SAD = faceEmotions['Confidence']
                        if(faceEmotions['Type']=='ANGRY'):
                            Emotion_ANGRY = faceEmotions['Confidence']
                        if(faceEmotions['Type']=='CONFUSED'):
                            Emotion_CONFUSED = faceEmotions['Confidence']
                        if(faceEmotions['Type']=='HAPPY'):
                            Emotion_HAPPY = faceEmotions['Confidence']

                        if(faceEmotions['Type']=='CALM'):
                            Emotion_CALM= faceEmotions['Confidence']
                        if(faceEmotions['Type']=='DISGUSTED'):
                            Emotion_DISGUSTED = faceEmotions['Confidence']
                        if(faceEmotions['Type']=='SURPRISED'):
                            Emotion_SURPRISED = faceEmotions['Confidence']
                        if(faceEmotions['Type']=='FEAR'):
                            Emotion_FEAR = faceEmotions['Confidence']
                    print(faceDetails)
                    imageFaceData = imageFaceData.append({'Image Name':filename,
                                                          'AgeRange-Low':faceDetails[
                                                              'AgeRange'][
                                                              'Low'],
                                                          'AgeRange-High':faceDetails['AgeRange']['High'],
                                                          'Smile':faceDetails['Smile']['Value'],
                                                          'Smile Confidence':faceDetails['Smile']['Confidence'],
                                                          'Eyeglasses':faceDetails['Eyeglasses']['Value'] ,
                                                          'Eyeglasses Confidence':faceDetails['Eyeglasses']['Confidence'],
                                                          'Sunglasses': faceDetails['Sunglasses']['Value'],
                                                          'Sunglasses Confidence': faceDetails['Sunglasses']['Confidence'],
                                                          'Gender':faceDetails['Gender']['Value'],
                                                          'Gender Confidence':faceDetails['Gender']['Confidence'],
                                                          'Beard':faceDetails['Beard']['Value'],
                                                          'Beard Confidence':faceDetails['Beard']['Confidence'],
                                                          'Mustache': faceDetails['Mustache']['Value'],
                                                          'Mustache Confidence':faceDetails['Mustache']['Confidence'],
                                                          'EyesOpen': faceDetails['EyesOpen']['Value'],
                                                          'EyesOpen Confidence': faceDetails['EyesOpen']['Confidence'],
                                                          'MouthOpen': faceDetails['MouthOpen']['Value'],
                                                          'MouthOpen Confidence':faceDetails['MouthOpen']['Confidence'],
                                                          'Emotion-SAD':Emotion_SAD,'Emotion-ANGRY':Emotion_ANGRY,
                                                          'Emotion-CONFUSED':Emotion_CONFUSED,'Emotion-HAPPY':Emotion_HAPPY,
                                                          'Emotion-CALM':Emotion_CALM,'Emotion-DISGUSTED':Emotion_DISGUSTED,
                                                          'Emotion-SURPRISED':Emotion_SURPRISED,'Emotion-FEAR':Emotion_FEAR}, ignore_index=True)
            else:
                imageFaceData = imageFaceData.append({'Image Name':filename,'Image Category': filename,
                                                  'Is Face present':'No'}, ignore_index=True)
        except:
            imageFaceData = imageFaceData.append({'Image Name':filename,'Image Category': filename,
                                                  'Is Face present':'Image Exception'}, ignore_index=True)
        return imageFaceData
    # for image in column_data:
    #     if(image in os.listdir(imageFolderPath)):
    #         imageFaceData = getFaceDetails(imageFolderPath,image,
    #                                        imageFaceData)
    # for file in os.listdir(imageFolderPath):
    #     imageFaceData = getFaceDetails(imageFolderPath,file,
    #                                    imageFaceData)
    # print(imageFaceData)
    for image in os.listdir(imageFolderPath):
        imageFaceData = getFaceDetails(imageFolderPath,image,imageFaceData)
    imageFaceData.to_csv(destination_csv_folder + '/Image_FaceDetails.csv', index = False,
                         header=True,encoding='utf-8')
if __name__ == "__main__":
    main()