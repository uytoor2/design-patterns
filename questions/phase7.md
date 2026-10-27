# Phase 7 — Facade questions


## A. Pattern

1. State the intent of Facade in plain language. What problem appears when every HTTP handler (or every UI screen) repeats the same multi-step dance across repositories and services?

> [!NOTE]
> **_Your Answer_**
>
> _(Facade gives you one simple place to call a big complex system, if every HTTP handler or UI screen repeats the same steps to get data from many places, the code gets messy, duplicated, and hard to fix when things change.)_

2. A facade **orchestrates** collaborators. What should it **not** become (a god object that owns all domain logic)? Where should irrigation policy, sensor translation, and persistence stay instead?

> [!NOTE]
> **_Your Answer_**
>
> _(A facade should not become a giant god object that does all the work, irrigation policy stays in strategy, sensor translation stays in adapter, and persistence stays in repositories.)_

3. When should you use Facade, and when should you skip it (a single repository call is enough; or you actually need to **translate** a mismatched interface)?

> [!NOTE]
> **_Your Answer_**
>
> _(You use Facade when you need to talk to many repositories and services at once to get a summary, you skip it if you only need data from one repository, or if you need to convert an ugly payload shape which is the job for an adapter.)_

## B. This phase of the application

4. What does `GET /api/locations/{location_id}/overview` return? Name the main pieces of the overview DTO: location, assigned device counts, and `zones` (thresholds, assigned devices, and those devices’ latest readings, including `tracking_enabled` and `sampling_interval_seconds`), plus strategy key and last recommendation. Why may those reading rows come from the sampler or MQTT ingest, not only from `POST /read`? Why is overview scoped by `location_id`?

> [!NOTE]
> **_Your Answer_**
>
> _(It returns one big overview DTO with location info, counts of assigned sensors and actuators, zone list with thresholds, assigned devices, and latest readings, plus strategy key and last recommendation, reading rows come from any source like the sampler or MQTT because all readings go into sensor readings table, overview uses location id because everything in the site belongs to a location.)_

5. Why does this phase **not** require a new business table? What already exists from Phases 2–6 that the facade only **composes**?

> [!NOTE]
> **_Your Answer_**
>
> _(No new table is needed because we already saved locations, zones, devices, sensor readings, and automation rules in past phases, the facade just reads and combines data that is already in the database.)_

6. The overview HTTP handler should call **only** the facade, not reading/strategy/device repositories directly. Why? How does that help tests and later changes to the query shape?

> [!NOTE]
> **_Your Answer_**
>
> _(The handler calls only the facade so the web layer stays clean, it makes testing easy because you only mock the facade, and changing database queries later will not break the router code.)_

7. The location selector may use the existing locations list. The Overview cards come from **one** overview fetch, and Refresh repeats that same fetch. Why must the React page not stitch device, reading, and automation calls together to build the same snapshot? How does a new reading or a saved strategy show up on overview without extra frontend glue?

> [!NOTE]
> **_Your Answer_**
>
> _(The frontend should not mix different API calls because that makes React code complicated and slow, fetching the overview endpoint gets the newest database data in one go, so new readings or strategy changes show up automatically on refresh.)_

## C. Compare, contrast, and scenarios

8. Contrast Facade with **Adapter**. One makes an existing interface usable; the other makes a subsystem simpler to call. Which is which, and how do both appear in this greenhouse app (Phase 5 vs Phase 7)?

> [!NOTE]
> **_Your Answer_**
>
> _(Adapter turns a weird payload into a clean format like converting raw sensor data in Phase 5, Facade combines many backend services into one simple endpoint like the overview call in Phase 7.)_

9. This phase mentions **N+1** queries. What is an N+1 problem in an overview that lists latest readings for many devices, and what can the facade (or its repository) do about it without putting SQL in the router?

> [!NOTE]
> **_Your Answer_**
>
> _(N+1 happens when the database runs a separate query for every device inside a loop, the facade repository fixes this by using one JOIN or subquery to fetch all latest readings for all devices in a single database call.)_

10. A classmate hides every error behind a generic “overview failed,” so a missing location, a DB outage, and a strategy error look the same. Why is that a trap for a facade?

> [!NOTE]
> **_Your Answer_**
>
> _(Hiding all errors makes debugging impossible for developers and hides real issues from users, a missing location should give a 404 error, while database or strategy bugs should give proper error messages so you know what broke.)_