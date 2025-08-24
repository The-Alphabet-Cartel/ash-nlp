# dev_server.py
"""
Ash-NLP: Crisis Detection Backend for The Alphabet Cartel Discord Community
CORE PRINCIPLE: Zero-Shot AI Models → Pattern Enhancement → Crisis Classification
******************  CORE SYSTEM VISION (Never to be violated):  ****************
Ash-NLP is a CRISIS DETECTION BACKEND that:
1. FIRST: Uses Zero-Shot AI models for primary semantic classification
2. SECOND: Enhances AI results with contextual pattern analysis  
3. FALLBACK: Uses pattern-only classification if AI models fail
4. PURPOSE: Detect crisis messages in Discord community communications
********************************************************************************
Development Server Script - Preserves Original uvicorn Workflow
---
FILE VERSION: v3.1-gunicorn-1-1
LAST MODIFIED: 2025-08-24
PHASE: Gunicorn Migration - Development Compatibility
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

PURPOSE: Preserve single-worker development workflow while main.py is gunicorn-ready
USAGE: python dev_server.py (maintains original development experience)
"""

import uvicorn
import logging
import sys
from pathlib import Path

def run_development_server():
    """
    Run the development server with original uvicorn configuration
    
    This preserves the development workflow while main.py is optimized for gunicorn
    """
    
    print("🔧 Starting Ash-NLP Development Server...")
    print("🏳️‍🌈 Serving The Alphabet Cartel LGBTQIA+ Community (DEV MODE)")
    print("=" * 70)
    
    try:
        # Import the configured app from main.py
        # main.py now initializes everything at module level
        from main import app, unified_config
        
        print("✅ Application imported successfully from main.py")
        
        # Get server configuration from unified config
        try:
            host = unified_config.get_config_section(
                'server_config', 
                'server_configuration.network_settings.host', 
                '0.0.0.0'
            )
            port = unified_config.get_config_section(
                'server_config', 
                'server_configuration.network_settings.port', 
                8881
            )
        except Exception as e:
            print(f"⚠️  Could not load server config: {e}")
            print("🔧 Using default values: host=0.0.0.0, port=8881")
            host = '0.0.0.0'
            port = 8881
        
        print(f"🌐 Server will bind to: {host}:{port}")
        print("🔄 Development features enabled: hot reload, single worker")
        print("=" * 70)
        
        # Run in development mode with features that help during development
        uvicorn.run(
            app,  # Use the already-initialized app object
            host=host, 
            port=port,
            workers=1,          # Single worker for development
            reload=False,       # Set to True if you want hot reload (requires main:app string instead)
            log_config=None,    # Use our existing logging setup
            access_log=False,   # Disable uvicorn access logging (we have our own)
            server_header=False, # Disable server header
            date_header=False   # Disable date header
        )
        
    except ImportError as e:
        print(f"❌ Failed to import application: {e}")
        print("💡 Ensure main.py is properly configured for module-level initialization")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Development server startup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("=" * 70)
    print("🚀 ASH-NLP DEVELOPMENT SERVER")
    print("=" * 70)
    run_development_server()