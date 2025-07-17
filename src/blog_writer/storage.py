import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import re


class BlogStorage:
    """Handles storage and retrieval of generated blog posts."""
    
    def __init__(self, base_dir: str = "blogs"):
        """
        Initialize the blog storage system.
        
        Args:
            base_dir: Directory to store all blog posts
        """
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        self.metadata_file = self.base_dir / "metadata.json"
        self._load_metadata()
    
    def _load_metadata(self):
        """Load or create metadata file."""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {"blogs": []}
            self._save_metadata()
    
    def _save_metadata(self):
        """Save metadata to file."""
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)
    
    def _sanitize_filename(self, topic: str) -> str:
        """Convert topic to a safe filename."""
        # Remove special characters and replace spaces with underscores
        sanitized = re.sub(r'[^\w\s-]', '', topic)
        sanitized = re.sub(r'[-\s]+', '_', sanitized)
        return sanitized.lower()[:50]  # Limit length
    
    def _generate_filename(self, topic: str, suffix: str = "") -> str:
        """Generate a unique filename for the blog post."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sanitized_topic = self._sanitize_filename(topic)
        filename = f"{sanitized_topic}_{timestamp}"
        if suffix:
            filename += f"_{suffix}"
        return filename
    
    def create_blog_directory(self, topic: str) -> Path:
        """Create a directory for a specific blog post."""
        blog_dir = self.base_dir / self._generate_filename(topic)
        blog_dir.mkdir(exist_ok=True)
        return blog_dir
    
    def save_blog_post(self, topic: str, content: str, stage: str = "final") -> str:
        """
        Save a blog post to the storage system.
        
        Args:
            topic: The blog topic
            content: The blog content
            stage: The stage of the blog (draft, final, etc.)
            
        Returns:
            Path to the saved file
        """
        blog_dir = self.create_blog_directory(topic)
        filename = f"{stage}_blog_post.md"
        file_path = blog_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Update metadata
        blog_info = {
            "topic": topic,
            "directory": blog_dir.name,
            "stage": stage,
            "filename": filename,
            "created_at": datetime.now().isoformat(),
            "file_path": str(file_path)
        }
        
        # Check if this blog already exists in metadata
        existing_blog = None
        for blog in self.metadata["blogs"]:
            if blog["directory"] == blog_dir.name:
                existing_blog = blog
                break
        
        if existing_blog:
            # Update existing blog entry
            existing_blog.update(blog_info)
        else:
            # Add new blog entry
            self.metadata["blogs"].append(blog_info)
        
        self._save_metadata()
        return str(file_path)
    
    def get_blog_list(self) -> List[Dict]:
        """Get a list of all stored blogs."""
        return self.metadata["blogs"]
    
    def get_blog_content(self, blog_id: str) -> Optional[str]:
        """
        Retrieve the content of a specific blog.
        
        Args:
            blog_id: The blog directory name or topic
            
        Returns:
            Blog content if found, None otherwise
        """
        for blog in self.metadata["blogs"]:
            if blog["directory"] == blog_id or blog["topic"].lower() == blog_id.lower():
                file_path = Path(blog["file_path"])
                if file_path.exists():
                    with open(file_path, 'r', encoding='utf-8') as f:
                        return f.read()
        return None
    
    def get_latest_blog(self) -> Optional[Dict]:
        """Get the most recently created blog."""
        if not self.metadata["blogs"]:
            return None
        
        # Sort by creation time (newest first)
        sorted_blogs = sorted(
            self.metadata["blogs"], 
            key=lambda x: x["created_at"], 
            reverse=True
        )
        return sorted_blogs[0]
    
    def search_blogs(self, query: str) -> List[Dict]:
        """
        Search blogs by topic or content.
        
        Args:
            query: Search query
            
        Returns:
            List of matching blogs
        """
        results = []
        query_lower = query.lower()
        
        for blog in self.metadata["blogs"]:
            if (query_lower in blog["topic"].lower() or 
                query_lower in blog.get("directory", "").lower()):
                results.append(blog)
        
        return results
    
    def delete_blog(self, blog_id: str) -> bool:
        """
        Delete a blog and its directory.
        
        Args:
            blog_id: The blog directory name or topic
            
        Returns:
            True if deleted successfully, False otherwise
        """
        for i, blog in enumerate(self.metadata["blogs"]):
            if blog["directory"] == blog_id or blog["topic"].lower() == blog_id.lower():
                # Remove directory
                blog_dir = self.base_dir / blog["directory"]
                if blog_dir.exists():
                    import shutil
                    shutil.rmtree(blog_dir)
                
                # Remove from metadata
                del self.metadata["blogs"][i]
                self._save_metadata()
                return True
        
        return False
    
    def get_storage_stats(self) -> Dict:
        """Get statistics about the blog storage."""
        total_blogs = len(self.metadata["blogs"])
        total_size = 0
        
        for blog in self.metadata["blogs"]:
            file_path = Path(blog["file_path"])
            if file_path.exists():
                total_size += file_path.stat().st_size
        
        return {
            "total_blogs": total_blogs,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "storage_directory": str(self.base_dir)
        } 