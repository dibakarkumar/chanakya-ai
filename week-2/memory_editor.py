#!/usr/bin/env python3
"""
Memory Editor CLI - Interactive tool to manage Chanakya's memory
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from week_2.memory_system import MemorySystem

class MemoryEditor:
    """CLI interface for memory management"""
    
    def __init__(self):
        self.memory = MemorySystem()
    
    def display_menu(self):
        print("\n" + "="*50)
        print("🧠 CHANAKYA MEMORY EDITOR")
        print("="*50)
        print("1. View Personal Info")
        print("2. Update Personal Info")
        print("3. Add Memory")
        print("4. View Memories")
        print("5. Delete Memory")
        print("6. Log Health")
        print("7. Add Goal")
        print("8. Backup Memory")
        print("9. Get LLM Context")
        print("0. Exit")
        print("="*50)
    
    def view_personal_info(self):
        info = self.memory.get_personal_info()
        print("\n👤 Personal Information:")
        for key, value in info.items():
            print(f"  {key}: {value}")
    
    def update_personal_info(self):
        print("\n📝 Update Personal Info (leave blank to skip):")
        name = input("Name: ") or None
        age = input("Age: ") or None
        city = input("City: ") or None
        profession = input("Profession: ") or None
        
        info = {}
        if name: info["name"] = name
        if age: info["age"] = int(age)
        if city: info["city"] = city
        if profession: info["profession"] = profession
        
        if info:
            self.memory.update_personal_info(info)
        else:
            print("No updates made.")
    
    def add_memory(self):
        print("\n➕ Add New Memory:")
        category = input("Category (personal/work/health/goals/other): ").strip()
        key = input("Memory key/topic: ").strip()
        value = input("Memory value/detail: ").strip()
        importance = input("Importance (1-10, default 5): ").strip()
        
        try:
            importance = int(importance) if importance else 5
            self.memory.add_memory(category, key, value, importance)
        except ValueError:
            print("❌ Invalid importance value")
    
    def view_memories(self):
        print("\n📂 View Memories By Category:")
        print("1. All Memories")
        print("2. Personal")
        print("3. Work")
        print("4. Health")
        print("5. Goals")
        
        choice = input("Select (1-5): ").strip()
        
        if choice == "1":
            self.memory.list_all_memories()
        else:
            categories = {"2": "personal", "3": "work", "4": "health", "5": "goals"}
            category = categories.get(choice)
            if category:
                memories = self.memory.get_memory(category)
                print(f"\n📋 {category.upper()} Memories:")
                for key, value in memories:
                    print(f"  • {key}: {value}")
    
    def delete_memory(self):
        print("\n🗑️ Delete Memory:")
        category = input("Category: ").strip()
        key = input("Memory key: ").strip()
        
        confirm = input(f"Delete {category}/{key}? (yes/no): ").strip().lower()
        if confirm == "yes":
            self.memory.delete_memory(category, key)
        else:
            print("Cancelled.")
    
    def log_health(self):
        print("\n🏥 Log Health Information:")
        date = input("Date (YYYY-MM-DD): ").strip()
        symptoms = input("Symptoms (or 'none'): ").strip()
        mood = input("Mood (1-10): ").strip()
        medications = input("Medications taken: ").strip()
        notes = input("Additional notes: ").strip()
        
        try:
            mood = int(mood) if mood else None
            self.memory.log_health(
                date,
                symptoms or None,
                mood,
                medications or None,
                notes or None
            )
        except ValueError:
            print("❌ Invalid mood value")
    
    def add_goal(self):
        print("\n🎯 Add New Goal:")
        goal_name = input("Goal name: ").strip()
        category = input("Category (fitness/study/work/health/other): ").strip()
        target_date = input("Target date (YYYY-MM-DD): ").strip()
        frequency = input("Frequency (daily/weekly/monthly): ").strip()
        
        self.memory.add_goal(goal_name, category, target_date, frequency)
    
    def backup_memory(self):
        print("\n💾 Creating backup...")
        self.memory.backup_memory()
    
    def get_llm_context(self):
        print("\n📝 LLM Context (for injection into Ollama):")
        print("-" * 50)
        context = self.memory.get_context_for_llm()
        print(context)
        print("-" * 50)
    
    def run(self):
        """Main loop"""
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (0-9): ").strip()
            
            if choice == "0":
                print("\n👋 Goodbye!")
                break
            elif choice == "1":
                self.view_personal_info()
            elif choice == "2":
                self.update_personal_info()
            elif choice == "3":
                self.add_memory()
            elif choice == "4":
                self.view_memories()
            elif choice == "5":
                self.delete_memory()
            elif choice == "6":
                self.log_health()
            elif choice == "7":
                self.add_goal()
            elif choice == "8":
                self.backup_memory()
            elif choice == "9":
                self.get_llm_context()
            else:
                print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    editor = MemoryEditor()
    editor.run()
