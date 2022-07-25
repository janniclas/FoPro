import preprocessor
import os
from initialize import ivermectin, lassehallstroemtweets, lassehallstroemfollower

lassehallstroem = lassehallstroemtweets.iloc[4]
lassehallstroemfollower.set_axis(["User", "Username", "Displayname", "IrId"], axis=1, inplace=True)
interactions = ivermectin.loc[ivermectin["IrId"] == lassehallstroem["Id"]]

impressions = preprocessor.preprocess(lassehallstroem, interactions, lassehallstroemfollower)
impressions.to_csv(os.path.join("impressions", "lassehallstroem_impressions.csv"))
