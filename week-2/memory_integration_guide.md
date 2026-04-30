# Week 2: Memory Integration Guide

## How Chanakya Uses Your Memory

### Step 1: Load Personal Info
When Chanakya starts, it automatically loads:
- Your name, age, city, profession
- Health conditions and medications
- Goals and preferences
- Recent conversation history

### Step 2: Inject Into LLM Context

Before sending any query to Ollama, Chanakya prepends this context:

```
**User Profile (Memory):**
Name: [Your Name]
Age: [Your Age]
City: [Your City]
Profession: [Your Profession]

**Recent Memories:**
- [category] key: value
- [category] key: value
...

User Query: [User's Actual Question]
```

### Step 3: Ollama Responds with Context

Ollama now understands:
- Who you are
- What your goals are
- Your health conditions
- Your preferences

Responses become personalized!

---

## Example Flow

### Without Memory:
```
User: "Mujhe workout plan chahiye"
Changakya: "Yeh general workout plan hai..." (generic response)
```

### With Memory:
```
Memory contains:
- Age: 25
- Profession: Software Engineer
- Goal: Build muscle
- Health: No injuries
- Preference: Home workouts (no gym)

Changakya: "25 saal ke software engineer ke liye, ghar pe 30 minute daily..."
(personalized response!)
```

---

## Setup Instructions

### 1. Initialize Memory Database

```python
from week_2.memory_system import MemorySystem

memory = MemorySystem()

# Add personal info
memory.update_personal_info({
    "name": "Aapka Naam",
    "age": 25,
    "city": "Kolkata",
    "profession": "Developer"
})

# Add some initial memories
memory.add_memory("personal", "hobby", "Photography", importance=7)
memory.add_memory("health", "allergies", "Peanuts", importance=10)
memory.add_memory("work", "current_project", "Building Chanakya AI", importance=9)
```

### 2. Use Memory Editor CLI

```bash
python week-2/memory_editor.py
```

Interactive menu to:
- View personal info
- Add/update/delete memories
- Log health
- Add goals
- Backup memory

### 3. Integrate with Ollama

When sending query to Ollama:

```python
# Get memory context
context = memory.get_context_for_llm(max_memories=10)

# Prepend to user query
full_prompt = context + "\n\nUser Question: " + user_input

# Send to Ollama
response = ollama.generate(model='llama3.2', prompt=full_prompt)
```

---

## Memory Categories

Organize memories into categories:

| Category | Examples |
|----------|----------|
| **personal** | Name, age, city, hobbies, interests |
| **health** | Conditions, medications, allergies, weight |
| **work** | Job, company, projects, skills, goals |
| **goals** | Short-term and long-term objectives |
| **preferences** | Language, timezone, voice speed |
| **relationships** | Family, friends, important people |
| **important_dates** | Birthday, anniversary, deadlines |

---

## Privacy & Security

### What's Stored
- Personal info (name, age, city, profession)
- Health data (conditions, medications)
- Conversation history
- Goals and preferences
- Important dates

### Where It's Stored
- **LOCAL ONLY** - Never sent to cloud
- Encrypted SQLite database
- Encrypted JSON backups
- Optional password protection

### Backup Strategy

```bash
# Automatic daily backup at 2 AM
# Manual backup anytime:
python -c "from week_2.memory_system import MemorySystem; MemorySystem().backup_memory()"
```

Backups stored in `memory/backups/` folder

---

## Testing Memory Integration

```python
from week_2.memory_system import MemorySystem

memory = MemorySystem()

# Add test memories
memory.add_memory("personal", "name", "Test User", importance=10)
memory.add_memory("health", "allergies", "Peanuts", importance=10)

# Test retrieval
name = memory.get_memory("personal", "name")
print(f"Name: {name}")

# Test LLM context generation
context = memory.get_context_for_llm()
print(context)

# Test conversation logging
memory.add_conversation(
    user_input="Hello Chanakya",
    ai_response="Namaste! Aap kaisa ho?",
    category="greeting"
)
```

---

## Troubleshooting

### Memory Not Persisting
- Check if `memory/` folder exists
- Verify database permissions
- Check `chanakya_memory.db` file size

### Context Too Long for LLM
- Reduce `max_memories` parameter
- Delete old, less important memories
- Archive old conversations

### Backup Fails
- Verify `memory/backups/` folder exists
- Check disk space
- Verify file write permissions

---

## Next Steps (Week 3)

Week 3 will add:
- Voice input (Whisper) with memory context
- Automatic memory updates from conversations
- Health tracking integration
- Goal progress tracking
