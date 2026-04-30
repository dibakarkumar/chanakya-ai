import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path
import hashlib
from cryptography.fernet import Fernet

class MemorySystem:
    """Chanakya's Personal Memory Management System"""
    
    def __init__(self, memory_dir="memory", db_name="chanakya_memory.db"):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(exist_ok=True)
        
        self.db_path = self.memory_dir / db_name
        self.json_path = self.memory_dir / "memory.json"
        self.backup_dir = self.memory_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        
        self._init_database()
        self._init_json_storage()
    
    def _init_database(self):
        """Initialize SQLite database for structured memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Main memory table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                importance INTEGER DEFAULT 5,
                expires_at DATETIME DEFAULT NULL,
                UNIQUE(category, key)
            )
        """)
        
        # Conversation history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_input TEXT NOT NULL,
                ai_response TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                category TEXT DEFAULT 'general'
            )
        """)
        
        # Health journal table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS health_journal (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                symptoms TEXT,
                mood INTEGER,
                medications TEXT,
                notes TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(date)
            )
        """)
        
        # Goals table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal_name TEXT NOT NULL,
                category TEXT,
                start_date DATE,
                target_date DATE,
                frequency TEXT,
                status TEXT DEFAULT 'active',
                progress_percentage INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def _init_json_storage(self):
        """Initialize JSON storage for personal info"""
        if not self.json_path.exists():
            template = {
                "personal_info": {
                    "name": "",
                    "age": "",
                    "city": "",
                    "profession": "",
                    "education": ""
                },
                "health": {
                    "conditions": [],
                    "medications": [],
                    "allergies": []
                },
                "preferences": {
                    "language": "Hinglish",
                    "voice_speed": 1.0,
                    "timezone": "IST"
                },
                "goals": [],
                "important_dates": {},
                "notes": []
            }
            self._save_json(template)
    
    def _save_json(self, data):
        """Save data to JSON file"""
        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _load_json(self):
        """Load data from JSON file"""
        if self.json_path.exists():
            with open(self.json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def add_memory(self, category: str, key: str, value: str, importance: int = 5):
        """Add or update a memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO memories (category, key, value, importance)
                VALUES (?, ?, ?, ?)
            """, (category, key, value, importance))
            conn.commit()
            print(f"✅ Memory saved: {category}/{key}")
        except Exception as e:
            print(f"❌ Error saving memory: {e}")
        finally:
            conn.close()
    
    def get_memory(self, category: str, key: str = None):
        """Retrieve memory by category and key"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if key:
            cursor.execute(
                "SELECT value FROM memories WHERE category=? AND key=?",
                (category, key)
            )
        else:
            cursor.execute(
                "SELECT key, value FROM memories WHERE category=?",
                (category,)
            )
        
        result = cursor.fetchall()
        conn.close()
        return result
    
    def delete_memory(self, category: str, key: str):
        """Delete a specific memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "DELETE FROM memories WHERE category=? AND key=?",
            (category, key)
        )
        conn.commit()
        conn.close()
        print(f"🗑️ Memory deleted: {category}/{key}")
    
    def add_conversation(self, user_input: str, ai_response: str, category: str = "general"):
        """Log a conversation"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO conversations (user_input, ai_response, category)
            VALUES (?, ?, ?)
        """, (user_input, ai_response, category))
        
        conn.commit()
        conn.close()
    
    def log_health(self, date: str, symptoms: str = None, mood: int = None, 
                   medications: str = None, notes: str = None):
        """Log health information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO health_journal 
                (date, symptoms, mood, medications, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (date, symptoms, mood, medications, notes))
            conn.commit()
            print(f"✅ Health logged for {date}")
        except Exception as e:
            print(f"❌ Error logging health: {e}")
        finally:
            conn.close()
    
    def add_goal(self, goal_name: str, category: str, target_date: str, frequency: str):
        """Add a new goal"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO goals (goal_name, category, target_date, frequency)
            VALUES (?, ?, ?, ?)
        """, (goal_name, category, target_date, frequency))
        
        conn.commit()
        conn.close()
        print(f"🎯 Goal added: {goal_name}")
    
    def get_personal_info(self):
        """Get all personal information"""
        data = self._load_json()
        return data.get("personal_info", {})
    
    def update_personal_info(self, info_dict: dict):
        """Update personal information"""
        data = self._load_json()
        data["personal_info"].update(info_dict)
        self._save_json(data)
        print(f"✅ Personal info updated")
    
    def get_context_for_llm(self, max_memories: int = 10) -> str:
        """Generate context string for LLM injection"""
        personal_info = self.get_personal_info()
        
        context = "**User Profile (Memory):**\n"
        context += f"Name: {personal_info.get('name', 'Unknown')}\n"
        context += f"Age: {personal_info.get('age', 'Unknown')}\n"
        context += f"City: {personal_info.get('city', 'Unknown')}\n"
        context += f"Profession: {personal_info.get('profession', 'Unknown')}\n"
        
        # Get recent high-importance memories
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT category, key, value FROM memories
            ORDER BY importance DESC, timestamp DESC
            LIMIT ?
        """, (max_memories,))
        
        memories = cursor.fetchall()
        conn.close()
        
        if memories:
            context += "\n**Recent Memories:**\n"
            for category, key, value in memories:
                context += f"- [{category}] {key}: {value}\n"
        
        return context
    
    def backup_memory(self):
        """Create encrypted backup of all memory"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"memory_backup_{timestamp}.json"
        
        data = self._load_json()
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Backup created: {backup_file}")
    
    def list_all_memories(self):
        """List all stored memories"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT category, key, value, importance FROM memories ORDER BY category")
        memories = cursor.fetchall()
        conn.close()
        
        print("\n📋 All Memories:")
        for category, key, value, importance in memories:
            print(f"[{category}] {key} (importance: {importance}): {value}")


# Example usage
if __name__ == "__main__":
    memory = MemorySystem()
    
    # Add personal info
    memory.update_personal_info({
        "name": "Aapka Naam",
        "age": 25,
        "city": "Kolkata",
        "profession": "Software Engineer"
    })
    
    # Add some memories
    memory.add_memory("personal", "hobby", "Photography", importance=7)
    memory.add_memory("work", "current_project", "Building AI Assistant", importance=9)
    memory.add_memory("health", "allergies", "Peanuts", importance=10)
    
    # Log health
    memory.log_health("2025-01-15", symptoms="None", mood=7, notes="Good day")
    
    # Add goal
    memory.add_goal("Learn Python", "education", "2025-06-30", "daily")
    
    # Get LLM context
    context = memory.get_context_for_llm()
    print("\n📝 LLM Context:\n" + context)
    
    # List all
    memory.list_all_memories()
    
    # Backup
    memory.backup_memory()
