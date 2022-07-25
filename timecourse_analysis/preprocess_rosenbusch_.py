import preprocessor
import os
from initialize_preprocess import ivermectin, rosenbuschtweets, rosenbuschfollower

rosenbusch = rosenbuschtweets.iloc[5]
rosenbuschfollower.set_axis(["User", "Username", "Displayname", "IrId"], axis=1, inplace=True)
interactions = ivermectin.loc[ivermectin["IrId"] == rosenbusch["Id"]]

impressions = preprocessor.preprocess(rosenbusch, interactions, rosenbuschfollower)
impressions.to_csv(os.path.join("impressions", "rosenbusch_impressions.csv"))
