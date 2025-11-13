
# generate_streamhub_dataset.py
# Synthetic Dataset Generator for StreamHub 2024
# Author: Deepa Mallipeddi

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_users(n=10000):
    plans = ["ad_supported", "basic", "premium"]
    regions = ["US","IN","GB","CA","AU"]
    users = []
    base = datetime(2024,1,1)
    for uid in range(1, n+1):
        signup = base + timedelta(days=random.randint(0,180))
        users.append([uid, signup.date(), random.choice(plans), random.choice(regions)])
    return pd.DataFrame(users, columns=["user_id","signup_date","plan_type","region"])

def main():
    users = generate_users(10000)
    users.to_csv("users.csv", index=False)

if __name__ == "__main__":
    main()
