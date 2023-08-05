# SurveyDataCollection
"Automated Qualtrics Survey Deployment &amp; AMT Integration: A project enabling seamless creation and publication of Qualtrics surveys. Integrates with Amazon Mechanical Turk to gather user responses through HIT publication."


README

-> DropBoxQualtricsIntegration_v1.0.1.y : 
This file is responsible for embedding images into surveys and publishing Qualtrics surveys

-> example.qsf : 
Sample qsf file (Qualtrics survey file)

-> RekognitionClassification.py : 
Image recongnition file

-> TextAnalysis.py : 
To analyze if text present in image or not

-> LabelDetection.py : 
To detect labels and types

-> FaceAnalysis.py : 
Face detectiona and features

->MTurk.py : 
Responsible for creating and publishing Amazon MTurk HIT

->HITLayout.XML : 
Layout page of HIT which defines the look and structure of the HIT

-> TurkListAssignment.py : 
To retrieve all the assignments associated with a HIT ID

-> GetResponse.py : 
Get all the responses associated to a Qualtrics survey

-> HITLayoutSanbox.xml : 
HIT layout for Sanbox publication

-> HITLayoutProduction.xml :
HIT layout for Producation publication

-> ApproveAssignment.py : 
To approve and pay for the eligible turkers

-> ChangeStatus.py : 
To change the status of a HIT

-> Webscraping.py : 
To extract images from the links

