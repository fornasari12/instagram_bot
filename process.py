import pandas as pd
from datetime import datetime

df = pd.read_csv('/Users/nicolasfornasari/PycharmProjects/instagram_bot/selenium_bot/not_following_back_2020-11-25.csv')

not_followers = list(df.columns)

df_unfollowers = pd.DataFrame({"unfollowers": not_followers})

df_unfollowers.to_csv(f'df_unfollowers_{datetime.now().date()}.csv')

print(not_followers)