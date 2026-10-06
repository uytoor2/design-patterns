# Adapter Pattern

## Problem
Incompatible payload representations across simulation generators, proprietary vendor SDKs, and incoming MQTT JSON feeds force application code to handle conditional logic per protocol.

## Solution
We implemented SensorPort and ActuatorPort abstract interfaces. Concrete adapters (SimulationSensorAdapter, VendorStubSensorAdapter, MqttSensorAdapter, and SimulationActuatorAdapter) translate external or generated formats into unified domain Reading objects before writing to ensor_readings.

## Key Benefits
Clean Architecture: Domain and application services interact solely with ports, unaware of underlying hardware drivers or transport mechanisms.
guarantees consistent persistence and formatting across all sensor data feeds.