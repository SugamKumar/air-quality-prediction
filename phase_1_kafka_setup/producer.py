import time
import json
import pandas as pd
from kafka import KafkaProducer

def clean_and_split_data():
    # Load data with proper datetime handling
    df = pd.read_csv("AirQualityUCI.csv", 
                     delimiter=';', 
                     decimal=',', 
                     na_values=-200)
    
    # Clean dataset
    df.drop(['Unnamed: 15', 'Unnamed: 16'], axis=1, inplace=True)
    df.dropna(inplace=True)
    
    # Combine date and time columns manually
    df['Time'] = df['Time'].str.replace('.', ':')
    df['Date_Time'] = pd.to_datetime(
        df['Date'] + ' ' + df['Time'], 
        format='%d/%m/%Y %H:%M:%S'
    )
    df = df.drop(['Date', 'Time'], axis=1)
    df = df.set_index('Date_Time').sort_index()
    
    # Feature engineering
    df['hour'] = df.index.hour
    df['day_of_week'] = df.index.dayofweek
    df['month'] = df.index.month
    
    # Chronological split (80-20)
    split_idx = int(len(df) * 0.8)
    test_data = df.iloc[split_idx:][['hour', 'day_of_week', 'month', 'CO(GT)']]
    return test_data

def main():
    # Get test data
    test_data = clean_and_split_data()
    
    # Create Kafka producer
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')  # JSON serialization
    )
    
    # Send test data
    for idx, row in test_data.iterrows():
        # Create message with features and actual value
        message = {
            "hour": int(row['hour']),
            "day_of_week": int(row['day_of_week']),
            "month": int(row['month']),
            "CO_GT": float(row['CO(GT)'])
        }
        
        # Send to Kafka topic
        producer.send('air-quality', message)
        print(f"Sent: {message}")
        
        # Simulate hourly data (1 second delay for demo purposes)
        time.sleep(1)
    
    producer.flush()

if __name__ == "__main__":
    main()
