import paho.mqtt.client as mqtt
import time

# Function to read broker info from a file
def read_broker_info(file_path):
    broker_info = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            broker_info[key] = value
    return broker_info

# Read broker info from the txt file
broker_info = read_broker_info('mqttbroker.txt')

# Dictionary to store topics
topics = {}

# Callback when a message is received
def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode('utf-8')
    print(f"Received message on topic '{topic}': {payload}")
    
    if topic not in topics:
        topics[topic] = 1
    else:
        topics[topic] += 1

# Create an MQTT client instance
client = mqtt.Client()

# Assign the on_message callback function
client.on_message = on_message

# Set username and password for the MQTT broker
client.username_pw_set(broker_info['username'], broker_info['password'])

# Connect to the MQTT broker using info from the txt file
client.connect(broker_info['broker_address'], int(broker_info['port']), int(broker_info['keepalive']))

client.publish("/status","topic checker starting")
# Subscribe to all topics
client.subscribe("#")

# Start the MQTT client loop in a separate thread
client.loop_start()

# Wait for 10 seconds to collect topics
time.sleep(10)

# Stop the MQTT client loop
client.loop_stop()

# Print all topics that were used in the last 10 seconds
print("Topics used in the last 10 seconds:")
for topic in topics:
    print(topic)
if len(topics) == 0:
    print("no topics found")
# Disconnect from the broker
client.disconnect()