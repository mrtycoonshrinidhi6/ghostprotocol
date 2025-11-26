# Memory Architecture Diagram

## Memory Bank Structure

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           MEMORY BANK ARCHITECTURE                          │
└─────────────────────────────────────────────────────────────────────────────┘

                         ┌────────────────────────┐
                         │    MEMORY BANK         │
                         │  (Long-term Storage)   │
                         └───────────┬────────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
                    ▼                ▼                ▼
          ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
          │  EPISODIC    │  │  SEMANTIC    │  │ PROCEDURAL   │
          │  MEMORY      │  │  MEMORY      │  │ MEMORY       │
          └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
                 │                 │                 │
                 │                 │                 │
        Life Events         Beliefs/Facts        Habits/Routines
        Experiences         Knowledge            Patterns
        Moments             Values               Skills
                 │                 │                 │
                 └─────────────────┴─────────────────┘
                                   │
                                   ▼
                         ┌──────────────────┐
                         │  VECTOR INDEX    │
                         │  (Embeddings)    │
                         │  768-dim         │
                         └────────┬─────────┘
                                  │
                      ┌───────────┴───────────┐
                      │                       │
                      ▼                       ▼
              Semantic Search          Similarity Match
              (query → top K)          (cosine distance)


═══════════════════════════════════════════════════════════════════════════

MEMORY ENTRY STRUCTURE
═══════════════════════════════════════════════════════════════════════════

┌────────────────────────────────────────────────────────────────┐
│ MemoryEntry                                                    │
├────────────────────────────────────────────────────────────────┤
│ memory_id:     "mem_a1b2c3d4"                                  │
│ user_id:       "user_12345"                                    │
│ content:       "I proposed to Sarah at Golden Gate Bridge..."  │
│ memory_type:   "episodic"                                      │
│ timestamp:     2010-06-15T14:30:00Z                            │
│ embedding:     [0.12, -0.45, 0.78, ..., 0.33]  # 768 dims     │
│ metadata:      {"event": "proposal", "location": "SF"}        │
│ tags:          ["sarah", "marriage", "milestone"]             │
│ importance:    1.0  # Scale: 0.0 - 1.0                        │
└────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════

CONTEXT COMPACTION PROCESS (for AI Twin)
═══════════════════════════════════════════════════════════════════════════

Input: Generate farewell message to "Michael" (son)

Step 1: RETRIEVE RELEVANT MEMORIES
         │
         ├─► High-importance memories (threshold > 0.8)
         │   └─ "I proposed to Sarah..." (1.0)
         │   └─ "Michael was born on..." (1.0)
         │   └─ "Family is most important..." (0.9)
         │
         ├─► Recent memories (last 90 days)
         │   └─ "Sunday park with Michael..." (60 days ago)
         │   └─ "Michael's graduation..." (45 days ago)
         │
         ├─► Recipient-specific memories (search: "Michael")
         │   └─ 10 memories mentioning Michael
         │
         └─► Context-specific memories (tags: "farewell")
             └─ 5 memories about legacy/values

Step 2: DEDUPLICATE
         │
         ├─ Remove duplicate memory IDs
         └─ 25 unique memories → 18 unique

Step 3: SCORE MEMORIES
         │
         │ Score = (importance × 0.6) + (recency × 0.4)
         │
         ├─ Memory A: (1.0 × 0.6) + (0.9 × 0.4) = 0.96
         ├─ Memory B: (0.8 × 0.6) + (0.7 × 0.4) = 0.76
         └─ Memory C: (0.5 × 0.6) + (0.2 × 0.4) = 0.38
         │
         └─► Sort descending by score

Step 4: FIT TO TOKEN BUDGET (8000 tokens)
         │
         ├─ Memory 1: 150 tokens  ✓ (total: 150)
         ├─ Memory 2: 200 tokens  ✓ (total: 350)
         ├─ Memory 3: 180 tokens  ✓ (total: 530)
         │  ...
         ├─ Memory 15: 220 tokens ✓ (total: 7890)
         └─ Memory 16: 250 tokens ✗ (would exceed 8000)
         │
         └─► 15 memories selected

Step 5: FORMAT AS CONTEXT STRING
         │
         ▼
┌──────────────────────────────────────────────────────────┐
│ Context for message to Michael (farewell):              │
│                                                          │
│ Personal Experiences:                                   │
│ - I proposed to Sarah at Golden Gate Bridge on June 15, │
│   2010. She said yes!                                   │
│ - When you were born, Michael, I held you in my arms... │
│ - Every Sunday morning, I took you to the park to feed  │
│   ducks. Those were my favorite moments.                │
│                                                          │
│ Beliefs & Knowledge:                                    │
│ - Family is the most important thing in life. Always    │
│   put them first.                                       │
│ - Chase your dreams, Michael. I believe in you.         │
│                                                          │
│ Habits & Patterns:                                      │
│ - I always called you "champ" since you were little.    │
│ - Sunday pancakes were our tradition.                   │
└──────────────────────────────────────────────────────────┘
         │
         └─► Send to AI Twin for message generation


═══════════════════════════════════════════════════════════════════════════

SESSION MEMORY INTEGRATION
═══════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────┐
│                      SESSION MEMORY                         │
├─────────────────────────────────────────────────────────────┤
│ session_id:    "sess_xyz789"                                │
│ user_id:       "user_12345"                                 │
│ state:         "LEGACY_EXECUTING"                           │
│ created_at:    2025-11-25T18:00:00Z                         │
│ updated_at:    2025-11-25T18:05:00Z                         │
│                                                             │
│ data:                                                       │
│   ├─ death_confirmation: {...}                             │
│   ├─ asset_inventory: {...}                                │
│   ├─ memory_bank_ref: <MemoryBank instance>                │
│   ├─ legacy_context: "Context for message to Michael..."   │
│   └─ generated_messages: [...]                             │
│                                                             │
│ checkpoint:                                                 │
│   ├─ state: "ASSET_SCANNING"                               │
│   ├─ data_snapshot: {...}                                  │
│   └─ timestamp: 2025-11-25T18:03:00Z                       │
└─────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════

MEMORY RETRIEVAL METHODS
═══════════════════════════════════════════════════════════════════════════

1. SEMANTIC SEARCH
   ┌────────────────────────────────────┐
   │ Query: "advice for my son"         │
   └────────────┬───────────────────────┘
                │
                ├─► Embed query → [0.23, -0.12, ...]
                │
                ├─► Compute similarity with all memories
                │   ├─ Memory 1: cos_sim = 0.92 ✓
                │   ├─ Memory 2: cos_sim = 0.87 ✓
                │   ├─ Memory 3: cos_sim = 0.45 ✗
                │
                └─► Return top 10 matches

2. TYPE FILTER
   ┌────────────────────────────────────┐
   │ get_by_type("episodic")            │
   └────────────┬───────────────────────┘
                │
                └─► Filter all memories where type == "episodic"
                    └─► 45 episodic memories found

3. TAG FILTER
   ┌────────────────────────────────────┐
   │ get_by_tags(["family", "michael"]) │
   └────────────┬───────────────────────┘
                │
                └─► Filter memories containing ANY tag
                    └─► 23 memories with "family" or "michael"

4. IMPORTANCE FILTER
   ┌────────────────────────────────────┐
   │ get_important(threshold=0.8)       │
   └────────────┬───────────────────────┘
                │
                └─► Filter memories where importance >= 0.8
                    └─► 12 high-importance memories

5. RECENCY FILTER
   ┌────────────────────────────────────┐
   │ get_recent(limit=50)               │
   └────────────┬───────────────────────┘
                │
                ├─► Sort by timestamp DESC
                └─► Return first 50


═══════════════════════════════════════════════════════════════════════════

MEMORY LIFECYCLE
═══════════════════════════════════════════════════════════════════════════

CREATE                STORE              RETRIEVE            UPDATE
  │                     │                   │                  │
  ▼                     ▼                   ▼                  ▼
┌─────┐            ┌─────────┐        ┌──────────┐      ┌─────────┐
│User │──content──►│Embedding│──vec──►│Vector DB │──┐   │Metadata │
│Input│            │Model    │        │          │  │   │Update   │
└─────┘            └─────────┘        └──────────┘  │   └─────────┘
  │                     │                   │        │        │
  │                     │                   │        │        │
  └─ tags, metadata ────┴──────────────────┴────────┘        │
                                                              │
                                                              │
DELETE ◄───────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════

STORAGE OPTIMIZATION
═══════════════════════════════════════════════════════════════════════════

User has 1000 memories

┌──────────────────────────────────────────────────────────┐
│ STRATEGY 1: Time-based Compression                      │
├──────────────────────────────────────────────────────────┤
│ Memories > 5 years old:                                  │
│   - Keep only importance > 0.7                           │
│   - Reduce from 400 → 80 memories                        │
│   - 80% reduction                                        │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ STRATEGY 2: Importance-based Pruning                     │
├──────────────────────────────────────────────────────────┤
│ Low-importance memories (< 0.3):                         │
│   - Delete after 1 year                                  │
│   - Free up storage space                                │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ STRATEGY 3: Semantic Clustering                          │
├──────────────────────────────────────────────────────────┤
│ Similar memories clustered together:                     │
│   - "Sunday park with Michael" (50 instances)            │
│   - Merge into single representative memory              │
│   - Metadata tracks count: 50 occurrences                │
└──────────────────────────────────────────────────────────┘
```
