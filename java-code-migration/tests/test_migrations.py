import os
import pytest
from pathlib import Path
import sys

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from wca_java import (
    upgrade_java,
    migrate_jaxrpc_to_jaxws,
    migrate_jsch_to_j2ssh,
    migrate_was_to_liberty,
    migrate_ejb_to_pojo,
    migrate_gradle_to_maven
)

# Test data paths
SAMPLE_DIR = Path("sample")
TEST_OUTPUT_DIR = Path("test_output")

# Create output directory if it doesn't exist
TEST_OUTPUT_DIR.mkdir(exist_ok=True)

def read_sample_file(filename):
    """Helper to read sample files"""
    with open(f"{SAMPLE_DIR}/{filename}", 'r') as f:
        return f.read()

def test_jaxrpc_to_jaxws_migration():
    """Test JAX-RPC to JAX-WS migration"""
    # Setup
    input_file = SAMPLE_DIR / "jaxrpc/HelloService.java"
    output_file = TEST_OUTPUT_DIR / "HelloService_jaxws.java"
    
    # Run migration
    migrate_jaxrpc_to_jaxws(input_file, output_file)
    
    # Read and validate output
    migrated_code = output_file.read_text()
    assert migrated_code is not None
    assert len(migrated_code) > 0
    
    # Validate specific patterns
    assert "@WebService" in migrated_code
    assert "sayHello" in migrated_code
    assert "javax.jws" in migrated_code
    assert "RemoteException" not in migrated_code
    assert "ServiceLifecycle" not in migrated_code

def test_jsch_to_j2ssh_migration():
    """Test JSch to J2SSH migration"""
    input_file = SAMPLE_DIR / "sftp/JSchFileTransfer.java"
    output_file = TEST_OUTPUT_DIR / "SftpClient_j2ssh.java"
    
    migrate_jsch_to_j2ssh(input_file, output_file)
    
    migrated_code = output_file.read_text()
    assert migrated_code is not None
    assert len(migrated_code) > 0
    
    assert "com.sshtools.j2ssh" in migrated_code
    assert "SshClient" in migrated_code
    assert "connect" in migrated_code
    assert "uploadFile" in migrated_code
    assert "downloadFile" in migrated_code
    assert "JSch" not in migrated_code
    assert "ChannelSftp" not in migrated_code

def test_was_to_liberty_migration():
    """Test WebSphere to Liberty scheduler migration"""
    input_file = SAMPLE_DIR / "scheduler/WASScheduler.java"
    output_file = TEST_OUTPUT_DIR / "Scheduler_liberty.java"
    
    migrate_was_to_liberty(input_file, output_file)
    
    migrated_code = output_file.read_text()
    assert migrated_code is not None
    assert len(migrated_code) > 0
    
    assert "ManagedScheduledExecutorService" in migrated_code
    assert "scheduleTask" in migrated_code
    assert "cancelTask" in migrated_code
    assert "com.ibm.websphere.scheduler" not in migrated_code
    assert "BeanTaskInfo" not in migrated_code

def test_ejb_to_pojo_migration():
    """Test EJB to POJO migration"""
    input_file = SAMPLE_DIR / "ejb/CustomerService.java"
    output_file = TEST_OUTPUT_DIR / "CustomerService_pojo.java"
    
    migrate_ejb_to_pojo(input_file, output_file)
    
    migrated_code = output_file.read_text()
    assert migrated_code is not None
    assert len(migrated_code) > 0
    
    # Check for POJO patterns
    assert "@Service" in migrated_code
    assert "@Transactional" in migrated_code
    assert "CustomerService" in migrated_code
    assert "findCustomer" in migrated_code
    assert "updateCustomer" in migrated_code
    
    # Check removed EJB-specific code
    assert "EJBHome" not in migrated_code
    assert "EJBObject" not in migrated_code
    assert "SessionBean" not in migrated_code
    assert "ejbCreate" not in migrated_code
    assert "ejbActivate" not in migrated_code

def test_upgrade_java():
    """Test general Java upgrade functionality"""
    sample_files = [
        "jaxrpc/HelloService.java",
        "sftp/JSchFileTransfer.java",
        "scheduler/WASScheduler.java",
        "ejb/CustomerService.java"
    ]
    
    for sample_file in sample_files:
        input_file = SAMPLE_DIR / sample_file
        output_file = TEST_OUTPUT_DIR / f"{Path(sample_file).stem}_upgraded.java"
        
        java_code = read_sample_file(sample_file)
        upgraded_code = upgrade_java(java_code)
        output_file.write_text(upgraded_code)
        
        assert upgraded_code is not None
        assert len(upgraded_code) > 0
        
        # Validate specific patterns based on file type
        if "HelloService" in sample_file:
            assert "sayHello" in upgraded_code
        elif "JSchFileTransfer" in sample_file:
            assert "connect" in upgraded_code
            assert "uploadFile" in upgraded_code
            assert "downloadFile" in upgraded_code
        elif "WASScheduler" in sample_file:
            assert "scheduleTask" in upgraded_code
            assert "scheduler" in upgraded_code
        elif "CustomerService" in sample_file:
            assert "CustomerService" in upgraded_code
            assert "findCustomer" in upgraded_code
            assert "updateCustomer" in upgraded_code

def test_gradle_to_maven_migration():
    """Test Gradle to Maven migration"""
    input_file = SAMPLE_DIR / "gradle/build.gradle"
    output_file = TEST_OUTPUT_DIR / "pom.xml"
    
    migrate_gradle_to_maven(input_file, output_file)
    
    migrated_code = output_file.read_text()
    assert migrated_code is not None
    assert len(migrated_code) > 0
    
    # Validate XML structure
    assert "<project" in migrated_code
    
    # Check for Maven components
    assert "<dependencies>" in migrated_code
    assert "<properties>" in migrated_code
    assert "<build>" in migrated_code
    
    # Validate specific dependencies
    assert "spring-boot-starter-web" in migrated_code
    assert "spring-boot-starter-data-jpa" in migrated_code
    assert "h2" in migrated_code
    assert "lombok" in migrated_code
    
    # Check plugin configuration
    assert "spring-boot-maven-plugin" in migrated_code
    
    # Verify properties
    assert "<java.version>" in migrated_code

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 