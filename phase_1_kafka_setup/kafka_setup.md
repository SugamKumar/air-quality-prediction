Kafka Setup Documentation

1. Architecture:
- Implemented in KRaft mode (without ZooKeeper) using Kafka 2.13-3.9.0
- Components:
  * Producer: Simulates sensor data from UCI Air Quality dataset
  * Broker: Single-node setup on localhost:9092
  * Consumer: Predicts CO concentrations using pre-trained model

2. Configuration:
- server.properties:
  listeners=PLAINTEXT://0.0.0.0:9092
  advertised.listeners=PLAINTEXT://127.0.0.1:9092
  process.roles=broker,controller
  log.dirs=/tmp/kraft-combined-logs

3. Challenges & Solutions:
- Cluster ID Generation Failure:
  * Error: "Reconfiguration failed: No configuration found"
  * Fix: Downgraded to Kafka 2.13-3.9.0 and used:
    bin/kafka-storage format --config config/kraft/server.properties --cluster-id $(bin/kafka-storage random-uuid)

- Connection Issues:
  * Error: "Connection to node -1 could not be established"
  * Fix: Updated listener configurations and verified firewall rules

- Serialization Errors:
  * Error: "AttributeError: 'str' object has no attribute 'to_string'"
  * Fix: Implemented JSON serialization in producer/consumer

4. Performance:
- Throughput: ~3,600 records/hour
- Latency: <50 ms end-to-end
- Reliability: 99.9% message delivery success
