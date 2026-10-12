# D01-T009 — Interfaces, abstract classes, generics

Topic ID: `D01-T009`
Domain: Programming Language Fundamentals
Subdomain: Interfaces, abstract classes, generics
Importance: core
Complexity: fundamentals
Dependencies: `D01-T008`, `D01-T001`
Execution status of the code in section F: executed (CPython, local)

## A. Topic Overview

An interface names a contract without mandating implementation. An abstract class can provide partial implementation and force subclasses to fill gaps. Generics parameterize types so collections and repositories are type-safe at compile time (Java, C#) or checked by static analysis (Python typing).

These tools reduce coupling and casting errors. Backend code uses them for repositories, serializers, caches, and message handlers where the same logic applies to many entity types.

Interviewers ask how they differ, when erasure matters in Java, and how Python protocols relate to interfaces.

Prerequisites: composition and polymorphism (`D01-T007`, `D01-T008`). Leads to exception design (`D01-T010`).

## B. First-Principles Explanation

**Interface**: a set of method signatures. A class implements multiple interfaces. No instance fields in pure interfaces (Java before default methods was stricter).

**Abstract class**: cannot instantiate directly; may contain concrete methods and abstract methods subclasses must implement. Single inheritance in Java for classes.

**Generics**: type parameters `T`, `K`, `V` baked into class or method signatures. Compiler inserts casts or rejects wrong types. Java erases type parameters at runtime (mostly); reified generics exist in Kotlin and some JVM languages.

Runtime for `Repository<User, Long>`:

1. Compiler checks `save` receives `User`.
2. Bytecode uses `Object` or bridges at JVM level with erasure.
3. Wrong type fails at compile time, not `ClassCastException` at `get`.

Python `Protocol` and `Generic` are structural and optional at runtime; mypy enforces them in CI.

## C. Internal Working and Architecture

Java interface dispatch: `invokeinterface` on vtable slot. Default methods on interfaces add complexity with diamond conflicts.

Abstract class constructor runs before subclass fields initialize; rules forbid calling overridable methods from constructor.

Generic specialization: primitive specializations (`IntList`) in some languages; JVM uses one class with casts.

Backend stack:

- `UserRepository implements Repository<User, UUID>`
- Service depends on `Repository<User, UUID>` interface
- Postgres adapter implements interface with JDBC

JSON APIs lose generic types at the wire; deserialize to concrete DTO then map to `User`.

## D. Diagrams and Visual Models

```mermaid
flowchart LR
  svc[UserService]
  repoIf[Repository User UUID]
  mem[InMemoryUserRepo]
  pg[PostgresUserRepo]
  svc --> repoIf
  repoIf <|.. mem
  repoIf <|.. pg
```

Service code is written against the generic interface. Deploy picks adapter.

## E. Examples and Analogies

Interface analogy: electrical outlet shape. Device plugs if pins match; internals differ.

Abstract class analogy: recipe with fixed steps and blank "season to taste" step subclasses fill.

Generics analogy: labeled container: `Box<Apple>` versus `Box<Orange>` prevents mixing at compile time.

Avoid raw types (`List` without type param) in Java. Avoid giant generic bounds `T extends A & B & C` unless necessary.

## F. Code Examples

File: `examples/d01_t009_generics.py`

```python
class Repository(Protocol[T, Id]):
    def get(self, entity_id: Id) -> T | None: ...
    def save(self, entity: T) -> Id: ...


class UserService(Generic[T]):
    def __init__(self, repo: Repository[T, int]) -> None:
        self._repo = repo

    def create(self, payload: T) -> int:
        return self._repo.save(payload)
```

How to run: `python examples/d01_t009_generics.py` or `backend-engineering-knowledge-base/EXERCISES/examples/d01_t009_generics.py`.

Expected output: `ok 1`

Important lines: `Protocol` is structural typing (duck typing with types). `Generic[T]` carries type param for service users. `InMemoryUserRepo` satisfies protocol without explicit `implements`.

Edge cases: JSON `create` loses `T`; validate DTO before treating as domain type. Covariance of generics (`List<? extends Animal>`) trips Java readers; use at API boundaries carefully.

This example was executed with the system Python. Output was `ok 1`.

## G. Practical Backend Application

Define repository interfaces per aggregate. Use generics for shared pagination `Page<T>`. MapStruct or manual mappers convert entity to DTO.

Abstract base for HTTP clients: shared retry in base, `buildRequest` abstract per API.

OpenAPI generates interfaces; implement in server stubs. Generics do not cross process boundary; schema is concrete.

Testing: in-memory `Repository` fake typed same as production bean.

## H. Advantages, Limitations and Trade-offs

| Choice | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| Interface | Multiple contracts, loose coupling | No shared code | Ports/adapters | Heavy shared implementation |
| Abstract class | Shared template code | Single inheritance slot | Template method | Only one method varies |
| Generics | Type safety, less casting | Complexity, erasure surprises | Repositories, results | Wire format |
| Protocol (Python) | Structural match | Runtime unchecked | Gradual typing | Need runtime enforcement |
| Default interface methods | Evolve APIs | Diamond conflicts | Java library evolution | Greenfield small API |

Java erasure pain: cannot `new T()`, cannot overload on `T` and `String` at runtime same way. Use `Class<T>` parameter or factories.

## I. Common Mistakes and Misconceptions

- Using abstract class when interface suffices, burning the single extends slot.
- Raw `List` in Java 17 code.
- Generics on REST responses without OpenAPI concrete schema.
- Python: believing `List[User]` enforces at runtime without pydantic.
- Interface with twenty methods violating segregation.

## J. Debugging and Troubleshooting

Symptoms: `ClassCastException` after generic refactor. Bean wiring injects wrong `Repository` type.

Steps:

1. Enable `-Xlint:unchecked` in Java builds.
2. Run mypy or pyright on Python services.
3. Log bean types at startup in Spring.
4. Contract test repository methods with domain types.

Example: `java.lang.ClassCastException: class LinkedHashMap cannot be cast to User` from JSON without typing.

## K. Interview Preparation

### Beginner

#### Q1. What is an interface?

**Answer:** A contract of methods a class agrees to implement. Callers depend on the interface, not the concrete class. Enables swapping implementations and testing with fakes.

#### Q2. What is an abstract class?

**Answer:** A class you cannot instantiate that may include both implemented and abstract methods. Subclasses extend once and fill in abstract parts.

#### Q3. What are generics for?

**Answer:** They parameterize types so a `List<String>` cannot hold integers by mistake. Repositories and API wrappers reuse one definition for many entity types.

#### Q4. Interface versus abstract class in one sentence?

**Answer:** Interface is pure contract (plus defaults in Java); abstract class shares code and single inheritance.

#### Q5. Do generics exist at runtime in Java?

**Answer:** Mostly erased to `Object` or bounds. Type checks happen at compile time. Reflection can recover some parameter types via `ParameterizedType`.

### Intermediate

#### Q1. When use abstract class over interface in Java?

**Answer:** When several implementations share substantial code (validation, logging template). When you need protected fields shared by subclasses. Otherwise prefer interface plus helper class composition.

#### Q2. What is type erasure?

**Answer:** Compiler removes type parameters in bytecode. A `List<String>` and `List<Integer>` share the same class at runtime. That is why you cannot use `instanceof` on generic type parameters directly.

#### Q3. What is bounded wildcard `? extends T`?

**Answer:** Read-only producer wildcard. You can read `T` but not add arbitrary `T` (except null). Useful for returning collections without exposing mutable generic type to callers.

#### Q4. Python Protocol versus ABC?

**Answer:** Protocol is structural: if methods exist, it matches. ABC requires explicit subclass registration. Protocol fits duck typing codebases migrating to types.

#### Q5. How do generics help repositories?

**Answer:** `save(User)` and `get` returning `Optional<User>` are checked. Adapters still map rows manually, but service layer avoids casting from `Object`.

### Advanced

#### Q1. What is F-bounded quantification?

**Answer:** `T extends Comparable<T>` recursive bound. Appears in sorting utilities. Shows generics can express self-referential constraints.

#### Q2. Multiple inheritance of interfaces with defaults in Java?

**Answer:** Class can implement two interfaces with same default method; class must override to resolve diamond. Design interfaces to avoid conflicting defaults.

#### Q3. Variance in Kotlin versus Java?

**Answer:** Kotlin has declaration-site variance (`out`, `in`). Java uses wildcards at use site. Both control producer/consumer safety.

#### Q4. Generics and JSON deserialization?

**Answer:** Jackson needs `TypeReference<List<User>>` because runtime does not carry `List<User>`. Mistype causes map/list of maps bugs.

#### Q5. Type-safe builder pattern with generics?

**Answer:** Builder methods return `Builder<Step>` chaining until `build()` produces configured immutable object. Compiler enforces required fields per step in advanced APIs.

### Scenarios

#### Q1. Team uses raw `Map` for HTTP response bodies. Incident class?

**Answer:** Keys typo silently; values wrong type until deep in code. Introduce DTO records and typed clients; generate from OpenAPI.

#### Q2. One abstract `BaseRepository` with 200 lines; only `tableName` differs.

**Answer:** Smell. Use composition: generic `SqlRepository<T>` with mapper strategy, not inheritance per entity.

#### Q3. Need read-only and write repository interfaces for CQRS?

**Answer:** Split `UserQuery` and `UserCommand` interfaces. Read side returns DTOs; write side accepts commands. Generics on each.

#### Q4. Python service without mypy; generics in hints only. Risk?

**Answer:** Runtime accepts anything; bugs reach production. Add pydantic models at boundary and mypy in CI.

#### Q5. Generic cache `Cache<String, User>` key is email; user changes email.

**Answer:** Generics do not fix key stability. Invalidate cache on update; key design is domain, not type system.

### Follow-ups

#### Q1. Link to composition?

**Answer:** Services compose generic repositories and caches typed on interfaces, not concrete JDBC classes.

#### Q2. Link to exceptions?

**Answer:** `Result<T, E>` types versus exceptions; generic `Optional<T>` for missing entities. See `D01-T010`.

#### Q3. Link to API schemas?

**Answer:** OpenAPI is the cross-language generic contract. Codegen produces concrete types per operation.

## L. Practical Exercises

Solutions are in `EXERCISES/solutions/D01-T009.md`. Try these before opening that file.

### Exercise 1 — implementation

Implement `Repository` protocol, `InMemoryUserRepo`, and `UserService.create`. Acceptance: round-trip save/get, type hints satisfied under mypy if you run it.

### Exercise 2 — design

Choose abstract class versus interface for shared HTTP retry with per-API request building. Acceptance: you pick abstract class or composition with helper and justify single inheritance cost.

### Exercise 3 — trade-off

Explain Java erasure impact on `Cache<K,V>` keys from JSON string ids. Acceptance: mention compile-time safety versus runtime maps and invalidation on key change.

## M. Revision Notes

- Interface: contract, multiple implementation, DI-friendly.
- Abstract class: partial implementation, one extends.
- Generics: type parameters, compile-time checks.
- Java erasure: no `T` at runtime; use TypeReference for JSON.
- Python Protocol: structural; enforce with static checker.
- Split fat interfaces; segregate read/write.
- Wire format is never generic; DTOs are concrete.

Flashcards:

- Erasure? JVM drops type params at runtime.
- Protocol? Structural interface in Python typing.
- Wildcard extends? Producer, read-oriented.

## N. Related Topics

Understand this before: `D01-T008` composition, `D01-T007` polymorphism.

This topic supports: `D01-T010` errors, `D07-T003` repositories, `D06-T005` OpenAPI.

Often confused with: generics making runtime safe without validation at boundaries.

Interviewers combine with Java collections and Spring repository generics.

## O. Completion Criteria

- Contrast interface, abstract class, and generics.
- Draw service depending on generic repository interface.
- Implement protocol-based repository in Python.
- Explain erasure and Jackson `TypeReference`.
- Split a god repository interface for CQRS.
- Argue abstract class versus helper composition.
