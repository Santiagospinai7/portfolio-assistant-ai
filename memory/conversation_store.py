# memory/conversation_store.py
import json
import os
from datetime import datetime
from typing import Dict, List


class ConversationMemory:
    """
    A class to store and manage conversation history with the portfolio AI
    """
    def __init__(self, storage_path: str = "./data/conversations"):
        self.storage_path = storage_path
        self.in_memory_conversations = {}
        
        # Create storage directory if it doesn't exist
        os.makedirs(storage_path, exist_ok=True)
    
    
    def add_message(self, conversation_id: str, role: str, content: str) -> bool:
        """
        Add a message to a conversation
        
        Args:
            conversation_id: Unique identifier for the conversation
            role: Either 'user' or 'assistant'
            content: The message content
            
        Returns:
            bool: True if successful
        """
        # Validate inputs
        if role not in ["user", "assistant"]:
            raise ValueError("Role must be either 'user' or 'assistant'")
        
        # Ensure content is a string
        if not isinstance(content, str):
            if hasattr(content, 'raw'):
                content = content.raw
            elif hasattr(content, '__str__'):
                content = str(content)
            else:
                content = f"Unable to convert content of type {type(content)} to string"
        
        # Create timestamp
        timestamp = datetime.now().isoformat()
        
        # Create message object
        message = {
            "role": role,
            "content": content,
            "timestamp": timestamp
        }
        
        # Add to in-memory store
        if conversation_id not in self.in_memory_conversations:
            self.in_memory_conversations[conversation_id] = []
        
        self.in_memory_conversations[conversation_id].append(message)
        
        # Persist to disk
        self._save_conversation(conversation_id)
        
        return True
    
    def get_conversation(self, conversation_id: str) -> List[Dict]:
        """
        Retrieve a conversation by ID
        
        Args:
            conversation_id: Unique identifier for the conversation
            
        Returns:
            List of message dictionaries
        """
        # Check in-memory cache first
        if conversation_id in self.in_memory_conversations:
            return self.in_memory_conversations[conversation_id]
        
        # Try to load from disk
        conversation_path = os.path.join(self.storage_path, f"{conversation_id}.json")
        if os.path.exists(conversation_path):
            try:
                with open(conversation_path, 'r') as f:
                    conversation = json.load(f)
                
                # Cache in memory
                self.in_memory_conversations[conversation_id] = conversation
                return conversation
            except Exception as e:
                print(f"Error loading conversation {conversation_id}: {str(e)}")
        
        # Return empty list if not found
        return []
    
    def get_conversation_summary(self, conversation_id: str, max_length: int = 3) -> str:
        """
        Get a summary of the conversation for context
        
        Args:
            conversation_id: Unique identifier for the conversation
            max_length: Maximum number of previous exchanges to include
            
        Returns:
            Formatted string with conversation summary
        """
        conversation = self.get_conversation(conversation_id)
        
        if not conversation:
            return "No previous conversation."
        
        # Take the most recent exchanges, limited by max_length
        recent_messages = conversation[-max_length*2:] if len(conversation) > max_length*2 else conversation
        
        # Format the summary
        summary = "Previous conversation:\n\n"
        for msg in recent_messages:
            speaker = "User" if msg["role"] == "user" else "Assistant"
            summary += f"{speaker}: {msg['content']}\n\n"
        
        return summary
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """
        Delete a conversation
        
        Args:
            conversation_id: Unique identifier for the conversation
            
        Returns:
            bool: True if successful
        """
        # Remove from memory if present
        if conversation_id in self.in_memory_conversations:
            del self.in_memory_conversations[conversation_id]
        
        # Remove from disk if present
        conversation_path = os.path.join(self.storage_path, f"{conversation_id}.json")
        if os.path.exists(conversation_path):
            try:
                os.remove(conversation_path)
                return True
            except Exception as e:
                print(f"Error deleting conversation {conversation_id}: {str(e)}")
                return False
        
        # Return False if not found
        return False
    
    def _save_conversation(self, conversation_id: str) -> bool:
        """
        Save a conversation to disk
        
        Args:
            conversation_id: Unique identifier for the conversation
            
        Returns:
            bool: True if successful
        """
        if conversation_id not in self.in_memory_conversations:
            return False
        
        conversation_path = os.path.join(self.storage_path, f"{conversation_id}.json")
        try:
            with open(conversation_path, 'w') as f:
                json.dump(self.in_memory_conversations[conversation_id], f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving conversation {conversation_id}: {str(e)}")
            return False

    def format_for_context(self, conversation_id: str, max_tokens: int = 1000) -> str:
        """
        Format conversation history for inclusion in LLM context window
        
        Args:
            conversation_id: Unique identifier for the conversation
            max_tokens: Approximate maximum tokens to include
            
        Returns:
            Formatted string suitable for LLM context
        """
        conversation = self.get_conversation(conversation_id)
        
        if not conversation:
            return ""
        
        # Format for LLM context
        formatted = "# Previous Conversation:\n\n"
        
        # Start from the most recent and work backwards until we hit the token limit
        # This is a very rough approximation of tokens
        total_chars = 0
        messages_to_include = []
        
        for msg in reversed(conversation):
            msg_text = f"{msg['role'].title()}: {msg['content']}\n\n"
            msg_chars = len(msg_text)
            
            # Very rough approximation: 4 chars ≈ 1 token
            if total_chars + msg_chars > max_tokens * 4:
                break
                
            messages_to_include.insert(0, msg_text)
            total_chars += msg_chars
        
        formatted += "".join(messages_to_include)
        return formatted