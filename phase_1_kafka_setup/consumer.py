from kafka import KafkaConsumer
import pandas as pd
import json
import joblib

def main():
    # Load pre-trained model (Linear Regression)
    model = joblib.load('linear_regression.joblib')
    
    # Create Kafka consumer
    consumer = KafkaConsumer(
        'air-quality',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # JSON deserialization
    )
    
    print("Listening for messages...")
    
    try:
        for message in consumer:
            # Parse message
            data = message.value
            
            # Extract features and create DataFrame for prediction
            input_df = pd.DataFrame([{
                "hour": data["hour"],
                "day_of_week": data["day_of_week"],
                "month": data["month"]
            }])
            
            # Make prediction using the pre-trained model
            prediction = model.predict(input_df)[0]
            
            print(f"Actual CO: {data['CO_GT']:.2f} | Predicted CO: {prediction:.2f}")
            
    except KeyboardInterrupt:
        print("Stopping consumer...")

if __name__ == "__main__":
    main()
