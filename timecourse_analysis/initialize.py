import pandas as pd
import os
import sys 
from initialize_preprocess import * 


data_directory = sys.argv[1]
os.chdir(data_directory) # directory with queried follower - files

docknack = pd.read_csv(os.path.join("impressions", "docknack_impressions.csv"))
deuxcvsix = pd.read_csv(os.path.join("impressions", "deuxcvsix_impressions.csv"))
florianaigner = pd.read_csv(os.path.join("impressions", "florianaigner_impressions.csv"))
lassehallstroem = pd.read_csv(os.path.join("impressions", "lassehallstroem_impressions.csv"))
rosenbusch = pd.read_csv(os.path.join("impressions", "rosenbusch_impressions.csv"))
themios = pd.read_csv(os.path.join("impressions", "themios_impressions.csv"))

docknackmaxfollower = docknack.iloc[-1]["Impressions"]
deuxcvsixmaxfollower = deuxcvsix.iloc[-1]["Impressions"]
florianaignermaxfollower = florianaigner.iloc[-1]["Impressions"]
lassehallstroemmaxfollower = lassehallstroem.iloc[-1]["Impressions"]
rosenbuschmaxfollower = rosenbusch.iloc[-1]["Impressions"]
themiosmaxfollower = themios.iloc[-1]["Impressions"]

docknackmaxinteractions = docknack.index[-1] 
deuxcvsixmaxinteractions = deuxcvsix.index[-1] 
florianaignermaxinteractions = florianaigner.index[-1] 
lassehallstroemmaxinteractions = lassehallstroem.index[-1] 
rosenbuschmaxinteractions = rosenbusch.index[-1] 
themiosmaxinteractions = themios.index[-1] 

plotdocknack = pd.DataFrame(columns=["Timestamp", "docknack"])
plotdeuxcvsix = pd.DataFrame(columns=["Timestamp", "deuxcvsix"])
plotflorianaigner = pd.DataFrame(columns=["Timestamp", "florianaigner"])
plotlassehallstroem = pd.DataFrame(columns=["Timestamp", "LasseHallstroem"])
plotrosenbusch = pd.DataFrame(columns=["Timestamp", "rosenbusch_"])
plotthemios = pd.DataFrame(columns=["Timestamp", "Themios"])

docknackcreated = pd.to_datetime(docknacktweets.iloc[1]["CreatedAt"])