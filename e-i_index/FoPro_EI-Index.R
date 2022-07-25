library(dplyr)
library(tidyverse)
library(ggplot2)
library(ggbeeswarm)
library(coin)

args = commandArgs(trailingOnly=TRUE)
data_path = args[1]
#import Twitter Data
data <- read.csv(paste(data_path, "/ivermectin.csv",sep=""), 
                 header = T,
                 sep = ",",
                 encoding = "UTF-8", 
                 stringsAsFactors = FALSE, 
                 numerals = "no.loss")

#Filter data for retweets of each selected post
docknack <- data %>% filter(IrId=="1436701733942661120") %>% filter(grepl("RT", Text))
rosenbusch_ <- data %>% filter(IrId=="1386610811091800064") %>% filter(grepl("RT", Text))
LasseHallstroem <- data %>% filter(IrId=="1456272436236750856") %>% filter(grepl("RT", Text))
deuxcvsix <- data %>% filter(IrId=="1436045882282102795") %>% filter(grepl("RT", Text))
florianaigner <- data %>% filter(IrId=="1452950980933394433") %>% filter(grepl("RT", Text))
themios <- data %>% filter(IrId=="1460638456204435467") %>% filter(grepl("RT", Text))

#create Vectors with every user that retweeted each type of tweet
allRumors <- c(docknack$UserId, LasseHallstroem$UserId, rosenbusch_$UserId)
allDebunking <- c(deuxcvsix$UserId, florianaigner$UserId, themios$UserId)
allRumors <- unique(allRumors)
allDebunking <- unique(allDebunking)

#check for users that retweeted with types
checkDoubles <- intersect(allRumors, allDebunking)


#import follower tables
debunkingFollowers <- read.csv(paste(data_path, "/debunking-all.csv",sep=""), 
                               header = F, 
                               sep = ",", 
                               encoding = "UTF-8", 
                               stringsAsFactors = FALSE,
                               numerals = "no.loss")
rumorsFollowers <- read.csv(paste(data_path, "/fake-all.csv",sep=""), 
                            header = F, 
                            sep = ",", 
                            encoding = "UTF-8", 
                            stringsAsFactors = FALSE,
                            numerals = "no.loss")

# create vectors with all users that were reached by each type of post
debunkingReach <- unique(debunkingFollowers$V1)
rumorsReach <- unique(rumorsFollowers$V1)
#bothReach <- intersect(debunkingFollowers$V1, rumorsFollowers$V1)

#create one follower table for lookup
FollowersAll <- rbind(rumorsFollowers, debunkingFollowers) %>%
  group_by(V4) %>% summarise(followers=list(unique(V1)))


##calculate mean EI index for debunking posts

#create dataframe with every user that retweeted a debunking post and that has an entry in the follower table
#for example: deleted users don't have an entry
debunking <- data.frame(interactions=intersect(allDebunking, FollowersAll$V4))
#create new column that contains a vector with all followers of that user
debunking <- merge(debunking, FollowersAll, by.x="interactions", by.y="V4")
#calculate in- and out-links and EI index by intersecting the followers with the users that were reached by false information posts
debunking <- debunking %>% rowwise() %>% mutate(outGroup= list(intersect(followers, rumorsReach))) %>%
  mutate(Xout=length(outGroup), Xin=length(followers)-Xout, EI=(Xout-Xin)/(Xout+Xin))

debunkingEI <- debunking$EI
#debunkingEI <- debunking$EI[!debunking$EI %in% boxplot.stats(debunking$EI)$out]

#Mean EI index
EiMeanDebunk = mean(debunkingEI)
EiMedianDebunk = median(debunking$EI)


##calculate mean EI index for false information posts (identical to debunking)

rumors <- data.frame(interactions=intersect(allRumors, FollowersAll$V4))
rumors <- merge(rumors, FollowersAll, by.x="interactions", by.y="V4")
rumors <- rumors %>% rowwise() %>% mutate(outGroup= list(intersect(followers, debunkingReach))) %>%
  mutate(Xout=length(outGroup), Xin=length(followers)-Xout, EI=(Xout-Xin)/(Xout+Xin))

rumorsEI <- rumors$EI
#rumorsEI <- rumors$EI[!rumors$EI %in% boxplot.stats(rumors$EI)$out]

EiMeanRumor = mean(rumorsEI)
EiMedianRumor = median(rumors$EI)


#create histogram
EIdf <- rbind(data.frame(value=rumorsEI, type=factor("false information")), data.frame(value=debunkingEI, type=factor("debunking")))
ggplot(EIdf, aes(x = type, y = value, fill = type)) +
  geom_violin(alpha = 0.5) +
  stat_summary(fun = "mean",
               geom = "crossbar",
               width = 0.9,
               aes(colour = type)) +
  scale_fill_manual(values=c(rgb(0.815,0.5,0.655),rgb(0.655,0.71,0.57)))+
  scale_colour_manual(values=c(rgb(0.815,0.5,0.655),rgb(0.655,0.71,0.57)))+
  theme_classic(base_size = 10)

# test for normal distribution
shapiro.test(rumorsEI)
shapiro.test(debunkingEI)

#test for variance similarity
var.test(rumorsEI, debunkingEI)

#test for median difference
wilcox_test(value ~ type, data = EIdf)
