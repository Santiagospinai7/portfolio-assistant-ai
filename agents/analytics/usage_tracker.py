# agents/analytics/usage_tracker.py
import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class AnalyticsTracker:
    """
    Simple analytics tracker for monitoring queries to the portfolio assistant
    """
    def __init__(self, storage_path: str = "./data/analytics"):
        self.storage_path = storage_path
        
        # Create storage directory if it doesn't exist
        os.makedirs(storage_path, exist_ok=True)
        
        # Create or load queries file
        self.queries_file = os.path.join(storage_path, "queries.json")
        self.queries = self._load_queries()
    
    def _load_queries(self) -> List[Dict]:
        """Load existing queries from file"""
        if os.path.exists(self.queries_file):
            try:
                with open(self.queries_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading queries: {str(e)}")
        
        return []
    
    def _save_queries(self) -> bool:
        """Save queries to file"""
        try:
            with open(self.queries_file, 'w') as f:
                json.dump(self.queries, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving queries: {str(e)}")
            return False
    
    def track_query(
        self, 
        query: str, 
        user_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        response_time: Optional[float] = None
    ) -> bool:
        """
        Track a query for analytics
        
        Args:
            query: The user's query
            user_id: Optional user identifier
            conversation_id: Optional conversation identifier
            response_time: Optional time taken to process the query
            
        Returns:
            bool: True if successful
        """
        # Create query record
        query_record = {
            "query": query,
            "user_id": user_id or "anonymous",
            "conversation_id": conversation_id,
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "response_time": response_time
        }
        
        # Add to queries list
        self.queries.append(query_record)
        
        # Save to file
        self._save_queries()
        
        # Also save to daily file for better organization
        daily_file = os.path.join(
            self.storage_path, 
            f"queries_{datetime.now().strftime('%Y-%m-%d')}.json"
        )
        
        try:
            daily_queries = []
            if os.path.exists(daily_file):
                with open(daily_file, 'r') as f:
                    daily_queries = json.load(f)
            
            daily_queries.append(query_record)
            
            with open(daily_file, 'w') as f:
                json.dump(daily_queries, f, indent=2)
        except Exception as e:
            print(f"Error saving to daily file: {str(e)}")
        
        return True
    
    def get_recent_queries(self, limit: int = 10) -> List[Dict]:
        """
        Get recent queries
        
        Args:
            limit: Maximum number of queries to return
            
        Returns:
            List of query dictionaries
        """
        return self.queries[-limit:] if self.queries else []
    
    def get_popular_queries(self, limit: int = 10) -> List[Dict]:
        """
        Get most popular queries (naive implementation)
        
        Args:
            limit: Maximum number of results to return
            
        Returns:
            List of dictionaries with query and count
        """
        query_counts = {}
        for query_record in self.queries:
            query = query_record["query"].lower()
            if query in query_counts:
                query_counts[query] += 1
            else:
                query_counts[query] = 1
        
        # Sort by count
        sorted_queries = sorted(
            query_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        # Format results
        return [
            {"query": query, "count": count} 
            for query, count in sorted_queries[:limit]
        ]
    
    def get_analytics_summary(self) -> Dict:
        """
        Get an analytics summary
        
        Returns:
            Dictionary with analytics summary
        """
        if not self.queries:
            return {
                "total_queries": 0,
                "unique_queries": 0,
                "unique_users": 0,
                "avg_response_time": 0,
                "recent_queries": []
            }
        
        # Calculate stats
        total_queries = len(self.queries)
        unique_queries = len(set(q["query"].lower() for q in self.queries))
        unique_users = len(set(q["user_id"] for q in self.queries))
        
        # Calculate average response time
        response_times = [
            q["response_time"] 
            for q in self.queries 
            if q.get("response_time") is not None
        ]
        
        avg_response_time = (
            sum(response_times) / len(response_times) 
            if response_times else 0
        )
        
        # Get recent queries
        recent_queries = self.get_recent_queries(5)
        
        return {
            "total_queries": total_queries,
            "unique_queries": unique_queries,
            "unique_users": unique_users,
            "avg_response_time": avg_response_time,
            "recent_queries": recent_queries
        }