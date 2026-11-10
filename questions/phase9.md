## A. Pattern

1. State the intent of Decorator in plain language. Why is stacking wrappers a flexible alternative to a combinatorial explosion of subclasses (`LoggingRetryMaxRuntimeActuator`, …)?

> [!NOTE]
> ***Your Answer***
>
> _(Decorator lets you add new behavior to an object by wrapping it inside another object, stacking wrappers is flexible because you can mix and match small features like logging or max run time without creating a giant list of messy subclasses for every combination.)_

2. Name the participants (**component**, **concrete component**, **decorator**, **concrete decorators**). What interface does every decorator present to the caller, and why must that match the wrapped component?

> [!NOTE]
> ***Your Answer***
>
> _(The component is ActuatorPort interface, concrete component is SimulationActuatorAdapter, decorator is the base wrapper class, concrete decorators are LoggingActuatorDecorator and MaxRunTimeActuatorDecorator, every decorator presents the exact same ActuatorPort interface so the caller does not know it is talking to a wrapper.)_

3. **Order matters.** Using logging and retry (or logging and max-run-time) as an example, explain how wrapping A around B can change what you observe compared with wrapping B around A.

> [!NOTE]
> ***Your Answer***
>
> _(Order changes what gets recorded, if logging is wrapped on the outside it catches every attempt and records when max run time blocks a call, if max run time is wrapped on the outside the logging wrapper on the inside never runs when a call gets blocked.)_

## B. This phase of the application

4. What is `ActuatorPort` here, and which **at least two** decorators did you stack around the real adapter (for example logging and max run-time)? Where is the chain wired (composition root / factory), and why not inside the HTTP router?

> [!NOTE]
> ***Your Answer***
>
> _(ActuatorPort is the main interface for controlling actuators, we stacked LoggingActuatorDecorator and MaxRunTimeActuatorDecorator around SimulationActuatorAdapter, the chain is wired inside the application service, it is not placed inside the HTTP router so web routes stay clean and simple.)_

5. Max run-time can **short-circuit**: the inner adapter is never called. Why must a blocked attempt still produce a row in `actuator_execution_log` with `success=false` and the policy named in `policy_applied`JS?

> [!NOTE]
> ***Your Answer***
>
> _(A blocked attempt must write a row so operators can see that someone tried to run the device, setting success to false with the policy name lets the dashboard log show clearly that max run time stopped the action.)_

6. How does max run-time know the actuator has been running too long (for example `actuator_states.updated_at` from Phase 8)? Why is that data from **State**, not something the decorator should invent as a second lifecycle?

> [!NOTE]
> ***Your Answer***
>
> _(It reads the state and updated_at time saved in the database from Phase 8, it uses State data so there is only one source of truth, creating a second lifecycle inside the decorator would make the code confusing and cause bugs.)_

7. `GET /api/actuators/executions` feeds the dashboard execution log. Why persist attempts in the database instead of only printing to stdout? What should the UI show after a blocked attempt and a refresh?

> [!NOTE]
> ***Your Answer***
>
> _(Attempts are saved in the database so history is kept even if the server restarts, terminal prints disappear easily, after a blocked attempt the UI should show a failed row with the message max run time exceeded when refreshed.)_

## C. Compare, contrast, and scenarios

8. Contrast Decorator with **Adapter**. Both wrap. One **keeps** the interface and **adds** behaviour; the other **changes** the interface and **translates**. Which is which in this greenhouse (Phase 9 vs Phase 5)?

> [!NOTE]
> ***Your Answer***
>
> _(Adapter in Phase 5 changes a strange vendor format into a clean reading format, Decorator in Phase 9 keeps the same ActuatorPort interface and adds extra rules like logging and safety limits.)_

9. Contrast Decorator with **inheritance** of combined policies. How does composition let you add or remove a policy without a new subclass for every combination?

> [!NOTE]
> ***Your Answer***
>
> _(Composition lets you wrap objects together at runtime like building blocks, inheritance forces you to write a new class for every combination, with composition you can add or remove a policy simply by changing wrapper order.)_

10. A classmate’s decorator changes the method signature “a little” (extra required argument, different return type). Another ignores wrap order and cannot explain whether logging runs once per logical call or per inner attempt. Explain why each is a trap.

> [!NOTE]
> ***Your Answer***
>
> _(Changing the method signature breaks the interface so the caller cannot use wrappers interchangeably, ignoring wrap order leads to unpredictable behavior where logs miss blocked calls or record incorrect failure details.)_