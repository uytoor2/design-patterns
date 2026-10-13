

## A. Pattern

1. In your own words, what is a design pattern? What is it **not**?

> [!NOTE]
> ***Your Answer***
>
> _(A design pattern is a reusable, proven solution for a recurring architectural or design problem. It provides a common template or logical approach for solving similar problems across different applications. A design pattern is NOT copy-paste code or a fixed library implementation; it must be adapted thoughtfully to fit the specific context of the problem.)_

2. Name the three GoF pattern families. For each family, give one sentence: what kind of design problem it addresses. Then place **Factory Method** and **Strategy** into the correct family.

> [!NOTE]
> ***Your Answer***
>
> _(Creational Patterns: Address object creation mechanisms to make code dynamic, flexible, and decoupled from direct class instantiation. Structural Patterns: Address how classes and objects are composed to form larger, scalable structures and interfaces. Behavioral Patterns: Address how objects communicate, assign responsibilities, and distribute algorithms among each other. Factory Method belongs to the Creational family, and Strategy belongs to the Behavioral family.)_

3. A teammate wants to add a pattern “because it is on the course list,” even though the feature is small and unlikely to grow. When should you **skip** a pattern? What risk do you take if you apply one too early?

> [!NOTE]
> ***Your Answer***
>
> _(You should skip a pattern when the feature is small, simple, and unlikely to grow, as simple direct code or functions are clearer and easier to maintain in that scenario. Applying a pattern too early introduces over-engineering risks, such as unnecessarily complex code, extra boilerplate files, harder debugging, and reduced readability.)_

## B. This phase of the application

4. Why does Phase 1 ship a vertical slice that does almost no greenhouse business logic? What does “empty but running” prove that a folder of unimplemented classes would not?

> [!NOTE]
> ***Your Answer***
>
> _(Phase 1 ships a vertical slice to establish and verify the underlying technical foundation, project layout, and deployment pipeline before adding business logic. "Empty but running" proves that Docker, the database connection, API routes, database migrations, and frontend integration are properly wired and communicating end-to-end, which a folder of static, unimplemented classes cannot prove.)_

5. List the four backend layer packages used in this course (**domain**, **application**, **infrastructure**, **interfaces/api**). For each, state what belongs there and give one example of something that must **not** live in **domain**.

> [!NOTE]
> ***Your Answer***
>
> _(Domain: Contains core business concepts, entities, and validation rules independent of frameworks or databases. Application: Contains use-case orchestrators and services that execute domain logic (e.g., creating a sensor or running automation). Infrastructure: Contains technical details, database repositories, ORM models, and external device drivers. Interfaces/API: Contains web layer code like FastAPI routers, request/response DTOs, and HTTP handlers. FastAPI routing decorators, SQLAlchemy models, and Docker configs must NOT live in the domain.)_

6. What does `GET /health` return, and why does it check the database instead of only reporting that the HTTP process is up? Why is API documentation served at `/scalar`, and why is `/docs` disabled?

> [!NOTE]
> ***Your Answer***
>
> _(`GET /health` returns `{"status": "ok", "db": "ok"}`. It checks the database to confirm that the persistent data layer is reachable and functioning, as a running HTTP process alone does not guarantee a healthy application. Documentation is served at `/scalar` to satisfy the project requirements and provide a modern, clean interface for API inspection, while default Swagger `/docs` is disabled to enforce a single consistent documentation standard.)_

7. Phase 1 requires Alembic (or equivalent) with a **baseline** migration and **no** business tables such as `devices`. Why introduce the migration toolchain before any product schema? What would go wrong if you created tables by hand in Postgres and only added migrations later?

> [!NOTE]
> ***Your Answer***
>
> _(Introducing Alembic early ensures a repeatable, version-controlled database schema history before any product tables exist, proving that the migration environment and database connection are configured correctly. Creating tables manually in PostgreSQL leads to schema drift, missing migration history, and synchronization errors when deploying across different environments.)_

## C. Compare, contrast, and scenarios

8. Explain **dependency direction** in this skeleton: which layers may import which? Why must domain code not import FastAPI, SQLAlchemy, or Pydantic models used as HTTP schemas?

> [!NOTE]
> ***Your Answer***
>
> _(Dependency direction flows inwards: `interfaces/api` imports `application` and `domain`; `infrastructure` imports `application` and `domain`; `application` imports `domain`. Domain code must never import FastAPI, SQLAlchemy, or Pydantic HTTP schemas because those are technical delivery details. Keeping the domain layer pure ensures business logic remains framework-agnostic, decoupled, and easy to unit test.)_

9. The frontend cannot show a healthy badge. A classmate blames “the patterns.” What should you check first (stack, CORS/proxy, health JSON), and why is that a Phase 1 concern rather than a later pattern concern?

> [!NOTE]
> ***Your Answer***
>
> _(You should first check if Docker containers are running (`docker compose ps`), inspect the backend response (`curl http://localhost:8000/api/health`), and verify CORS or proxy settings to ensure the JSON payload returns `{"status": "ok", "db": "ok"}`. This is a Phase 1 concern because it deals with foundational network reachability, infrastructure, and stack configuration rather than software design patterns.)_

10. Course completion is at **Phase 12**, not Phase 1. What is still missing after a successful skeleton, and how do later phases add behaviour without rewriting the foundations you laid here?

> [!NOTE]
> ***Your Answer***
>
> _(A successful skeleton is still missing actual greenhouse domain features, device models, telemetry ingestion, automation strategies, and real-time updates. Later phases can add these behaviors seamlessly because the clean layered architecture, database migration pipeline, repository interfaces, and UI placeholders are already established without needing to alter the core foundation.)_