# Week 1: Computer Setup & Learning Ka Pehla Din

## 🎯 Week 1 Goal
Apne laptop ko AI-ready banao — zero se shuruat

## 📅 Day-by-Day Plan

### **Monday: Python Install**
- [ ] Download Python 3.11 from **python.org**
- [ ] Install Python (add to PATH)
- [ ] Verify: `python --version` in terminal
- [ ] If Windows: Install **Windows Terminal** from Microsoft Store

### **Tuesday: VS Code & Git**
- [ ] Download **VS Code** from code.visualstudio.com
- [ ] Install extensions: Python, GitLens
- [ ] Download **Git** from git-scm.com
- [ ] Verify: `git --version` in terminal

### **Wednesday: Ollama Installation**
- [ ] Download Ollama from **ollama.com**
- [ ] Install and launch
- [ ] Terminal command: `ollama pull llama3.2` (wait for ~3GB download)
- [ ] Test: `ollama run llama3.2`
- [ ] Try: "Hello Ollama" in terminal

### **Thursday: Open WebUI**
- [ ] Terminal: `pip install open-webui`
- [ ] Terminal: `open-webui serve`
- [ ] Browser: Open `localhost:8080`
- [ ] Select llama3.2 model
- [ ] Say "Hello" to your first Chanakya

### **Friday: System Prompt**
- [ ] Copy system_prompt.txt content
- [ ] Paste into Open WebUI settings
- [ ] Have 10-15 minute test conversation
- [ ] Note any issues

### **Saturday: Download Bigger Model**
- [ ] Terminal: `ollama pull llama3.1:8b` (wait for ~5GB)
- [ ] Compare both models — which is better?
- [ ] Write notes about your observations

### **Sunday: Rest + Planning**
- [ ] Spend 30 min on Python basics (learnpython.org)
- [ ] Read Week 2 plan
- [ ] Rest — you've earned it!

## 🛠 Command Reference

```bash
# Verify installations
python --version          # Should be 3.11+
pip --version
git --version

# Ollama commands
ollama pull llama3.2      # Download smallest model
ollama pull llama3.1:8b   # Download bigger model
ollama run llama3.2       # Test the model

# Open WebUI
pip install open-webui
open-webui serve          # Starts on localhost:8080
```

## ✅ Week 1 Completion Checklist

- [ ] Python 3.11+ installed
- [ ] VS Code installed with Python extension
- [ ] Git installed
- [ ] Ollama installed and running
- [ ] llama3.2 model downloaded
- [ ] Open WebUI working on localhost:8080
- [ ] System prompt configured
- [ ] Had first conversation with Chanakya
- [ ] llama3.1:8b model also downloaded
- [ ] Both models compared

## 🎯 Week 1 Expected Outcome

**Chanakya v0.1 is running on your laptop:**
- ✅ Fully local
- ✅ Completely private
- ✅ Responding to text questions
- ✅ No internet required
- ✅ Ready for Week 2 (Voice)

## 📝 Notes for Your Future Self

Write down:
1. Which model felt better? (llama3.2 vs llama3.1:8b)
2. What was the response time?
3. Any errors? Write them down.
4. What would you like to improve?

---

**Next Week:** Voice input + Text-to-speech + Wake word detection 🎤
