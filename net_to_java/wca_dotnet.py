from rich.console import Console
from rich.markdown import Markdown
import typer
from wca_backend import call_wca_api, stream_response
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
import os
import sys
from datetime import datetime

load_dotenv()
console = Console()
app = typer.Typer(help=".NET Code Analysis and Generation Tool")

def check_api_key():
    """Check if IBM Cloud API key is set"""
    api_key = os.getenv("IAM_APIKEY")
    if not api_key:
        console.print("[red]Error: IAM_APIKEY not found in environment variables[/red]")
        console.print("Please set your IBM Cloud API key in .env file:")
        console.print("IAM_APIKEY=your_api_key_here")
        raise typer.Exit(1)
    return api_key


def read_file(file_path: Path) -> str:
    """Read and return contents of file"""
    try:
        return file_path.read_text()
    except Exception as e:
        console.print(f"[red]Error reading file: {e}[/red]")
        raise typer.Exit(1)

def save_markdown_output(input_file: Path, content: str, suffix: str = "review") -> Path:
    """Save content as markdown file in the same folder as input file"""
    output_file = input_file.parent / f"{input_file.stem}_{suffix}.md"
    output_file.write_text(content)
    return output_file

def unfold_code_blocks(content: str) -> str:
    """Remove code block markers from markdown content"""
    lines = content.splitlines()
    result = []
    in_code_block = False
    
    for line in lines:
        if line.startswith('```'):
            if not in_code_block:
                in_code_block = True
                continue
            else:
                in_code_block = False
                continue
        result.append(line)
    
    return '\n'.join(result)

def generate_unit_tests(code: str, test_framework: str = "xunit") -> str:
    """Generate unit tests for .NET code"""
    test_prompt = f"""Analyze this .NET code and generate unit tests:
- Use {test_framework} test framework
- Include test cases for:
  * Happy path scenarios
  * Edge cases
  * Error conditions
- Follow AAA pattern (Arrange, Act, Assert)
- Use meaningful test names
- Include proper test data setup
- Mock external dependencies
- Test both positive and negative scenarios

<<SYS>>
code: ```csharp
{code}
```
<</SYS>>

Generate complete unit test class(es) with:
1. Proper test attributes
2. Setup/teardown if needed
3. Mock setup where required
4. Clear assertions
5. Comments explaining test scenarios

Return the test code in a code block with the path format:
```csharp:Tests/YourTestClass.cs
[Your test code here]
```"""

    try:
        test_payload = {
            "message_payload": {
                "messages": [{"content": test_prompt, "role": "USER"}]
            }
        }
        test_response = call_wca_api(test_payload)
        tests = stream_response(test_response, action="Generating unit tests")
        
        # If response doesn't include file path, wrap it with default path
        if not (tests.startswith("```") and ":" in tests.splitlines()[0]):
            tests = f"```csharp:Tests/GeneratedTests.cs\n{tests}\n```"
            
        return tests
    except Exception as e:
        console.print(f"[red]Error generating unit tests: {str(e)}[/red]")
        return ""

def find_dotnet_files(directory: Path) -> list[Path]:
    """Find all .NET source files in directory"""
    dotnet_files = []
    for ext in ['.cs', '.vb']:  # Add more extensions if needed
        dotnet_files.extend(directory.rglob(f"*{ext}"))
    
    # Filter out test files and obj/bin directories
    return [
        f for f in dotnet_files 
        if not any(x in str(f) for x in ['test', 'Test', 'obj', 'bin'])
    ]

@app.command()
def unittest(
    source_path: Path = typer.Argument(..., help=".NET source file or directory to generate tests for", exists=True),
    framework: str = typer.Option("xunit", "--framework", "-f", help="Test framework to use (xunit/nunit/mstest)"),
    output_dir: Optional[Path] = typer.Option(None, "--output", "-o", help="Output directory for test project"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed progress")
):
    """Generate unit tests for .NET code"""
    try:
        check_api_key()
        
        # Set up output directory
        if not output_dir:
            output_dir = Path("output") / "tests"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Handle both file and directory input
        if source_path.is_file():
            source_files = [source_path]
        else:
            console.print(f"[yellow]Scanning directory: {source_path}[/yellow]")
            source_files = find_dotnet_files(source_path)
        
        total_files = len(source_files)
        console.print(f"[green]Found {total_files} .NET source files[/green]")
        
        # Process each source file
        with console.status("[bold blue]Generating unit tests...") as status:
            for index, source_file in enumerate(source_files, 1):
                try:
                    status.update(f"[bold blue]Processing file {index}/{total_files} ({(index/total_files)*100:.1f}%)")
                    
                    if verbose:
                        console.print(f"\n[yellow]Processing: {source_file}[/yellow]")
                    
                    code = read_file(source_file)
                    result = generate_unit_tests(code, framework)
                    
                    # Parse the generated code to extract file structure
                    files = parse_generated_code(result)
                    
                    # Determine source project structure
                    try:
                        # Try to find src directory
                        src_dir = source_file.parent
                        while src_dir.name and not (src_dir / "src").exists():
                            src_dir = src_dir.parent
                            if src_dir == src_dir.parent:  # Reached root
                                break
                        
                        if (src_dir / "src").exists():
                            # Standard src/project structure
                            relative_path = source_file.relative_to(src_dir / "src")
                            project_name = relative_path.parts[0]  # First folder after src is project name
                            sub_path = Path(*relative_path.parts[1:])  # Path after project name
                        else:
                            # Try to find by namespace structure
                            project_name = source_file.parent.name
                            while project_name.endswith(".API") or project_name.endswith(".Core") or project_name.endswith(".Infrastructure"):
                                project_name = project_name.rsplit(".", 1)[0]
                            sub_path = source_file.relative_to(source_file.parent.parent)
                    
                    except ValueError:
                        # Fallback if not in standard structure
                        project_name = source_file.parent.name
                        sub_path = source_file.name
                    
                    # Create test project directory in output folder
                    test_project_dir = output_dir / f"{project_name}.UnitTests"
                    test_project_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Save test file maintaining source structure
                    test_file_name = source_file.stem + "Tests.cs"
                    if sub_path.parent != Path("."):
                        test_file_path = test_project_dir / sub_path.parent / test_file_name
                    else:
                        test_file_path = test_project_dir / test_file_name
                        
                    test_file_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Combine all test content into one file
                    all_test_content = []
                    for content in files.values():
                        # Remove any remaining markdown or code block markers
                        clean_content = unfold_code_blocks(content)
                        all_test_content.append(clean_content)
                    
                    final_test_content = "\n\n".join(all_test_content)
                    
                    # Save test file
                    test_file_path.write_text(final_test_content)
                    if verbose:
                        console.print(f"[green]Unit tests saved to {test_file_path}[/green]")
                    
                except Exception as e:
                    console.print(f"[red]Error processing {source_file.name}: {str(e)}[/red]")
                    if verbose:
                        import traceback
                        console.print("[red]Traceback:[/red]")
                        console.print(traceback.format_exc())
                    continue
        
        console.print(f"\n[bold green]✓ Generated unit tests for {total_files} files in {output_dir}[/bold green]")
            
    except Exception as e:
        console.print(f"[red]Error in unittest command: {str(e)}[/red]")
        if verbose:
            import traceback
            console.print("[red]Traceback:[/red]")
            console.print(traceback.format_exc())
        raise typer.Exit(1)

def analyze_requirements(spec: str) -> dict:
    """Analyze the specification to determine what needs to be generated"""
    analysis_prompt = f"""Analyze this technical specification and identify required components.
Categorize into:
1. Frontend Components (if any)
2. Backend Services
3. Data Models/Entities
4. API Controllers
5. Infrastructure Requirements

Return the analysis in a structured format:

<<SYS>>
specification: ```markdown
{spec}
```
<</SYS>>

Return a JSON structure like:
```json
{{
    "frontend": {{
        "required": true/false,
        "components": ["component1", "component2"],
        "pages": ["page1", "page2"]
    }},
    "backend": {{
        "services": ["service1", "service2"],
        "controllers": ["controller1", "controller2"]
    }},
    "models": {{
        "entities": ["entity1", "entity2"],
        "dtos": ["dto1", "dto2"]
    }},
    "infrastructure": {{
        "auth": true/false,
        "database": true/false,
        "caching": true/false
    }}
}}
```"""

    try:
        payload = {
            "message_payload": {
                "messages": [{"content": analysis_prompt, "role": "USER"}]
            }
        }
        response = call_wca_api(payload)
        analysis = stream_response(response, action="Analyzing requirements")
        
        # Extract JSON from response
        import json
        start = analysis.find('{')
        end = analysis.rfind('}') + 1
        if start >= 0 and end > start:
            return json.loads(analysis[start:end])
        return {}
    except Exception as e:
        console.print(f"[red]Error analyzing requirements: {str(e)}[/red]")
        return {}

def generate_code_by_component(component_type: str, component_name: str, spec: str) -> str:
    """Generate code for a specific component"""
    prompts = {
        "frontend": """Generate React component with TypeScript and Tailwind CSS.
Include:
- Component interface/props
- State management
- Event handlers
- Styling
- Error handling""",
        
        "service": """Generate service class with proper interfaces.
Include:
- Interface definition
- Service implementation
- Dependency injection
- Error handling
- Logging""",
        
        "model": """Generate entity class with all properties.
Include:
- Properties with types
- Data annotations
- Navigation properties
- Validation
- XML documentation""",
        
        "controller": """Generate API controller with endpoints.
Include:
- CRUD operations
- DTO usage
- Authentication
- Input validation
- Swagger documentation"""
    }

    prompt = f"""{prompts.get(component_type, "Generate code")}

Component: {component_name}

<<SYS>>
specification: ```markdown
{spec}
```
<</SYS>>

Generate complete implementation with proper file path (use ```csharp:path/to/file format)."""

    try:
        payload = {
            "message_payload": {
                "messages": [{"content": prompt, "role": "USER"}]
            }
        }
        response = call_wca_api(payload)
        return stream_response(response, action=f"Generating {component_type}: {component_name}")
    except Exception as e:
        console.print(f"[red]Error generating {component_type}: {str(e)}[/red]")
        return ""

def generate_project_skeleton(project_name: str) -> str:
    """Generate basic .NET project structure"""
    skeleton = f"""```csharp:{project_name}.sln
Microsoft Visual Studio Solution File, Format Version 12.00
# Visual Studio Version 17
VisualStudioVersion = 17.0.31903.59
MinimumVisualStudioVersion = 10.0.40219.1
Project("{{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}}") = "{project_name}", "{project_name}\\{project_name}.csproj", "{{GUID}}"
EndProject
```

```csharp:{project_name}.csproj
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.AspNetCore.OpenApi" Version="8.0.0" />
    <PackageReference Include="Swashbuckle.AspNetCore" Version="6.5.0" />
    <PackageReference Include="Microsoft.EntityFrameworkCore" Version="8.0.0" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.SqlServer" Version="8.0.0" />
  </ItemGroup>
</Project>
```

```csharp:Program.cs
using Microsoft.EntityFrameworkCore;
using {project_name}.Data;
using {project_name}.Services;
using {project_name}.Repositories;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{{
    app.UseSwagger();
    app.UseSwaggerUI();
}}

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.Run();
```"""
    return skeleton

@app.command()
def generate(
    spec_file: Path = typer.Argument(..., help="Technical specification markdown file", exists=True),
    output_dir: Optional[Path] = typer.Option(None, "--output", "-o", help="Output directory for generated project"),
    project_name: Optional[str] = typer.Option(None, "--name", "-n", help="Project name (defaults to spec file name)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed progress")
):
    """Generate code based on technical specification"""
    try:
        check_api_key()
        
        # Set up output directory
        if not output_dir:
            output_dir = Path("output")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if not project_name:
            project_name = spec_file.stem
        
        console.print(f"[yellow]Reading specification file: {spec_file}[/yellow]")
        spec = read_file(spec_file)
        
        with console.status("[bold blue]Analyzing requirements...") as status:
            # Analyze requirements first
            requirements = analyze_requirements(spec)
            
            if not requirements:
                console.print("[red]Failed to analyze requirements[/red]")
                return
            
            # Show analysis results
            console.print("\n[bold]Requirements Analysis:[/bold]")
            if requirements.get("models", {}).get("entities"):
                console.print(f"  Models to generate: {len(requirements['models']['entities'])}")
            if requirements.get("backend", {}).get("services"):
                console.print(f"  Services to generate: {len(requirements['backend']['services'])}")
            if requirements.get("backend", {}).get("controllers"):
                console.print(f"  Controllers to generate: {len(requirements['backend']['controllers'])}")
            if requirements.get("frontend", {}).get("components"):
                console.print(f"  Frontend components to generate: {len(requirements['frontend']['components'])}")
            
            # Create project structure
            project_dir = output_dir / project_name
            project_dir.mkdir(parents=True, exist_ok=True)
            
            # Track progress
            total_components = (
                len(requirements.get("models", {}).get("entities", [])) +
                len(requirements.get("backend", {}).get("services", [])) +
                len(requirements.get("backend", {}).get("controllers", [])) +
                len(requirements.get("frontend", {}).get("components", []))
            )
            current_component = 0
            
            # Generate skeleton first
            status.update("[bold blue]Generating project skeleton...")
            skeleton = generate_project_skeleton(project_name)
            skeleton_files = parse_generated_code(skeleton)
            
            for file_path, content in skeleton_files.items():
                full_path = project_dir / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(content)
                if verbose:
                    console.print(f"[green]Created skeleton file: {file_path}[/green]")
            
            # Track all generated files
            generated_files = []
            
            # Generate Models
            if requirements.get("models", {}).get("entities"):
                models = requirements["models"]["entities"]
                for idx, model in enumerate(models, 1):
                    current_component += 1
                    status.update(
                        f"[bold blue]Generating models ({idx}/{len(models)}) - "
                        f"Overall progress: {(current_component/total_components)*100:.1f}%"
                    )
                    code = generate_code_by_component("model", model, spec)
                    files = parse_generated_code(code)
                    for file_path, content in files.items():
                        full_path = project_dir / file_path
                        full_path.parent.mkdir(parents=True, exist_ok=True)
                        full_path.write_text(content)
                        generated_files.append(file_path)
                        if verbose:
                            console.print(f"[green]Generated model: {file_path}[/green]")
            
            # Generate Services
            if requirements.get("backend", {}).get("services"):
                services = requirements["backend"]["services"]
                for idx, service in enumerate(services, 1):
                    current_component += 1
                    status.update(
                        f"[bold blue]Generating services ({idx}/{len(services)}) - "
                        f"Overall progress: {(current_component/total_components)*100:.1f}%"
                    )
                    code = generate_code_by_component("service", service, spec)
                    files = parse_generated_code(code)
                    for file_path, content in files.items():
                        full_path = project_dir / file_path
                        full_path.parent.mkdir(parents=True, exist_ok=True)
                        full_path.write_text(content)
                        generated_files.append(file_path)
                        if verbose:
                            console.print(f"[green]Generated service: {file_path}[/green]")
            
            # Generate Controllers
            if requirements.get("backend", {}).get("controllers"):
                controllers = requirements["backend"]["controllers"]
                for idx, controller in enumerate(controllers, 1):
                    current_component += 1
                    status.update(
                        f"[bold blue]Generating controllers ({idx}/{len(controllers)}) - "
                        f"Overall progress: {(current_component/total_components)*100:.1f}%"
                    )
                    code = generate_code_by_component("controller", controller, spec)
                    files = parse_generated_code(code)
                    for file_path, content in files.items():
                        full_path = project_dir / file_path
                        full_path.parent.mkdir(parents=True, exist_ok=True)
                        full_path.write_text(content)
                        generated_files.append(file_path)
                        if verbose:
                            console.print(f"[green]Generated controller: {file_path}[/green]")
            
            # Generate Frontend
            if requirements.get("frontend", {}).get("required"):
                frontend_dir = project_dir / "ClientApp"
                frontend_dir.mkdir(exist_ok=True)
                
                components = requirements["frontend"]["components"]
                for idx, component in enumerate(components, 1):
                    current_component += 1
                    status.update(
                        f"[bold blue]Generating frontend components ({idx}/{len(components)}) - "
                        f"Overall progress: {(current_component/total_components)*100:.1f}%"
                    )
                    code = generate_code_by_component("frontend", component, spec)
                    files = parse_generated_code(code)
                    for file_path, content in files.items():
                        full_path = frontend_dir / file_path
                        full_path.parent.mkdir(parents=True, exist_ok=True)
                        full_path.write_text(content)
                        generated_files.append(f"ClientApp/{file_path}")
                        if verbose:
                            console.print(f"[green]Generated frontend component: {file_path}[/green]")
        
        console.print(f"\n[bold green]✓ Project generated successfully in {project_dir}[/bold green]")
        console.print(f"\n[bold]Generated {len(generated_files)} files:[/bold]")
        
        # Group files by type for better readability
        file_groups = {
            "Models": [f for f in generated_files if "/Models/" in f],
            "Services": [f for f in generated_files if "/Services/" in f],
            "Controllers": [f for f in generated_files if "/Controllers/" in f],
            "Frontend": [f for f in generated_files if "ClientApp/" in f],
            "Other": [f for f in generated_files if not any(x in f for x in ["/Models/", "/Services/", "/Controllers/", "ClientApp/"])]
        }
        
        for group, files in file_groups.items():
            if files:
                console.print(f"\n  [bold]{group}:[/bold]")
                for file in sorted(files):
                    console.print(f"    {file}")
        
        return generated_files
        
    except Exception as e:
        console.print(f"[red]Error generating project: {str(e)}[/red]")
        if verbose:
            import traceback
            console.print("[red]Traceback:[/red]")
            console.print(traceback.format_exc())
        raise typer.Exit(1)

def parse_generated_code(result: str) -> dict[str, str]:
    """Parse generated code and extract individual files"""
    files = {}
    current_file = None
    current_content = []
    
    for line in result.splitlines():
        if line.startswith("```") and ":" in line:
            # New file block
            if current_file and current_content:
                files[current_file] = unfold_code_blocks("\n".join(current_content))
                current_content = []
            
            # Extract file path from ```csharp:path/to/file.cs
            current_file = line.split(":", 1)[1].strip()
            
        elif line.startswith("```") and current_file:
            # End of file block
            if current_content:
                files[current_file] = unfold_code_blocks("\n".join(current_content))
            current_file = None
            current_content = []
            
        elif current_file and not line.startswith("```"):
            # Collect file content
            current_content.append(line)
    
    # Handle last file if any
    if current_file and current_content:
        files[current_file] = unfold_code_blocks("\n".join(current_content))
    
    return files

if __name__ == "__main__":
    app()