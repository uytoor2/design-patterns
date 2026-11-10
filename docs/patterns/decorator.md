# Decorator Pattern — Actuator Execution Policies

## Problem
Adding execution policies (such as audit logging and safety run-time limits) directly into `SimulationActuatorAdapter` or HTTP handlers creates tight coupling, violates the Single Responsibility Principle, and clutters routers with nested `if/else` checks.

## Solution
We implemented the Decorator Pattern around the `ActuatorPort` interface. `LoggingActuatorDecorator` and `MaxRunTimeActuatorDecorator` wrap `SimulationActuatorAdapter`. Callers interact exclusively with `ActuatorPort.apply(...)`.
