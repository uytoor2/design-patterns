# Phase 6 — Strategy questions

**Pattern / focus:** Strategy.

**Read first:** [Guide 06](../../materials/guides/06-strategy.md) · [Requirements](requirements.md)

## How to answer

- Use your own wording. Do not paste teaching-example types (for example shipping quotes) as if they were your greenhouse classes.
- When a question asks about *this application*, refer to irrigation (or lighting) policies, location context, and the automation API from the lab.
- Short answers are fine when the question is narrow. Write a few sentences when it asks you to explain or compare.
- Write each answer inside the matching **Your Answer** note. Replace the placeholder; leave the question text unchanged.

## A. Pattern

1. State the intent of Strategy in plain language. How does the **context** use a strategy, and why must “choose which algorithm” stay separate from “run the algorithm”?

> [!NOTE]
> ***Your Answer***
>
> _(Strategy lets you define a family of algorithms, put each one in its own class, and swap them out at runtime without breaking the rest of the application. The context holds the input data and calls the decide method on the active strategy interface. Keeping algorithm selection separate from execution keeps configuration logic away from calculation logic, making algorithms easier to test and extend..)_

2. Name the participants (**strategy**, **concrete strategies**, **context**, **client**). What goes wrong when all policies live as `if/elif` inside the context (or inside an HTTP router)?

> [!NOTE]
> ***Your Answer***
>
> _(The participants are strategy, concrete strategies, context, and client. Strategy is the common interface defining the decision contract. Concrete strategies are the actual algorithms like conservative or aggressive. Context is the plain object carrying moisture and zone thresholds. Client is the service that selects the strategy and triggers evaluation. If all policies live as if/elif blocks, the router or context becomes a bloated monolith that forces you to modify existing code whenever a new rule is added, risking bugs across all rules.)_

3. When should you use Strategy, and when should you skip it (one algorithm only; or the variation is a **lifecycle mode** rather than a chosen policy)?

> [!NOTE]
> ***Your Answer***
>
> _(Use Strategy when you have multiple interchangeable business rules that users or locations can choose between. Skip it if there is only ever one fixed calculation, or if behavior changes automatically based on internal system lifecycle transitions, which is better handled by the State pattern.)_

## B. This phase of the application

4. In this lab, what does a strategy’s `decide(context)` return (action + reason)? Give a concrete difference you implemented (or were required to implement) between **conservative** and **aggressive** on the **same** moisture reading and zone thresholds.

> [!NOTE]
> ***Your Answer***
>
> _(It returns a Recommendation object containing an overall action, a summary reason, and individual zone details. Given a zone with thresholds 0.20 to 0.60 VWC and a reading of 0.35 VWC, the conservative strategy returns wait because moisture is above the low threshold of 0.20 VWC. The aggressive strategy returns irrigate on the exact same context because moisture is below the target midpoint of 0.40 VWC.)_

5. Where do the numbers in `LocationAutomationContext` (or your equivalent) come from? Latest moisture may already be in `sensor_readings` from a manual read, the simulation sampler, or MQTT translation — why does this phase not add a scheduler or a broker? Why must strategies receive a plain context object, not SQLAlchemy rows or FastAPI types? Why are thresholds read from **zones**, not hardcoded in the strategy class?

> [!NOTE]
> ***Your Answer***
>
> _(Latest moisture values are loaded from sensor_readings and threshold boundaries are loaded from zones. This phase focuses purely on algorithmic decision-making, so adding background schedulers or brokers now would confuse network transport with domain logic. Strategies receive plain context objects to keep them in the pure domain layer, making them lightweight and easy to unit test without database or web framework dependencies. Thresholds come from zones because every zone has unique plant requirements, and hardcoding numbers breaks flexibility.)_

6. The active `strategy_key` is **persisted** per `location_id` (for example in `automation_rules`). Why must `POST .../automation/evaluate` use the **saved** key rather than a key the client sends only in that request? What happens on the next evaluate after the operator changes strategy but moisture stays the same?

> [!NOTE]
> ***Your Answer***
>
> _(Automation is an ongoing site setting, so evaluation must reflect the actual configured policy saved in the database for that location. If the operator switches the saved strategy from conservative to aggressive, the next evaluation can return irrigate instead of wait even if the moisture level has not changed at all.)_

7. Strategy **recommends** (irrigate / wait). It should not itself start a pump. Why keep **decide** separate from **execute**? Which later pattern is meant to carry out the action?

> [!NOTE]
> ***Your Answer***
>
> _(Decision-making should be a pure calculation with no unexpected side effects like triggering hardware. Keeping decide separate from execute allows safely running evaluations, previews, or dry-runs without turning on real physical pumps. The Command and Observer patterns in later phases will carry out the actual execution..)_

## C. Compare, contrast, and scenarios

8. Contrast Strategy with **State** (Phase 8). Both delegate to an object with the same shape. Who typically **changes** the active object, and is the variation a **policy** or a **lifecycle**?

> [!NOTE]
> ***Your Answer***
>
> _(In Strategy, the client or user explicitly chooses and assigns the policy, such as selecting conservative in settings, making it a chosen policy. In State, the state object itself typically triggers transitions automatically based on events, making it a representation of a lifecycle.)_

9. Contrast Strategy with **Adapter** (Phase 5) and with **Builder** (Phase 4). Which one translates a foreign API, which one assembles a valid aggregate, and which one swaps an algorithm?

> [!NOTE]
> ***Your Answer***
>
> _(Adapter translates an incompatible external payload or API into a clean domain format. Builder assembles a complex, multi-step aggregate object with validation. Strategy swaps out an algorithm or decision rule dynamically behind a common interface.)_

10. A classmate writes one “mega-strategy” that still contains `if conservative` / `if aggressive` inside a single class. Another strategy class calls the actuator adapter to water immediately. Explain why each is a trap.

> [!NOTE]
> ***Your Answer***
>
> _(The mega-strategy trap defeats the purpose of the Strategy pattern by recreating conditional spaghetti inside a single class, violating the Single Responsibility and Open/Closed Principles. The direct execution trap mixes calculation logic with side-effects, making the strategy impossible to test or preview safely without firing real hardware commands.)_
