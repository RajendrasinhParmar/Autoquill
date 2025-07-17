#!/usr/bin/env python
"""
Visualization module for Blog Writer CrewAI workflow.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import networkx as nx


class BlogWriterVisualizer:
    """Visualizes the Blog Writer CrewAI workflow and agents."""
    
    def __init__(self):
        self.colors = {
            'researcher': '#FF6B6B',    # Red
            'blog_writer': '#4ECDC4',   # Teal
            'proofreader': '#45B7D1',   # Blue
            'task': '#96CEB4',          # Green
            'output': '#FFEAA7'         # Yellow
        }
    
    def create_workflow_diagram(self, save_path: str = "workflow_diagram.png"):
        """
        Create a workflow diagram showing the blog generation process.
        
        Args:
            save_path: Path to save the diagram
        """
        fig, ax = plt.subplots(1, 1, figsize=(14, 10))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Title
        ax.text(5, 9.5, 'Blog Writer CrewAI Workflow', 
                fontsize=20, fontweight='bold', ha='center')
        
        # Agents
        agents = [
            {'name': 'Researcher', 'x': 1, 'y': 7, 'color': self.colors['researcher']},
            {'name': 'Blog Writer', 'x': 5, 'y': 7, 'color': self.colors['blog_writer']},
            {'name': 'Proofreader', 'x': 9, 'y': 7, 'color': self.colors['proofreader']}
        ]
        
        # Draw agents
        for agent in agents:
            # Agent box
            box = FancyBboxPatch(
                (agent['x'] - 1.2, agent['y'] - 0.8),
                2.4, 1.6,
                boxstyle="round,pad=0.1",
                facecolor=agent['color'],
                edgecolor='black',
                linewidth=2
            )
            ax.add_patch(box)
            
            # Agent name
            ax.text(agent['x'], agent['y'], agent['name'], 
                   fontsize=12, fontweight='bold', ha='center', va='center')
            
            # Agent description
            if agent['name'] == 'Researcher':
                desc = "Conducts research\non the topic"
            elif agent['name'] == 'Blog Writer':
                desc = "Writes the blog\npost content"
            else:
                desc = "Proofreads and\nimproves content"
            
            ax.text(agent['x'], agent['y'] - 0.3, desc, 
                   fontsize=9, ha='center', va='center')
        
        # Tasks
        tasks = [
            {'name': 'Research Task', 'x': 1, 'y': 4, 'color': self.colors['task']},
            {'name': 'Write Blog Task', 'x': 5, 'y': 4, 'color': self.colors['task']},
            {'name': 'Proofread Task', 'x': 9, 'y': 4, 'color': self.colors['task']}
        ]
        
        # Draw tasks
        for task in tasks:
            # Task box
            box = FancyBboxPatch(
                (task['x'] - 1.2, task['y'] - 0.6),
                2.4, 1.2,
                boxstyle="round,pad=0.1",
                facecolor=task['color'],
                edgecolor='black',
                linewidth=1.5
            )
            ax.add_patch(box)
            
            # Task name
            ax.text(task['x'], task['y'], task['name'], 
                   fontsize=10, fontweight='bold', ha='center', va='center')
        
        # Outputs
        outputs = [
            {'name': 'Research\nFindings', 'x': 1, 'y': 1.5, 'color': self.colors['output']},
            {'name': 'Blog Post\n(Draft)', 'x': 5, 'y': 1.5, 'color': self.colors['output']},
            {'name': 'Final Blog\nPost', 'x': 9, 'y': 1.5, 'color': self.colors['output']}
        ]
        
        # Draw outputs
        for output in outputs:
            # Output box
            box = FancyBboxPatch(
                (output['x'] - 1, output['y'] - 0.5),
                2, 1,
                boxstyle="round,pad=0.1",
                facecolor=output['color'],
                edgecolor='black',
                linewidth=1
            )
            ax.add_patch(box)
            
            # Output name
            ax.text(output['x'], output['y'], output['name'], 
                   fontsize=9, ha='center', va='center')
        
        # Arrows showing flow
        arrows = [
            # Agent to Task connections
            (1, 7, 1, 4.8),    # Researcher to Research Task
            (5, 7, 5, 4.8),    # Blog Writer to Write Task
            (9, 7, 9, 4.8),    # Proofreader to Proofread Task
            
            # Task to Output connections
            (1, 3.2, 1, 2),    # Research Task to Research Findings
            (5, 3.2, 5, 2),    # Write Task to Blog Post
            (9, 3.2, 9, 2),    # Proofread Task to Final Blog
            
            # Sequential flow
            (2.5, 4, 3.5, 4),  # Research to Write
            (6.5, 4, 7.5, 4),  # Write to Proofread
        ]
        
        for arrow in arrows:
            ax.annotate('', xy=(arrow[2], arrow[3]), xytext=(arrow[0], arrow[1]),
                       arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        
        # Flow labels
        ax.text(3, 4.3, 'Research\nResults', fontsize=8, ha='center', va='center')
        ax.text(7, 4.3, 'Blog\nContent', fontsize=8, ha='center', va='center')
        
        # Legend
        legend_elements = [
            patches.Patch(color=self.colors['researcher'], label='Agents'),
            patches.Patch(color=self.colors['task'], label='Tasks'),
            patches.Patch(color=self.colors['output'], label='Outputs')
        ]
        ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Workflow diagram saved to: {save_path}")
    
    def create_agent_network(self, save_path: str = "agent_network.png"):
        """
        Create a network diagram showing agent interactions.
        
        Args:
            save_path: Path to save the diagram
        """
        G = nx.DiGraph()
        
        # Add nodes (agents and tasks)
        agents = ['Researcher', 'Blog Writer', 'Proofreader']
        tasks = ['Research Task', 'Write Blog Task', 'Proofread Task']
        outputs = ['Research Findings', 'Blog Post (Draft)', 'Final Blog Post']
        
        # Add all nodes
        for agent in agents:
            G.add_node(agent, type='agent')
        for task in tasks:
            G.add_node(task, type='task')
        for output in outputs:
            G.add_node(output, type='output')
        
        # Add edges (relationships)
        edges = [
            # Agent to Task
            ('Researcher', 'Research Task'),
            ('Blog Writer', 'Write Blog Task'),
            ('Proofreader', 'Proofread Task'),
            
            # Task to Output
            ('Research Task', 'Research Findings'),
            ('Write Blog Task', 'Blog Post (Draft)'),
            ('Proofread Task', 'Final Blog Post'),
            
            # Sequential flow
            ('Research Task', 'Write Blog Task'),
            ('Write Blog Task', 'Proofread Task'),
        ]
        
        G.add_edges_from(edges)
        
        # Create the plot
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G, k=3, iterations=50)
        
        # Draw nodes
        node_colors = []
        node_sizes = []
        
        for node in G.nodes():
            node_type = G.nodes[node]['type']
            if node_type == 'agent':
                node_colors.append(self.colors['researcher'])
                node_sizes.append(3000)
            elif node_type == 'task':
                node_colors.append(self.colors['task'])
                node_sizes.append(2500)
            else:  # output
                node_colors.append(self.colors['output'])
                node_sizes.append(2000)
        
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes)
        nx.draw_networkx_edges(G, pos, edge_color='black', arrows=True, arrowsize=20)
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
        
        plt.title('Blog Writer Agent Network', fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Agent network diagram saved to: {save_path}")
    
    def create_execution_timeline(self, save_path: str = "execution_timeline.png"):
        """
        Create a timeline diagram showing the execution flow.
        
        Args:
            save_path: Path to save the diagram
        """
        fig, ax = plt.subplots(1, 1, figsize=(12, 6))
        
        # Timeline data
        phases = [
            {'name': 'Research Phase', 'start': 0, 'end': 2, 'agent': 'Researcher'},
            {'name': 'Writing Phase', 'start': 2, 'end': 5, 'agent': 'Blog Writer'},
            {'name': 'Proofreading Phase', 'start': 5, 'end': 7, 'agent': 'Proofreader'},
            {'name': 'Final Output', 'start': 7, 'end': 8, 'agent': 'System'}
        ]
        
        colors = [self.colors['researcher'], self.colors['blog_writer'], 
                 self.colors['proofreader'], self.colors['output']]
        
        # Draw timeline bars
        for i, phase in enumerate(phases):
            ax.barh(phase['name'], phase['end'] - phase['start'], 
                   left=phase['start'], color=colors[i], alpha=0.8, 
                   edgecolor='black', linewidth=1)
            
            # Add agent label
            ax.text(phase['start'] + (phase['end'] - phase['start'])/2, 
                   i, phase['agent'], ha='center', va='center', 
                   fontweight='bold', fontsize=10)
        
        # Customize the plot
        ax.set_xlabel('Time (arbitrary units)', fontsize=12)
        ax.set_ylabel('Execution Phases', fontsize=12)
        ax.set_title('Blog Generation Execution Timeline', fontsize=16, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, 8)
        
        # Add retry information
        ax.text(0.5, -0.5, 'Retry Configuration: Research=2, Writing=3, Proofreading=2', 
               fontsize=10, style='italic')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Execution timeline saved to: {save_path}")
    
    def generate_all_visualizations(self, output_dir: str = "visualizations"):
        """
        Generate all visualization types.
        
        Args:
            output_dir: Directory to save all visualizations
        """
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        print("🎨 Generating Blog Writer visualizations...")
        
        self.create_workflow_diagram(output_path / "workflow_diagram.png")
        self.create_agent_network(output_path / "agent_network.png")
        self.create_execution_timeline(output_path / "execution_timeline.png")
        
        # Create a summary file
        summary = {
            "generated_at": datetime.now().isoformat(),
            "visualizations": [
                "workflow_diagram.png - Shows the complete workflow",
                "agent_network.png - Shows agent interactions",
                "execution_timeline.png - Shows execution timeline"
            ],
            "crew_info": {
                "agents": ["Researcher", "Blog Writer", "Proofreader"],
                "tasks": ["Research Task", "Write Blog Task", "Proofread Task"],
                "retry_config": {
                    "research_task": 2,
                    "write_blog_task": 3,
                    "proofread_task": 2,
                    "crew_retries": 2
                }
            }
        }
        
        with open(output_path / "visualization_summary.json", 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"✅ All visualizations saved to: {output_dir}/")
        print("📊 Files generated:")
        print("   - workflow_diagram.png")
        print("   - agent_network.png") 
        print("   - execution_timeline.png")
        print("   - visualization_summary.json") 