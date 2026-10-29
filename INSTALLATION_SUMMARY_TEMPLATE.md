# UAT DevOps Installation Summary — Dry Run

**Project:** Hello UAT pipeline  
**Date:** YYYY-MM-DD  
**Team member 1:** ____________________  
**Team member 2:** ____________________  
**Machine/OS:** ____________________  
**Repository URL:** ____________________  
**Jenkins job/build number:** ____________________

> Fill in the Status and Evidence columns only after running each verification command. Do not mark a tool Successful just because it was downloaded or installed; verify the command/output.

| Tool / component | Purpose | Commands used | Status (Successful / Failed / Pending) | Evidence / version / remarks |
|---|---|---|---|---|
| VS Code | Edit and manage the project | `code --version` | Pending | |
| Python 3.12 | Run app, tests, monitor | `py -3 --version` (Windows) or `python3 --version` | Pending | |
| pip / venv | Install isolated dependencies | `py -3 -m pip --version`; `py -3 -m venv .venv` | Pending | |
| Git | Version control and GitHub push/pull | `git --version`; `git status`; `git clone <repo-url>` | Pending | |
| GitHub repository | Store source and Jenkinsfile | `git push -u origin main`; Jenkins checkout log | Pending | |
| Java 21+ | Runtime required by current Jenkins | `java -version` | Pending | |
| Jenkins | CI orchestration | Open `http://localhost:8080`; click **Build Now** | Pending | |
| Docker Desktop / Engine | Build and run Linux container | `docker --version`; `docker info` | Pending | |
| Python image | Lightweight runtime image | `docker pull python:3.12-slim` | Pending | |
| pytest | Unit test execution | `py -3 -m pytest -q` or `.venv\\Scripts\\python.exe -m pytest -q` | Pending | Expected: `1 passed` |
| Evidently + pandas | Generate data-drift smoke-test report | `.venv\\Scripts\\python.exe monitor.py` | Pending | Expected HTML and JSON under `reports/` |
| Docker app run | Verify container startup | `docker run --rm hello-uat:<build-number>` | Pending | Expected greeting in output |
| Docker pytest | Verify test runs inside container | `docker run --rm hello-uat:<build-number> python -m pytest -q` | Pending | Expected: `1 passed` |
| Jenkins Pipeline | Automate checkout, tests, Docker, report | Jenkins job **Build Now**; inspect Console Output | Pending | Expected overall result: SUCCESS |

## Acceptance criteria

- [ ] Two team members assigned; responsibilities agreed.
- [ ] `hello.py` runs and prints the greeting.
- [ ] Source structure is committed and pushed to GitHub.
- [ ] Jenkins checks out the repository from GitHub.
- [ ] Host-side pytest reports one passing test.
- [ ] Docker image builds from `python:3.12-slim` and runs successfully.
- [ ] pytest passes inside the container.
- [ ] Evidently produces `reports/evidently_data_drift.html` and `reports/evidently_data_drift.json`.
- [ ] Jenkins archives the test and monitoring reports.
- [ ] Any failures, fixes and evidence are documented below.

## Issues and corrective actions

| Date/time | Step / error | Root cause | Corrective action | Retest result |
|---|---|---|---|---|
| | | | | |
| | | | | |

## Final outcome

**Overall status:** Pending / Successful / Successful with issues / Failed  
**Summary:** ________________________________________________  
**Verified by:** ____________________  
**Date:** ____________________
