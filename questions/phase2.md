

## A. Pattern

1. State the intent of Factory Method in plain language. What problem appears when callers scatter `new` / constructors (or a growing `if type == ...`) across the application?

> [!NOTE]
> ***Your Answer***
>
> _(Factory Method simply separates the logic of creating objects of different types from the code where those objects are used. It provides a special creator that determines how specific object types are created. Without this, using constructors or growing `if/else` logic causes code repetition throughout the application, making it harder to maintain as new object types are introduced.)_

2. Name the main participants of Factory Method (**product**, **concrete product**, **creator**, **concrete creator**, **client**). For each, give one sentence: what it is responsible for.

> [!NOTE]
> ***Your Answer***
>
> _(Product: It is the main abstract interface or type being created, which in this phase is `Sensor`. Concrete Product: The specific implementation created by a creator, such as `MoistureSensor` or `LightSensor`. Creator: The abstract class or interface declaring the creation method, such as `SensorCreator`. Concrete Creator: The specific creation class responsible for instantiating a concrete product, such as `MoistureSensorCreator` or `LightSensorCreator`. Client: The application code that needs a product without deciding or knowing its exact concrete class, such as `SensorService`.)_

3. How do you add a new product variant when creators are polymorphic (new class + registry entry) versus when creation lives in one shared `if/elif` function? Why does that difference matter for extension?

> [!NOTE]
> ***Your Answer***
>
> _(When creators are polymorphic, adding a new variant requires creating a new concrete creator class and registering it in the creators dictionary, keeping each class small, isolated, and clean. In contrast, using a single shared `if/elif` function means modifying existing code that grows with every new type, increasing complexity and risking bugs in existing products. This difference matters because polymorphic creators respect the Open/Closed Principle.)_

## B. This phase of the application

4. In this lab, what is the product and what are the concrete creators? Why must the API handler (or sensor service) go through a creator/registry instead of constructing `MoistureSensor` / `LightSensor` itself?

> [!NOTE]
> ***Your Answer***
>
> _(The product is `Sensor`, and the concrete creators are `MoistureSensorCreator` and `LightSensorCreator`. The API handler or `SensorService` must go through the registry and creators so instantiation is decoupled from the web layer. Constructing concrete sensors directly would require inline conditional blocks that bloat as new device types are added, breaking clean architecture and making unit testing difficult.)_

5. `POST /api/sensors` accepts a short type key such as `"moisture"` or `"light"`, while the stored/returned field is `device_type` (for example `moisture_sensor`). Why are those two fields different? Who decides the stored `device_type` and `default_config`JS?

> [!NOTE]
> ***Your Answer***
>
> _(The request uses a short key like `"moisture"` or `"light"` as an API input parameter for selection, while `device_type` (such as `"moisture_sensor"`) and `default_config` are internal domain properties. The concrete creator for that sensor type decides the stored `device_type` and its initial `default_config` values when instantiating the object.)_

6. Why is there a single `devices` table with `role="sensor"` instead of a dedicated `sensors` table? What later phase does that choice prepare for?

> [!NOTE]
> ***Your Answer***
>
> _(A single `devices` table with `role="sensor"` avoids duplicating common device fields like ID, display name, and config. This choice prepares for Phase 3, where actuators are introduced and stored in the same `devices` table with `role="actuator"`.)_

7. What should happen when the client posts an unknown type? Where should that rejection be decided (registry/service vs router constructing a concrete class anyway)?

> [!NOTE]
> ***Your Answer***
>
> _(An error should be raised and returned as an HTTP 400 Bad Request to the client. This rejection must be decided at the registry or service level when looking up the type key, before any attempt to construct a concrete class occurs.)_

## C. Compare, contrast, and scenarios

8. Contrast Factory Method with a simple factory (one function full of `if type == ...`). When is the simple factory “good enough,” and why does this phase still want polymorphic creators?

> [!NOTE]
> ***Your Answer***
>
> _(A simple factory uses a single function with conditional statements to instantiate objects, which is "good enough" when there are very few fixed types and low expectation of future growth. This phase insists on polymorphic creators because the application is designed to scale with more sensor types and actuators in later phases without modifying existing creator code.)_

9. Contrast Factory Method with Abstract Factory (Phase 3). Factory Method answers which question? Abstract Factory answers which different question? Why is Factory Method enough for Phase 2 sensors?

> [!NOTE]
> ***Your Answer***
>
> _(Factory Method answers "Which single product should be created?" and configures its individual defaults. Abstract Factory answers "Which entire family of related products should be created together?". Factory Method is sufficient for Phase 2 because the system only needs to instantiate individual, standalone sensors.)_

10. A classmate puts SQLAlchemy session commits (or FastAPI request parsing) inside a concrete creator. Why is that a trap? Where should persistence and HTTP stay instead?

> [!NOTE]
> ***Your Answer***
>
> _(Putting database commits or HTTP request parsing inside a concrete creator mixes object instantiation with infrastructure logic. This makes the creator dependent on a database session or web framework, making unit tests difficult. HTTP parsing belongs in the API routers, and database commits belong in the application service or repository layer.)_