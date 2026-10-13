

## A. Pattern

1. State the intent of Adapter in plain language. What problem appears when business code speaks a vendor or legacy protocol (odd field names, units, XML, status codes) directly?

> [!NOTE]
> ***Your Answer***
>
> _(Adapter translates a weird or external interface into a clean format your application already expects. If your business code talks directly to vendor formats (like weird payload keys or strange units), your main code gets cluttered with vendor details. Every time a vendor changes their API, your core business logic breaks.)_

2. Name the participants (**target / port**, **adaptee**, **adapter**, **client**). What does the adapter translate, and what must it **not** decide (business policy)?

> [!NOTE]
> ***Your Answer***
>
> _(Target / Port: The clean interface your app expects (e.g., SensorPort). Adaptee: The raw external data source or vendor payload. Adapter: The middleman class that converts raw data into the clean format. Client: The service asking for data without caring where it comes from. What it translates: Raw fields, units, and data structures into a clean domain object (like Reading). What it must NOT decide: Any business rules or decisions (like deciding when to turn on a water pump).)_

3. GoF distinguishes an **object adapter** (composition) from a **class adapter** (inheritance). Which does modern code prefer, and why?

> [!NOTE]
> ***Your Answer***
>
> _(Modern code prefers the object adapter. Why: Holding an instance of an object inside a class is much more flexible than hard-coupling classes together through multiple inheritance. It keeps code cleaner and easier to test or swap out later.)_

## B. This phase of the application

4. What is `SensorPort` in this lab, and what normalized value type (for example `Reading`) do adapters return? Why do application services depend on the port rather than on a simulation driver or vendor SDK?

> [!NOTE]
> ***Your Answer***
>
> _(SensorPort: An abstract interface that defines a standard read() action. Returned Value: A clean reading object with standard fields device_id etc. Why depend on the port. So application services don't care if data comes from a mock simulator or a physical vendor device. You can swap device drivers anytime without modifying your application logic.)_

5. You need three translations onto the same normalized reading: a simulation adapter, a vendor stub, and an MQTT translator that accepts a payload dict. Why is the different raw shape the point of the exercise? How does `source` (simulation, vendor, or mqtt) show which adapter produced the reading, and why must the MQTT translator not open a broker in this phase? Phase 12 may deliver that same dict on a device HTTP route or through an optional broker — why must this phase still not open either transport?

> [!NOTE]
> ***Your Answer***
>
> _(Why different raw shapes: The whole purpose of an Adapter is showing how different raw data formats get converted into one uniform domain format. Role of source: It acts as a clear tag ("simulation", "vendor", or "mqtt") in the database telling you which adapter converted that reading. Why no broker or transport now: Adapters only care about data translation, not network communication. Opening socket connections or brokers in Phase 5 mixes networking concerns into data mapping and makes tests unnecessarily complex.)_

6. Readings are **appended** to `sensor_readings` (history grows). Why not keep only the latest value in memory or overwrite a single row, and which later phase consumes this history? Why do a manual read, the simulation sampler, and (later) MQTT share **one** writer of that table? Why does the sampler skip devices with tracking off and MQTT devices, and why do sensor cards poll the latest stored reading until Phase 12?

> [!NOTE]
> ***Your Answer***
>
> _(Why append history: Overwriting rows destroys past telemetry needed for trends and automated triggers. Later phases (like Phase 6 Strategy) use this historical data to make smart irrigation decisions. Why share one writer (ReadingIngest): Having one central service write to sensor_readings keeps data formatting, database interactions, and timestamp handling completely consistent. Why sampler skips them: Disabled devices shouldn't generate fake logs, and MQTT devices push their own data instead of being polled locally. Why frontend polls: Until WebSockets are added in Phase 12, polling GET .../readings is the simplest way for sensor cards to show new DB rows without manual page refreshes.)_

7. `POST /api/sensors/{id}/read` runs an adapter, persists, and returns a DTO. What HTTP status is appropriate when the device is missing versus when the adapter fails? Why must the router never see vendor-shaped types?

> [!NOTE]
> ***Your Answer***
>
> _(HTTP Statuses: 404 Not Found if the device ID doesn't exist; 400 Bad Request if adapter translation or validation fails. Why router stays clean: Web routers handle HTTP inputs and outputs. Exposing vendor-specific raw payloads inside the router leaks internal driver details into your web layer.)_

## C. Compare, contrast, and scenarios

8. Contrast Adapter with **Facade**. Adapter changes the **shape** of an existing interface; Facade simplifies **how to use** a subsystem. Give a greenhouse-shaped example of each (Adapter this phase; Facade in Phase 7).

> [!NOTE]
> ***Your Answer***
>
> _(Adapter (Phase 5): Takes raw, incompatible vendor telemetry payloads and converts them into a uniform Reading object so the system can read them easily. Facade (Phase 7): Provides a single high-level endpoint or helper function to summarize dashboard metrics, hiding a multi-step query process across locations, zones, and devices behind one easy call.)_

9. Contrast Adapter with **Decorator**. Both wrap an object. What is different about the interface they present to the client?

> [!NOTE]
> ***Your Answer***
>
> _(Adapter: Changes the interface into something completely different so incompatible classes can talk to each other. Decorator: Keeps the exact same interface, adding new functionality (like logging or retry logic) while wrapping around the original object.)_

10. A classmate puts irrigation policy (“if moisture < 0.3 then water”) inside the vendor adapter. Why is that a trap? Where should that decision live instead (later Strategy), and what should stay in the adapter?

> [!NOTE]
> ***Your Answer***
>
> _(Why it's a trap: Adapters should only translate raw data format, not make decision rules. Putting watering rules inside an adapter forces you to duplicate irrigation logic across every vendor driver you write. Where it belongs: Decision logic belongs in an application service or domain strategy (Phase 6 Strategy). What stays in the adapter: Pure translation, taking raw sensor readings and returning a clean, normalised Reading.)_