import pandas as pd
from initialize_preprocess import ivermectin

def preprocess(tweet, interactions, follower):
    interactions["CreatedAt"] = pd.to_datetime(interactions["CreatedAt"])
    interactions.sort_values(by="CreatedAt", inplace=True)

    impressions_user = pd.DataFrame(columns=["Timestamp", "Follower"])
    impressions = pd.DataFrame(columns=["Timestamp", "Impressions"])

    originaluserId = tweet["UserId"]
    originalfollowerdf = follower.loc[follower["IrId"] == originaluserId]
    originalfollower = originalfollowerdf["User"].tolist()
    createdat = pd.to_datetime(tweet["CreatedAt"])
    impressions_user = impressions_user.append({"Timestamp": createdat, "Follower": originalfollower}, ignore_index=True)
    impressions = impressions.append({"Timestamp": createdat, "Impressions": len(originalfollower)}, ignore_index=True)

    for index, row in interactions.iterrows():
        userId = row["UserId"]
        timestamp = row["CreatedAt"]
        userfollowerdf = follower.loc[follower["IrId"] == userId]
        userfollower = userfollowerdf["User"].tolist()

        lastrow = impressions_user.iloc[-1]
        lastfollower = lastrow["Follower"]
        uniquef = []
        for f in userfollower:
            if f not in lastfollower:
                uniquef.append(f)
        impressions_user = impressions_user.append({"Timestamp": timestamp, "Follower": lastfollower + uniquef}, ignore_index=True)
        impressions = impressions.append({"Timestamp": timestamp, "Impressions": len(lastfollower+uniquef)}, ignore_index=True)
        
    return impressions

def preprocess_data(iloc, tweets, follower, output_file):
    user = tweets.iloc[iloc]
    follower.set_axis(["User", "Username", "Displayname", "IrId"], axis=1, inplace=True)
    retweets = ivermectin.loc[ivermectin["IrId"] == user["Id"]]

    impressions = preprocess(user, retweets, follower)
    impressions.to_csv(output_file)