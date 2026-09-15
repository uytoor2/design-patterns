Problem:
this smart green house application can create different sensor types. it creates moisture sensor and light sensor etc. they have different types, different units, names, sample intervels and configuration. creating these directly in FastAPI route would mix code and it will become larger every time new sensor is introduced. 
Solution:
this application uses create_sensor method with SensorCreator abstraction. each creator creates different sensor with different configurations. get_creator registers a given valuie such as moisture or light and returns the correct creator according to the request.
code paths:
backend/src/domain/sensors/entity.py it defines a simple sensor object
backend/src/domain/sensors/creators.py it has SensorCreator abstraction the creators for sensors and get_creator
backend/src/application/sensors/service.py selection and creation of sensors.
backend/src/infrastructure/persistence/device_repository.py saves sensors data in PostgreSQL devices taable. returns the data with database.
backend/src/interfaces/api/sensors.py it handles the http request and response.
frontend/src/features/sensors/SensorList.tsx calls the rest api, displays the stored sensoras in the dashboard.
Exercise for temperature sensor:
edit backend/src/domain/sensors/creators.py add class for temperature sensorcreator beside other creators. then update the temperature sensor in creator dictionary in get_creator(). 
