# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Created by: RoxyBasicNeedBot
# 7z Archive Maker Module - Create 7z archives with optional encryption
# © 2025 RoxyBasicNeedBot. All Rights Reserved.

import os
import logging

logger = logging.getLogger(__name__)

# Check if py7zr is available
try:
    import py7zr
    PY7ZR_AVAILABLE = True
except ImportError:
    PY7ZR_AVAILABLE = False
    logger.warning("⚠️ py7zr not installed. 7z support disabled. Install with: pip install py7zr")


class Roxy7zMaker:
    """Create 7z archives with optional encryption"""
    
    def __init__(self):
        self.output_dir = "archives"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def is_available(self) -> bool:
        """Check if 7z creation is available"""
        return PY7ZR_AVAILABLE
    
    async def roxybot_create_7z(
        self, 
        files: list, 
        archive_name: str, 
        password: str = None
    ) -> str:
        """
        Create a 7z archive from files.
        
        Args:
            files: List of file paths to include
            archive_name: Name for the archive (without extension)
            password: Optional password for encryption (AES-256)
            
        Returns:
            Path to created archive
        """
        if not PY7ZR_AVAILABLE:
            raise ImportError("py7zr is not installed. Run: pip install py7zr")
        
        try:
            archive_path = os.path.join(self.output_dir, f"{archive_name}.7z")
            
            logger.info(f"🗜️ Creating 7z archive: {archive_path}")
            logger.info(f"📁 Files to include: {len(files)}")
            logger.info(f"🔐 Encrypted: {'Yes' if password else 'No'}")
            
            # Create 7z archive
            with py7zr.SevenZipFile(archive_path, 'w', password=password) as archive:
                for file_path in files:
                    if os.path.exists(file_path):
                        # Get base filename
                        arcname = os.path.basename(file_path)
                        # Remove user_id and timestamp prefix if present
                        parts = arcname.split("_", 2)
                        if len(parts) >= 3:
                            arcname = parts[2]
                        
                        archive.write(file_path, arcname)
                        logger.info(f"  ✅ Added: {arcname}")
            
            logger.info(f"✅ 7z archive created: {archive_path}")
            return archive_path
            
        except Exception as e:
            logger.error(f"❌ Error creating 7z: {e}")
            raise
    
    def roxybot_get_archive_size(self, archive_path: str) -> int:
        """Get archive file size in bytes"""
        try:
            return os.path.getsize(archive_path)
        except:
            return 0
    
    def roxybot_format_size(self, size_bytes: int) -> str:
        """Format size in bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    
    def roxybot_cleanup_files(self, files: list):
        """Remove downloaded files after archiving"""
        for file_path in files:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logger.info(f"🗑️ Removed: {file_path}")
            except Exception as e:
                logger.warning(f"⚠️ Could not remove {file_path}: {e}")


# Create singleton instance
roxybot_7zmaker = Roxy7zMaker()


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Follow me on:
# YouTube: @roxybasicneedbot | Instagram: roxybasicneedbot1
# Telegram: https://t.me/roxybasicneedbot1
# © 2025 RoxyBasicNeedBot. All Rights Reserved.
