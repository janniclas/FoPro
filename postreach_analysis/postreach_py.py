# -*- coding: utf-8 -*-

#######################################################################################################
#                                                                                                     #
#                                    # Post Reach Analysis #                                          #
#                                                                                                     #
#######################################################################################################

import os
import pandas as pd
import numpy as np
import re
from varname import nameof
import sys

data_directory = sys.argv[1]
os.chdir(data_directory) # directory with queried follower - files

#######################################################################################################

col_names = ["col1", "col2"]

# read the files

themios = pd.read_csv("80293090-themios-debunking-unique.csv", names=col_names, sep=",", encoding='UTF8')
deuxcvsix = pd.read_csv("194895383-deuxcvsix-debunking-unique.csv", names=col_names, encoding='UTF8')
florianaigner = pd.read_csv("433607851-florianaigner-debunking-unique.csv", names=col_names, encoding='UTF8')

LasseHallstroem = pd.read_csv("374522219-LasseHallstroem-fakenews-unique.csv", names=col_names, encoding='UTF8')
docknack = pd.read_csv("1010248944977416194-docknack-fakenews-unique.csv", names=col_names, encoding='UTF8')
rosenbusch = pd.read_csv("1314116355197743105-rosenbusch_-fakenews-unique.csv", names=col_names, encoding='UTF8')

#######################################################################################################

# clean entries

themios.reset_index(inplace = True)
col_names = list(themios.columns)
themios[col_names]=themios[col_names].astype(str)
themios["new"] = themios.apply(','.join, axis=1)
themios["new"] = themios['new'].apply(lambda x: re.sub(r"\D*$","", str(x)))
themios = themios["new"]
themios = pd.DataFrame(themios)

deuxcvsix.reset_index(inplace = True)
col_names = list(deuxcvsix.columns)
deuxcvsix[col_names]=deuxcvsix[col_names].astype(str)
deuxcvsix["new"] = deuxcvsix.apply(','.join, axis=1)
deuxcvsix["new"] = deuxcvsix['new'].apply(lambda x: re.sub(r"\D*$","", str(x)))
deuxcvsix = deuxcvsix["new"]
deuxcvsix = pd.DataFrame(deuxcvsix)

florianaigner.reset_index(inplace = True)
col_names = list(florianaigner.columns)
florianaigner[col_names]=florianaigner[col_names].astype(str)
florianaigner["new"] = florianaigner.apply(','.join, axis=1)
florianaigner["new"] = florianaigner['new'].apply(lambda x: re.sub(r"\D*$","", str(x)))
florianaigner = florianaigner["new"]
florianaigner = pd.DataFrame(florianaigner)

LasseHallstroem.reset_index(inplace = True)
col_names = list(LasseHallstroem.columns)
LasseHallstroem[col_names]=LasseHallstroem[col_names].astype(str)
LasseHallstroem["new"] = LasseHallstroem.apply(','.join, axis=1)
LasseHallstroem["new"] = LasseHallstroem['new'].apply(lambda x: re.sub(r"\D*$","", str(x)))
LasseHallstroem = LasseHallstroem["new"]
LasseHallstroem = pd.DataFrame(LasseHallstroem)

docknack.reset_index(inplace = True)
col_names = list(docknack.columns)
docknack[col_names]=docknack[col_names].astype(str)
docknack["new"] = docknack.apply(','.join, axis=1)
docknack["new"] = docknack['new'].apply(lambda x: re.sub(r"\D*$","", str(x)))
docknack = docknack["new"]
docknack = pd.DataFrame(docknack)

rosenbusch.reset_index(inplace = True)
col_names = list(rosenbusch.columns)
rosenbusch[col_names]=rosenbusch[col_names].astype(str)
rosenbusch["new"] = rosenbusch.apply(','.join, axis=1)
rosenbusch["new"] = rosenbusch['new'].apply(lambda x: re.sub(r"\D*$","", str(x)))
rosenbusch = rosenbusch["new"]
rosenbusch = pd.DataFrame(rosenbusch)

#######################################################################################################

# themios splitten 
themios= themios["new"].str.rsplit(',', 1, expand=True)
themios= themios.join(themios[0].str.split(',', 2, expand=True), rsuffix="new")
themios.drop(["0"], axis=1, inplace=True)
col_renamed = ["ParentID","UserID","UserName","UserScreenName"]
themios.columns = col_renamed


# deuxcvsix splitten
deuxcvsix= deuxcvsix["new"].str.rsplit(',', 1, expand=True)
deuxcvsix= deuxcvsix.join(deuxcvsix[0].str.split(',', 2, expand=True), rsuffix="new")
deuxcvsix.drop(["0"], axis=1, inplace=True)
deuxcvsix.columns = col_renamed


# florianaigner splitten
florianaigner= florianaigner["new"].str.rsplit(',', 1, expand=True)
florianaigner= florianaigner.join(florianaigner[0].str.split(',', 2, expand=True), rsuffix="new")
florianaigner.drop(["0"], axis=1, inplace=True)
florianaigner.columns = col_renamed


# LasseHallstroem splitten
LasseHallstroem= LasseHallstroem["new"].str.rsplit(',', 1, expand=True)
LasseHallstroem= LasseHallstroem.join(LasseHallstroem[0].str.split(',', 2, expand=True), rsuffix="new")
LasseHallstroem.drop(["0"], axis=1, inplace=True)
LasseHallstroem.columns = col_renamed


# docknack splitten
docknack= docknack["new"].str.rsplit(',', 1, expand=True)
docknack= docknack.join(docknack[0].str.split(',', 2, expand=True), rsuffix="new")
docknack.drop(["0"], axis=1, inplace=True)
docknack.columns = col_renamed


# rosenbusch splitten
rosenbusch= rosenbusch["new"].str.rsplit(',', 1, expand=True)
rosenbusch= rosenbusch.join(rosenbusch[0].str.split(',', 2, expand=True), rsuffix="new")
rosenbusch.drop(["0"], axis=1, inplace=True)
rosenbusch.columns = col_renamed



#######################################################################################################

# calculate the unions through merging

merge_col = col_renamed[1:]

themios_deuxcvsix = pd.merge(themios, deuxcvsix, how='inner', on=merge_col)
themios_LasseHallstroem = pd.merge(themios, florianaigner, how='inner', on=merge_col)
themios_florianaigner = pd.merge(themios, LasseHallstroem, how='inner', on=merge_col)
themios_docknack = pd.merge(themios, docknack, how='inner', on=merge_col)
themios_rosenbusch = pd.merge(themios, rosenbusch, how='inner', on=merge_col)

deuxcvsix_LasseHallstroem = pd.merge(deuxcvsix, florianaigner, how='inner', on=merge_col)
deuxcvsix_florianaigner = pd.merge(deuxcvsix, LasseHallstroem, how='inner', on=merge_col)
deuxcvsix_docknack = pd.merge(deuxcvsix, docknack, how='inner', on=merge_col)
deuxcvsix_rosenbusch = pd.merge(deuxcvsix, rosenbusch, how='inner', on=merge_col)

LasseHallstroem_florianaigner = pd.merge(florianaigner, LasseHallstroem, how='inner', on=merge_col)
LasseHallstroem_docknack = pd.merge(florianaigner, docknack, how='inner', on=merge_col)
LasseHallstroem_rosenbusch = pd.merge(florianaigner, rosenbusch, how='inner', on=merge_col)

florianaigner_docknack = pd.merge(LasseHallstroem, docknack, how='inner', on=merge_col)
florianaigner_rosenbusch = pd.merge(LasseHallstroem, rosenbusch, how='inner', on=merge_col)

rosenbusch_docknack = pd.merge(docknack, rosenbusch, how='inner', on=merge_col)


#######################################################################################################

# prepare data set structure

U_A = {
       "Post_A":[], 
       "Post_B":[], 
       "PostType_A":[], 
       "PostType_B":[],
       "UserID_A":[],
       "UserID_B":[],
       "Total_A":[], 
       "Total_B":[],
       "IntersectionID_AB":[], 
       "IntersectionTotal_AB":[], 
       "Pct_ABA":[],
       "Pct_ABB":[]
       }

debunk_fal = { "debunking": ("themios", "deuxcvsix", "florianaigner"),
               "false information": ("LasseHallstroem", "docknack", "rosenbusch"),
               "themios": (themios["UserID"]),
               "deuxcvsix": (deuxcvsix["UserID"]),
               "florianaigner": (florianaigner["UserID"]),
               "LasseHallstroem": (LasseHallstroem["UserID"]),
               "docknack": (docknack["UserID"]),
               "rosenbusch": (rosenbusch["UserID"]),
               "themios_deuxcvsix":(themios_deuxcvsix), "themios_LasseHallstroem": (themios_LasseHallstroem), "themios_florianaigner":(themios_florianaigner),
               "themios_docknack":(themios_docknack), "themios_rosenbusch":(themios_rosenbusch), "deuxcvsix_LasseHallstroem":(deuxcvsix_LasseHallstroem), \
             "deuxcvsix_florianaigner":(deuxcvsix_florianaigner), "deuxcvsix_docknack":(deuxcvsix_docknack), "deuxcvsix_rosenbusch":(deuxcvsix_rosenbusch), \
             "LasseHallstroem_florianaigner":(LasseHallstroem_florianaigner), "LasseHallstroem_docknack":(LasseHallstroem_docknack), \
             "LasseHallstroem_rosenbusch":(LasseHallstroem_rosenbusch), "florianaigner_docknack":(florianaigner_docknack), \
             "florianaigner_rosenbusch":(florianaigner_rosenbusch), "rosenbusch_docknack":(rosenbusch_docknack)
             }


names = ("themios_deuxcvsix", "themios_LasseHallstroem", "themios_florianaigner", "themios_docknack", "themios_rosenbusch", "deuxcvsix_LasseHallstroem", \
             "deuxcvsix_florianaigner", "deuxcvsix_docknack", "deuxcvsix_rosenbusch", "LasseHallstroem_florianaigner", "LasseHallstroem_docknack", \
             "LasseHallstroem_rosenbusch", "florianaigner_docknack", "florianaigner_rosenbusch", "rosenbusch_docknack")


# append calculated numbers to prepared dataset

for name in names:
        Post_A = name.rsplit("_")[0]
        U_A["Post_A"].append(Post_A)
        PostType_A = [k for k, v in debunk_fal.items() if Post_A in v][0]
        U_A["PostType_A"].append(PostType_A)
        UserID_A = [v for k, v in debunk_fal.items() if Post_A in k][0]
        U_A["UserID_A"].append(UserID_A)
        U_A["Total_A"].append(len(UserID_A))
                
        Post_B = name.rsplit("_")[1]
        U_A["Post_B"].append(Post_B)
        PostType_B = [k for k, v in debunk_fal.items() if Post_B in v][0]
        U_A["PostType_B"].append(PostType_B)
        UserID_B = [v for k, v in debunk_fal.items() if Post_B in k][0]
        U_A["UserID_B"].append(UserID_B)
        U_A["Total_B"].append(len(UserID_B))
        
        IntersectionID_AB = [v for k, v in debunk_fal.items() if name in k][0]["UserID"]
        U_A["IntersectionID_AB"].append(IntersectionID_AB)
        U_A["IntersectionTotal_AB"].append(len(IntersectionID_AB))
        
        U_A["Pct_ABA"].append(len(IntersectionID_AB)/len(UserID_A))
        U_A["Pct_ABB"].append(len(IntersectionID_AB)/len(UserID_B))


df_UA = pd.DataFrame.from_dict(U_A)

df_UA.to_excel("postreach_UA.xlsx",
             sheet_name='Sheet_name_1') 
