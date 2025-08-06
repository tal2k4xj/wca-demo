from rich.console import Console
from rich.markdown import Markdown
import typer
from wca_backend import call_wca_api, stream_response
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
import os
import sys

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
def migrate_jaxrpc_to_jaxws(
    java_file: Path = typer.Argument(..., help="JAX-RPC source file to migrate", exists=True),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output Java file")
):
    """Migrate JAX-RPC web service to JAX-WS"""
    check_api_key()
    console.print("[blue]Starting JAX-RPC to JAX-WS migration...[/blue]")
    
    try:
        source_code = read_java_file(java_file)
        console.print(f"[green]Successfully read source file ({len(source_code)} bytes)[/green]")
        
        prompt = create_jaxws_migration_prompt(source_code)
        console.print("[yellow]Preparing JAX-WS migration...[/yellow]")
        
        payload = {"message_payload": {"messages": [{"content": prompt, "role": "USER"}]}}
        response = call_wca_api(payload)
        migrated_code = stream_response(response, action="Migrating to JAX-WS")
        
        if output:
            output.write_text(migrated_code)
            console.print(f"[green]Migrated code saved to {output}[/green]")
        else:
            print(migrated_code)
            
    except Exception as e:
        console.print(f"[red]Error during migration: {str(e)}[/red]")
        raise typer.Exit(1)

@app.command()
def migrate_jsch_to_j2ssh(
    java_file: Path = typer.Argument(..., help="JSch source file to migrate", exists=True),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output Java file")
):
    """Migrate JSch SFTP implementation to J2SSH"""
    check_api_key()
    console.print("[blue]Starting JSch to J2SSH migration...[/blue]")
    
    try:
        source_code = read_java_file(java_file)
        console.print(f"[green]Successfully read source file ({len(source_code)} bytes)[/green]")
        
        prompt = create_j2ssh_migration_prompt(source_code)
        console.print("[yellow]Preparing J2SSH migration...[/yellow]")
        
        payload = {"message_payload": {"messages": [{"content": prompt, "role": "USER"}]}}
        response = call_wca_api(payload)
        migrated_code = stream_response(response, action="Migrating to J2SSH")
        
        if output:
            output.write_text(migrated_code)
            console.print(f"[green]Migrated code saved to {output}[/green]")
        else:
            print(migrated_code)
            
    except Exception as e:
        console.print(f"[red]Error during migration: {str(e)}[/red]")
        raise typer.Exit(1)

@app.command()
def migrate_was_to_liberty(
    java_file: Path = typer.Argument(..., help="WebSphere scheduler file to migrate", exists=True),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output Java file")
):
    """Migrate WebSphere scheduler to Liberty"""
    check_api_key()
    console.print("[blue]Starting WebSphere to Liberty migration...[/blue]")
    
    try:
        source_code = read_java_file(java_file)
        console.print(f"[green]Successfully read source file ({len(source_code)} bytes)[/green]")
        
        prompt = create_liberty_migration_prompt(source_code)
        console.print("[yellow]Preparing Liberty migration...[/yellow]")
        
        payload = {"message_payload": {"messages": [{"content": prompt, "role": "USER"}]}}
        response = call_wca_api(payload)
        migrated_code = stream_response(response, action="Migrating to Liberty")
        
        if output:
            output.write_text(migrated_code)
            console.print(f"[green]Migrated code saved to {output}[/green]")
        else:
            print(migrated_code)
            
    except Exception as e:
        console.print(f"[red]Error during migration: {str(e)}[/red]")
        raise typer.Exit(1)

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
                        "enum": ["JAX-RPC", "JSch", "WAS-Scheduler", "EJB2.0"]
                    },
                    "target_api": {
                        "type": "string",
                        "description": "Target API specification",
                        "enum": ["JAX-WS", "J2SSH", "Liberty-Scheduler", "POJO"]
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
                                    "source_api": {"enum": ["JAX-RPC"]},
                                    "target_api": {"enum": ["JAX-WS"]}
                                }
                            },
                            {
                                "properties": {
                                    "source_api": {"enum": ["JSch"]},
                                    "target_api": {"enum": ["J2SSH"]}
                                }
                            },
                            {
                                "properties": {
                                    "source_api": {"enum": ["WAS-Scheduler"]},
                                    "target_api": {"enum": ["Liberty-Scheduler"]}
                                }
                            },
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

def create_jaxws_migration_prompt(source_code):
    return f"""Convert this JAX-RPC web service to JAX-WS following these specific steps:
1. Update imports:
    - Remove javax.xml.rpc.* imports
    - Add javax.jws.WebService
    - Add javax.jws.WebMethod if needed
    
2. Update service interface:
    - Add @WebService annotation with proper name and targetNamespace
    - Remove extends Remote if present
    - Update method signatures to remove RemoteException
    
3. Update implementation class:
    - Add @WebService(endpointInterface="...") annotation
    - Remove ServiceLifecycle implementation
    - Remove init/destroy methods
    - Update exception handling
    
4. Maintain business logic intact
<<SYS>>
Original code:
`{source_code}`
<</SYS>>
Generate complete JAX-WS implementation maintaining the same business logic.
"""

def create_j2ssh_migration_prompt(source_code):
    return f"""Convert this JSch SFTP implementation to J2SSH Maverick following these steps:
1. Update imports:
    - Remove com.jcraft.jsch.*
    - Add com.sshtools.j2ssh.*
    - Add com.sshtools.j2ssh.sftp.*
    
2. Update connection handling:
    - Replace JSch with SshClient
    - Update authentication method
    - Handle connection properties
    
3. Update SFTP operations:
    - Replace ChannelSftp with SftpClient
    - Update file transfer methods
    - Maintain error handling
    
4. Preserve all functionality:
    - Keep connection pooling if present
    - Maintain retry logic
    - Keep security configurations
<<SYS>>
Original code:
`{source_code}`
<</SYS>>
Generate complete J2SSH implementation with equivalent functionality.
"""

def create_liberty_migration_prompt(source_code):
    return f"""you are a senior java developer. Migrate this WebSphere scheduler to Liberty following these steps:
- DONT be lazy, please generate all the code, dont skip implementation.

1. java Imports:
- NEVER import com.ibm.websphere.scheduler.*
- ONLY import relevant Liberty scheduler imports
    
2. Update scheduler configuration:
- Replace BeanTaskInfo with Liberty equivalent
- Update task submission mechanism
- Handle persistence settings
    
3. Update scheduling logic:
- ensure to generate scheduleTask and cancelTask methods in the implementation class
- Convert cron expressions if needed
- Update task execution methods
- Handle transaction boundaries
    
4. Error handling:
- ensure to handle ManagedScheduledExecutorService.
- Update exception types
- Maintain retry logic
- Preserve logging
<<SYS>>
Original code:
`{source_code}`
<</SYS>>
Generate complete Liberty scheduler implementation maintaining the same functionality.
"""

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

def handle_java_api_migration(parameters, context):
    source_api = parameters["source_api"]
    target_api = parameters["target_api"]
    file_path = parameters["file_path"]
    
    console.print(f"[blue]Starting migration from {source_api} to {target_api}[/blue]")
    console.print(f"[blue]Processing file: {file_path}[/blue]")
    
    try:
        with open(file_path, 'r') as file:
            source_code = file.read()
            console.print(f"[green]Successfully read source file ({len(source_code)} bytes)[/green]")
    except Exception as e:
        console.print(f"[red]Error reading source file: {str(e)}[/red]")
        raise
    
    # Handle only specific migration types
    try:
        if source_api == "JAX-RPC" and target_api == "JAX-WS":
            console.print("[yellow]Preparing JAX-WS migration prompt...[/yellow]")
            prompt = create_jaxws_migration_prompt(source_code)
        elif source_api == "JSch" and target_api == "J2SSH":
            console.print("[yellow]Preparing J2SSH migration prompt...[/yellow]")
            prompt = create_j2ssh_migration_prompt(source_code)
        elif source_api == "WAS-Scheduler" and target_api == "Liberty-Scheduler":
            console.print("[yellow]Preparing Liberty Scheduler migration prompt...[/yellow]")
            prompt = create_liberty_migration_prompt(source_code)
        elif source_api == "EJB2.0" and target_api == "POJO":
            console.print("[yellow]Preparing POJO migration prompt...[/yellow]")
            prompt = create_pojo_migration_prompt(source_code)
        else:
            raise ValueError(f"Unsupported migration: {source_api} to {target_api}")
        
        console.print("[green]Successfully created migration prompt[/green]")
    except Exception as e:
        console.print(f"[red]Error creating migration prompt: {str(e)}[/red]")
        raise
    
    # Get the refactored code from the LLM
    try:
        with console.status("[bold blue]Generating migrated code...", spinner="dots") as status:
            console.print("[yellow]Sending request to LLM...[/yellow]")
            response = context.llm.generate_code(prompt)
            
            if not response:
                raise ValueError("Empty response received from LLM")
            
            console.print(f"[green]Successfully generated code ({len(response)} bytes)[/green]")
            
            # Basic validation of the response
            if "class" not in response.lower() and "interface" not in response.lower():
                console.print("[red]Warning: Generated code might not be valid Java[/red]")
            
            # For POJO migration, add extra validation
            if target_api == "POJO":
                if "ejb" in response.lower():
                    console.print("[yellow]Warning: Generated POJO might still contain EJB references[/yellow]")
                if "@Stateless" in response or "@Stateful" in response:
                    console.print("[yellow]Warning: Generated POJO contains EJB annotations[/yellow]")
    except Exception as e:
        console.print(f"[red]Error generating code: {str(e)}[/red]")
        raise
    
    result = {
        "changes": [
            {
                "file": file_path,
                "content": response,
                "description": f"Migrated from {source_api} to {target_api}"
            }
        ]
    }
    
    console.print("[green]Migration completed successfully[/green]")
    
    # For POJO migration, show a summary of changes
    if target_api == "POJO":
        console.print("\n[bold]POJO Migration Summary:[/bold]")
        console.print("1. Original file size: {} bytes".format(len(source_code)))
        console.print("2. Generated code size: {} bytes".format(len(response)))
        console.print("3. Major changes:")
        
        changes = []
        if "@Entity" in response and "@Entity" not in source_code:
            changes.append("- Added JPA annotations")
        if "@Inject" in response and "@Inject" not in source_code:
            changes.append("- Added CDI annotations")
        if "@Transactional" in response and "@Transactional" not in source_code:
            changes.append("- Added transaction management")
        
        for change in changes:
            console.print(change)
    
    return result

if __name__ == "__main__":
    app()