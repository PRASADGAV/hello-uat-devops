# 🚀 Quick Start Guide - Hello UAT DevOps Pipeline

## 📋 What This Project Does

A simple Python application with automated CI/CD pipeline using Jenkins and Docker:
- Python "Hello World" app
- Automated testing with pytest
- Docker containerization
- Jenkins pipeline for CI/CD

---

## 🔧 Prerequisites Check

Before starting, verify these are running:

### 1. **Docker Desktop**
```powershell
docker --version
# Should show: Docker version 29.x.x or similar
```

### 2. **Jenkins**
- Open browser: http://localhost:8081
- Should see Jenkins dashboard

### 3. **Git**
```powershell
git --version
# Should show: git version 2.x.x or similar
```

---

## 🎯 How to Run the Pipeline

### Option 1: Jenkins UI (Recommended)

1. **Open Jenkins**
   - Go to: http://localhost:8081
   - Click on `hello-uat-pipeline` job

2. **Trigger Build**
   - Click **"Build Now"** (left sidebar)
   - Watch the build progress in real-time

3. **View Results**
   - Click on the build number (e.g., #7, #8)
   - Click **"Console Output"** to see logs
   - Look for: ✅ `Pipeline completed successfully!`

### Option 2: Manual Local Testing

```powershell
# Navigate to project
cd C:\Users\prasa\Desktop\hello-uat-devops

# Build Docker image
docker build -t hello-uat:local .

# Run tests
docker run --rm hello-uat:local python -m pytest -v

# Run application
docker run --rm hello-uat:local
```

---

## 📂 Project Structure

```
hello-uat-devops/
├── hello.py                    # Main Python application
├── test_hello.py               # Pytest tests
├── Dockerfile                  # Docker build instructions
├── Jenkinsfile                 # Jenkins pipeline definition
├── requirements.txt            # Python dependencies (just pytest)
├── requirements-monitoring.txt # Optional monitoring tools (not used in pipeline)
├── monitor.py                  # Optional monitoring script (not used in pipeline)
└── README.md                   # Project documentation
```

---

## 🔄 Pipeline Stages Explained

The Jenkins pipeline has 4 simple stages:

### 1️⃣ **Checkout**
- Pulls latest code from GitHub
- Repository: https://github.com/PRASADGAV/hello-uat-devops.git

### 2️⃣ **Build Docker Image**
- Creates Docker container with Python 3.12
- Installs pytest dependency
- Copies application code

### 3️⃣ **Run Tests**
- Executes pytest inside container
- Tests the `greet()` function

### 4️⃣ **Run Application**
- Runs the hello.py application
- Prints greeting messages

### 🧹 **Cleanup (Post-Build)**
- Removes the Docker image to save space
- Runs whether build succeeds or fails

---

## 🛠️ Common Tasks

### Make Code Changes

1. **Edit files locally**
   ```powershell
   cd C:\Users\prasa\Desktop\hello-uat-devops
   # Edit hello.py or test_hello.py with your IDE
   ```

2. **Commit and push**
   ```powershell
   git add .
   git commit -m "Your change description"
   git push origin main
   ```

3. **Trigger Jenkins build**
   - Jenkins will automatically detect the change
   - Or manually click "Build Now"

### Add New Tests

1. Edit `test_hello.py`:
   ```python
   def test_new_feature():
       result = hello.greet("World")
       assert "Hello" in result
   ```

2. Commit and push changes
3. Jenkins will run the new tests automatically

### Update Dependencies

1. Edit `requirements.txt`:
   ```
   pytest==9.2.0
   requests==2.32.0  # Example: add new package
   ```

2. Commit and push
3. Docker will install new dependencies on next build

---

## 🐛 Troubleshooting

### Build Fails at Docker Build Stage
**Problem**: Network timeout or dependency installation fails

**Solution**:
```powershell
# Try building locally first to test
docker build -t hello-uat:test .

# If it works locally but not in Jenkins, click "Build Now" again
# Network issues are often temporary
```

### Tests Fail
**Problem**: Test assertions are failing

**Solution**:
```powershell
# Run tests locally to debug
docker run --rm hello-uat:local python -m pytest -v

# Or run without Docker
cd C:\Users\prasa\Desktop\hello-uat-devops
python -m pytest -v
```

### Jenkins Not Accessible
**Problem**: Cannot open http://localhost:8081

**Solution**:
```powershell
# Check if Jenkins service is running
Get-Service -Name Jenkins

# If not running, start it
Start-Service Jenkins
```

### Docker Not Working
**Problem**: Docker commands fail

**Solution**:
1. Open Docker Desktop
2. Wait for it to fully start (green icon in system tray)
3. Verify: `docker ps` (should not error)

---

## 📊 Understanding Build Results

### ✅ Successful Build
```
[Pipeline] { (Run Tests)
....
2 passed in 0.05s
[Pipeline] { (Run Application)
Hello, DevOps World!
Hello, Jenkins!
✅ Pipeline completed successfully!
```

### ❌ Failed Build
```
[Pipeline] { (Run Tests)
FAILED test_hello.py::test_greet - AssertionError
❌ Pipeline failed!
```

**What to do**: 
- Click on the failed build number
- Read "Console Output"
- Fix the issue in code
- Commit and push
- Build again

---

## 🎓 Learning Resources

### Key Concepts to Understand

1. **Docker**: Containerization platform
   - Dockerfile = instructions to build container
   - Image = built container template
   - Container = running instance of image

2. **Jenkins Pipeline**: Automated CI/CD workflow
   - Jenkinsfile = pipeline definition
   - Stages = steps in the workflow
   - Agent = where the pipeline runs

3. **pytest**: Python testing framework
   - test_*.py = test files
   - Test functions start with `test_`
   - Assertions verify expected behavior

### Useful Commands

```powershell
# View running containers
docker ps

# View all Docker images
docker images

# Clean up unused Docker resources
docker system prune -a

# View Jenkins logs (if needed)
Get-Content C:\ProgramData\Jenkins\.jenkins\logs\jenkins.log -Tail 50

# Git status
git status

# Git pull latest changes
git pull origin main
```

---

## 🔐 Important Locations

| Resource | Location/URL |
|----------|-------------|
| **Jenkins Dashboard** | http://localhost:8081 |
| **Project Directory** | `C:\Users\prasa\Desktop\hello-uat-devops` |
| **Jenkins Workspace** | `C:\ProgramData\Jenkins\.jenkins\workspace\hello-uat-pipeline` |
| **GitHub Repository** | https://github.com/PRASADGAV/hello-uat-devops.git |
| **Docker Desktop** | Windows system tray icon |

---

## 📝 Quick Reference

### Daily Workflow

1. ☕ **Start your day**
   - Verify Docker Desktop is running
   - Open Jenkins: http://localhost:8081
   - Check if any builds failed overnight

2. 💻 **Make changes**
   - Edit code in VS Code or your IDE
   - Run tests locally (optional): `docker build -t test . && docker run --rm test python -m pytest -v`

3. 🚀 **Deploy**
   - Commit: `git add . && git commit -m "message"`
   - Push: `git push origin main`
   - Build: Click "Build Now" in Jenkins

4. ✅ **Verify**
   - Watch build progress
   - Check console output
   - Confirm all stages pass

---

## 💡 Tips for Tomorrow

1. **Before making changes**: Always pull latest code
   ```powershell
   git pull origin main
   ```

2. **Test locally first**: Build Docker image locally before pushing
   ```powershell
   docker build -t hello-test .
   docker run --rm hello-test python -m pytest -v
   ```

3. **Small commits**: Commit often with clear messages
   ```powershell
   git commit -m "Add feature X"  # Good
   git commit -m "updates"        # Bad
   ```

4. **Check Jenkins regularly**: Monitor builds after pushing changes

5. **Keep Docker clean**: Periodically clean up old images
   ```powershell
   docker system prune -a
   ```

---

## 🆘 Need Help?

### Common Questions

**Q: How do I know if the build succeeded?**
A: Look for green checkmarks (✅) next to all stages and "SUCCESS" in blue at the top.

**Q: Can I run multiple builds at once?**
A: Yes! Jenkins will queue them and run them sequentially.

**Q: What if I pushed bad code?**
A: Just fix it, commit, and push again. Previous builds remain in history.

**Q: How do I see what changed between builds?**
A: Click on a build → "Changes" tab → Shows git commits.

**Q: Can I stop a running build?**
A: Yes! Click the red X next to the running build.

---

## ✨ Next Steps (Future Enhancements)

Once comfortable with the basics, consider:

1. ⚡ Add more tests to increase code coverage
2. 📊 Re-enable monitoring reports (evidently)
3. 🌐 Deploy to a cloud platform (AWS, Azure)
4. 🔔 Add Slack/email notifications on build failures
5. 🔄 Set up automatic builds on Git push (webhooks)
6. 🏷️ Add Docker image tagging and registry push
7. 📈 Set up performance testing
8. 🔒 Add security scanning (Trivy, Snyk)

---

## 📞 Support

- **Jenkins Documentation**: https://www.jenkins.io/doc/
- **Docker Documentation**: https://docs.docker.com/
- **pytest Documentation**: https://docs.pytest.org/

---

**Last Updated**: October 29, 2026  
**Pipeline Status**: ✅ Simplified & Optimized  
**Build Time**: ~1-2 minutes per build

---

**Good luck tomorrow! 🎉**

Remember: If something breaks, don't panic. Check the console output, Google the error, and try again. You got this! 💪
