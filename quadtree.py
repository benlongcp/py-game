"""
QuadTree implementation for efficient spatial collision detection.
Provides O(log n) average case collision detection instead of O(n²).
"""

from typing import List, Tuple, Optional
import math


class QuadTreeNode:
    """A node in the QuadTree for spatial partitioning."""
    
    def __init__(self, x: float, y: float, width: float, height: float, max_objects: int = 4, max_levels: int = 5, level: int = 0):
        """
        Initialize a QuadTree node.
        
        Args:
            x, y: Center coordinates of the node
            width, height: Dimensions of the node
            max_objects: Maximum objects per node before subdivision
            max_levels: Maximum depth of the tree
            level: Current depth level
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_objects = max_objects
        self.max_levels = max_levels
        self.level = level
        
        # Objects stored in this node
        self.objects: List[Tuple[int, object]] = []  # (index, projectile)
        
        # Child nodes (NW, NE, SW, SE)
        self.children: List[Optional['QuadTreeNode']] = [None, None, None, None]
        
        # Boundaries
        self.left = x - width / 2
        self.right = x + width / 2
        self.top = y - height / 2
        self.bottom = y + height / 2
    
    def clear(self):
        """Clear all objects and children from this node."""
        self.objects.clear()
        for i in range(4):
            if self.children[i] is not None:
                self.children[i].clear()
                self.children[i] = None
    
    def subdivide(self):
        """Split this node into four quadrants."""
        if self.children[0] is not None:
            return  # Already subdivided
        
        half_width = self.width / 2
        half_height = self.height / 2
        quarter_width = half_width / 2
        quarter_height = half_height / 2
        
        # Create four child nodes
        # NW (0)
        self.children[0] = QuadTreeNode(
            self.x - quarter_width, self.y - quarter_height,
            half_width, half_height,
            self.max_objects, self.max_levels, self.level + 1
        )
        
        # NE (1)
        self.children[1] = QuadTreeNode(
            self.x + quarter_width, self.y - quarter_height,
            half_width, half_height,
            self.max_objects, self.max_levels, self.level + 1
        )
        
        # SW (2)
        self.children[2] = QuadTreeNode(
            self.x - quarter_width, self.y + quarter_height,
            half_width, half_height,
            self.max_objects, self.max_levels, self.level + 1
        )
        
        # SE (3)
        self.children[3] = QuadTreeNode(
            self.x + quarter_width, self.y + quarter_height,
            half_width, half_height,
            self.max_objects, self.max_levels, self.level + 1
        )
    
    def get_quadrant(self, obj_x: float, obj_y: float, obj_radius: float) -> int:
        """
        Determine which quadrant an object belongs to.
        Returns -1 if object spans multiple quadrants.
        """
        # Check if object fits entirely in one quadrant
        obj_left = obj_x - obj_radius
        obj_right = obj_x + obj_radius
        obj_top = obj_y - obj_radius
        obj_bottom = obj_y + obj_radius
        
        vertical_midpoint = self.y
        horizontal_midpoint = self.x
        
        # Top quadrants
        in_top = obj_bottom <= vertical_midpoint
        # Bottom quadrants
        in_bottom = obj_top >= vertical_midpoint
        
        # Left quadrants
        in_left = obj_right <= horizontal_midpoint
        # Right quadrants
        in_right = obj_left >= horizontal_midpoint
        
        if in_top:
            if in_left:
                return 0  # NW
            elif in_right:
                return 1  # NE
        elif in_bottom:
            if in_left:
                return 2  # SW
            elif in_right:
                return 3  # SE
        
        return -1  # Spans multiple quadrants
    
    def insert(self, index: int, obj) -> bool:
        """
        Insert an object into the appropriate quadrant.
        
        Args:
            index: Index of the object
            obj: Object with x, y, and radius attributes
            
        Returns:
            bool: True if inserted successfully
        """
        # Check if object is within this node's bounds
        if not self.contains(obj.x, obj.y, obj.radius):
            return False
        
        # If we have children, try to insert into appropriate child
        if self.children[0] is not None:
            quadrant = self.get_quadrant(obj.x, obj.y, obj.radius)
            if quadrant != -1:
                return self.children[quadrant].insert(index, obj)
        
        # Insert into this node
        self.objects.append((index, obj))
        
        # Check if we need to subdivide
        if (len(self.objects) > self.max_objects and 
            self.level < self.max_levels and 
            self.children[0] is None):
            
            self.subdivide()
            
            # Try to redistribute objects to children
            remaining_objects = []
            for obj_index, obj_data in self.objects:
                quadrant = self.get_quadrant(obj_data.x, obj_data.y, obj_data.radius)
                if quadrant != -1:
                    self.children[quadrant].insert(obj_index, obj_data)
                else:
                    remaining_objects.append((obj_index, obj_data))
            
            self.objects = remaining_objects
        
        return True
    
    def contains(self, x: float, y: float, radius: float) -> bool:
        """Check if an object is within this node's bounds."""
        return (x - radius >= self.left and 
                x + radius <= self.right and
                y - radius >= self.top and
                y + radius <= self.bottom)
    
    def retrieve(self, x: float, y: float, radius: float) -> List[Tuple[int, object]]:
        """
        Retrieve all objects that could potentially collide with the given object.
        
        Args:
            x, y: Object position
            radius: Object radius
            
        Returns:
            List of (index, object) tuples
        """
        candidates = []
        
        # Add objects from this node
        candidates.extend(self.objects)
        
        # If we have children, check relevant quadrants
        if self.children[0] is not None:
            quadrant = self.get_quadrant(x, y, radius)
            
            if quadrant != -1:
                # Object fits in one quadrant
                candidates.extend(self.children[quadrant].retrieve(x, y, radius))
            else:
                # Object spans multiple quadrants, check all children
                for child in self.children:
                    if child is not None:
                        child_candidates = child.retrieve(x, y, radius)
                        candidates.extend(child_candidates)
        
        return candidates


class QuadTree:
    """Main QuadTree class for collision detection optimization."""
    
    def __init__(self, x: float, y: float, width: float, height: float, max_objects: int = 4, max_levels: int = 5):
        """
        Initialize the QuadTree.
        
        Args:
            x, y: Center coordinates of the root node
            width, height: Dimensions of the root node
            max_objects: Maximum objects per node before subdivision
            max_levels: Maximum depth of the tree
        """
        self.root = QuadTreeNode(x, y, width, height, max_objects, max_levels)
        self.total_objects = 0
    
    def clear(self):
        """Clear the entire tree."""
        self.root.clear()
        self.total_objects = 0
    
    def insert(self, index: int, obj) -> bool:
        """Insert an object into the tree."""
        success = self.root.insert(index, obj)
        if success:
            self.total_objects += 1
        return success
    
    def retrieve_candidates(self, obj) -> List[Tuple[int, object]]:
        """Retrieve all objects that could potentially collide with the given object."""
        return self.root.retrieve(obj.x, obj.y, obj.radius)
    
    def get_stats(self) -> dict:
        """Get statistics about the tree structure."""
        def count_nodes(node):
            if node is None:
                return 0, 0, 0  # nodes, leaves, max_depth
            
            if node.children[0] is None:
                # Leaf node
                return 1, 1, 1
            
            total_nodes = 1
            total_leaves = 0
            max_depth = 1
            
            for child in node.children:
                if child is not None:
                    nodes, leaves, depth = count_nodes(child)
                    total_nodes += nodes
                    total_leaves += leaves
                    max_depth = max(max_depth, depth + 1)
            
            return total_nodes, total_leaves, max_depth
        
        nodes, leaves, depth = count_nodes(self.root)
        
        return {
            'total_objects': self.total_objects,
            'total_nodes': nodes,
            'leaf_nodes': leaves,
            'max_depth': depth,
            'avg_objects_per_leaf': self.total_objects / max(1, leaves)
        }
