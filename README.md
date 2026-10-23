# MotorScope

MotorScope is a Python-based used-vehicle research tool designed to help evaluate vehicle candidates, estimate maintenance needs, and compare total ownership costs.

## Objectives

- Track used-vehicle listings and candidate information.
- Compare vehicles based on price, mileage, condition, and available evidence.
- Track maintenance items and service intervals.
- Estimate acquisition costs, annual upkeep, and multi-year ownership expenses.
- Identify unresolved concerns and information that needs verification.

## Planned Technology

- Python
- SQLite
- pytest
- Git

## Project Status

Initial development.

The first milestone is a command-line application for recording and reviewing used-vehicle listings. Maintenance planning and ownership-cost estimation will be added incrementally.

## Design Principles

- Keep business logic separate from user interaction and database access.
- Prefer simple, understandable designs over unnecessary abstraction.
- Test calculations and important business rules.
- Make assumptions and cost estimates explicit.
- Distinguish verified information from estimates and unknowns.