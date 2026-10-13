# Strategy Pattern — Automation & Irrigation Policies

## Problem
Different greenhouses require different irrigation policies (e.g., conservative water usage vs. aggressive moisture maintenance). Hardcoding `if strategy == "conservative"` across HTTP endpoints creates rigid, unmaintainable code.

## Solution
We implemented the `AutomationStrategy` interface with polymorphic concrete implementations (`ConservativeMoistureStrategy` and `AggressiveMoistureStrategy`). The active strategy key is saved per location in `automation_rules`. At evaluation time, `AutomationService` dynamically loads the context and delegates the decision to the matching strategy instance.

## Key Architectural Highlights
* **Zero ORM Leakage:** `AutomationStrategy` operates exclusively on pure domain objects (`LocationAutomationContext`).
* **Interchangeability:** Adding a third strategy (e.g., `TimeBasedScheduleStrategy`) requires only extending `AutomationStrategy` and adding it to the factory dictionary.