import sys 
import preprocessor
from initialize_preprocess import *


def preprocess(): 
    preprocessor.preprocess_data(0, deuxcvsixtweets, deuxcvsixfollower, os.path.join("impressions", "deuxcvsix_impressions.csv"))
    preprocessor.preprocess_data(1, docknacktweets, docknackfollower, os.path.join("impressions", "docknack_impressions.csv"))
    preprocessor.preprocess_data(3, florianaignertweets, florianaignerfollower, os.path.join("impressions", "florianaigner_impressions.csv"))
    preprocessor.preprocess_data(4, lassehallstroemtweets, lassehallstroemfollower, os.path.join("impressions", "lassehallstroem_impressions.csv"))
    preprocessor.preprocess_data(5, rosenbuschtweets, rosenbuschfollower, os.path.join("impressions", "rosenbusch_impressions.csv"))
    preprocessor.preprocess_data(0, themiostweets, themiosfollower, os.path.join("impressions", "themios_impressions.csv"))

def statistics(): 
    from diffusion import all_diffusions 
    from interactions import all_interactions 
    from spreadingrate import all_spreading_rates 
    all_diffusions()
    all_interactions()
    all_spreading_rates()


data_directory = sys.argv[1]
os.chdir(data_directory) # directory with queried follower - files
preprocess()
statistics()
