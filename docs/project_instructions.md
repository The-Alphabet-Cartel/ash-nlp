# Ash-NLP Project Instructions

**Repository**: https://github.com/the-alphabet-cartel/ash-nlp  
**Project**: Ash-NLP v3.1
**Community**: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org  
**FILE VERSION**: v3.1-3e-5.5-6-1
**LAST UPDATED**: 2025-08-21
**CLEAN ARCHITECTURE**: v3.1 Compliant  

---

# The Alphabet Cartel
We are an LGBTQIA+ Discord community centered around gaming, political discourse and activism, community, and societal advocacy.

We can be found on the internet and Discord at:
https://alphabetcartel.org
http://discord.gg/alphabetcartel
https://github.com/the-alphabet-cartel

# Ash-NLP

## 🎯 CORE SYSTEM VISION (Never to be violated):

### **Ash-NLP is a CRISIS DETECTION Natural Language Processor that**:
1. **FIRST**: Uses Zero-Shot AI models for primary semantic classification
2. **SECOND**: Enhances AI results with contextual pattern analysis
3. **FALLBACK**: Uses pattern-only classification if AI models fail
4. **PURPOSE**: Detect crisis messages in Discord community communications


## Crisis Detection and Community Support Natural Language Processor
- `Ash-NLP`
  - https://github.com/the-alphabet-cartel/ash-nlp
  - GitHub submodule for the project `Ash`
    - https://github.com/the-alphabet-cartel/ash

## The Server
- `Ash-NLP`
  - Currently resides on a Debian 12 based Linux server that utilizes:
    - AMD Ryzen 7 5800x CPU
    - NVIDIA RTX 3060 with 12Gb VRAM GPU
    - 64Gb of RAM
    - Docker
      - We use a Docker first philosophy
        - Always containerize the code!
    - The server has an IP of 10.20.30.253

## Source Code and GitHub Repository Locations
- `Ash-NLP`: https://github.com/the-alphabet-cartel/ash-nlp
  - Backend NLP Server

## Port Assignments
- `Ash-NLP`: 8881

## General Instructions
- All hyperlinks shall be in lower case in the documentation as well as when trying to search GitHub.
- All references to The Alphabet Cartel or our discord server in documentation files shall include a link to the discord: https://discord.gg/alphabetcartel, as well as to our website: http://alphabetcartel.org.

### Coding Philosophy
- Modular Python Code
  - Separate the code into associated functions and methods as separate files based on the job that particular code class, or set of functions / methods is doing.
  - Python is only accessible from within the Docker container
    - `docker exec ash-nlp python *script_to_run.py*`
- **No Bash Scripting!**
- Configuration Variables and Settings
  - All default configuration variables and settings need to be defined in JSON files that are located in a directory named  `ash-nlp/config/`
  - All associated managers for these JSON configuration files need to be located in a directory named `ash-nlp/managers/`
  - All configuration variables and settings need to be able to be overridden by environmental variables located in a `.env` file located at `ash-nlp/.env`
- Sensitive Information
  - All sensitive information (passwords, access tokens, API tokens, etc.) need to utilize Docker Secrets functionality

Please adhere to this as best as possible, as this will ensure that the main code base stays clean and easy to read through for troubleshooting purposes, as well as to be easily able to add more functionality in the future.