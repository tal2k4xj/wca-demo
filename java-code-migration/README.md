# Java Code Migration Tool

A command-line tool for analyzing, reviewing, and migrating Java code between different frameworks and specifications, powered by watsonx Code Assistant (WCA) API.

[Owner Contact](https://ibm.enterprise.slack.com/archives/D08EJANBT8A)

## Features

- **Code Review**: Analyzes Java code and provides modernization recommendations using WCA's code analysis capabilities
- **Code Upgrade**: Upgrades Java code to use modern features and patterns
- **Specific Migrations**:
  - JAX-RPC → JAX-WS
  - JSch → J2SSH
  - WebSphere Scheduler → Liberty Scheduler
  - EJB → POJO
  - Gradle → Maven

## About

This tool leverages IBM's watsonx Code Assistant (WCA) API to:
- Analyze Java code for modernization opportunities
- Generate migration recommendations
- Transform code between different Java frameworks and specifications
- Preserve business logic while updating implementation patterns
- Convert build configurations between different build systems

## Installation

1. Clone the repository:
```bash
git clone https://github.ibm.com/watsonx-apac/wca-java.git
cd wca-java
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your IBM Cloud API key in `.env` file:
```bash
IAM_APIKEY=your_api_key_here
```

## Usage

### Code Review

Review Java code for modernization opportunities:

```bash
python wca_java.py review path/to/JavaFile.java --output review_report.md
```

### Code Upgrade

Upgrade Java code to use modern features:

```bash
python wca_java.py upgrade path/to/JavaFile.java --output ModernizedFile.java
```

### Specific Migrations

#### JAX-RPC to JAX-WS

Migrate JAX-RPC web services to JAX-WS:

```bash
python wca_java.py migrate-jaxrpc-to-jaxws path/to/OldService.java --output NewService.java
```

#### JSch to J2SSH

Migrate JSch SFTP implementations to J2SSH:

```bash
python wca_java.py migrate-jsch-to-j2ssh path/to/JSchFile.java --output J2SSHFile.java
```

#### WebSphere to Liberty Scheduler

Migrate WebSphere schedulers to Liberty:

```bash
python wca_java.py migrate-was-to-liberty path/to/WASScheduler.java --output LibertyScheduler.java
```

#### EJB to POJO

Migrate EJB code to POJOs:

```bash
python wca_java.py migrate-ejb-to-pojo path/to/EJBFile.java --output POJOFile.java
```

#### Gradle to Maven

Convert Gradle build files to Maven:

```bash
python wca_java.py migrate-gradle-to-maven build.gradle --output pom.xml
```

## Options

Common options available for all commands:

- `--output`, `-o`: Specify output file path
- `--verbose`, `-v`: Show detailed progress (review command only)

## Sample Files

The `sample/` directory contains example files for each migration type:

```
sample/
├── jaxrpc/
│   └── HelloService.java       # JAX-RPC web service
├── sftp/
│   └── JSchFileTransfer.java   # JSch SFTP implementation
├── scheduler/
│   └── WASScheduler.java       # WebSphere scheduler
├── ejb/
│   └── CustomerService.java    # EJB service
└── gradle/
    └── build.gradle           # Gradle build file
```

## Testing

Run the test suite:

```bash
pytest tests/test_migrations.py -v
```

Test outputs are saved in the `test_output/` directory for inspection.

## Migration Details

### JAX-RPC → JAX-WS
- Updates imports to use javax.jws
- Adds WebService annotations
- Removes RemoteException dependencies
- Updates method signatures

### JSch → J2SSH
- Updates SFTP client implementation
- Migrates connection handling
- Updates file transfer operations
- Preserves security configurations

### WebSphere → Liberty Scheduler
- Migrates to ManagedScheduledExecutorService
- Updates task scheduling mechanism
- Preserves cron expressions
- Maintains error handling

### EJB → POJO
- Removes EJB-specific code
- Adds Spring/CDI annotations
- Updates transaction handling
- Migrates to JPA for persistence
- Implements dependency injection

### Gradle → Maven
- Converts project structure
- Maps dependencies and scopes
- Configures plugins
- Preserves build settings
- Handles Spring Boot configuration
- Includes proper DTD declarations

## Requirements

- Python 3.8+
- IBM Cloud API key
- Java source files to analyze/migrate

## Dependencies

- typer: CLI interface
- rich: Terminal formatting
- python-dotenv: Environment variable management
- requests: API communication