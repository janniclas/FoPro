import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from initialize import *

def createSpreadingRateDf(df, createdTime, plotDf, name):
    interactions = 0
    for index, row in df.iterrows():
        interactions += 1
        timestamp = pd.to_datetime(row["Timestamp"])
        impression = row["Impressions"]
        newtimestamp = timestamp - createdTime
        x = str(newtimestamp).split()[-1]
        if str(newtimestamp.days) == "0":
            time = pd.to_datetime(x)
            spreadingrate = interactions / impression
            plotDf.loc[index, name] = spreadingrate
            plotDf.loc[index, "Timestamp"] = time
        else:
            break
def all_spreading_rates(): 
    createSpreadingRateDf(docknack, docknackcreated, plotdocknack, "docknack")
    createSpreadingRateDf(deuxcvsix, deuxcvsixcreated, plotdeuxcvsix, "deuxcvsix")
    createSpreadingRateDf(florianaigner, florianaignercreated, plotflorianaigner, "florianaigner")
    createSpreadingRateDf(lassehallstroem, lassehallstroemcreated, plotlassehallstroem, "LasseHallstroem")
    createSpreadingRateDf(rosenbusch, rosenbuschcreated, plotrosenbusch, "rosenbusch_")
    createSpreadingRateDf(themios, themisocreated, plotthemios, "Themios")

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
    ax.set_ylabel("Spreading Rate")
    ax.set_xlabel("Hours after the Tweet")
    plt.savefig('spreadingrate')
