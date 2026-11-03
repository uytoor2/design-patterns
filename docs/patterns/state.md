# State Pattern — Actuator Lifecycle

## What Problem Did We Have?
Actuators (like water pumps or lights) go through different stages in real life:
- `off`
- `idle` (on, but waiting)
- `running` (currently working)
- `error` (something broke)
- `maintenance` (being fixed)

If we let the system jump between any stage randomly, bad things could happen. For example, turning a pump into `maintenance` mode while it is still `running` could cause physical damage or safety hazards.

## How Did State Fix It?
We created a rules engine that protects how an actuator changes its stage.

Each stage knows:
1. Which new stages it is safely allowed to switch to.
2. Which buttons or commands make sense right now (for example, showing a "stop pump" button only when the pump is actually running).

If someone tries to force an illegal change (like going straight from `running` to `maintenance`), the system blocks it and returns an error before saving anything to the database.

## Key Design Details
- **Safe Rules:** The domain code enforces all transition rules. The web layer or front-end cannot bypass them.
- **Saved in Database:** The state is saved in the `actuator_states` table, so if the server restarts, the pump remembers its current stage.
- **Smart Commands:** The system automatically sends a list of `allowed_commands` back to the UI so it only shows buttons that actually make sense for the current stage.