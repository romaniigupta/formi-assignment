import re
import tiktoken

class TokenManager:
    """
    Utility class for managing token count and chunking text to stay under token limits.
    Uses tiktoken for OpenAI-compatible token counting.
    """
    
    def __init__(self, max_tokens=800, model="gpt-3.5-turbo"):
        """
        Initialize the token manager.
        
        Args:
            max_tokens (int): Maximum token size allowed per response
            model (str): Model name to use for tokenization
        """
        self.max_tokens = max_tokens
        self.tokenizer = tiktoken.encoding_for_model(model)
    
    def count_tokens(self, text):
        """
        Count the number of tokens in a text string.
        
        Args:
            text (str): Text to count tokens for
            
        Returns:
            int: Number of tokens in text
        """
        if not text:
            return 0
        
        # Encode the text into tokens
        tokens = self.tokenizer.encode(text)
        return len(tokens)
    
    def truncate_to_max_tokens(self, text):
        """
        Truncate text to stay under max token limit.
        
        Args:
            text (str): Text to truncate
            
        Returns:
            str: Truncated text
        """
        tokens = self.tokenizer.encode(text)
        
        # If already under limit, return the original text
        if len(tokens) <= self.max_tokens:
            return text
            
        # Truncate tokens and decode back to text
        truncated_tokens = tokens[:self.max_tokens]
        truncated_text = self.tokenizer.decode(truncated_tokens)
        
        # Add ellipsis to indicate truncation
        truncated_text += "..."
        
        return truncated_text
    
    def chunk_text(self, text, chunk_size=None):
        """
        Split text into chunks that fit within the token limit.
        
        Args:
            text (str): Text to chunk
            chunk_size (int, optional): Size for each chunk. Defaults to max_tokens.
            
        Returns:
            list: List of text chunks, each under the token limit
        """
        if chunk_size is None:
            chunk_size = self.max_tokens
        
        # Encode the full text
        tokens = self.tokenizer.encode(text)
        
        # If already under limit, return as a single chunk
        if len(tokens) <= chunk_size:
            return [text]
            
        # Create chunks based on token count
        chunks = []
        for i in range(0, len(tokens), chunk_size):
            chunk_tokens = tokens[i:i + chunk_size]
            chunk_text = self.tokenizer.decode(chunk_tokens)
            chunks.append(chunk_text)
            
        return chunks
    
    def optimize_response(self, data, important_fields=None):
        """
        Optimize a data structure to fit within token limits by prioritizing important fields.
        
        Args:
            data (dict or list): Data structure to optimize
            important_fields (list, optional): List of fields to prioritize
            
        Returns:
            dict or list: Optimized data structure
        """
        if important_fields is None:
            important_fields = []
            
        # Convert data to string to count tokens
        data_str = str(data)
        curr_tokens = self.count_tokens(data_str)
        
        # If already under limit, return the original data
        if curr_tokens <= self.max_tokens:
            return data
        
        # Handle lists of dictionaries (like outlets)
        if isinstance(data, list):
            # Create a copy of the list
            optimized_list = []
            
            # Process each item in the list
            for item in data:
                if isinstance(item, dict):
                    # Optimize the dictionary
                    optimized_item = {}
                    
                    # Include only important fields
                    for field in important_fields:
                        if field in item:
                            optimized_item[field] = item[field]
                    
                    optimized_list.append(optimized_item)
                else:
                    # For non-dict items, add them as is
                    optimized_list.append(item)
            
            # Check if optimized list is under the token limit
            if self.count_tokens(str(optimized_list)) <= self.max_tokens:
                return optimized_list
            
            # If still too large, return a smaller subset
            max_items = min(len(optimized_list), 10)  # Return at most 10 items
            return optimized_list[:max_items]
        
        # Create a copy to modify for dictionaries
        optimized_data = data.copy() if isinstance(data, dict) else data
        
        # If it's a dictionary, try to optimize it
        if isinstance(optimized_data, dict):
            # Start by truncating non-important fields
            for key, value in list(optimized_data.items()):
                if key not in important_fields and isinstance(value, str) and len(value) > 100:
                    # Truncate long string fields
                    optimized_data[key] = value[:100] + "..."
            
            # Check if it's now under the limit
            if self.count_tokens(str(optimized_data)) <= self.max_tokens:
                return optimized_data
                
            # If still over limit, remove non-important fields
            for key in list(optimized_data.keys()):
                if key not in important_fields:
                    del optimized_data[key]
                    # Check if we're under the limit after each removal
                    if self.count_tokens(str(optimized_data)) <= self.max_tokens:
                        break
        
        # If we're still over the limit, return only the important data
        if self.count_tokens(str(optimized_data)) > self.max_tokens:
            if isinstance(data, dict):
                return {k: data.get(k) for k in important_fields if k in data}
            return optimized_data
                
        return optimized_data
