

## A. Pattern

1. State the intent of Builder in plain language. Why does construction of a complex object need **stepwise assembly** and **validation at the end** (`build()`), instead of a telescoping constructor or a half-filled dict written straight to the database?

> [!NOTE]
> ***Your Answer***
>
> _(The intent is to build a complex object step-by-step and make sure it is completely valid before using it. Long constructors with too many parameters are confusing and can cause errors. A half-filled dict written to the database causes corrupted data and runtime crashes. `build()` acts as a single guard that checks everything at the end so broken data never gets saved.)_

2. Name the main participants (**product**, **builder**, **optional director**, **client**). Until `build()` succeeds, is the intermediate object a finished domain product? Why does that distinction matter?

> [!NOTE]
> ***Your Answer***
>
> _(Product: It is the final, valid object e.g., LocationConfig. Builder: The helper class that collects parts and validates them. Director: Code that controls the build steps in a set order. Client: The code or API service asking to build the product. No, it is not a finished product. It matters because the builder holds incomplete data. Treating incomplete data as a real product lets invalid state leak into your database or business logic before it is verified.)_

3. List at least three kinds of invalid configuration a location/zone `build()` should reject in **this** lab (name, zones, moisture thresholds). Why must those rules live in the **domain builder**, not only in the HTTP layer?

> [!NOTE]
> ***Your Answer***
>
> _(Empty or missing location name, zero zones added to the location, and low moisture threshold greater than or equal to high threshold. They should be in the domain builder and not only in HTTP because HTTP validation only protects web requests. If a background job, terminal script, or test creates a location directly, domain-level validation ensures those paths cannot save invalid data either.)_

## B. This phase of the application

4. What aggregate does the builder produce (location plus zones)? Why does this course use `location_id` (and never `greenhouse_id`) as the name for that scope?

> [!NOTE]
> ***Your Answer***
>
> _(It produces LocationConfig. We use location_id because it is a generic and standard naming convention across the dataset, schemas, and APIs.)_

5. Describe the path from API request to persistence: DTO → builder steps → `build()` → repository. What must **not** be persisted if `build()` raises `ConfigurationError` (or equivalent)? Why does assigning a device wait until the zone row exists, and why does the client send only `zone_id`JS?

> [!NOTE]
> ***Your Answer***
>
> _(The API receives a JSON request (DTO) -> the service loops over the DTO data calling builder steps -> `build()` validates everything -> if valid, the repository saves it to PostgreSQL. Nothing must be persisted if `build()` fails. A zone cannot have a database ID until it is saved. The client sends `zone_id` because a device belongs directly to a zone; the server automatically looks up that zone's `location_id` and copies both IDs at once, preventing location/zone mismatches.)_

6. Saving a location and its zones must be **one transaction**. What goes wrong if the location row commits and a later zone insert fails? How does that relate to “no half-built aggregates in the database”?

> [!NOTE]
> ***Your Answer***
>
> _(You end up with a location in the database that has no zones. An aggregate (location + zones) is an all-or-nothing unit. A single database transaction rolls back the whole save if any zone fails, keeping partial or incomplete records out of the database.)_

7. The configuration wizard UI collects fields in steps. How does that UI map to Builder without turning React (or the HTTP handler) into the place that owns domain validation?

> [!NOTE]
> ***Your Answer***
>
> _(The UI collects form inputs step-by-step and sends a plain JSON payload to the API endpoint. The backend handler passes those fields into `LocationConfigBuilder`, letting the domain builder execute the actual validation rules and return errors if anything is invalid.)_

## C. Compare, contrast, and scenarios

8. Contrast Builder with **Factory Method** and with **Abstract Factory**. Which pattern answers “which type?”, which answers “which matching kit?”, and which answers “how do we assemble one **valid whole** in steps?”

> [!NOTE]
> ***Your Answer***
>
> _(Factory Method answers "Which single type/subclass do I create?". Abstract Factory answers "Which matching kit/family of products do I create?". Builder answers "How do we assemble one valid whole in steps?".)_

9. Fluent method chaining (`builder.add_zone(...).build()`) is a coding style. Why is a fluent interface **not** the same thing as the Builder pattern?

> [!NOTE]
> ***Your Answer***
>
> _(Method chaining is just syntax (returning `self` from methods so you can chain them with dots). The Builder pattern is an architectural design that separates step-by-step construction and delayed validation from the final product object. You can build objects without fluent method chaining, and you can write fluent interfaces for non-builder classes.)_

10. A classmate validates thresholds only in FastAPI / Pydantic and leaves `build()` empty. Another mutates builder fields after `build()` while treating the product as immutable. Explain why each is a trap.

> [!NOTE]
> ***Your Answer***
>
> _(Validating only in Pydantic leaves the core domain unprotected. Any code calling the builder outside an HTTP route (like unit tests or background workers) can create invalid objects. Mutating fields after `build()` ruins immutability. Modifying draft state after validation can bypass validation checks and secretly corrupt the product object that was already verified and returned.)_