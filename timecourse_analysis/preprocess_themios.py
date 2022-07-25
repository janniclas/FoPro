import preprocessor
import os
from initialize import ivermectin, themiostweets, themiosfollower

themios = themiostweets.iloc[0]
themiosfollower.set_axis(["User", "Username", "Displayname", "IrId"], axis=1, inplace=True)
interactions = ivermectin.loc[ivermectin["IrId"] == themios["Id"]]

impressions = preprocessor.preprocess(themios, interactions, themiosfollower)
impressions.to_csv(os.path.join("impressions", "themios_impressions.csv"))