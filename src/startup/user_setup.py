#!/usr/bin/env python3
"""
============================================================================
Ash-NLP: Crisis Detection NLP Server
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================

MISSION - NEVER TO BE VIOLATED:
    Analyze  → Process messages through multi-model ensemble classification
    Detect   → Identify crisis signals with weighted consensus algorithms
    Explain  → Provide human-readable explanations for all decisions
    Protect  → Safeguard our LGBTQIA+ community through accurate detection

============================================================================
Runtime User Setup for LinuxServer.io-style PUID/PGID Support
---
FILE VERSION: v5.0-8-1.0-1
LAST MODIFIED: 2026-01-05
PHASE: Phase 8 Step 1.0 - PUID/PGID User Setup
CLEAN ARCHITECTURE: v5.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
============================================================================
DESCRIPTION:
    Handles runtime user/group setup similar to LinuxServer.io containers.
    Reads PUID and PGID from environment variables and:
    1. Creates/modifies the application user with specified UID
    2. Creates/modifies the application group with specified GID
    3. Updates ownership of application directories
    4. Drops privileges to the specified user for the main process

    This follows the project's "No Bash Scripting" philosophy by implementing
    all user setup logic in Python.

USAGE:
    from src.startup.user_setup import setup_user_and_permissions, drop_privileges

    # During entrypoint (as root)
    setup_user_and_permissions()

    # Before starting main application
    drop_privileges()
"""

import grp
import logging
import os
import pwd
import sys
from pathlib import Path
from typing import Optional, Tuple

# Module version
__version__ = "v5.0-8-1.0-1"

# Configure logging
logger = logging.getLogger(__name__)

# Default values (matching Dockerfile defaults)
DEFAULT_PUID = 1000
DEFAULT_PGID = 1000
DEFAULT_USERNAME = "ash-nlp"
DEFAULT_GROUPNAME = "ash-nlp"

# Application directories that need correct ownership
APP_DIRECTORIES = [
    "/app",
    "/app/config",
    "/app/logs",
    "/app/models-cache",
]


def get_puid_pgid() -> Tuple[int, int]:
    """
    Get PUID and PGID from environment variables.

    Returns:
        Tuple of (puid, pgid) as integers
    """
    puid_str = os.environ.get("PUID", str(DEFAULT_PUID))
    pgid_str = os.environ.get("PGID", str(DEFAULT_PGID))

    try:
        puid = int(puid_str)
    except ValueError:
        logger.warning(
            f"⚠️  Invalid PUID value '{puid_str}', using default {DEFAULT_PUID}"
        )
        puid = DEFAULT_PUID

    try:
        pgid = int(pgid_str)
    except ValueError:
        logger.warning(
            f"⚠️  Invalid PGID value '{pgid_str}', using default {DEFAULT_PGID}"
        )
        pgid = DEFAULT_PGID

    # Validate ranges (standard Linux UID/GID ranges)
    if puid < 0 or puid > 65534:
        logger.warning(
            f"⚠️  PUID {puid} out of valid range (0-65534), using default {DEFAULT_PUID}"
        )
        puid = DEFAULT_PUID

    if pgid < 0 or pgid > 65534:
        logger.warning(
            f"⚠️  PGID {pgid} out of valid range (0-65534), using default {DEFAULT_PGID}"
        )
        pgid = DEFAULT_PGID

    return puid, pgid


def is_root() -> bool:
    """Check if the current process is running as root."""
    return os.geteuid() == 0


def group_exists(gid: int) -> bool:
    """Check if a group with the given GID exists."""
    try:
        grp.getgrgid(gid)
        return True
    except KeyError:
        return False


def user_exists(uid: int) -> bool:
    """Check if a user with the given UID exists."""
    try:
        pwd.getpwuid(uid)
        return True
    except KeyError:
        return False


def create_group(gid: int, groupname: str = DEFAULT_GROUPNAME) -> bool:
    """
    Create a group with the specified GID.

    Args:
        gid: Group ID to create
        groupname: Name for the group

    Returns:
        True if successful, False otherwise
    """
    if group_exists(gid):
        logger.info(f"   Group with GID {gid} already exists")
        return True

    try:
        # Use groupadd via subprocess (Python has no native way to create groups)
        import subprocess

        result = subprocess.run(
            ["groupadd", "-o", "--gid", str(gid), groupname], capture_output=True, text=True
        )
        if result.returncode == 0:
            logger.info(f"   ✅ Created group '{groupname}' with GID {gid}")
            return True
        elif result.returncode == 9:
            # Group name already exists (but different GID)
            logger.info(f"   Group name '{groupname}' exists, modifying GID")
            subprocess.run(["groupmod", "--gid", str(gid), groupname], check=True)
            return True
        else:
            logger.error(f"   ❌ Failed to create group: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"   ❌ Error creating group: {e}")
        return False


def create_user(uid: int, gid: int, username: str = DEFAULT_USERNAME) -> bool:
    """
    Create a user with the specified UID and GID.

    Args:
        uid: User ID to create
        gid: Primary group ID for the user
        username: Name for the user

    Returns:
        True if successful, False otherwise
    """
    if user_exists(uid):
        logger.info(f"   User with UID {uid} already exists")
        return True

    try:
        import subprocess

        result = subprocess.run(
            [
                "useradd",
                "--uid",
                str(uid),
                "--gid",
                str(gid),
                "--shell",
                "/bin/bash",
                "--create-home",
                "--no-log-init",
                username,
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            logger.info(f"   ✅ Created user '{username}' with UID {uid}")
            return True
        elif result.returncode == 9:
            # User name already exists (but different UID)
            logger.info(f"   User name '{username}' exists, modifying UID")
            subprocess.run(
                ["usermod", "--uid", str(uid), "--gid", str(gid), username], check=True
            )
            return True
        else:
            logger.error(f"   ❌ Failed to create user: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"   ❌ Error creating user: {e}")
        return False


def fix_ownership(uid: int, gid: int, directories: Optional[list] = None) -> bool:
    """
    Fix ownership of application directories.

    Args:
        uid: User ID to set as owner
        gid: Group ID to set as group
        directories: List of directories to fix (defaults to APP_DIRECTORIES)

    Returns:
        True if successful, False otherwise
    """
    dirs_to_fix = directories or APP_DIRECTORIES
    success = True

    for dir_path in dirs_to_fix:
        path = Path(dir_path)
        if path.exists():
            try:
                # Recursively change ownership
                for item in path.rglob("*"):
                    try:
                        os.chown(item, uid, gid)
                    except PermissionError:
                        pass  # Skip files we can't change
                os.chown(path, uid, gid)
                logger.info(f"   ✅ Fixed ownership for {dir_path}")
            except Exception as e:
                logger.warning(f"   ⚠️  Could not fix ownership for {dir_path}: {e}")
                success = False
        else:
            try:
                path.mkdir(parents=True, exist_ok=True)
                os.chown(path, uid, gid)
                logger.info(f"   ✅ Created and set ownership for {dir_path}")
            except Exception as e:
                logger.warning(f"   ⚠️  Could not create {dir_path}: {e}")
                success = False

    return success


def setup_user_and_permissions() -> Tuple[int, int]:
    """
    Main setup function - creates user/group and fixes permissions.

    This should be called at the start of the entrypoint while running as root.

    Returns:
        Tuple of (puid, pgid) that were configured
    """
    logger.info("=" * 60)
    logger.info("  User and Permissions Setup (LinuxServer.io-style)")
    logger.info("=" * 60)

    # Check if running as root
    if not is_root():
        logger.info("   ℹ️  Not running as root, skipping user setup")
        current_uid = os.getuid()
        current_gid = os.getgid()
        logger.info(f"   Running as UID={current_uid}, GID={current_gid}")
        return current_uid, current_gid

    # Get PUID/PGID from environment
    puid, pgid = get_puid_pgid()
    logger.info(f"   PUID: {puid}")
    logger.info(f"   PGID: {pgid}")

    # Create group if needed
    create_group(pgid, DEFAULT_GROUPNAME)

    # Create user if needed
    create_user(puid, pgid, DEFAULT_USERNAME)

    # Fix ownership of application directories
    fix_ownership(puid, pgid)

    logger.info("   ✅ User setup complete")
    logger.info("")

    return puid, pgid


def drop_privileges(uid: int, gid: int) -> None:
    """
    Drop privileges from root to the specified user/group.

    This should be called after setup and before starting the main application.

    Args:
        uid: User ID to drop to
        gid: Group ID to drop to
    """
    if not is_root():
        logger.debug("   Not running as root, no privileges to drop")
        return

    try:
        # Set supplementary groups (empty list - just primary group)
        os.setgroups([])

        # Set GID first (can't change after dropping UID if not root)
        os.setgid(gid)
        os.setegid(gid)

        # Set UID
        os.setuid(uid)
        os.seteuid(uid)

        # Verify the change
        logger.info(f"   ✅ Dropped privileges to UID={os.getuid()}, GID={os.getgid()}")

    except Exception as e:
        logger.error(f"   ❌ Failed to drop privileges: {e}")
        raise


def get_exec_user_args(uid: int, gid: int) -> dict:
    """
    Get arguments for subprocess calls that should run as the specified user.

    This is useful when we need to spawn subprocesses after setting up
    but before dropping privileges in the main process.

    Args:
        uid: User ID
        gid: Group ID

    Returns:
        Dictionary suitable for subprocess.Popen preexec_fn
    """

    def set_ids():
        os.setgid(gid)
        os.setuid(uid)

    return {"preexec_fn": set_ids}
