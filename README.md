# Blog Writer with Storage System

A powerful blog generation system using CrewAI with integrated storage capabilities for managing and organizing generated blog posts.

## Features

- 🤖 **AI-Powered Blog Generation**: Uses CrewAI with multiple agents (researcher, writer, proofreader)
- 📁 **Automatic Storage**: Automatically saves generated blogs with proper naming and organization
- 🔍 **Blog Management**: List, search, retrieve, and delete stored blogs
- 📊 **Storage Statistics**: Track storage usage and blog metadata
- 🏷️ **Smart Naming**: Automatic filename generation based on topic and timestamp
- 📝 **Metadata Tracking**: Comprehensive metadata for each blog post
- 🎨 **Workflow Visualization**: Visualize agents, tasks, and execution flow
- 🔄 **Retry System**: Configurable retry logic for both tasks and crew execution

## Installation

```bash
# Install the package
pip install -e .

# Or using uv
uv sync
```

## Usage

### Generate a New Blog

```bash
# Run the blog writer
$ blog-writer
```

This will:
1. Prompt you for a blog topic
2. Generate a comprehensive blog post using AI agents
3. Automatically save the blog to the `output/` directory
4. Display the save location

### Blog Management Commands

#### List All Blogs
```bash
$ blog-writer list
```

#### Show a Specific Blog
```bash
$ blog-writer show <blog_id>
# Example: show ai_llms_20241201_143022
```

#### Search Blogs
```bash
$ blog-writer search <query>
# Example: search AI
```

#### Show Latest Blog
```bash
$ blog-writer latest
```

#### Delete a Blog
```bash
$ blog-writer delete <blog_id>
# Example: delete ai_llms_20241201_143022
```

#### Storage Statistics
```bash
blog-writer stats
```

### Workflow Visualization

#### Generate All Visualizations
```bash
blog-writer visualize
```

#### Generate Specific Visualizations
```bash
blog-writer viz workflow    # Workflow diagram
blog-writer viz network     # Agent network
blog-writer viz timeline    # Execution timeline
```

The visualizations will be saved in the `visualizations/` directory:
- `workflow_diagram.png` - Complete workflow showing agents, tasks, and outputs
- `agent_network.png` - Network diagram of agent interactions
- `execution_timeline.png` - Timeline of execution phases
- `visualization_summary.json` - Metadata about the visualizations

### Retry Configuration

#### Default Retries
```bash
blog-writer
# Uses: 2 crew retries, 5s delay, task-specific retries
```

#### Custom Retries
```bash
blog-writer retry
# Prompts for custom retry settings
```

## Storage Structure

The system creates a `blogs/` directory with the following structure:

```
blogs/
├── metadata.json                    # Database of all blogs
├── ai_llms_20241201_143022/        # Individual blog directory
│   ├── draft_blog_post.md          # Draft version
│   └── final_blog_post.md          # Final version
├── machine_learning_20241201_150000/
│   └── final_blog_post.md
└── ...
```

### File Naming Convention

- **Directory**: `{sanitized_topic}_{YYYYMMDD_HHMMSS}`
- **Files**: `{stage}_blog_post.md` (e.g., `draft_blog_post.md`, `final_blog_post.md`)

### Metadata Structure

Each blog entry in `metadata.json` contains:

```json
{
  "topic": "AI and Machine Learning",
  "directory": "ai_and_machine_learning_20241201_143022",
  "stage": "final",
  "filename": "final_blog_post.md",
  "created_at": "2024-12-01T14:30:22.123456",
  "file_path": "blogs/ai_and_machine_learning_20241201_143022/final_blog_post.md"
}
```

## Workflow Visualization

The system provides three types of visualizations:

### 1. Workflow Diagram
Shows the complete blog generation process:
- **Agents**: Researcher, Blog Writer, Proofreader
- **Tasks**: Research Task, Write Blog Task, Proofread Task
- **Outputs**: Research Findings, Blog Post (Draft), Final Blog Post
- **Flow**: Sequential execution with dependencies

### 2. Agent Network
Network diagram showing:
- Agent interactions and relationships
- Task dependencies
- Data flow between components
- Visual representation of the crew structure

### 3. Execution Timeline
Timeline showing:
- Execution phases and duration
- Agent responsibilities
- Retry configuration
- Sequential processing flow

## API Usage

### BlogStorage Class

```python
from blog_writer.storage import BlogStorage

# Initialize storage
storage = BlogStorage("custom_blogs_dir")

# Save a blog post
file_path = storage.save_blog_post("My Topic", "Blog content...", "final")

# List all blogs
blogs = storage.get_blog_list()

# Retrieve a blog
content = storage.get_blog_content("blog_directory_name")

# Search blogs
results = storage.search_blogs("AI")

# Get latest blog
latest = storage.get_latest_blog()

# Delete a blog
success = storage.delete_blog("blog_directory_name")

# Get storage statistics
stats = storage.get_storage_stats()
```

### Visualization

```python
from blog_writer.visualization import BlogWriterVisualizer

# Create visualizer
visualizer = BlogWriterVisualizer()

# Generate all visualizations
visualizer.generate_all_visualizations("my_visualizations")

# Generate specific visualization
visualizer.create_workflow_diagram("workflow.png")
visualizer.create_agent_network("network.png")
visualizer.create_execution_timeline("timeline.png")
```

## Configuration

### Storage Directory

You can customize the storage directory:

```python
# In your code
blog_writer = BlogWriter(storage_dir="my_blogs")

# Or for storage only
storage = BlogStorage("my_blogs")
```

### Retry Configuration

Default retry settings:
- **Crew Retries**: 2 attempts
- **Crew Delay**: 5 seconds between retries
- **Research Task**: 2 retries
- **Writing Task**: 3 retries (most complex)
- **Proofreading Task**: 2 retries

### Environment Variables

- `BLOG_STORAGE_DIR`: Default storage directory (defaults to "blogs")

## Development

### Project Structure

```
src/blog_writer/
├── __init__.py
├── main.py              # CLI entry points
├── crew.py              # CrewAI crew definition
├── storage.py           # Storage system
├── visualization.py     # Workflow visualization
├── cli.py               # Command-line interface
├── config/
│   ├── agents.yaml      # Agent configurations
│   └── tasks.yaml       # Task configurations
```

### Adding New Features

1. **New Storage Methods**: Add methods to `BlogStorage` class
2. **New CLI Commands**: Add functions to `main.py` and update `cli.py`
3. **New Visualizations**: Add methods to `BlogWriterVisualizer` class
4. **New Tools**: Create tools and integrate with agents

## Troubleshooting

### Common Issues

1. **Permission Errors**: Ensure write permissions to the storage directory
2. **File Not Found**: Check if the blog directory exists in the metadata
3. **Encoding Issues**: All files are saved with UTF-8 encoding
4. **Visualization Errors**: Install required packages: `pip install matplotlib networkx`

### Debug Mode

Enable verbose logging by setting the `verbose` parameter in the CrewAI configuration.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.