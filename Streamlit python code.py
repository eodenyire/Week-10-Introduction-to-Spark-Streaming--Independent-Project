# Importing the necessary libraries
from confluent_kafka import Consumer, KafkaError, KafkaException
import pandas as pd
import streamlit as st

# Configure Kafka consumer
bootstrap_servers = 'pkc-lzvrd.us-west4.gcp.confluent.cloud:9092'
sasl_username = 'ATT27BW7IKWVVS7C'
sasl_password = 'N+mQd+xm1CRv4GhKgoMTWpAXISNzLudR0w+VW/SACm7AW6JSjntN1Fgz0nwSKaA8'
topic_name = 'processed-data'

conf = {
  'bootstrap.servers': bootstrap_servers,
  'security.protocol': 'SASL_SSL',
  'sasl.mechanisms': 'PLAIN',
  'sasl.username': sasl_username,
  'sasl.password': sasl_password,
  'group.id': 'my-consumer-group',  # Specify a unique consumer group ID
  'auto.offset.reset':
  'earliest'  # Start consuming from the beginning of the topic
}

consumer = Consumer(conf)
consumer.subscribe([topic_name])

# Creating an empty pandas DataFrame to hold the processed data
processed_df = pd.DataFrame(
  columns=['timestamp', 'source_ip', 'total_bytes_sent'])

# Reading data from Kafka topic
try:
  while True:
    messages = consumer.consume(num_messages=100, timeout=60.0)
    if messages is None:
      continue

    for message in messages:
      if message is None:
        continue

      if message.error():
        raise KafkaException(message.error())

      value = message.value().decode('utf-8')
      #print(f"Received message: {value}")

      # Process the received message and update the pandas DataFrame
      processed_data = [(value.split(',')[0], value.split(',')[1],
                         value.split(',')[2])]
      processed_data_df = pd.DataFrame(
        processed_data, columns=['timestamp', 'source_ip', 'total_bytes_sent'])
      #processed_df = processed_df.append(processed_data_df)
      processed_df = pd.concat([processed_df, processed_data_df])

      # Perform any further operations on the processed DataFrame
      # For example, you can create visualizations using Streamlit

except (KeyboardInterrupt, KafkaException) as e:
  print(f"Error occurred: {e}")

finally:
  consumer.close()

# Using Streamlit to create visualizations
st.title('Processed Data Visualization')
st.bar_chart(processed_df['total_bytes_sent'])
