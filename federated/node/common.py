"""
Common functionality for federated learning nodes.
"""

from mininet.node import Docker

def create_docker_container(name, image="ubuntu:latest", **kwargs):
    """Create a Docker container using mininet's Docker class."""
    return Docker(name=name, dimage=image, **kwargs)

class BaseNode:
    """Base class for federated learning nodes."""
    
    def __init__(self, name, node_type="worker"):
        self.name = name
        self.node_type = node_type
        self.status = "inactive"
        
    def start(self):
        """Start the node."""
        self.status = "active"
        print(f"Starting {self.node_type} node: {self.name}")
        
    def stop(self):
        """Stop the node."""
        self.status = "inactive"
        print(f"Stopping {self.node_type} node: {self.name}")
        
    def get_status(self):
        """Get the current status of the node."""
        return self.status