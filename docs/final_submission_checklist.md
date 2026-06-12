# Final Submission Checklist Evidence

This document maps the final project repository to the take-home final checklist items.

## Team Information

- **Team ID:** Kelompok 7
- **Project:** Constructing a Cybersecurity Knowledge Graph from Unstructured Data
- **Repository:** `Software-Engineering-2026-Class/cskg-from-unstructure-kelompok-7`
- **Members:** Axelle Chandra, Danar Fathurahman, Kesya Izumi, Keyne Elvaretta

## A. Repository Structure & Setup

- [x] Repository is public and accessible through the submitted GitHub link.
- [x] Repository name matches the CSKG project topic.
- [x] Team members are listed in `README.md`.
- [x] Repository uses branches and pull requests for final fixes.
- [x] Commit messages are descriptive and meaningful.
- [x] No credentials are committed; secrets should be placed in `.env`, with `.env.example` provided.

## B. GitHub Issues & Project Management

- [x] Lecturer/team feedback items are represented as GitHub issues.
- [x] Closed issues should be linked to commits or pull requests when resolved.
- [x] Issues are labeled by area such as documentation, evaluation, infrastructure, or feature.
- [x] Final output coverage issue is addressed by documenting generated TTL output, graph statistics, and use-case evidence.

## C. Docker & Environment

- [x] `Dockerfile` is present in the repository root.
- [x] `compose.yml` defines the full service stack.
- [x] `docker-compose.yml` is provided as a compatibility entrypoint for evaluators expecting that filename.
- [x] `.env.example` lists required environment variables.
- [x] Docker Compose services include Redis, Virtuoso, FastAPI API, producer, extractor, graph builder, and summary worker.
- [x] Containers are named clearly, for example `cskg_redis`, `cskg_virtuoso`, and `cskg_api`.
- [x] Port mappings are documented in `compose.yml` and `README.md`.

## D. README & Documentation

- [x] `README.md` exists at repository root.
- [x] README includes project description, architecture, ontology, API endpoints, SPARQL examples, and run instructions.
- [x] README includes Docker quick start commands.
- [x] README documents service access ports.
- [x] README lists team members.
- [x] At least three use cases are documented in `docs/usecases.md` and `queries/usecases/`.
- [x] `CHANGELOG.md` is present.

## E. Code Quality & Organization

- [x] Source code is organized into logical folders: `pipeline/`, `server/`, `docs/`, `queries/`, and `reports/`.
- [x] Dependency file `requirements.txt` is present.
- [x] Runtime configuration uses `.env` instead of hardcoded API keys.
- [x] Non-obvious runtime logic is documented through README, evidence files, and comments in Compose configuration.

## F. Evaluation & Results

- [x] RDF/Turtle output is committed as `cskg_full_dump.ttl`.
- [x] Runtime statistics are documented in `README.md` and `docs/evidence/final_runtime_verification.md`.
- [x] Evaluation notes are present in `docs/evaluation.md`.
- [x] Use-case query inputs and outputs are documented in `docs/usecases.md` and `queries/usecases/`.

## Remaining Notes

The repository is mostly complete for the final checklist. The main final-submission additions are the standard `docker-compose.yml` wrapper, `.env.example`, `CHANGELOG.md`, and this checklist-evidence document.
