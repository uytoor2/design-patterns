# Builder Pattern — Location Configuration

## Problem
Creating a `LocationConfig` requires assembling a `Location` with multiple `Zone` children. Validating business constraints (non-empty names, non-empty zone lists, and strictly ordered thresholds) across multiple components before persistence is complex and error-prone.

## Solution
We implemented `LocationConfigBuilder` to construct `LocationConfig` aggregates step-by-step. The `.build()` method acts as a transactional validation gate that verifies all constraints and returns an immutable `LocationConfig` domain entity or raises a `ConfigurationError`.

## Pattern Comparisons
* **Factory Method:** Answers *which single product type* to instantiate.
* **Abstract Factory:** Answers *which family of matching products* to construct.
* **Builder:** Answers *how to assemble a complex, multi-part object step-by-step with validation*.

## Design Decisions
* **Separation of Concerns:** Devices are not attached during builder execution because a `Zone` row has no database ID until saved. Device assignment is handled post-persist by `ZoneAssignmentService`.
* **Naming Consistency:** Used `location_id` exclusively across schema and endpoints to prevent domain model synonyms.