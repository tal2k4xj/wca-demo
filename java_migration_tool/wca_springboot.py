from rich.console import Console
from rich.markdown import Markdown
import typer
from wca_backend import call_wca_api, stream_response
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
import os
import sys
import argparse

load_dotenv()
console = Console()
app = typer.Typer(help="Java code review and upgrade tool")

def check_api_key():
    """Check if IBM Cloud API key is set"""
    api_key = os.getenv("IAM_APIKEY")
    if not api_key:
        console.print("[red]Error: IAM_APIKEY not found in environment variables[/red]")
        console.print("Please set your IBM Cloud API key in .env file:")
        console.print("IAM_APIKEY=your_api_key_here")
        raise typer.Exit(1)
    return api_key

def review_java(java: str) -> str:
    """Generate review for Java upgrade and migration"""
    # Parse Java code into sections based on classes/methods
    sections = []
    try:
        # Simple class-based sectioning
        current_class = ""
        current_content = []
        
        for line in java.split('\n'):
            if line.strip().startswith("public class") or line.strip().startswith("public interface"):
                if current_class:
                    sections.append((current_class, "\n".join(current_content)))
                current_class = line.strip().split()[2]  # Get class name
                current_content = [line]
            else:
                current_content.append(line)
        
        if current_class:
            sections.append((current_class, "\n".join(current_content)))
            
        if not sections:
            sections = [("Main", java)]
    except Exception as e:
        console.print(f"[yellow]Warning: Error parsing Java code into sections: {str(e)}[/yellow]")
        sections = [("Main", java)]
    
    all_reviews = []
    
    with console.status("[bold blue]Reviewing Java code...", spinner="dots") as status:
        for section_name, section_content in sections:
            status.update(f"[bold blue]Processing {section_name}...")
            
            prompt = f"""Review this Java code section for modernization and migration:
- Identify upgrade opportunities
- Check for deprecated APIs and patterns
- Suggest modern alternatives
- Review for design patterns and best practices
<<SYS>>
section: {section_name}
code: `{section_content}`
<</SYS>>
Generate review in table format with columns: Component, Current Implementation, Recommended Changes, Priority (High/Medium/Low)."""
            
            payload = {
                "message_payload": {
                    "messages": [{"content": prompt, "role": "USER"}]
                }
            }
            
            try:
                response = call_wca_api(payload)
                section_review = stream_response(response, action=f"Processing {section_name}")
                
                if section_review:
                    all_reviews.append(f"## {section_name}\n\n{section_review}\n")
                
            except Exception as e:
                console.print(f"[red]Error processing {section_name}: {str(e)}[/red]")
                all_reviews.append(f"## {section_name}\n\n*Error processing this section: {str(e)}*\n")
    
    final_review = "# Java Code Review\n\n" + "\n".join(all_reviews)
    
    # Generate summary with modernization recommendations
    summary_prompt = """Summarize the key modernization points:
- Identify major upgrade opportunities
- List required framework/library migrations
- Suggest architectural improvements
- Estimate effort and complexity
<<SYS>>
review: `{final_review}`
<</SYS>>
Generate summary in table format with columns: Category, Recommendations, Priority, Effort Estimate."""
    
    try:
        summary_payload = {
            "message_payload": {
                "messages": [{"content": summary_prompt, "role": "USER"}]
            }
        }
        summary_response = call_wca_api(summary_payload)
        summary = stream_response(summary_response, action="Generating summary")
        
        if summary:
            final_review = f"# Summary\n\n{summary}\n\n# Detailed Review\n\n{final_review}"
    except Exception as e:
        console.print(f"[red]Error generating summary: {str(e)}[/red]")
    
    return final_review

def upgrade_java(java: str) -> str:
    """Upgrade Java code to modern Java"""
    prompt = f"""Upgrade this Java code to modern Java:
- Focus on preserving business logic and data structures
- Maintain original program flow and validations
- Keep business rules intact
- Dont be lazy, please convert the Java provided to modern Java implementation in detail.
<<SYS>>
java: `{java}`
<</SYS>>
Generate Java code implementation with comments explaining key business logic.
"""

    payload = {
        "message_payload": {
            "messages": [{"content": prompt, "role": "USER"}]
        }
    }
    response = call_wca_api(payload)
    return stream_response(response, action="Upgrading Java")

def read_java_file(java_file: Path) -> str:
    """Read and return contents of Java file"""
    try:
        return java_file.read_text()
    except Exception as e:
        console.print(f"[red]Error reading Java file: {e}[/red]")
        raise typer.Exit(1)

@app.command()
def review(
    java_file: Path = typer.Argument(..., help="Java source file to review", exists=True),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file for review"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed progress")
):
    """Review Java code and provide Java conversion suggestions"""
    try:
        api_key = check_api_key()
        console.print(f"[green]API key found: {api_key[:4]}...{api_key[-4:]}[/green]")
        
        console.print(f"[yellow]Reading Java file: {java_file}[/yellow]")
        java = read_java_file(java_file)
        console.print(f"[green]Successfully read {len(java)} characters from file[/green]")
        
        if verbose:
            console.print("[yellow]First 100 characters of Java code:[/yellow]")
            console.print(java[:100] + "...")
        
        result = review_java(java)
        
        if output:
            console.print(f"[yellow]Saving review to {output}[/yellow]")
            output.write_text(result)
            console.print(f"[green]Review saved to {output}[/green]")
        else:
            console.print("\n[bold]Review Result:[/bold]")
            console.print(Markdown(result))
            
        return result
        
    except Exception as e:
        console.print(f"[red]Error in review command: {str(e)}[/red]")
        if verbose:
            import traceback
            console.print("[red]Traceback:[/red]")
            console.print(traceback.format_exc())
        raise typer.Exit(1)

@app.command()
def upgrade(
    java_file: Path = typer.Argument(..., help="Java source file to upgrade", exists=True),
    output: Path = typer.Option(None, "--output", "-o", help="Output Java file")
):
    """Upgrade Java code to modern Java"""
    check_api_key()
    java = read_java_file(java_file)
    
    java_code = upgrade_java(java)
    
    if output:
        output.write_text(java_code)
        console.print(f"[green]Upgraded Java code saved to {output}[/green]")
    return java_code

@app.command()
def migrate_ejb_to_pojo(
    java_file: Path = typer.Argument(..., help="EJB source file to migrate", exists=True),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output Java file")
):
    """Migrate EJB to POJO"""
    check_api_key()
    console.print("[blue]Starting EJB to POJO migration...[/blue]")
    
    try:
        source_code = read_java_file(java_file)
        console.print(f"[green]Successfully read source file ({len(source_code)} bytes)[/green]")
        
        prompt = create_pojo_migration_prompt(source_code)
        console.print("[yellow]Preparing POJO migration...[/yellow]")
        
        payload = {"message_payload": {"messages": [{"content": prompt, "role": "USER"}]}}
        response = call_wca_api(payload)
        migrated_code = stream_response(response, action="Migrating to POJO")
        
        # Validate the migrated code
        if "class" not in migrated_code.lower() and "interface" not in migrated_code.lower():
            console.print("[red]Warning: Generated code might not be valid Java[/red]")
        
        if "ejb" in migrated_code.lower():
            console.print("[yellow]Warning: Generated POJO might still contain EJB references[/yellow]")
        
        if "@Stateless" in migrated_code or "@Stateful" in migrated_code:
            console.print("[yellow]Warning: Generated POJO contains EJB annotations[/yellow]")
        
        # Show migration summary
        console.print("\n[bold]POJO Migration Summary:[/bold]")
        console.print("1. Original file size: {} bytes".format(len(source_code)))
        console.print("2. Generated code size: {} bytes".format(len(migrated_code)))
        console.print("3. Major changes:")
        
        changes = []
        if "@Entity" in migrated_code and "@Entity" not in source_code:
            changes.append("- Added JPA annotations")
        if "@Inject" in migrated_code and "@Inject" not in source_code:
            changes.append("- Added CDI annotations")
        if "@Transactional" in migrated_code and "@Transactional" not in source_code:
            changes.append("- Added transaction management")
        
        for change in changes:
            console.print(change)
        
        if output:
            output.write_text(migrated_code)
            console.print(f"[green]Migrated code saved to {output}[/green]")
        else:
            print(migrated_code)
            
    except Exception as e:
        console.print(f"[red]Error during migration: {str(e)}[/red]")
        raise typer.Exit(1)

@app.command()
def migrate_gradle_to_maven(
    gradle_file: Path = typer.Argument(..., help="Gradle build file to migrate", exists=True),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output pom.xml file")
):
    """Migrate Gradle build file to Maven pom.xml"""
    check_api_key()
    console.print("[blue]Starting Gradle to Maven migration...[/blue]")
    
    try:
        source_code = read_java_file(gradle_file)
        console.print(f"[green]Successfully read source file ({len(source_code)} bytes)[/green]")
        
        prompt = create_maven_migration_prompt(source_code)
        console.print("[yellow]Preparing Maven migration...[/yellow]")
        
        payload = {"message_payload": {"messages": [{"content": prompt, "role": "USER"}]}}
        response = call_wca_api(payload)
        migrated_code = stream_response(response, action="Migrating to Maven")
        
        # Validate the migrated code
        if "<?xml" not in migrated_code:
            console.print("[red]Warning: Generated code might not be valid XML[/red]")
        
        if "<project" not in migrated_code:
            console.print("[red]Warning: Generated code might not be a valid POM file[/red]")
        
        # Show migration summary
        console.print("\n[bold]Maven Migration Summary:[/bold]")
        console.print("1. Original file size: {} bytes".format(len(source_code)))
        console.print("2. Generated POM size: {} bytes".format(len(migrated_code)))
        console.print("3. Major components:")
        
        changes = []
        if "<dependencies>" in migrated_code:
            changes.append("- Dependencies section")
        if "<properties>" in migrated_code:
            changes.append("- Properties section")
        if "<plugins>" in migrated_code:
            changes.append("- Plugins section")
        if "<profiles>" in migrated_code:
            changes.append("- Profiles section")
        
        for change in changes:
            console.print(change)
        
        if output:
            output.write_text(migrated_code)
            console.print(f"[green]Migrated POM saved to {output}[/green]")
        else:
            print(migrated_code)
            
    except Exception as e:
        console.print(f"[red]Error during migration: {str(e)}[/red]")
        raise typer.Exit(1)

def get_commands():
    return [
        {
            "name": "java_api_migration",
            "description": "Migrate Java API implementations between different specifications",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_api": {
                        "type": "string",
                        "description": "Source API specification",
                        "enum": ["EJB2.0"]
                    },
                    "target_api": {
                        "type": "string",
                        "description": "Target API specification",
                        "enum": ["POJO"]
                    },
                    "file_path": {
                        "type": "string",
                        "description": "Path to the Java source file"
                    }
                },
                "required": ["source_api", "target_api", "file_path"],
                "additionalProperties": False,
                "dependencies": {
                    "source_api": {
                        "oneOf": [
                            {
                                "properties": {
                                    "source_api": {"enum": ["EJB2.0"]},
                                    "target_api": {"enum": ["POJO"]}
                                }
                            }
                        ]
                    }
                }
            }
        }
    ]

def handle_command(command_name, parameters, context):
    if command_name == "java_api_migration":
        return handle_java_api_migration(parameters, context)
    return None

def create_pojo_migration_prompt(source_code):
    return f"""You are a senior Java developer. Convert this EJB code to POJO following these specific steps:
1. Remove EJB-specific code:
    - Remove EJB interfaces (Home, Remote, Local)
    - Remove EJB lifecycle methods (ejbCreate, ejbActivate, etc.)
    - Remove EJB annotations (@Stateless, @Stateful, etc.)
    
2. Create clean POJO structure:
    - Extract business interface (if not exists)
    - Create implementation class
    - Add Spring/CDI annotations (@Service, @Inject)
    - Implement proper constructors
    
3. Handle transactions:
    - Replace container-managed transactions with @Transactional
    - Add proper transaction attributes (readOnly, propagation)
    - Update exception handling (remove EJB-specific exceptions)
    - Add proper transaction boundaries
    
4. Update persistence:
    - Update entity access (use JPA instead of EJB entity beans)
    - Add proper JPA annotations (@Entity, @Table, etc.)
    - Update query methods (use JPA queries)
    - Handle relationships properly
    
5. Dependency Injection:
    - Replace JNDI lookups with @Inject/@Autowired
    - Add constructor injection for required dependencies
    - Handle service references with proper DI
    - Add proper scoping annotations

6. Additional modernization:
    - Add proper logging
    - Update exception handling
    - Add validation annotations if needed
    - Implement proper equals/hashCode if needed

<<SYS>>
Original Java code:
`{source_code}`
<</SYS>>

Generate complete POJO implementation following these requirements:
1. Preserve all business logic exactly as is
2. Use modern Java features (Optional, Stream API if applicable)
3. Add proper JavaDoc comments
4. Include all necessary imports
5. Generate code in Java language
6. Maintain proper package structure

Respond only with the complete Java code implementation.
"""

def create_maven_migration_prompt(source_code):
    return f"""You are a senior Java developer. Convert this Gradle build file to Maven pom.xml following these steps:
1. Project Information:
- Extract group, artifact, and version info
- Set appropriate packaging type
- Configure Java version
- ALWAYS provide DTD for the pom.xml file
    
2. Dependencies:
- Convert Gradle dependency configurations to Maven scopes
- Map implementation to compile/runtime
- Map testImplementation to test
- Handle compileOnly dependencies
- Preserve versions
    
3. Plugins:
- Convert Gradle plugins to Maven equivalents
- Configure plugin executions
- Map Spring Boot plugin configuration
- Handle test configurations
    
4. Properties:
- Extract and convert Gradle properties
- Set appropriate Maven properties
- Configure encoding and Java version
    
5. Build Configuration:
- Convert Gradle tasks to Maven phases/goals
- Handle custom task configurations
- Configure resource handling
- Set up test execution

<<SYS>>
Gradle build file:
`{source_code}`
<</SYS>>

Generate complete Maven pom.xml following these requirements:
1. Use proper XML formatting
2. Include all necessary dependencies
3. Configure all required plugins
4. Maintain build lifecycle configuration
5. Add appropriate comments

Respond only with the complete pom.xml content.
"""

@app.command()
def migrate_structs(
    source_dir: str = typer.Argument(..., help="Source directory containing Struts application"),
    output_dir: str = typer.Option(
        "output/spring-app",
        "--output", 
        "-o", 
        help="Output directory for Spring Boot application"
    )
):
    """Migrate Struts application to SpringBoot"""
    try:
        console.print("[blue]Starting Struts to SpringBoot migration...[/blue]")
        
        # Convert input paths to Path objects
        source_path = Path(source_dir)
        output_path = Path(str(output_dir))
        
        # 1. Identify Struts configuration files
        struts_config = list(source_path.glob("**/struts-config.xml"))
        if not struts_config:
            console.print("[red]No struts-config.xml found. Please ensure you're in a Struts project directory.[/red]")
            raise typer.Exit(code=1)
        
        try:
            # Create output directory and its parents
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Create necessary subdirectories
            (output_path / "src/main/java/com/example/application/controller").mkdir(parents=True, exist_ok=True)
            (output_path / "src/main/java/com/example/application/model").mkdir(parents=True, exist_ok=True)
            (output_path / "src/main/java/com/example/application/service").mkdir(parents=True, exist_ok=True)
            (output_path / "src/main/resources").mkdir(parents=True, exist_ok=True)
            
            console.print(f"[yellow]Output directory: {output_path}[/yellow]")
        except Exception as e:
            console.print(f"[red]Error creating directory structure: {str(e)}[/red]")
            raise typer.Exit(code=1)
        
        try:
            # 2. Create SpringBoot basic structure
            create_spring_structure(output_path)
            console.print("[green]Created Spring Boot project structure[/green]")
        except Exception as e:
            console.print(f"[red]Error creating Spring Boot structure: {str(e)}[/red]")
            raise typer.Exit(code=1)
        
        try:
            # 3. Convert Struts Actions to Controllers
            convert_actions_to_controllers(source_path, output_path)
            console.print("[green]Converted Actions to Controllers[/green]")
        except Exception as e:
            console.print(f"[red]Error converting Actions to Controllers: {str(e)}[/red]")
            raise typer.Exit(code=1)
        
        try:
            # 4. Migrate form beans and DTOs
            migrate_form_beans(source_path, output_path)
            console.print("[green]Migrated Form beans and DTOs[/green]")
        except Exception as e:
            console.print(f"[red]Error migrating Form beans: {str(e)}[/red]")
            raise typer.Exit(code=1)
        
        try:
            # 5. Migrate service layer
            migrate_service_layer(source_path, output_path)
            console.print("[green]Migrated Service layer[/green]")
        except Exception as e:
            console.print(f"[red]Error migrating Service layer: {str(e)}[/red]")
            raise typer.Exit(code=1)
        
        try:
            # 6. Migrate model classes
            migrate_model_classes(source_path, output_path)
            console.print("[green]Migrated Model classes[/green]")
        except Exception as e:
            console.print(f"[red]Error migrating Model classes: {str(e)}[/red]")
            raise typer.Exit(code=1)
        
        try:
            # 7. Update dependencies in pom.xml
            update_pom_dependencies(source_path, output_path)
            console.print("[green]Updated project dependencies[/green]")
        except Exception as e:
            console.print(f"[red]Error updating dependencies: {str(e)}[/red]")
            raise typer.Exit(code=1)
        
        try:
            # 8. Migrate JSP pages to Thymeleaf
            migrate_jsp_to_thymeleaf(source_path, output_path)
            console.print("[green]Migrated JSP pages to Thymeleaf[/green]")
        except Exception as e:
            console.print(f"[red]Error migrating JSP to Thymeleaf: {str(e)}\nTraceback: {e.__traceback__}[/red]")
            raise typer.Exit(code=1)
        
        console.print("[green]Struts to SpringBoot migration completed successfully![/green]")
        console.print(f"[blue]Migration output saved to: {output_path}[/blue]")
        
        return output_path  # Return the output path for testing
        
    except typer.Exit:
        raise  # Re-raise Typer exits
    except Exception as e:
        console.print(f"[red]Unexpected error during migration:[/red]")
        console.print(f"[red]Error type: {type(e).__name__}[/red]")
        console.print(f"[red]Error message: {str(e)}[/red]")
        console.print(f"[red]Traceback: {e.__traceback__}[/red]")
        raise typer.Exit(code=1)

def create_spring_structure(output_dir: Path):
    """Create basic SpringBoot project structure"""
    base_package = output_dir / "src/main/java/com/example/application"
    base_package.joinpath("controller").mkdir(parents=True, exist_ok=True)
    base_package.joinpath("model").mkdir(parents=True, exist_ok=True)
    base_package.joinpath("service").mkdir(parents=True, exist_ok=True)
    base_package.joinpath("repository").mkdir(parents=True, exist_ok=True)
    output_dir.joinpath("src/main/resources").mkdir(parents=True, exist_ok=True)

def extract_java_code(response: str) -> str:
    """Extract Java code from WCA API response"""
    # Remove markdown code block markers
    code = response.replace("```java", "").replace("```", "")
    
    # Remove any leading/trailing whitespace
    code = code.strip()
    
    # Remove any comments about Watson assistance
    lines = code.split("\n")
    lines = [line for line in lines if not line.strip().startswith("// Assisted by")]
    
    # Join lines back together
    code = "\n".join(lines)
    
    return code

def convert_actions_to_controllers(source_dir: Path, output_dir: Path):
    """Convert Struts Actions to Spring Controllers"""
    action_files = source_dir.glob("**/action/*.java")
    
    for action_file in action_files:
        content = action_file.read_text()
        
        prompt = f"""Convert this Struts Action to a Spring Boot REST Controller.

Requirements:
1. Package and imports:
   - Use proper Spring Boot imports
   - Add validation imports
   - Add REST annotations

2. Class structure:
   - Convert Action class to Controller
   - Add @RestController annotation
   - Add @RequestMapping for base path
   - Add proper constructor injection

3. Method conversion:
   - Convert execute() to proper HTTP methods
   - Use @GetMapping, @PostMapping, etc.
   - Handle path variables and request params
   - Return ResponseEntity with proper types
   - Add proper error handling

4. Form handling:
   - Convert ActionForm to @Valid DTO
   - Use proper validation annotations
   - Handle form submission properly
   - Return proper response status

<<SYS>>
Original Struts Action:
```java
{content}
```
<</SYS>>

Generate a complete Spring Boot Controller that follows REST principles and includes proper error handling."""

        # Call WCA API
        payload = {"message_payload": {"messages": [{"content": prompt, "role": "USER"}]}}
        response = call_wca_api(payload)
        response_content = stream_response(response, action="Converting Action to Controller")
        controller_content = extract_java_code(response_content)
        
        # Force package declaration if not present
        if not controller_content.strip().startswith("package"):
            controller_content = "//" + controller_content
        
        # Create new controller file
        controller_name = action_file.stem.replace("Action", "Controller")
        controller_path = output_dir / f"src/main/java/com/example/application/controller/{controller_name}.java"
        controller_path.parent.mkdir(parents=True, exist_ok=True)
        controller_path.write_text(controller_content)

def migrate_form_beans(source_dir: Path, output_dir: Path):
    """Migrate Struts form beans and DTOs to Spring DTOs"""
    # Migrate form beans
    form_files = source_dir.glob("**/form/*.java")
    dto_files = source_dir.glob("**/dto/*.java")
    
    for file in list(form_files) + list(dto_files):
        content = file.read_text()
        
        prompt = f"""Convert this Struts Form/DTO to a Spring Boot DTO.
Requirements:
1. Package and imports:
   - Use package com.example.application.model
   - Use javax.validation.constraints.* (NOT jakarta)

2. Add validation annotations:
   - @NotNull for required fields
   - @NotBlank for required strings
   - @Size for string length constraints
   - @Email for email fields
   - @Pattern for specific formats
   - @Min/@Max for numeric constraints

3. Add validation messages for each constraint
4. Remove any Struts-specific code
5. Keep all business fields and methods
6. Add proper getters/setters
7. Add proper toString/equals/hashCode
<<SYS>>
Original Form/DTO:
```java
{content}
```
<</SYS>>

Generate a complete DTO with all fields and validations from the original form/model.
"""

        # Call WCA API
        payload = {"message_payload": {"messages": [{"content": prompt, "role": "USER"}]}}
        response = call_wca_api(payload)
        response_content = stream_response(response, action="Converting to DTO")
        dto_content = extract_java_code(response_content)
        
        # Force package declaration if not present
        if not dto_content.strip().startswith("package"):
            dto_content = "//" + dto_content
        
        # Create new DTO file - Fix naming logic
        if file.name.endswith("Form.java"):
            # For Form files, replace Form with DTO
            dto_name = file.name.replace("Form.java", "DTO.java")
        elif file.name.endswith("DTO.java"):
            # For DTO files, keep the name as is
            dto_name = file.name
        else:
            # For other files, append DTO
            dto_name = file.stem + "DTO.java"
            
        dto_path = output_dir / "src/main/java/com/example/application/model" / dto_name
        dto_path.write_text(dto_content)

def migrate_service_layer(source_dir: Path, output_dir: Path):
    """Migrate service layer to Spring Boot"""
    # Look for service classes in multiple possible locations
    service_patterns = [
        "**/service/*.java",
        "**/delegate/*.java",
        "**/business/*.java",
        "**/action/*Action.java"  # Actions often contain business logic
    ]
    
    for pattern in service_patterns:
        service_files = source_dir.glob(pattern)
        for service_file in service_files:
            content = service_file.read_text()
            
            prompt = f"""Extract and convert business logic to a Spring Boot service.
Requirements:
1. Package and structure:
   - Use package com.example.application.service
   - Extract business logic from Actions/Delegates into Service methods
   - Keep method names meaningful and business-focused
   - Group related operations together

2. Spring annotations:
   - @Service for the class
   - @Autowired for dependencies
   - @Transactional for data operations
   - @PreAuthorize for security if needed

3. Method structure:
   - Extract business logic from execute() methods
   - Convert ActionForm parameters to DTOs
   - Handle form validation logic
   - Preserve business rules and validations
   - Return domain objects (not ActionForwards)

4. Error handling:
   - Convert ActionErrors to exceptions
   - Add proper exception classes
   - Use meaningful error messages
   - Handle null cases properly

5. Dependencies:
   - Inject required repositories
   - Use constructor injection
   - Remove Struts-specific dependencies
<<SYS>>
Original Struts class:
```java
{content}
```
<</SYS>>

Generate a Spring Service that encapsulates all the business logic from the original class."""

            # Call WCA API
            payload = {"message_payload": {"messages": [{"content": prompt, "role": "USER"}]}}
            response = call_wca_api(payload)
            response_content = stream_response(response, action="Converting Service")
            service_content = extract_java_code(response_content)
            
            # Force package declaration if not present
            if not service_content.strip().startswith("package"):
                service_content = "//" + service_content
            
            # Create new service file
            service_path = output_dir / "src/main/java/com/example/application/service" / service_file.name
            service_path.write_text(service_content)

def migrate_model_classes(source_dir: Path, output_dir: Path):
    """Migrate model classes to Spring Boot entities"""
    model_files = source_dir.glob("**/model/*.java")
    for model_file in model_files:
        content = model_file.read_text()
        
        # Create prompt for model conversion
        prompt = f"""Convert this model class to a Spring Boot entity:
- Add proper JPA annotations if needed
- Add validation annotations
- Maintain all fields and methods
- Add proper equals/hashCode/toString
- Add proper JavaDoc

<<SYS>>
Original model:
`{content}`
<</SYS>>

Generate complete Spring entity implementation.
"""

        # Call WCA API
        payload = {"message_payload": {"messages": [{"content": prompt, "role": "USER"}]}}
        response = call_wca_api(payload)
        response_content = stream_response(response, action="Converting Model")
        model_content = extract_java_code(response_content)
        
        # Create new model file
        model_path = output_dir / "src/main/java/com/example/application/model" / model_file.name
        model_path.write_text(model_content)

def update_pom_dependencies(source_dir: Path, output_dir: Path):
    """Update pom.xml with Spring Boot dependencies"""
    pom_template = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.7.0</version>
    </parent>
    <groupId>com.example</groupId>
    <artifactId>application</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
    </dependencies>
</project>"""
    
    pom_path = output_dir / "pom.xml"
    pom_path.write_text(pom_template)

def migrate_jsp_to_html(source_dir: Path, output_dir: Path):
    """Convert JSP files to HTML templates"""
    jsp_files = source_dir.glob("**/webapp/pages/**/*.jsp")
    
    for jsp_file in jsp_files:
        content = jsp_file.read_text()
        
        prompt = f"""Convert this JSP page to a modern HTML template.
Requirements:
1. Convert to modern HTML5
2. Remove all JSP-specific tags and directives
3. Use semantic HTML elements
4. Add proper CSS classes for styling
5. Keep the same functionality and structure
6. Make it responsive
7. Add Bootstrap classes if appropriate

<<SYS>>
Original JSP:
```jsp
{content}
```
<</SYS>>

Generate only the HTML template, no explanations.
"""

        # Call WCA API
        payload = {"message_payload": {"messages": [{"content": prompt, "role": "USER"}]}}
        response = call_wca_api(payload)
        response_content = stream_response(response, action="Converting JSP to HTML")
        html_content = extract_html_code(response_content)
        
        # Create new HTML file
        relative_path = jsp_file.relative_to(source_dir / "src/main/webapp/pages")
        html_path = output_dir / "src/main/resources/templates" / relative_path.with_suffix(".html")
        html_path.parent.mkdir(parents=True, exist_ok=True)
        html_path.write_text(html_content)

def extract_html_code(response: str) -> str:
    """Extract HTML code from WCA API response"""
    # Remove markdown code block markers
    code = response.replace("```html", "").replace("```", "")
    
    # Remove any leading/trailing whitespace
    code = code.strip()
    
    return code

def migrate_jsp_to_thymeleaf(source_dir: Path, output_dir: Path):
    """Migrate JSP pages to Thymeleaf templates"""
    # First convert JSP to HTML
    migrate_jsp_to_html(source_dir, output_dir)
    
    # Then convert HTML to Thymeleaf
    html_files = list(output_dir.glob("**/templates/**/*.html"))
    
    if not html_files:
        console.print("[yellow]No HTML files found to convert to Thymeleaf[/yellow]")
        return
        
    console.print(f"[blue]Found {len(html_files)} HTML files to convert[/blue]")
    
    for html_file in html_files:
        try:
            content = html_file.read_text()
            relative_path = html_file.relative_to(output_dir / "src/main/resources/templates")
            console.print(f"[blue]Converting {relative_path} to Thymeleaf...[/blue]")
            
            # Determine template type based on path/filename
            template_type = "list" if "list" in html_file.stem else "form"
            
            if template_type == "list":
                prompt = create_list_template_prompt(content)
            else:
                prompt = create_form_template_prompt(content)

            # Call WCA API
            payload = {"message_payload": {"messages": [{"content": prompt, "role": "USER"}]}}
            response = call_wca_api(payload)
            response_content = stream_response(response, action=f"Converting {relative_path} to Thymeleaf")
            template_content = extract_html_code(response_content)
            
            # Update the file with Thymeleaf content
            html_file.write_text(template_content)
            console.print(f"[green]Successfully converted {relative_path}[/green]")
            
        except Exception as e:
            console.print(f"[red]Error converting {html_file}: {str(e)}[/red]")
            raise

def create_list_template_prompt(content: str) -> str:
    """Create prompt for list template conversion"""
    return f"""Convert this HTML template to a Thymeleaf list template.

Requirements:
1. List-specific conversions:
   - Add table structure with headers
   - Use th:each for iteration
   - Display item properties with th:text
   - Add links for actions (edit/delete)
   - Handle empty list case
   - Add sorting if applicable

2. Common Thymeleaf requirements:
   - Add xmlns:th="http://www.thymeleaf.org"
   - Convert all expressions to Thymeleaf syntax
   - Add proper error handling
   - Maintain HTML structure

<<SYS>>
Original HTML:
```html
{content}
```
<</SYS>>

Generate a complete Thymeleaf list template.
"""

def create_form_template_prompt(content: str) -> str:
    """Create prompt for form template conversion"""
    return f"""Convert this HTML template to a Thymeleaf form template.

Requirements:
1. Form-specific conversions:
   - Add th:object for form binding
   - Use th:field for inputs
   - Add validation error display
   - Handle form submission
   - Add CSRF token
   - Proper button handling

2. Common Thymeleaf requirements:
   - Add xmlns:th="http://www.thymeleaf.org"
   - Convert all expressions to Thymeleaf syntax
   - Add proper error handling
   - Maintain HTML structure

<<SYS>>
Original HTML:
```html
{content}
```
<</SYS>>

Generate a complete Thymeleaf form template.
"""

if __name__ == "__main__":
    app()