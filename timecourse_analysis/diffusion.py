import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from initialize import *

def createDiffusionDf(df, createdTime, plotDf, maxFollower, name):
    for index, row in df.iterrows():
        timestamp = pd.to_datetime(row["Timestamp"])
        impression = row["Impressions"]
        newtimestamp = timestamp - createdTime
        x = str(newtimestamp).split()[-1]
        if str(newtimestamp.days) == "0":
            time = pd.to_datetime(x)
            newimpression = impression / maxFollower * 100
            if newimpression <= 81:
                plotDf.loc[index, name] = newimpression
                plotDf.loc[index, "Timestamp"] = time
        else:
            break

def all_diffusions(): 
    createDiffusionDf(docknack, docknackcreated, plotdocknack, docknackmaxfollower, "docknack")
    createDiffusionDf(deuxcvsix, deuxcvsixcreated, plotdeuxcvsix, deuxcvsixmaxfollower, "deuxcvsix")
    createDiffusionDf(florianaigner, florianaignercreated, plotflorianaigner, florianaignermaxfollower, "florianaigner")
    createDiffusionDf(lassehallstroem, lassehallstroemcreated, plotlassehallstroem, lassehallstroemmaxfollower, "LasseHallstroem")
    createDiffusionDf(rosenbusch, rosenbuschcreated, plotrosenbusch, rosenbuschmaxfollower, "rosenbusch_")
    createDiffusionDf(themios, themisocreated, plotthemios, themiosmaxfollower, "Themios")

    fig,ax = plt.subplots()
    ax.plot("Timestamp", "docknack", data=plotdocknack, color="red", label="False Information")
    ax.plot("Timestamp", "deuxcvsix", data=plotdeuxcvsix, color="black", label = "Debunker")
    ax.plot("Timestamp", "florianaigner", data=plotflorianaigner, color="black", label = "_nolegend_")
    ax.plot("Timestamp", "LasseHallstroem", data=plotlassehallstroem, color="red", label = "_nolegend_")
    ax.plot("Timestamp", "rosenbusch_", data=plotrosenbusch, color="red", label = "_nolegend_")
    ax.plot("Timestamp", "Themios", data=plotthemios, color="black", label = "_nolegend_")
    hh_mm = DateFormatter('%H')
    ax.xaxis.set_major_formatter(hh_mm)
    plt.legend(loc="upper left")
    ax.set_ylabel("Reach in Percentage", fontsize=20)
    ax.set_xlabel("Hours after the Tweet", fontsize=20)
    plt.savefig('diffusion')
        
