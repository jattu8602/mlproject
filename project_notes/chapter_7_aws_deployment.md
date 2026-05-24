# Chapter 7: Deploy to AWS Elastic Beanstalk

## What is Elastic Beanstalk?
AWS Elastic Beanstalk (EB) is a Platform-as-a-Service (PaaS). You upload your code, and AWS handles:
- Provisioning EC2 servers
- Setting up load balancers
- Auto-scaling based on traffic
- Installing dependencies from requirements.txt
- Running your Flask app

## Prerequisites
1. **AWS Account** — sign up at https://aws.amazon.com
2. **AWS CLI** — command-line tool: `pip3 install awscli`
3. **EB CLI** — Elastic Beanstalk CLI: `pip3 install awsebcli`

## Files Needed for Deployment

### 1. `application.py` — EB Entry Point
```python
from app import application

if __name__ == "__main__":
    application.run()
```
EB looks for `application:application` (file:variable). Our Flask app variable is named `application` in `app.py`, so this wrapper imports it.

### 2. `.ebextensions/python.config`
```yaml
option_settings:
  "aws:elasticbeanstalk:container:python":
    WSGIPath: application:application
```
This tells EB: "The WSGI app is in `application.py`, variable named `application`."

### 3. `requirements.txt`
EB runs `pip install -r requirements.txt` automatically on the server.

## Deployment Steps

### Step 1: Install AWS CLI & Configure
```bash
pip3 install awscli
aws configure
```
Enter your AWS Access Key ID, Secret Key, region (e.g. us-east-1), output format (json).

### Step 2: Install EB CLI
```bash
pip3 install awsebcli
```

### Step 3: Initialize EB
```bash
eb init
```
- Pick region
- Select Python platform
- Name the application (default: mlproject)
- Set up SSH (optional)

### Step 4: Create Environment & Deploy
```bash
eb create mlproject-env
```
This takes ~5 minutes. EB creates:
- EC2 instance (server)
- Security group
- Load balancer
- Auto-scaling group
- Installs your dependencies
- Deploys your app

### Step 5: Open the App
```bash
eb open
```
Opens your deployed URL in the browser.

## Useful EB Commands
| Command | What it does |
|---------|-------------|
| `eb status` | Check environment status |
| `eb logs` | View server logs |
| `eb deploy` | Redeploy after code changes |
| `eb terminate mlproject-env` | Shut down environment (to avoid charges) |
