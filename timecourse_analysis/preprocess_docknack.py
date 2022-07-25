import preprocessor 
import os
from initialize_preprocess import ivermectin, docknacktweets, docknackfollower

def preprocess_docknack():
    docknack = docknacktweets.iloc[1]
    docknackfollower.set_axis(["User", "Username", "Displayname", "IrId"], axis=1, inplace=True)
    interactions = ivermectin.loc[ivermectin["IrId"] == docknack["Id"]]

    impressions = preprocessor.preprocess(docknack, interactions, docknackfollower)
    impressions.to_csv(os.path.join("impressions", "docknack_impressions.csv"))






