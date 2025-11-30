"""
Ghost Protocol - Memory & Session Architecture
Long-term memory, session management, and context compaction
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import hashlib


# ============================================================================
# SESSION STATE MANAGEMENT
# ============================================================================

class SessionState(Enum):
    CREATED = "created"
    MONITORING = "monitoring"
    DEATH_DETECTED = "death_detected"
    ASSET_SCANNING = "asset_scanning"
    LEGACY_EXECUTING = "legacy_executing"
    CONTRACT_EXECUTING = "contract_executing"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


@dataclass
class SessionMetadata:
    session_id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    state: SessionState
    current_agent: Optional[str] = None
    checkpoint: Optional[Dict] = None
    error: Optional[str] = None


# ============================================================================
# 1. IN-MEMORY SESSION SERVICE
# ============================================================================

class InMemorySessionService:
    """Manages session lifecycle and state transitions"""
    
    def __init__(self, persistence_file: str = "sessions.json"):
        self.sessions: Dict[str, SessionMetadata] = {}
        self.session_data: Dict[str, Dict] = {}
        self.state_history: Dict[str, List[Dict]] = {}
        self.persistence_file = persistence_file
        self._load_from_disk()
    
    def create_session(self, user_id: str) -> str:
        """Create new session"""
        session_id = self._generate_session_id(user_id)
        
        session = SessionMetadata(
            session_id=session_id,
            user_id=user_id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            state=SessionState.CREATED
        )
        
        self.sessions[session_id] = session
        self.session_data[session_id] = {}
        self.state_history[session_id] = [{
            "state": SessionState.CREATED.value,
            "timestamp": datetime.now().isoformat()
        }]
        
        self._save_to_disk()
        return session_id
    
    def get_session(self, session_id: str) -> Optional[SessionMetadata]:
        """Retrieve session metadata"""
        return self.sessions.get(session_id)
    
    def update_state(self, session_id: str, new_state: SessionState, 
                     agent: Optional[str] = None, checkpoint: Optional[Dict] = None):
        """Transition session to new state"""
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        # Validate state transition
        if not self._is_valid_transition(session.state, new_state):
            raise ValueError(f"Invalid transition: {session.state} -> {new_state}")
        
        session.state = new_state
        session.updated_at = datetime.now()
        session.current_agent = agent
        session.checkpoint = checkpoint
        
        # Log state change
        self.state_history[session_id].append({
            "state": new_state.value,
            "agent": agent,
            "timestamp": datetime.now().isoformat()
        })
        
        self._save_to_disk()
    
    def set_data(self, session_id: str, key: str, value: Any):
        """Store data in session"""
        if session_id not in self.session_data:
            raise ValueError(f"Session {session_id} not found")
        self.session_data[session_id][key] = value
        self._save_to_disk()
        
    def _save_to_disk(self):
        """Persist session state to disk"""
        try:
            data = {
                "sessions": {
                    sid: {
                        "session_id": s.session_id,
                        "user_id": s.user_id,
                        "created_at": s.created_at.isoformat(),
                        "updated_at": s.updated_at.isoformat(),
                        "state": s.state.value,
                        "current_agent": s.current_agent,
                        "checkpoint": s.checkpoint,
                        "error": s.error
                    } for sid, s in self.sessions.items()
                },
                "session_data": self.session_data,
                "state_history": self.state_history
            }
            
            with open(self.persistence_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
                
        except Exception as e:
            print(f"Failed to save sessions: {e}")

    def _load_from_disk(self):
        """Load session state from disk"""
        import os
        if not os.path.exists(self.persistence_file):
            return
            
        try:
            with open(self.persistence_file, 'r') as f:
                data = json.load(f)
                
            self.session_data = data.get("session_data", {})
            self.state_history = data.get("state_history", {})
            
            # Reconstruct SessionMetadata objects
            for sid, s_dict in data.get("sessions", {}).items():
                self.sessions[sid] = SessionMetadata(
                    session_id=s_dict["session_id"],
                    user_id=s_dict["user_id"],
                    created_at=datetime.fromisoformat(s_dict["created_at"]),
                    updated_at=datetime.fromisoformat(s_dict["updated_at"]),
                    state=SessionState(s_dict["state"]),
                    current_agent=s_dict.get("current_agent"),
                    checkpoint=s_dict.get("checkpoint"),
                    error=s_dict.get("error")
                )
                
        except Exception as e:
            print(f"Failed to load sessions: {e}")
    
    def get_data(self, session_id: str, key: str) -> Any:
        """Retrieve data from session"""
        return self.session_data.get(session_id, {}).get(key)
    
    def get_all_data(self, session_id: str) -> Dict:
        """Get all session data"""
        return self.session_data.get(session_id, {})
    
    def pause_session(self, session_id: str):
        """Pause session execution"""
        self.update_state(session_id, SessionState.PAUSED)
    
    def resume_session(self, session_id: str):
        """Resume from paused state"""
        session = self.sessions.get(session_id)
        if session and session.checkpoint:
            # Restore from checkpoint
            previous_state = session.checkpoint.get("previous_state")
            if previous_state:
                self.update_state(session_id, SessionState[previous_state])
    
    def close_session(self, session_id: str, success: bool = True):
        """Mark session as completed or failed"""
        new_state = SessionState.COMPLETED if success else SessionState.FAILED
        self.update_state(session_id, new_state)
    
    def create_checkpoint(self, session_id: str) -> Dict:
        """Create checkpoint for rollback"""
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        checkpoint = {
            "state": session.state.value,
            "agent": session.current_agent,
            "data_snapshot": self.session_data[session_id].copy(),
            "timestamp": datetime.now().isoformat()
        }
        
        session.checkpoint = checkpoint
        return checkpoint
    
    def rollback_to_checkpoint(self, session_id: str):
        """Restore session to last checkpoint"""
        session = self.sessions.get(session_id)
        if not session or not session.checkpoint:
            raise ValueError("No checkpoint available")
        
        checkpoint = session.checkpoint
        self.session_data[session_id] = checkpoint["data_snapshot"]
        session.state = SessionState[checkpoint["state"]]
        session.current_agent = checkpoint["agent"]
    
    def _generate_session_id(self, user_id: str) -> str:
        """Generate unique session ID"""
        timestamp = datetime.now().isoformat()
        raw = f"{user_id}_{timestamp}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]
    
    def _is_valid_transition(self, current: SessionState, target: SessionState) -> bool:
        """Validate state transitions"""
        valid_transitions = {
            SessionState.CREATED: [SessionState.MONITORING],
            SessionState.MONITORING: [SessionState.DEATH_DETECTED, SessionState.PAUSED],
            SessionState.DEATH_DETECTED: [SessionState.ASSET_SCANNING],
            SessionState.ASSET_SCANNING: [SessionState.LEGACY_EXECUTING, SessionState.CONTRACT_EXECUTING],
            SessionState.LEGACY_EXECUTING: [SessionState.COMPLETED, SessionState.FAILED],
            SessionState.CONTRACT_EXECUTING: [SessionState.COMPLETED, SessionState.FAILED],
            SessionState.PAUSED: [SessionState.MONITORING, SessionState.ASSET_SCANNING],
            SessionState.COMPLETED: [],
            SessionState.FAILED: []
        }
        
        return target in valid_transitions.get(current, [])


# ============================================================================
# 2. MEMORY BANK IMPLEMENTATION
# ============================================================================

@dataclass
class MemoryEntry:
    memory_id: str
    user_id: str
    content: str
    memory_type: str  # episodic, semantic, procedural
    timestamp: datetime
    embedding: Optional[List[float]] = None
    metadata: Dict = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    importance: float = 0.5  # 0.0 - 1.0


class MemoryBank:
    """Long-term memory storage with semantic search"""
    
    def __init__(self, embedding_model: Optional[Any] = None):
        self.memories: Dict[str, MemoryEntry] = {}
        self.user_memories: Dict[str, List[str]] = {}  # user_id -> memory_ids
        self.embedding_model = embedding_model
        self.index = {}  # Simple index, would use vector DB in production
    
    def store_memory(self, user_id: str, content: str, memory_type: str,
                     metadata: Optional[Dict] = None, tags: Optional[List[str]] = None,
                     importance: float = 0.5) -> str:
        """Store new memory"""
        memory_id = self._generate_memory_id(user_id, content)
        
        embedding = None
        if self.embedding_model:
            embedding = self._embed(content)
        
        memory = MemoryEntry(
            memory_id=memory_id,
            user_id=user_id,
            content=content,
            memory_type=memory_type,
            timestamp=datetime.now(),
            embedding=embedding,
            metadata=metadata or {},
            tags=tags or [],
            importance=importance
        )
        
        self.memories[memory_id] = memory
        
        if user_id not in self.user_memories:
            self.user_memories[user_id] = []
        self.user_memories[user_id].append(memory_id)
        
        return memory_id
    
    def retrieve_memory(self, memory_id: str) -> Optional[MemoryEntry]:
        """Get specific memory by ID"""
        return self.memories.get(memory_id)
    
    def search_memories(self, user_id: str, query: str, limit: int = 10) -> List[MemoryEntry]:
        """Semantic search for relevant memories"""
        user_memory_ids = self.user_memories.get(user_id, [])
        user_mems = [self.memories[mid] for mid in user_memory_ids]
        
        if self.embedding_model:
            query_embedding = self._embed(query)
            scored = [(m, self._cosine_similarity(query_embedding, m.embedding)) 
                     for m in user_mems if m.embedding]
            scored.sort(key=lambda x: x[1], reverse=True)
            return [m for m, score in scored[:limit]]
        else:
            # Simple keyword search fallback
            filtered = [m for m in user_mems if query.lower() in m.content.lower()]
            return filtered[:limit]
    
    def get_by_type(self, user_id: str, memory_type: str) -> List[MemoryEntry]:
        """Retrieve memories by type"""
        user_memory_ids = self.user_memories.get(user_id, [])
        return [self.memories[mid] for mid in user_memory_ids 
                if self.memories[mid].memory_type == memory_type]
    
    def get_by_tags(self, user_id: str, tags: List[str]) -> List[MemoryEntry]:
        """Retrieve memories by tags"""
        user_memory_ids = self.user_memories.get(user_id, [])
        return [self.memories[mid] for mid in user_memory_ids
                if any(tag in self.memories[mid].tags for tag in tags)]
    
    def get_recent_memories(self, user_id: str, limit: int = 50) -> List[MemoryEntry]:
        """Get most recent memories"""
        user_memory_ids = self.user_memories.get(user_id, [])
        mems = [self.memories[mid] for mid in user_memory_ids]
        mems.sort(key=lambda x: x.timestamp, reverse=True)
        return mems[:limit]
    
    def get_important_memories(self, user_id: str, threshold: float = 0.7) -> List[MemoryEntry]:
        """Get high-importance memories"""
        user_memory_ids = self.user_memories.get(user_id, [])
        return [self.memories[mid] for mid in user_memory_ids 
                if self.memories[mid].importance >= threshold]
    
    def compact_memories(self, user_id: str, time_window_days: int = 30) -> List[MemoryEntry]:
        """Get memories within time window, sorted by importance"""
        cutoff = datetime.now() - timedelta(days=time_window_days)
        user_memory_ids = self.user_memories.get(user_id, [])
        
        recent = [self.memories[mid] for mid in user_memory_ids 
                 if self.memories[mid].timestamp >= cutoff]
        recent.sort(key=lambda x: x.importance, reverse=True)
        
        return recent
    
    def delete_memory(self, memory_id: str):
        """Remove memory from bank"""
        if memory_id in self.memories:
            user_id = self.memories[memory_id].user_id
            del self.memories[memory_id]
            if user_id in self.user_memories:
                self.user_memories[user_id].remove(memory_id)
    
    def _generate_memory_id(self, user_id: str, content: str) -> str:
        """Generate unique memory ID"""
        timestamp = datetime.now().isoformat()
        raw = f"{user_id}_{content[:100]}_{timestamp}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]
    
    def _embed(self, text: str) -> List[float]:
        """Generate embedding (mock)"""
        # In production: use sentence-transformers or OpenAI embeddings
        return [0.1] * 768  # Mock 768-dim embedding
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity (mock)"""
        return 0.85  # Mock similarity score


# ============================================================================
# 3. CONTEXT COMPACTION FOR LEGACY AGENT
# ============================================================================

class ContextCompactor:
    """Compact context for LegacyAgent AI Twin"""
    
    def __init__(self, memory_bank: MemoryBank):
        self.memory_bank = memory_bank
        self.max_tokens = 8000  # Context window limit
    
    def compact_for_message_generation(self, user_id: str, recipient: str,
                                       context_type: str) -> str:
        """Compact user memories into context for AI Twin"""
        
        # Strategy: importance-weighted + recency + relevance
        
        # 1. Get high-importance memories (life events)
        important = self.memory_bank.get_important_memories(user_id, threshold=0.8)
        
        # 2. Get recent memories (last 90 days)
        recent = self.memory_bank.compact_memories(user_id, time_window_days=90)
        
        # 3. Get recipient-specific memories
        recipient_mems = self.memory_bank.search_memories(user_id, recipient, limit=20)
        
        # 4. Get context-specific memories
        context_mems = self.memory_bank.get_by_tags(user_id, [context_type])
        
        # 5. Merge and deduplicate
        all_memories = self._deduplicate([
            *important[:10],
            *recipient_mems[:10],
            *context_mems[:10],
            *recent[:20]
        ])
        
        # 6. Sort by importance * recency
        scored = self._score_memories(all_memories)
        
        # 7. Fit within token budget
        compacted = self._fit_to_budget(scored, self.max_tokens)
        
        # 8. Format as context string
        context = self._format_context(compacted, recipient, context_type)
        
        return context
    
    def _deduplicate(self, memories: List[MemoryEntry]) -> List[MemoryEntry]:
        """Remove duplicate memories"""
        seen = set()
        unique = []
        for mem in memories:
            if mem.memory_id not in seen:
                seen.add(mem.memory_id)
                unique.append(mem)
        return unique
    
    def _score_memories(self, memories: List[MemoryEntry]) -> List[tuple]:
        """Score memories by importance and recency"""
        now = datetime.now()
        scored = []
        
        for mem in memories:
            age_days = (now - mem.timestamp).days
            recency_score = max(0, 1 - (age_days / 365))  # Decay over 1 year
            combined_score = (mem.importance * 0.6) + (recency_score * 0.4)
            scored.append((mem, combined_score))
        
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored
    
    def _fit_to_budget(self, scored_memories: List[tuple], max_tokens: int) -> List[MemoryEntry]:
        """Select memories that fit within token budget"""
        selected = []
        total_tokens = 0
        
        for mem, score in scored_memories:
            mem_tokens = len(mem.content.split())  # Rough estimate
            if total_tokens + mem_tokens <= max_tokens:
                selected.append(mem)
                total_tokens += mem_tokens
            else:
                break
        
        return selected
    
    def _format_context(self, memories: List[MemoryEntry], recipient: str, 
                       context_type: str) -> str:
        """Format memories into context string"""
        sections = {
            "episodic": [],
            "semantic": [],
            "procedural": []
        }
        
        for mem in memories:
            sections[mem.memory_type].append(mem.content)
        
        context = f"Context for message to {recipient} ({context_type}):\n\n"
        
        if sections["episodic"]:
            context += "Personal Experiences:\n"
            for exp in sections["episodic"]:
                context += f"- {exp}\n"
            context += "\n"
        
        if sections["semantic"]:
            context += "Beliefs & Knowledge:\n"
            for fact in sections["semantic"]:
                context += f"- {fact}\n"
            context += "\n"
        
        if sections["procedural"]:
            context += "Habits & Patterns:\n"
            for habit in sections["procedural"]:
                context += f"- {habit}\n"
        
        return context


# ============================================================================
# 4. MEMORY WRITE/READ EXAMPLES
# ============================================================================

def example_memory_operations():
    """Demonstrate memory write and read operations"""
    
    # Initialize memory bank
    memory_bank = MemoryBank()
    user_id = "user_12345"
    
    # WRITE: Store episodic memory (life event)
    memory_bank.store_memory(
        user_id=user_id,
        content="I proposed to Sarah at Golden Gate Bridge on June 15, 2010. She said yes!",
        memory_type="episodic",
        metadata={"event": "proposal", "location": "Golden Gate Bridge"},
        tags=["sarah", "marriage", "milestone"],
        importance=1.0
    )
    
    # WRITE: Store semantic memory (belief)
    memory_bank.store_memory(
        user_id=user_id,
        content="Family is the most important thing in life. Always put them first.",
        memory_type="semantic",
        metadata={"category": "values"},
        tags=["family", "values"],
        importance=0.9
    )
    
    # WRITE: Store procedural memory (habit)
    memory_bank.store_memory(
        user_id=user_id,
        content="Every Sunday morning, I take my daughter Emma to the park to feed ducks.",
        memory_type="procedural",
        metadata={"frequency": "weekly", "day": "Sunday"},
        tags=["emma", "routine", "parenting"],
        importance=0.7
    )
    
    # READ: Search for memories about Sarah
    sarah_memories = memory_bank.search_memories(user_id, "Sarah", limit=5)
    
    # READ: Get all episodic memories
    life_events = memory_bank.get_by_type(user_id, "episodic")
    
    # READ: Get recent memories (last 30 days)
    recent = memory_bank.get_recent_memories(user_id, limit=10)
    
    # READ: Get important memories
    important = memory_bank.get_important_memories(user_id, threshold=0.8)
    
    # READ: Get memories by tags
    family_mems = memory_bank.get_by_tags(user_id, ["family", "emma"])
    
    return {
        "sarah_memories": sarah_memories,
        "life_events": life_events,
        "recent": recent,
        "important": important,
        "family": family_mems
    }


def example_session_usage():
    """Demonstrate session lifecycle"""
    
    service = InMemorySessionService()
    
    # Create session
    session_id = service.create_session(user_id="user_12345")
    
    # Transition: CREATED -> MONITORING
    service.update_state(session_id, SessionState.MONITORING, agent="LoopAgent")
    
    # Store data
    service.set_data(session_id, "last_check", datetime.now().isoformat())
    service.set_data(session_id, "check_count", 0)
    
    # Create checkpoint
    service.create_checkpoint(session_id)
    
    # Transition: MONITORING -> DEATH_DETECTED
    service.update_state(session_id, SessionState.DEATH_DETECTED, 
                        agent="DeathDetectionAgent")
    
    # Store detection results
    service.set_data(session_id, "death_confirmation", {
        "confidence": 0.98,
        "sources": ["obituary", "death_registry"]
    })
    
    # Transition: DEATH_DETECTED -> ASSET_SCANNING
    service.update_state(session_id, SessionState.ASSET_SCANNING,
                        agent="DigitalAssetAgent")
    
    # Retrieve session data
    all_data = service.get_all_data(session_id)
    
    # Pause if needed
    service.pause_session(session_id)
    
    # Resume later
    service.resume_session(session_id)
    
    # Complete
    service.close_session(session_id, success=True)
    
    return session_id


# ============================================================================
# 5. SESSION LIFECYCLE STATE DIAGRAM (ASCII)
# ============================================================================

SESSION_LIFECYCLE_DIAGRAM = """
SESSION LIFECYCLE STATE DIAGRAM
================================

                    ┌─────────────┐
                    │   CREATED   │
                    └──────┬──────┘
                           │
                           │ initialize
                           ▼
                    ┌─────────────┐
                ┌───┤  MONITORING │◄───┐
                │   └──────┬──────┘    │
                │          │            │
                │          │ death      │
                │          │ confirmed  │ resume
                │          ▼            │
       pause    │   ┌──────────────┐   │
                └──►│DEATH_DETECTED│   │
                    └──────┬───────┘   │
                           │            │
                           │ trigger    │
                           │ pipeline   │
                           ▼            │
                    ┌──────────────┐   │
                ┌───┤ASSET_SCANNING│   │
                │   └──────┬───────┘   │
                │          │            │
       pause    │          │ assets     │
                │          │ found      │
                └──────────┼────────────┘
                           │
                           ├─────────────────┐
                           │                 │
                           ▼                 ▼
                  ┌─────────────────┐ ┌──────────────────┐
                  │LEGACY_EXECUTING │ │CONTRACT_EXECUTING│
                  └────────┬─────────┘ └────────┬─────────┘
                           │                    │
                           │ messages           │ transfers
                           │ sent               │ complete
                           │                    │
                           └──────────┬─────────┘
                                      │
                                      ▼
                              ┌───────────────┐
                              │   COMPLETED   │
                              └───────────────┘

                           Error at any stage
                                      │
                                      ▼
                              ┌───────────────┐
                              │    FAILED     │
                              └───────────────┘

State Transitions:
- CREATED → MONITORING (init)
- MONITORING → DEATH_DETECTED (death confirmed)
- MONITORING → PAUSED (manual pause)
- DEATH_DETECTED → ASSET_SCANNING (pipeline trigger)
- ASSET_SCANNING → LEGACY_EXECUTING (parallel start)
- ASSET_SCANNING → CONTRACT_EXECUTING (parallel start)
- LEGACY_EXECUTING → COMPLETED (success)
- CONTRACT_EXECUTING → COMPLETED (success)
- PAUSED → MONITORING (resume)
- PAUSED → ASSET_SCANNING (resume)
- Any state → FAILED (error)
"""


# ============================================================================
# INTEGRATION EXAMPLE
# ============================================================================

def integrated_memory_session_example():
    """Full example integrating memory and session"""
    
    # Setup
    memory_bank = MemoryBank()
    session_service = InMemorySessionService()
    compactor = ContextCompactor(memory_bank)
    
    user_id = "user_12345"
    
    # Store user memories
    memory_bank.store_memory(
        user_id, 
        "Tell my son Michael that I'm proud of him and to follow his dreams",
        "episodic",
        tags=["michael", "farewell"],
        importance=1.0
    )
    
    # Create session
    session_id = session_service.create_session(user_id)
    
    # Store memory bank reference in session
    session_service.set_data(session_id, "memory_bank", memory_bank)
    session_service.set_data(session_id, "user_id", user_id)
    
    # Later: LegacyAgent needs context
    context = compactor.compact_for_message_generation(
        user_id=user_id,
        recipient="Michael",
        context_type="farewell"
    )
    
    # Store generated context in session
    session_service.set_data(session_id, "legacy_context", context)
    
    return {
        "session_id": session_id,
        "context_length": len(context),
        "memory_count": len(memory_bank.user_memories.get(user_id, []))
    }
