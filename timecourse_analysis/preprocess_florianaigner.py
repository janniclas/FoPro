import preprocessor
import os
from initialize_preprocess import ivermectin, florianaignertweets, florianaignerfollower

def preprocess_florianaigner():
    florianaigner = florianaignertweets.iloc[3]
    florianaignerfollower.set_axis(["User", "Username", "Displayname", "IrId"], axis=1, inplace=True)
    retweets = ivermectin.loc[ivermectin["IrId"] == florianaigner["Id"]]

    impressions = preprocessor.preprocess(florianaigner, retweets, florianaignerfollower)
    impressions.to_csv(os.path.join("impressions", "florianaigner_impressions.csv"))

