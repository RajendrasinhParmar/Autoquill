#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from pathlib import Path
from blog_writer.crew import BlogWriter
from blog_writer.storage import BlogStorage
from blog_writer.visualization import BlogWriterVisualizer

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run(max_crew_retries: int = 2, delay_between_retries: int = 5):
    """
    Run the crew and save only the final generated blog.
    
    Args:
        max_crew_retries: Maximum number of times to retry the entire crew execution
        delay_between_retries: Seconds to wait between retry attempts
    """
    topic = input("Enter the blog topic: ")
    inputs = {
        'topic': topic,
        'current_year': str(datetime.now().year)
    }
    
    # Crew-level retry logic
    for attempt in range(1, max_crew_retries + 1):
        try:
            print(f"\n🤖 Running blog generation crew (Attempt {attempt}/{max_crew_retries})...")
            
            # Create blog writer with storage
            blog_writer = BlogWriter()
            
            # Run the crew
            result = blog_writer.crew().kickoff(inputs=inputs)
            print("✅ Crew execution completed successfully.")
            
            # Read the final blog content from the output file
            final_content = None
            final_file = Path("final_blog_post.md")
            blog_file = Path("blog_post.md")
            
            if final_file.exists():
                with open(final_file, 'r', encoding='utf-8') as f:
                    final_content = f.read()
                print(f"✅ Found final blog post in {final_file}")
            elif blog_file.exists():
                with open(blog_file, 'r', encoding='utf-8') as f:
                    final_content = f.read()
                print(f"✅ Found blog post in {blog_file}")
            else:
                print("❌ No output files found. Crew may not have completed successfully.")
                if result:
                    print("Result object:", result)
                    print("Result type:", type(result))
                raise Exception("No output files generated")
            
            # --- Strip markdown code block markers if present ---
            if final_content:
                lines = final_content.strip().splitlines()
                if lines and (lines[0].strip().startswith('```')):
                    # Remove the first line (``` or ```markdown)
                    lines = lines[1:]
                    # Remove the last line if it's a closing code block
                    if lines and lines[-1].strip() == '```':
                        lines = lines[:-1]
                    final_content = '\n'.join(lines).lstrip('\n')
            # ---------------------------------------------------

            if final_content:
                # Create a clean output directory
                output_dir = Path("output")
                output_dir.mkdir(exist_ok=True)
                
                # Generate a clean filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                sanitized_topic = topic.replace(" ", "_").replace("/", "_").replace("\\", "_")[:50]
                filename = f"{sanitized_topic}_{timestamp}.md"
                
                # Save the final blog post
                output_file = output_dir / filename
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(final_content)
                
                print(f"\n✅ Final blog post saved to: {output_file}")
                print(f"📁 You can find it in the 'output' directory")
                
                # Also save to storage for management purposes
                storage_file = blog_writer.storage.save_blog_post(topic, final_content, "final")
                print(f"💾 Also saved to storage: {storage_file}")
                
                # Clean up temporary files
                for temp_file in ["blog_post.md", "final_blog_post.md"]:
                    temp_path = Path(temp_file)
                    if temp_path.exists():
                        temp_path.unlink()
                        print(f"🧹 Cleaned up temporary file: {temp_file}")
                
                return result  # Success, exit retry loop
            else:
                print("❌ No content was generated. Please check the crew execution.")
                raise Exception("No content generated")
                
        except Exception as e:
            print(f"❌ Attempt {attempt} failed: {e}")
            
            if attempt < max_crew_retries:
                print(f"⏳ Waiting {delay_between_retries} seconds before retry...")
                import time
                time.sleep(delay_between_retries)
            else:
                print(f"💥 All {max_crew_retries} attempts failed. Exiting.")
                raise Exception(f"All crew execution attempts failed. Last error: {e}")


def run_with_custom_retries():
    """
    Run the crew with custom retry settings.
    """
    print("🔄 Crew Retry Configuration")
    print("=" * 40)
    
    try:
        max_retries = input("Enter max crew retries (default: 2): ").strip()
        max_retries = int(max_retries) if max_retries else 2
        
        delay = input("Enter delay between retries in seconds (default: 5): ").strip()
        delay = int(delay) if delay else 5
        
        print(f"\n📋 Configuration:")
        print(f"   Max crew retries: {max_retries}")
        print(f"   Delay between retries: {delay} seconds")
        print(f"   Task retries: Research=2, Writing=3, Proofreading=2")
        
        run(max_crew_retries=max_retries, delay_between_retries=delay)
        
    except ValueError:
        print("❌ Invalid input. Using default values.")
        run()


def visualize_workflow():
    """
    Generate visualizations of the blog writer workflow.
    """
    try:
        visualizer = BlogWriterVisualizer()
        visualizer.generate_all_visualizations()
    except ImportError as e:
        print("❌ Visualization dependencies not installed.")
        print("Install required packages: pip install matplotlib networkx")
        print(f"Error: {e}")
    except Exception as e:
        print(f"❌ Error generating visualizations: {e}")


def visualize_single(type_name: str):
    """
    Generate a single type of visualization.
    
    Args:
        type_name: Type of visualization (workflow, network, timeline)
    """
    try:
        visualizer = BlogWriterVisualizer()
        
        if type_name == "workflow":
            visualizer.create_workflow_diagram()
        elif type_name == "network":
            visualizer.create_agent_network()
        elif type_name == "timeline":
            visualizer.create_execution_timeline()
        else:
            print(f"❌ Unknown visualization type: {type_name}")
            print("Available types: workflow, network, timeline")
            
    except ImportError as e:
        print("❌ Visualization dependencies not installed.")
        print("Install required packages: pip install matplotlib networkx")
        print(f"Error: {e}")
    except Exception as e:
        print(f"❌ Error generating visualization: {e}")


def list_blogs():
    """
    List all stored blog posts.
    """
    try:
        storage = BlogStorage()
        blogs = storage.get_blog_list()
        
        if not blogs:
            print("No blog posts found in storage.")
            return
        
        print("\n📚 Stored Blog Posts:")
        print("=" * 60)
        for i, blog in enumerate(blogs, 1):
            print(f"{i}. Topic: {blog['topic']}")
            print(f"   Directory: {blog['directory']}")
            print(f"   Stage: {blog['stage']}")
            print(f"   Created: {blog['created_at']}")
            print(f"   File: {blog['filename']}")
            print("-" * 40)
    
    except Exception as e:
        print(f"Error listing blogs: {e}")


def show_blog():
    """
    Display a specific blog post.
    """
    if len(sys.argv) < 2:
        print("Usage: python -m blog_writer.main show_blog <blog_id>")
        return
    
    blog_id = sys.argv[1]
    try:
        storage = BlogStorage()
        content = storage.get_blog_content(blog_id)
        
        if content:
            print(f"\n📖 Blog Content for '{blog_id}':")
            print("=" * 60)
            print(content)
        else:
            print(f"Blog with ID '{blog_id}' not found.")
    
    except Exception as e:
        print(f"Error retrieving blog: {e}")


def search_blogs():
    """
    Search for blog posts by topic.
    """
    if len(sys.argv) < 2:
        query = input("Enter search query: ")
    else:
        query = sys.argv[1]
    
    try:
        storage = BlogStorage()
        results = storage.search_blogs(query)
        
        if not results:
            print(f"No blogs found matching '{query}'.")
            return
        
        print(f"\n🔍 Search Results for '{query}':")
        print("=" * 60)
        for i, blog in enumerate(results, 1):
            print(f"{i}. Topic: {blog['topic']}")
            print(f"   Directory: {blog['directory']}")
            print(f"   Created: {blog['created_at']}")
            print("-" * 40)
    
    except Exception as e:
        print(f"Error searching blogs: {e}")


def delete_blog():
    """
    Delete a specific blog post.
    """
    if len(sys.argv) < 2:
        print("Usage: python -m blog_writer.main delete_blog <blog_id>")
        return
    
    blog_id = sys.argv[1]
    try:
        storage = BlogStorage()
        if storage.delete_blog(blog_id):
            print(f"Blog '{blog_id}' deleted successfully.")
        else:
            print(f"Blog '{blog_id}' not found.")
    
    except Exception as e:
        print(f"Error deleting blog: {e}")


def storage_stats():
    """
    Show storage statistics.
    """
    try:
        storage = BlogStorage()
        stats = storage.get_storage_stats()
        
        print("\n📊 Storage Statistics:")
        print("=" * 30)
        print(f"Total Blogs: {stats['total_blogs']}")
        print(f"Total Size: {stats['total_size_mb']} MB")
        print(f"Storage Directory: {stats['storage_directory']}")
    
    except Exception as e:
        print(f"Error getting storage stats: {e}")


def latest_blog():
    """
    Show the most recently created blog.
    """
    try:
        storage = BlogStorage()
        latest = storage.get_latest_blog()
        
        if latest:
            print(f"\n🆕 Latest Blog:")
            print("=" * 30)
            print(f"Topic: {latest['topic']}")
            print(f"Directory: {latest['directory']}")
            print(f"Created: {latest['created_at']}")
            
            # Show content
            content = storage.get_blog_content(latest['directory'])
            if content:
                print(f"\nContent Preview (first 200 chars):")
                print("-" * 40)
                print(content[:200] + "..." if len(content) > 200 else content)
        else:
            print("No blogs found in storage.")
    
    except Exception as e:
        print(f"Error getting latest blog: {e}")


def list_output():
    """
    List all blog posts in the output directory.
    """
    try:
        output_dir = Path("output")
        if not output_dir.exists():
            print("No output directory found.")
            return
        
        files = list(output_dir.glob("*.md"))
        if not files:
            print("No blog posts found in output directory.")
            return
        
        print("\n📁 Blog Posts in Output Directory:")
        print("=" * 60)
        for i, file in enumerate(sorted(files, key=lambda x: x.stat().st_mtime, reverse=True), 1):
            stat = file.stat()
            created_time = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            print(f"{i}. {file.name}")
            print(f"   Created: {created_time}")
            print(f"   Size: {stat.st_size} bytes")
            print("-" * 40)
    
    except Exception as e:
        print(f"Error listing output files: {e}")


def show_output():
    """
    Display a specific blog post from the output directory.
    """
    if len(sys.argv) < 2:
        print("Usage: python -m blog_writer.main show_output <filename>")
        return
    
    filename = sys.argv[1]
    try:
        output_dir = Path("output")
        file_path = output_dir / filename
        
        if not file_path.exists():
            print(f"File '{filename}' not found in output directory.")
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"\n📖 Blog Content from '{filename}':")
        print("=" * 60)
        print(content)
    
    except Exception as e:
        print(f"Error reading output file: {e}")
