#!/usr/bin/env python3
"""
Test uvicorn startup directly to see what's happening
"""

import os
import sys
import logging
import asyncio
import signal
import time

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def test_main_import():
    """Test if we can import main.py"""
    logger.info("🔍 Testing main.py import...")
    
    try:
        # Test if main.py can be imported
        import main
        logger.info("✅ main.py imported successfully")
        
        # Check if it has the required components
        if hasattr(main, 'app'):
            logger.info("✅ main.py has 'app' attribute")
        else:
            logger.error("❌ main.py missing 'app' attribute")
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"❌ main.py import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_uvicorn_startup():
    """Test uvicorn startup with timeout"""
    logger.info("🚀 Testing uvicorn startup with 30-second timeout...")
    
    try:
        import uvicorn
        
        # Set up signal handler for timeout
        def timeout_handler(signum, frame):
            logger.warning("⏰ Uvicorn startup timed out after 30 seconds")
            raise TimeoutError("Uvicorn startup timeout")
        
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(30)  # 30 second timeout
        
        try:
            # Try to start uvicorn with main:app
            logger.info("🔄 Starting uvicorn with main:app...")
            uvicorn.run(
                "main:app",
                host="0.0.0.0",
                port=8881,
                log_level="info",
                access_log=True
            )
            
        except TimeoutError:
            logger.error("❌ Uvicorn startup timed out")
            return False
        except KeyboardInterrupt:
            logger.info("✅ Uvicorn started successfully (interrupted by user)")
            return True
        finally:
            signal.alarm(0)  # Cancel timeout
            
    except Exception as e:
        logger.error(f"❌ Uvicorn startup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_manual_app_startup():
    """Test manual app startup without uvicorn"""
    logger.info("🔧 Testing manual app startup...")
    
    try:
        # Import and try to access the app directly
        import main
        app = main.app
        
        logger.info("✅ App object accessible")
        
        # Try to trigger the lifespan manually
        logger.info("🔄 Testing lifespan context manager...")
        
        async def test_lifespan():
            try:
                async with main.lifespan(app):
                    logger.info("✅ Lifespan startup completed")
                    await asyncio.sleep(1)  # Brief wait
                    logger.info("✅ Lifespan test completed")
            except Exception as e:
                logger.error(f"❌ Lifespan failed: {e}")
                import traceback
                traceback.print_exc()
                return False
            return True
        
        # Run the lifespan test
        result = asyncio.run(test_lifespan())
        return result
        
    except Exception as e:
        logger.error(f"❌ Manual app startup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    logger.info("🔍 Testing Uvicorn Startup")
    logger.info("=" * 50)
    
    # Test if main.py can be imported
    if not test_main_import():
        logger.error("❌ Cannot import main.py")
        return False
    
    # Test manual app startup
    logger.info("\n" + "=" * 50)
    logger.info("🔧 Testing manual app startup (no uvicorn)...")
    if not test_manual_app_startup():
        logger.error("❌ Manual app startup failed")
        return False
    
    logger.info("\n" + "=" * 50)
    logger.info("🚀 All tests passed! main.py should work.")
    logger.info("💡 If container still fails silently, the issue might be:")
    logger.info("   1. Docker CMD/ENTRYPOINT configuration")
    logger.info("   2. Container resource limits")
    logger.info("   3. Port binding issues")
    logger.info("   4. Long model loading time appearing as silent failure")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)