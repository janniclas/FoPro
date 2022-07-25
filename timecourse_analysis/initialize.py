import pandas as pd
import os

ivermectin = pd.read_csv("ivermectin.csv")

deuxcvsixfollower = pd.read_csv("194895383-deuxcvsix-debunking-new.csv")
docknackfollower = pd.read_csv("1010248944977416194-docknack-fakenews-new.csv")
florianaignerfollower = pd.read_csv("433607851-florianaigner-debunking-new.csv")
lassehallstroemfollower = pd.read_csv("374522219-LasseHallstroem-fakenews-new.csv")
rosenbuschfollower = pd.read_csv("1314116355197743105-rosenbusch_-fakenews-new.csv")
themiosfollower = pd.read_csv("8029309-themios-debunking-new.csv")

docknack = pd.read_csv(os.path.join("impressions", "docknack_impressions.csv"))
deuxcvsix = pd.read_csv(os.path.join("impressions", "deuxcvsix_impressions.csv"))
florianaigner = pd.read_csv(os.path.join("impressions", "florianaigner_impressions.csv"))
lassehallstroem = pd.read_csv(os.path.join("impressions", "lassehallstroem_impressions.csv"))
rosenbusch = pd.read_csv(os.path.join("impressions", "rosenbusch_impressions.csv"))
themios = pd.read_csv(os.path.join("impressions", "themios_impressions.csv"))

docknacktweets = ivermectin.loc[ivermectin["UserName"] == "docknack"]
docknackcreated = pd.to_datetime(docknacktweets.iloc[1]["CreatedAt"])
deuxcvsixtweets = ivermectin.loc[ivermectin["UserName"] == "deuxcvsix"]
deuxcvsixcreated = pd.to_datetime(deuxcvsixtweets.iloc[0]["CreatedAt"])
florianaignertweets = ivermectin.loc[ivermectin["UserName"] == "florianaigner"]
florianaignercreated = pd.to_datetime(florianaignertweets.iloc[3]["CreatedAt"])
lassehallstroemtweets = ivermectin.loc[ivermectin["UserName"] == "LasseHallstroem"]
lassehallstroemcreated = pd.to_datetime(lassehallstroemtweets.iloc[4]["CreatedAt"])
rosenbuschtweets = ivermectin.loc[ivermectin["UserName"] == "rosenbusch_"]
rosenbuschcreated = pd.to_datetime(rosenbuschtweets.iloc[5]["CreatedAt"])
themiostweets = ivermectin.loc[ivermectin["UserName"] == "Themios"]
themisocreated = pd.to_datetime(themiostweets.iloc[0]["CreatedAt"])

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