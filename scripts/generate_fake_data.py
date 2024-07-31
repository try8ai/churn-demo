import pandas as pd
import numpy as np

np.random.seed(42)

# Parameters
num_accounts = 1000
num_users_per_account = np.random.randint(5, 20, num_accounts)
initial_logins_mean = 20
initial_logins_std = 5
consistent_logins_mean = 15
consistent_logins_std = 20

decay_factor_mean = 0.85
decay_factor_std = 0.05
churn_probability = 0.2

global_user_id = 0
data = []

for account_id in range(num_accounts):
    for user_id in range(num_users_per_account[account_id]):
        logins_per_month = np.zeros(12)
        
        if np.random.random() < churn_probability:
            # High churn user with decaying behavior
            logins_per_month[0] = max(0, np.round(np.random.normal(loc=initial_logins_mean, scale=initial_logins_std)))
            decay_factor = np.random.normal(loc=decay_factor_mean, scale=decay_factor_std)
            for month in range(1, 12):
                logins_per_month[month] = max(0, np.round(logins_per_month[month-1] * decay_factor))
        else:
            # Consistent user
            logins_per_month = np.maximum(0, np.round(np.random.normal(loc=consistent_logins_mean, scale=consistent_logins_std, size=12)))
        
        # Calculate continuous churn score
        average_logins = np.mean(logins_per_month)
        decline_rate = (logins_per_month[0] - logins_per_month[-1]) / (logins_per_month[0] + 1)  # Normalize to avoid division by zero
        raw_churn_score = 0.5 * (1 - (average_logins / initial_logins_mean)) + 0.5 * decline_rate
        
        # Normalize and scale churn score to range [0, 100]
        churn_score = int(np.clip(raw_churn_score, 0, 1) * 100)
        
        user_data = {
            'account_id': account_id,
            'user_id': global_user_id,
            **{f'logins_month_{i+1}': int(logins_per_month[i]) for i in range(12)},
            'churn_score': churn_score,
        }
        data.append(user_data)
        global_user_id += 1

df = pd.DataFrame(data)

df.to_csv('customer_logins_data.csv', index=False)

# Calculate total logins for weighted average
df['total_logins'] = df[[f'logins_month_{i+1}' for i in range(12)]].sum(axis=1)
df['weighted_churn_score'] = df['churn_score'] * df['total_logins']

# Account-level churn score using different methods
account_churn_scores = df.groupby('account_id').agg(
    average_churn_score=('churn_score', 'mean'),
    median_churn_score=('churn_score', 'median'),
    weighted_average_churn_score=('weighted_churn_score', lambda x: x.sum() / df.loc[x.index, 'total_logins'].sum()),
    max_churn_score=('churn_score', 'max'),
    min_churn_score=('churn_score', 'min')
)

account_churn_scores = account_churn_scores.round(2)

account_churn_scores.to_csv('account_level_churn_scores.csv', index=True)