import pandas as pd
import os
import sys 

data_directory = sys.argv[1]
os.chdir(data_directory) # directory with queried follower - files

ivermectin = pd.read_csv("ivermectin.csv", encoding= 'unicode_escape')

deuxcvsixfollower = pd.read_csv("194895383-deuxcvsix-debunking.csv")
docknackfollower = pd.read_csv("1010248944977416194-docknack-fakenews.csv")
florianaignerfollower = pd.read_csv("433607851-florianaigner-debunking.csv")
lassehallstroemfollower = pd.read_csv("374522219-LasseHallstroem-fakenews.csv")
rosenbuschfollower = pd.read_csv("1314116355197743105-rosenbusch_-fakenews.csv")
themiosfollower = pd.read_csv("8029309-themios-debunking.csv")

docknacktweets = ivermectin.loc[ivermectin["UserName"] == "docknack"]

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
