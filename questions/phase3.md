

## A. Pattern

1. State the intent of Abstract Factory in plain language. What goes wrong when related products are chosen independently (for example for each piece) instead of as a **family**?

> [!NOTE]
> ***Your Answer***
>
> _(Abstract Factory provides an interface for creating a family of related products without specifying their concrete classes. If products are chosen independently without creating a family, it can cause incompatibility bugs and make the code break at runtime.)_

2. Name the main participants (**abstract factory**, **concrete factory**, **abstract products**, **concrete products**, **client**). How does choosing a factory at the start **commit** the client to one family?

> [!NOTE]
> ***Your Answer***
>
> _(Abstract Factory: The interface with information on what products can be made. Concrete Factory: The real factory that makes products for one specific family. Abstract Products: The common interface for the items being created, like Sensor or Actuator. Concrete Products: The actual products built for that specific setup, like SimulationSensor or EdgeSensor. Client: The code asking for products to be created. We give the client a specific factory when the app starts up, and since the client asks that factory for products, every item created belongs to that same family.)_

3. When should you use Abstract Factory, and when should you skip it (for example only one product type per request, or mixing siblings is valid)?

> [!NOTE]
> ***Your Answer***
>
> _(We should use Abstract Factory when the app needs multiple matching products of the same family created together. We should skip it when we only need to make one standalone product at a time or if mixing and matching components is valid.)_

## B. This phase of the application

4. In this lab, what is a **device family**, and what does `create_device_set()` (or your equivalent) return? Why must a simulation kit and an edge kit not mix incompatible siblings?

> [!NOTE]
> ***Your Answer***
>
> _(A device family is the product family of the Abstract Factory we implemented (simulation vs edge). `create_device_set()` returns a kit of matching products, like two sensors and two actuators. It should not mix incompatible siblings because real physical devices and software mocks expect different protocols, and mixing them causes system crashes or communication errors.)_

5. Phase 2 Factory Method creators still exist. How does Abstract Factory **compose** them rather than replace them? What would you lose if you deleted the sensor creators and inlined all construction inside the family factory?

> [!NOTE]
> ***Your Answer***
>
> _(They exist because they are used by the Abstract Factory behind the scenes to create individual items. Deleting them and inlining all logic inside one family factory creates a bloated monolith. You lose modularity and maintainability because you would have to modify the main family factory every time a new device type is added instead of simply adding a new creator class.)_

6. Why add a `device_family` column on the existing `devices` table (with a default/backfill such as `"simulation"`) instead of a new table per family? What happens to Phase 2 sensor rows if you forget the backfill?

> [!NOTE]
> ***Your Answer***
>
> _(All devices share the same core properties like ID, name, and status, so adding one column keeps the database schema clean and avoids cluttering it with duplicate tables. Without backfill, existing Phase 2 sensor rows will have NULL values in that column, causing queries that filter or group by family to throw errors or skip older records.)_

7. `POST /api/devices/provision` returns a kit (expected size: two sensors and two actuators). `GET /api/devices` can filter by `family` and `role`. Why must the UI be able to filter by family? Why do `/api/sensors` routes from Phase 2 still need to work?

> [!NOTE]
> ***Your Answer***
>
> _(The UI must be able to filter by family so operators can separate virtual test/simulation devices from real live hardware, preventing test actions on physical equipment. Legacy `/api/sensors` routes from Phase 2 still need to work for backward compatibility and simple tasks where clients need to query or manage single sensors directly without dealing with an entire kit.)_

## C. Compare, contrast, and scenarios

8. Draw the contrast in one paragraph: Factory Method vs Abstract Factory. Use the questions “which **one** product?” versus “which product **line**?” and mention that Abstract Factory often **uses** Factory Method–style methods inside.

> [!NOTE]
> ***Your Answer***
>
> _(Factory Method answers the question, "Which one specific product should be created?", letting subclasses handle the instantiation of a single concrete product. Abstract Factory answers the question, "Which entire product line am I using?", providing a kit builder for a whole set of matching products. In fact, Abstract Factories often use Factory Method-style methods inside to handle the creation of each individual item in that kit.)_

9. A DTO or HTTP handler constructs concrete simulation/edge device types directly, bypassing the family factory. What consistency bug can that reintroduce? How should HTTP stay on the abstract factory / service instead?

> [!NOTE]
> ***Your Answer***
>
> _(It reintroduces human error, where a developer might accidentally pair incompatible types, like a simulation actuator with an edge sensor. HTTP should stay abstract by accepting a simple string parameter like "simulation" or "edge" and passing it to a service layer that selects the appropriate factory to build the kit, keeping the HTTP layer clean and decoupled.)_

10. Someone proposes a single “god factory” that creates locations, readings, and devices “because we already have a factory.” Why is that a misuse of Abstract Factory?

> [!NOTE]
> ***Your Answer***
>
> _(Locations, sensor readings, and hardware devices belong to completely different domain contexts with different lifecycles. Abstract Factory is meant for pieces that belong together in a single co-varying family, not as a dumping ground for every object in the application. Combining them creates an unmanageable mess and breaks the Single Responsibility Principle.)_