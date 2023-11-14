import json

def calculate_weekly_retention(data):
    retention_dict = {}
    
    # Loop through each date and its corresponding values
    for date, values in data['session_end']['data']['series'][0]['values'].items():
        weekly_retention = []
        
        # Calculate retention rate for each interval (assuming 7-day intervals for weekly retention)
        for week_data in values[:7]:
            count = week_data['count']
            outof = week_data['outof']
            incomplete = week_data['incomplete']
            
            if not incomplete:
                retention_rate = (count / outof) * 100 if outof != 0 else 0
                weekly_retention.append(round(retention_rate, 2))
        
        retention_dict[date] = weekly_retention

    return retention_dict

file_path = 'retention_data_NOTIFICATION_TAP_20230901_20230930.json'

# Read the JSON file
with open(file_path, 'r') as f:
    data = json.load(f)
    weekly_retention_rates = calculate_weekly_retention(data)
    print(weekly_retention_rates)

# Calculate weekly retention rates
