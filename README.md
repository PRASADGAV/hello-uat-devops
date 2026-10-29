# Hello UAT — DevOps Dry Run

A beginner-friendly practice repository for a two-person team. It demonstrates:

1. A single-file Python application (`hello.py`).
2. Git/GitHub version control.
3. pytest with one unit test.
4. A lightweight `python:3.12-slim` Docker image.
5. Jenkins Pipeline-as-Code (`Jenkinsfile`).
6. An Evidently data-drift report using synthetic data.

**Important:** This is a local UAT/dry-run exercise. It does not deploy to a production server and does not send production data to Evidently. The sample monitoring script generates a local HTML/JSON report from synthetic reference and current datasets.

## 0. Suggested team split

- **Developer 1:** create `hello.py` and `test_hello.py`, run pytest, create/push the GitHub repo.
- **Developer 2:** set up Docker and Jenkins, configure the Pipeline job, review test logs.
- **Both:** run the Evidently report, complete `INSTALLATION_SUMMARY_TEMPLATE.md`, and verify the final Jenkins result.

## 1. Install prerequisites (Windows-first instructions)

Install these tools from their official websites:

- **VS Code:** https://code.visualstudio.com/
- **Python 3.12 (64-bit):** https://www.python.org/downloads/
- **Git for Windows:** https://git-scm.com/download/win
- **Java 21 or later:** https://adoptium.net/ (Jenkins requires a supported Java runtime; current Jenkins Windows docs specify Java 21+.)
- **Docker Desktop:** https://docs.docker.com/desktop/setup/install/windows-install/
- **Jenkins LTS:** https://www.jenkins.io/download/

For Docker Desktop on Windows, enable/update WSL 2 if the installer requests it. After installation, start Docker Desktop and wait until its engine is running. Use Linux containers (the default on most Windows setups).

Open **PowerShell** and verify tools:

```powershell
py -3 --version
py -3 -m pip --version
git --version
java -version
docker --version
docker info
```

If `docker info` fails, Docker Desktop is not running or the current user/session cannot access the Docker engine. Fix this before proceeding.

### Jenkins launch note for local Windows dry runs

A Windows Jenkins service may run under a different account from your interactive account, which can make Python/Git/Docker unavailable to the build. For a student laptop dry run, the simplest option is to start Jenkins from a terminal in the same user session while Docker Desktop is running:

1. Download the generic **jenkins.war** package from the official Jenkins download page.
2. Open PowerShell in the directory containing `jenkins.war`.
3. Run:

```powershell
java -jar .\jenkins.war --httpPort=8080
```

4. Open http://localhost:8080 and follow the setup wizard. Use the initial administrator password at the path shown by Jenkins in the terminal/setup instructions (the default WAR home on Windows is normally `%USERPROFILE%\.jenkins\secrets\initialAdminPassword`).
5. Install the suggested plugins. Make sure **Pipeline**, **Git**, and **JUnit** support are installed. If using a Windows MSI service installation instead, configure its service account and PATH so it can access Java, Git, Python, and the Docker engine.

Keep that terminal open while using Jenkins. If port 8080 is already occupied, use another port, e.g. `--httpPort=8081`, and open that port in the browser.

## 2. Open the project in VS Code

Extract this ZIP, then open the `hello-uat-devops` directory in VS Code (**File → Open Folder**). Or use PowerShell:

```powershell
cd path\to\hello-uat-devops
code .
```

Recommended VS Code extension: **Python** by Microsoft. The extension is optional for running the command-line steps.

## 3. Create and test a local Python environment

Run from the repository root in PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements-monitoring.txt
.\.venv\Scripts\python.exe hello.py
.\.venv\Scripts\python.exe -m pytest -q
```

Expected application output:

```text
Hello from the DevOps UAT environment!
```

Expected test result contains `1 passed`. To create a JUnit XML result:

```powershell
New-Item -ItemType Directory -Force reports | Out-Null
.\.venv\Scripts\python.exe -m pytest -q --junitxml=reports/pytest.xml
```

### Ubuntu/Linux equivalents

```bash
python3 --version
git --version
docker --version
docker info
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt -r requirements-monitoring.txt
.venv/bin/python hello.py
.venv/bin/python -m pytest -q
```

## 4. Create the GitHub repository and push the project

1. Sign in to GitHub and create a **new empty repository**, e.g. `hello-uat-devops`. For a clean first push, do not pre-add a README or `.gitignore` on GitHub.
2. In a terminal opened at the project root, run the commands below. Replace the example URL with your repository URL.

```bash
git init
git add .
git commit -m "Add hello UAT DevOps pipeline"
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/hello-uat-devops.git
git push -u origin main
```

Verify the files appear on GitHub. To pull the code on another machine, use:

```bash
git clone https://github.com/<YOUR_USERNAME>/hello-uat-devops.git
cd hello-uat-devops
```

If GitHub asks for authentication over HTTPS, use the supported browser/device login or a Personal Access Token; do not put a token in the repository, Jenkinsfile, or report.

## 5. Pull the lightweight Python Docker image

Make sure Docker Desktop is running, then execute:

```powershell
docker pull python:3.12-slim
docker run --rm python:3.12-slim python --version
```

The second command should print a Python 3.12 version. `python:3.12-slim` is the base image; the project image adds pytest and the two app/test files.

## 6. Build and run the project container

From the repository root:

```powershell
docker build -t hello-uat:local .
docker run --rm hello-uat:local
docker run --rm hello-uat:local python -m pytest -q
```

Expected: the first run prints the greeting and the test command reports `1 passed`.

## 7. Configure the Jenkins Pipeline

1. Start Jenkins and sign in at http://localhost:8080.
2. Select **New Item** → enter `hello-uat-pipeline` → choose **Pipeline** → **OK**.
3. Under **General**, add a description such as `UAT dry run: Git checkout, pytest, Docker and Evidently`.
4. Under **Pipeline**, select **Pipeline script from SCM**.
5. SCM: **Git**. Repository URL: `https://github.com/<YOUR_USERNAME>/hello-uat-devops.git`.
6. Branch specifier: `*/main`.
7. Script Path: `Jenkinsfile`.
8. Save and click **Build Now**.
9. Open the build number → **Console Output**. Review each stage and the final status.

For a private repository, add GitHub credentials in Jenkins (**Manage Jenkins → Credentials**) and select them in the job; never hard-code credentials.

The included Jenkinsfile runs these stages:

- Checkout from GitHub.
- Verify Python, Git and Docker commands.
- Create a virtual environment, install test/monitoring packages, and run pytest.
- Pull `python:3.12-slim`, build the project image, run the app and run pytest inside the container.
- Generate an Evidently HTML/JSON drift report.
- Publish the JUnit test result and archive reports.

### Jenkins troubleshooting

- **`py` or `python3` not found:** install Python 3.12 and ensure the executable is on PATH for the Jenkins process; restart Jenkins after changing PATH.
- **`git` not found:** install Git and restart Jenkins.
- **`docker info` fails in Jenkins but works in your desktop terminal:** Jenkins likely runs under a different user/session than Docker Desktop. For this laptop exercise, run the WAR in your logged-in session (see above), or explicitly configure a suitable Jenkins service account and Docker access.
- **Git checkout fails:** verify repository URL, branch `main`, network access and (for private repositories) Jenkins credentials.
- **Port 8080 is busy:** start Jenkins with `--httpPort=8081` and browse to `http://localhost:8081`.

## 8. Configure Evidently and generate the monitoring report

The project uses Evidently's Python API to compare two **synthetic** datasets and create a data-drift report. Run it locally:

```powershell
.\.venv\Scripts\python.exe monitor.py
```

Expected outputs:

- `reports/evidently_data_drift.html` — open this in a browser to inspect the report.
- `reports/evidently_data_drift.json` — machine-readable snapshot.

The monitor deliberately shifts sample age, spending, and region distributions so the drift report has something to inspect. Do not treat its findings as real-world model degradation.

### Optional Evidently local dashboard demo

To open Evidently's built-in sample dashboard, use a **separate terminal** in the same virtual environment:

```powershell
.\.venv\Scripts\evidently.exe ui --demo-projects all
```

Then open http://localhost:8000. This command launches Evidently's demo projects; it is separate from the project's generated HTML report. Stop it with `Ctrl+C` when finished.

For ongoing monitoring of a real system, you would need to repeatedly ingest approved reference/current data and persist/upload monitoring snapshots to a dashboard/service. This sample script is an offline configuration smoke test and does not configure alerts or production telemetry.

## 9. Installation summary report

Open `INSTALLATION_SUMMARY_TEMPLATE.md`. Record the actual version/output for each tool and mark each status as **Successful**, **Failed**, or **Pending** only after verifying it. Keep evidence such as Jenkins build number, Console Output, `1 passed` test result, Docker output and the generated report filenames. Do not report a step as successful if you have only downloaded the installer.

## 10. Final dry-run checklist

- [ ] `hello.py` prints the expected greeting.
- [ ] `pytest` reports one passing test locally.
- [ ] GitHub contains the project and `Jenkinsfile`.
- [ ] Jenkins successfully checks out the repository.
- [ ] Docker pulls `python:3.12-slim` and builds `hello-uat:<build-number>`.
- [ ] The app and pytest run inside Docker.
- [ ] Evidently HTML and JSON files are generated.
- [ ] Jenkins displays **SUCCESS** and stores artifacts.
- [ ] `INSTALLATION_SUMMARY_TEMPLATE.md` is completed with real results.

## Reference documentation

- Jenkins on Windows and Java prerequisites: https://www.jenkins.io/doc/book/installing/windows/
- Jenkins Pipelines / Jenkinsfile: https://www.jenkins.io/doc/book/pipeline/jenkinsfile/
- Docker Desktop for Windows: https://docs.docker.com/desktop/setup/install/windows-install/
- pytest getting started: https://docs.pytest.org/en/stable/getting-started.html
- Evidently project and current Python API examples: https://github.com/evidentlyai/evidently
