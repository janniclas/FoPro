import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from initialize import *

def createInteractionsDf(df, createdTime, plotDf, maxInteraction, name):
    counter = 1
    for index, row in df.iterrows():
        timestamp = pd.to_datetime(row["Timestamp"])
        newtimestamp = timestamp - createdTime
        x = str(newtimestamp).split()[-1]
        if str(newtimestamp.days) == "0":
            time = pd.to_datetime(x)
            percentageinteraction = counter / maxInteraction * 100
            if percentageinteraction <= 80:
                plotDf.loc[index, name] = percentageinteraction
                plotDf.loc[index, "Timestamp"] = time
            counter += 1
        else:
            break
    
createInteractionsDf(docknack, docknackcreated, plotdocknack, docknackmaxinteractions, "docknack")
createInteractionsDf(deuxcvsix, deuxcvsixcreated, plotdeuxcvsix, deuxcvsixmaxinteractions, "deuxcvsix")
createInteractionsDf(florianaigner, florianaignercreated, plotflorianaigner, florianaignermaxinteractions, "florianaigner")
createInteractionsDf(lassehallstroem, lassehallstroemcreated, plotlassehallstroem, lassehallstroemmaxinteractions, "LasseHallstroem")
createInteractionsDf(rosenbusch, rosenbuschcreated, plotrosenbusch, rosenbuschmaxinteractions, "rosenbusch_")
createInteractionsDf(themios, themisocreated, plotthemios, themiosmaxinteractions, "Themios")

fig,ax = plt.subplots()
ax.plot("Timestamp", "docknack", data=plotdocknack, color="red", label="False Information")
ax.plot("Timestamp", "deuxcvsix", data=plotdeuxcvsix, color="black", label = "Debunker")
ax.plot("Timestamp", "florianaigner", data=plotflorianaigner, color="black", label = "_nolegend_")
ax.plot("Timestamp", "LasseHallstroem", data=plotlassehallstroem, color="red", label = "_nolegend_")
ax.plot("Timestamp", "rosenbusch_", data=plotrosenbusch, color="red", label = "_nolegend_")
ax.plot("Timestamp", "Themios", data=plotthemios, color="black", label = "_nolegend_")
hh_mm = DateFormatter('%H')
ax.xaxis.set_major_formatter(hh_mm)
plt.legend(loc="upper left")#

ax.set_ylabel("Interactions in Percentage", fontsize=20)
ax.set_xlabel("Hours after the Tweet", fontsize=20)
plt.show()
    