#!/usr/bin/env python
"""
Command-line interface for Blog Writer with storage management.
"""

import argparse
import sys
from blog_writer.main import (
    run, run_with_custom_retries, list_blogs, show_blog, search_blogs, 
    delete_blog, storage_stats, latest_blog,
    list_output, show_output, visualize_workflow, visualize_single
)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Blog Writer with Storage Management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  blog-writer                    # Generate a new blog (default retries)
  blog-writer retry              # Generate with custom retry settings
  blog-writer list              # List all blogs in storage
  blog-writer output            # List all blogs in output directory
  blog-writer show <blog_id>    # Show a specific blog from storage
  blog-writer show-output <file> # Show a specific blog from output directory
  blog-writer search "AI"       # Search blogs in storage
  blog-writer latest            # Show latest blog from storage
  blog-writer delete <blog_id>  # Delete a blog from storage
  blog-writer stats             # Show storage statistics
  blog-writer visualize         # Generate all workflow visualizations
  blog-writer viz workflow      # Generate workflow diagram only
  blog-writer viz network       # Generate agent network diagram only
  blog-writer viz timeline      # Generate execution timeline only

Retry Configuration:
  - Default crew retries: 2
  - Default delay between retries: 5 seconds
  - Task retries: Research=2, Writing=3, Proofreading=2

Visualization Types:
  - workflow: Complete workflow diagram
  - network: Agent interaction network
  - timeline: Execution timeline
        """
    )
    
    parser.add_argument(
        'command',
        nargs='?',
        default='generate',
        choices=['generate', 'retry', 'list', 'output', 'show', 'show-output', 'search', 'delete', 'stats', 'latest', 'visualize', 'viz'],
        help='Command to execute (default: generate)'
    )
    
    parser.add_argument(
        'args',
        nargs='*',
        help='Additional arguments for the command'
    )
    
    args = parser.parse_args()
    
    try:
        if args.command == 'generate':
            run()
        elif args.command == 'retry':
            run_with_custom_retries()
        elif args.command == 'list':
            list_blogs()
        elif args.command == 'output':
            list_output()
        elif args.command == 'show':
            if not args.args:
                print("Error: blog_id is required for show command")
                sys.exit(1)
            sys.argv = ['show_blog'] + args.args
            show_blog()
        elif args.command == 'show-output':
            if not args.args:
                print("Error: filename is required for show-output command")
                sys.exit(1)
            sys.argv = ['show_output'] + args.args
            show_output()
        elif args.command == 'search':
            if args.args:
                sys.argv = ['search_blogs'] + args.args
            search_blogs()
        elif args.command == 'delete':
            if not args.args:
                print("Error: blog_id is required for delete command")
                sys.exit(1)
            sys.argv = ['delete_blog'] + args.args
            delete_blog()
        elif args.command == 'stats':
            storage_stats()
        elif args.command == 'latest':
            latest_blog()
        elif args.command == 'visualize':
            visualize_workflow()
        elif args.command == 'viz':
            if not args.args:
                print("Error: visualization type is required for viz command")
                print("Available types: workflow, network, timeline")
                sys.exit(1)
            visualize_single(args.args[0])
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main() 