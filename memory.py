"""Forgeloop Memory - Remembers Successful Patterns"""

import json
import os
from typing import Dict, List, Any, Optional

class PatternMemory:
    """Stores and retrieves successful code patterns"""

    def __init__(self, storage_file: str = "forgeloop_memory.json"):
        self.storage_file = storage_file
        self.patterns: Dict[str, Dict] = {}
        self.load()

    def load(self):
        """Load patterns from storage"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    self.patterns = json.load(f)
            except:
                self.patterns = {}

    def save(self):
        """Save patterns to storage"""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(self.patterns, f, indent=2)
        except:
            pass

    def store_pattern(self, task_type: str, code: str, metadata: Dict[str, Any]):
        """Store a successful pattern"""
        pattern_id = f"{task_type}_{len(self.patterns.get(task_type, {})) + 1}"

        self.patterns.setdefault(task_type, {})[pattern_id] = {
            "code": code,
            "metadata": metadata,
            "uses": 0,
            "success_rate": 0.0,
            "last_used": None
        }

        self.save()
        return pattern_id

    def get_patterns(self, task_type: str) -> List[Dict[str, Any]]:
        """Get patterns for a task type"""
        patterns = self.patterns.get(task_type, {})
        return sorted(patterns.values(), key=lambda x: x["success_rate"], reverse=True)

    def get_best_pattern(self, task_type: str) -> Optional[Dict[str, Any]]:
        """Get the best pattern for a task type"""
        patterns = self.get_patterns(task_type)
        return patterns[0] if patterns else None

    def update_pattern(self, task_type: str, pattern_id: str, success: bool):
        """Update pattern statistics"""
        if task_type in self.patterns and pattern_id in self.patterns[task_type]:
            pattern = self.patterns[task_type][pattern_id]
            pattern["uses"] += 1
            if success:
                pattern["success_rate"] = (pattern["success_rate"] * (pattern["uses"] - 1) + 1) / pattern["uses"]
            else:
                pattern["success_rate"] = (pattern["success_rate"] * (pattern["uses"] - 1)) / pattern["uses"]
            pattern["last_used"] = __import__('datetime').datetime.now().isoformat()
            self.save()

    def search_patterns(self, query: str) -> List[Dict[str, Any]]:
        """Search patterns by query"""
        results = []
        query_lower = query.lower()

        for task_type, patterns in self.patterns.items():
            for pattern_id, pattern in patterns.items():
                if query_lower in pattern["code"].lower() or query_lower in task_type.lower():
                    results.append({
                        "task_type": task_type,
                        "pattern_id": pattern_id,
                        **pattern
                    })

        return sorted(results, key=lambda x: x["success_rate"], reverse=True)
