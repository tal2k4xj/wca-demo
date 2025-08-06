import os
import pytest
from pathlib import Path
import sys
import shutil
import typer
import xml.etree.ElementTree as ET

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from wca_springboot import (
    migrate_structs, 
    create_spring_structure,
    convert_actions_to_controllers,
    migrate_form_beans,
    update_pom_dependencies,
    migrate_jsp_to_thymeleaf,
    migrate_service_layer
)

# Test data paths
TEST_DIR = Path(__file__).parent
SAMPLE_APP = TEST_DIR.parent / "sample/structs"
OUTPUT_DIR = TEST_DIR.parent / "output/spring-app"

def create_struts_config(config_path):
    """Create a sample struts-config.xml file"""
    config = ET.Element("struts-config")
    
    # Add form-beans
    form_beans = ET.SubElement(config, "form-beans")
    form_bean = ET.SubElement(form_beans, "form-bean")
    form_bean.set("name", "customerForm")
    form_bean.set("type", "com.example.app.form.CustomerForm")
    
    # Add action mappings
    action_mappings = ET.SubElement(config, "action-mappings")
    action = ET.SubElement(action_mappings, "action")
    action.set("path", "/customer")
    action.set("type", "com.example.app.action.CustomerAction")
    action.set("name", "customerForm")
    
    # Add forwards
    forward1 = ET.SubElement(action, "forward")
    forward1.set("name", "success")
    forward1.set("path", "/customer.do?method=list")
    
    forward2 = ET.SubElement(action, "forward")
    forward2.set("name", "list")
    forward2.set("path", "/pages/customer/list.jsp")
    
    # Write to file
    tree = ET.ElementTree(config)
    tree.write(config_path, encoding="UTF-8", xml_declaration=True)

def test_convert_actions_to_controllers():
    """Test conversion of Struts Actions to Spring Controllers"""
    print(f"\nTesting action to controller conversion...")
    print(f"Input directory: {SAMPLE_APP}")
    print(f"Output directory: {OUTPUT_DIR}")
    
    # Create Spring structure first
    print("Creating Spring structure...")
    create_spring_structure(OUTPUT_DIR)
    
    # Convert actions
    print("Converting actions to controllers...")
    convert_actions_to_controllers(SAMPLE_APP, OUTPUT_DIR)
    
    # Verify controller
    print("\nVerifying controller...")
    controller_file = OUTPUT_DIR / "src/main/java/com/example/application/controller/CustomerController.java"
    assert controller_file.exists(), f"Controller file not found: {controller_file}"
    
    content = controller_file.read_text()
    assert "@RestController" in content, "Missing @RestController annotation"
    assert "@GetMapping" in content, "Missing @GetMapping annotation"
    assert "@PostMapping" in content, "Missing @PostMapping annotation"
    assert "@PutMapping" in content, "Missing @PutMapping annotation"
    assert "@DeleteMapping" in content, "Missing @DeleteMapping annotation"
    print("Controller verification successful")

def test_create_spring_structure():
    """Test creation of Spring Boot project structure"""

    create_spring_structure(OUTPUT_DIR)
    
    # Verify directory structure
    assert (OUTPUT_DIR / "src/main/java/com/example/application/controller").exists()
    assert (OUTPUT_DIR / "src/main/java/com/example/application/model").exists()
    assert (OUTPUT_DIR / "src/main/java/com/example/application/service").exists()
    assert (OUTPUT_DIR / "src/main/java/com/example/application/repository").exists()
    assert (OUTPUT_DIR / "src/main/resources").exists()

def test_migrate_form_beans():
    """Test migration of Struts form beans to Spring DTOs"""
    # Create Spring structure first
    create_spring_structure(OUTPUT_DIR)
    
    # Migrate forms
    migrate_form_beans(SAMPLE_APP, OUTPUT_DIR)
    
    # Verify DTO
    dto_file = OUTPUT_DIR / "src/main/java/com/example/application/model/CustomerDTO.java"
    assert dto_file.exists(), "DTO file not found"
    
    content = dto_file.read_text()
    # Check validation annotations
    assert "package com.example.application.model;" in content, "Missing package declaration"
    assert "import jakarta.validation.constraints" in content, "Missing validation imports"
    assert "@NotBlank" in content, "Missing @NotBlank validation"
    assert "@Email" in content, "Missing @Email validation"
    assert "extends ActionForm" not in content, "Should not extend ActionForm"

def test_update_pom_dependencies():
    """Test updating of pom.xml with Spring Boot dependencies"""
    
    update_pom_dependencies(SAMPLE_APP, OUTPUT_DIR)
    
    # Verify pom.xml
    pom_file = OUTPUT_DIR / "pom.xml"
    assert pom_file.exists()
    
    content = pom_file.read_text()
    # Check parent
    assert "<artifactId>spring-boot-starter-parent</artifactId>" in content
    
    # Check dependencies
    assert "<artifactId>spring-boot-starter-web</artifactId>" in content
    assert "<artifactId>spring-boot-starter-validation</artifactId>" in content
    
    # Check structure
    assert "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" in content
    assert "<modelVersion>4.0.0</modelVersion>" in content


def test_jsp_to_thymeleaf_conversion():
    """Test conversion of JSP pages to Thymeleaf templates"""
    create_spring_structure(OUTPUT_DIR)
    
    # Migrate JSP files
    migrate_jsp_to_thymeleaf(SAMPLE_APP, OUTPUT_DIR)
    
    # Verify list template
    list_template = OUTPUT_DIR / "src/main/resources/templates/customer/list.html"
    assert list_template.exists(), "List template not found"
    
    content = list_template.read_text()
    # Check Thymeleaf specific content
    assert 'xmlns:th="http://www.thymeleaf.org"' in content
    
    # Verify form template
    form_template = OUTPUT_DIR / "src/main/resources/templates/customer/form.html"
    assert form_template.exists(), "Form template not found"
    
    content = form_template.read_text()
    # Check form specific content
    assert 'xmlns:th="http://www.thymeleaf.org"' in content

def test_form_to_dto_conversion():
    """Test conversion of Struts Forms to Spring DTOs"""
    # Create Spring structure first
    create_spring_structure(OUTPUT_DIR)
    
    # Migrate forms
    migrate_form_beans(SAMPLE_APP, OUTPUT_DIR)
    
    # Verify DTO
    dto_file = OUTPUT_DIR / "src/main/java/com/example/application/model/CustomerDTO.java"
    assert dto_file.exists(), "DTO file not found"
    
    content = dto_file.read_text()
    # Check validation annotations
    assert "validation.constraints" in content, "Missing validation imports"
    assert "@NotBlank" in content, "Missing @NotBlank validation"
    assert "@Email" in content, "Missing @Email validation"
    assert "extends ActionForm" not in content, "Should not extend ActionForm"

def test_service_conversion():
    """Test conversion of Struts service layer to Spring services"""
    # Create Spring structure first
    create_spring_structure(OUTPUT_DIR)
    
    # Migrate services
    migrate_service_layer(SAMPLE_APP, OUTPUT_DIR)
    
    # Verify service
    service_file = OUTPUT_DIR / "src/main/java/com/example/application/service/CustomerService.java"
    assert service_file.exists(), "Service file not found"
    
    content = service_file.read_text()
    # Check Spring annotations
    assert "@Service" in content, "Missing @Service annotation"
    assert "@Transactional" in content, "Missing @Transactional annotation"
    assert "@Autowired" in content, "Missing @Autowired annotation"
    assert "ResponseEntity" not in content, "Service should not use ResponseEntity"

def test_controller_conversion():
    """Test conversion of Struts Actions to Spring Controllers"""
    # Create Spring structure first
    create_spring_structure(OUTPUT_DIR)
    
    # Convert actions
    convert_actions_to_controllers(SAMPLE_APP, OUTPUT_DIR)
    
    # Verify controller
    controller_file = OUTPUT_DIR / "src/main/java/com/example/application/controller/CustomerController.java"
    assert controller_file.exists(), "Controller file not found"
    
    content = controller_file.read_text()
    # Check Spring annotations and patterns
    assert "@RestController" in content, "Missing @RestController annotation"
    assert "@GetMapping" in content, "Missing @GetMapping annotation"
    assert "ResponseEntity" in content, "Missing ResponseEntity return type"
    assert "@Valid" in content, "Missing @Valid annotation"
    assert "ActionForm" not in content, "Should not use ActionForm"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-x"]) 