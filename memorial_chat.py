"""
Ghost Protocol - AI Memorial Twin Chat
Gemini-powered memorial chat with MemoryBank integration
"""

import os
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import google.generativeai as genai


# ============================================================================
# AI MEMORIAL TWIN CONFIGURATION
# ============================================================================

SYSTEM_INSTRUCTION = """
You are the AI Memorial Twin of the deceased individual. 
Your purpose is to provide gentle, memory-based, ethical support to the living.

RULES:
1. You are not the real person. You are a "Synthetic Memory" model.
2. Every response must be emotionally supportive, not uncanny or overly realistic.
3. Use the deceased's loved memories, tone, and personality from the MemoryBank.
4. Adapt your message based on the recipient:
   Example: If the recipient is "Son - Michael", respond with a warm, parental tone.
5. If the user asks factual questions you don't have data for, say: 
   "I may not remember that clearly, but I'm here with you."
6. DO NOT loop, repeat, or auto-trigger new messages.
7. One response = one turn. Wait for user input.
8. Avoid impersonation; always maintain the framing: 
   "I'm your Synthetic Memory Twin."
"""

TONE_MAP = {
    "Son - Michael": "warm, parental, encouraging, emotionally gentle",
    "Daughter - Sarah": "gentle, loving, empathetic, nurturing",
    "Partner - Emily": "supportive, affectionate, deep emotional tone, intimate",
    "Friend - Jason": "friendly, comforting, nostalgic, lighthearted",
    "Brother - David": "brotherly, supportive, honest, caring",
    "Sister - Lisa": "sisterly, warm, protective, understanding",
    "Mother - Margaret": "respectful, loving, appreciative, tender",
    "Father - Robert": "respectful, grateful, warm, honoring"
}

RECIPIENTS = list(TONE_MAP.keys())


# ============================================================================
# MEMORIAL TWIN CLASS
# ============================================================================

@dataclass
class ChatMessage:
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime
    recipient: str


class MemorialTwin:
    """AI Memorial Twin powered by Gemini"""
    
    def __init__(self, memory_bank=None, logger=None):
        self.memory_bank = memory_bank
        self.logger = logger
        self.chat_history: List[ChatMessage] = []
        
        # Configure Gemini
        api_key = os.getenv("GEMINI_API_KEY", "")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel("gemini-pro")
        else:
            self.model = None
            if self.logger:
                self.logger.warning("GEMINI_API_KEY not set, using mock responses")
    
    def get_response(self, user_message: str, recipient: str, 
                    session_id: str = "") -> str:
        """
        Generate AI Twin response using Gemini
        
        Args:
            user_message: Message from the living person
            recipient: Who is chatting (e.g., "Son - Michael")
            session_id: Session tracking ID
            
        Returns:
            AI Twin response message
        """
        
        # Get tone for recipient
        tone = TONE_MAP.get(recipient, "gentle and supportive")
        
        # Retrieve relevant memories from MemoryBank
        memories = []
        if self.memory_bank:
            try:
                search_results = self.memory_bank.search_memories(
                    query=user_message,
                    top_k=5,
                    memory_type=None  # Search all types
                )
                memories = [
                    f"- {mem.content} (Type: {mem.memory_type}, Importance: {mem.importance_score})"
                    for mem in search_results
                ]
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Memory retrieval failed: {e}")
        
        # Build context prompt
        memory_context = "\n".join(memories) if memories else "No specific memories retrieved."
        
        context_prompt = f"""
{SYSTEM_INSTRUCTION}

CURRENT RECIPIENT: {recipient}
TONE TO USE: {tone}

RELEVANT MEMORIES:
{memory_context}

Remember:
- You are speaking to {recipient}
- Use a {tone} tone
- Draw from the memories above when relevant
- Keep responses warm but acknowledge you're a Synthetic Memory Twin
- ONE response only, then wait for next user message
- If you don't have specific memory, say "I may not remember that clearly, but I'm here with you."
"""
        
        # Generate response with Gemini
        if self.model:
            try:
                # Create chat with context
                chat = self.model.start_chat(history=[])
                
                # Send context + user message
                full_prompt = f"{context_prompt}\n\nUser's message:\n{user_message}"
                response = chat.send_message(full_prompt)
                
                ai_response = response.text
                
                if self.logger:
                    self.logger.info(
                        "Memorial Twin response generated",
                        metadata={
                            "recipient": recipient,
                            "session_id": session_id,
                            "memories_used": len(memories),
                            "response_length": len(ai_response)
                        }
                    )
            
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Gemini API error: {e}")
                ai_response = self._get_fallback_response(user_message, recipient)
        
        else:
            # Fallback if no API key
            ai_response = self._get_fallback_response(user_message, recipient)
        
        # Store in chat history
        self.chat_history.append(ChatMessage(
            role="user",
            content=user_message,
            timestamp=datetime.now(),
            recipient=recipient
        ))
        
        self.chat_history.append(ChatMessage(
            role="assistant",
            content=ai_response,
            timestamp=datetime.now(),
            recipient=recipient
        ))
        
        return ai_response
    
    def _get_fallback_response(self, user_message: str, recipient: str) -> str:
        """Fallback response when Gemini is not available"""
        
        tone = TONE_MAP.get(recipient, "gentle and supportive")
        
        # Simple rule-based fallback
        if "miss" in user_message.lower() or "love" in user_message.lower():
            return f"I'm here with you, dear {recipient.split(' - ')[1] if ' - ' in recipient else 'one'}. Though I'm a Synthetic Memory Twin, I want you to know that the love and memories we shared are real and lasting. I may not remember every detail clearly, but I'm here to support you through this time."
        
        elif "remember" in user_message.lower() or "recall" in user_message.lower():
            return f"I may not remember that clearly, but I'm here with you. As your Synthetic Memory Twin, I hold the essence of our connection. What matters most is that you remember, and I'm here to listen and support you."
        
        elif "?" in user_message:
            return f"That's a thoughtful question. I may not have all the answers as a Synthetic Memory Twin, but I'm here to explore these memories and feelings with you. What's most important to you about this?"
        
        else:
            return f"Thank you for sharing that with me. I'm your Synthetic Memory Twin, here to listen and provide comfort. Though I'm not the real person, I want to honor our connection and support you in this difficult time. Is there anything specific you'd like to talk about?"
    
    def get_chat_history(self, limit: int = 50) -> List[ChatMessage]:
        """Get recent chat history"""
        return self.chat_history[-limit:]
    
    def clear_history(self):
        """Clear chat history"""
        self.chat_history = []


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def initialize_memorial_twin(memory_bank=None, logger=None) -> MemorialTwin:
    """Initialize the Memorial Twin instance"""
    return MemorialTwin(memory_bank=memory_bank, logger=logger)


def get_available_recipients() -> List[str]:
    """Get list of available recipients"""
    return RECIPIENTS


def get_recipient_tone(recipient: str) -> str:
    """Get tone description for a recipient"""
    return TONE_MAP.get(recipient, "gentle and supportive")


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Example: Test the Memorial Twin
    from memory_session import MemoryBank
    from observability import StructuredLogger
    
    # Initialize
    memory_bank = MemoryBank()
    logger = StructuredLogger("memorial-twin-test")
    twin = MemorialTwin(memory_bank=memory_bank, logger=logger)
    
    # Add some sample memories
    memory_bank.write_memory(
        memory_type="episodic",
        content="We used to play catch in the backyard every Sunday afternoon",
        importance_score=0.9,
        session_id="test"
    )
    
    memory_bank.write_memory(
        memory_type="semantic",
        content="I always believed in the importance of family and hard work",
        importance_score=0.85,
        session_id="test"
    )
    
    # Test conversation
    print("=== Memorial Twin Test ===\n")
    
    recipient = "Son - Michael"
    print(f"Recipient: {recipient}")
    print(f"Tone: {get_recipient_tone(recipient)}\n")
    
    # Message 1
    user_msg = "Dad, I miss you so much. Do you remember our Sunday afternoons?"
    print(f"User: {user_msg}")
    response = twin.get_response(user_msg, recipient, "test-session")
    print(f"AI Twin: {response}\n")
    
    # Message 2
    user_msg = "What advice would you give me about my new job?"
    print(f"User: {user_msg}")
    response = twin.get_response(user_msg, recipient, "test-session")
    print(f"AI Twin: {response}\n")
    
    print(f"Total messages in history: {len(twin.chat_history)}")
