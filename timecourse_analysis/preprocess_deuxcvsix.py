import preprocessor
import os
from initialize import ivermectin, deuxcvsixtweets, deuxcvsixfollower

deuxcvsix = deuxcvsixtweets.iloc[0]
deuxcvsixfollower.set_axis(["User", "Username", "Displayname", "IrId"], axis=1, inplace=True)
interactions = ivermectin.loc[ivermectin["IrId"] == deuxcvsix["Id"]]

impressions = preprocessor.preprocess(deuxcvsix, interactions, deuxcvsixfollower)
impressions.to_csv(os.path.join("impressions", "deuxcvsix_impressions.csv"))