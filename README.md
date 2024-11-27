
# AWS CI/CD Pipeline

## Overview

This repository provides a complete framework for setting up **Continuous Integration (CI)** and **Continuous Deployment (CD)** pipelines on AWS. The solution leverages AWS services like **CodePipeline**, **CodeBuild**, and **CodeDeploy**, ensuring automated builds, tests, and deployments for seamless software delivery.

---

## Features

- Automated build and deployment process using AWS CodePipeline.
- Integration with AWS CodeBuild for compiling and testing code.
- Deployment using AWS CodeDeploy for EC2, ECS, or Lambda targets.
- Supports multiple runtime environments (Node.js, Python, Java, etc.).
- Modular and extensible design to fit various CI/CD requirements.
- Includes example application and deployment scripts.

---

## Table of Contents

1. [Architecture](#architecture)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Configuration](#configuration)
5. [Customization](#customization)
6. [Troubleshooting](#troubleshooting)
7. [Contributing](#contributing)
8. [License](#license)

---

## Architecture

### Pipeline Workflow

1. **Source Stage:** 
   - Monitors the source code repository (e.g., GitHub, CodeCommit) for changes.
2. **Build Stage:** 
   - Runs automated build and test scripts using AWS CodeBuild.
3. **Deploy Stage:** 
   - Deploys the built artifact to the specified environment using AWS CodeDeploy.

![AWS CI/CD Architecture](https://user-images.placeholder-for-architecture-diagram)

---

## Installation

### Prerequisites

- AWS account with administrative privileges.
- AWS CLI installed and configured.
- Node.js, Python, or other runtime environments (as per your project).
- IAM roles for CodePipeline, CodeBuild, and CodeDeploy with necessary permissions.

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/SmruthiRavichandran/aws-ci-cd.git
   cd aws-ci-cd
   ```

2. Deploy the pipeline using the provided CloudFormation template:

   ```bash
   aws cloudformation deploy \
     --template-file pipeline-template.yaml \
     --stack-name aws-ci-cd-pipeline \
     --capabilities CAPABILITY_NAMED_IAM
   ```

3. Verify that the pipeline is created successfully in the AWS Management Console.

---

## Usage

### 1. Source Integration

Update the `pipeline-template.yaml` file to link your GitHub or CodeCommit repository:

```yaml
Source:
  Repository: "https://github.com/<your-repo>"
  Branch: "main"
```

### 2. Build Configuration

Define your build steps in the `buildspec.yaml` file:

```yaml
version: 0.2

phases:
  install:
    runtime-versions:
      nodejs: 14
  build:
    commands:
      - npm install
      - npm run build
  post_build:
    commands:
      - echo "Build completed!"
artifacts:
  files:
    - "**/*"
```

### 3. Deployment Configuration

Update the `appspec.yaml` file to define your deployment steps:

```yaml
version: 0.0
os: linux
files:
  - source: /app
    destination: /var/www/app
hooks:
  ApplicationStart:
    - location: scripts/start.sh
      timeout: 300
      runas: root
```

### 4. Triggering the Pipeline

Push changes to the configured repository branch to trigger the pipeline automatically.

---

## Configuration

### CloudFormation Template Parameters

| Parameter            | Description                              | Default        |
|----------------------|------------------------------------------|----------------|
| `RepositoryUrl`      | URL of the source code repository.       | *Required*     |
| `BuildEnvironment`   | Build environment (Node.js, Python, etc.)| Node.js 14     |
| `DeploymentTarget`   | Target environment (EC2, ECS, Lambda).   | EC2            |

---

## Customization

1. **Adding Tests:**  
   Update the `buildspec.yaml` file to include test commands during the build phase:

   ```yaml
   build:
     commands:
       - npm test
   ```

2. **Multi-Environment Deployment:**  
   Use multiple deployment stages in the CloudFormation template to enable deployment to **staging** and **production** environments.

3. **Notification Integration:**  
   Add SNS or Slack notifications to the pipeline to receive updates on pipeline progress.

---

## Troubleshooting

### Common Issues

1. **Pipeline Fails at Source Stage:**
   - Verify the repository URL and branch name in the `pipeline-template.yaml` file.
   - Ensure webhook permissions are correctly set up for GitHub.

2. **Build Stage Errors:**
   - Check the build logs in AWS CodeBuild.
   - Validate the runtime version and build commands in `buildspec.yaml`.

3. **Deployment Fails:**
   - Verify IAM roles and permissions for CodeDeploy.
   - Check application lifecycle hooks in `appspec.yaml`.

---

## Contributing

We welcome contributions! Follow these steps to contribute:

1. Fork the repository.
2. Create a feature branch:

   ```bash
   git checkout -b feature-name
   ```

3. Commit your changes and push:

   ```bash
   git commit -m "Add feature"
   git push origin feature-name
   ```

4. Create a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

