# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Created by: RoxyBasicNeedBot
# TAR Archive Maker Module - Create TAR and TAR.GZ archives
# © 2025 RoxyBasicNeedBot. All Rights Reserved.

import os
import tarfile
import logging

logger = logging.getLogger(__name__)


class RoxyTarMaker:
    """Create TAR and TAR.GZ archives"""
    
    def __init__(self):
        self.output_dir = "archives"
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def roxybot_create_tar(
        self, 
        files: list, 
        archive_name: str, 
        compress: bool = True
    ) -> str:
        """
        Create a TAR or TAR.GZ archive from files.
        
        Args:
            files: List of file paths to include
            archive_name: Name for the archive (without extension)
            compress: If True, create .tar.gz, else .tar
            
        Returns:
            Path to created archive
        """
        try:
            # Determine extension and mode
            if compress:
                extension = ".tar.gz"
                mode = "w:gz"
            else:
                extension = ".tar"
                mode = "w"
            
            archive_path = os.path.join(self.output_dir, f"{archive_name}{extension}")
            
            logger.info(f"📦 Creating TAR archive: {archive_path}")
            logger.info(f"📁 Files to include: {len(files)}")
            
            with tarfile.open(archive_path, mode) as tar:
                for file_path in files:
                    if os.path.exists(file_path):
                        # Get base filename
                        arcname = os.path.basename(file_path)
                        # Remove user_id and timestamp prefix if present
                        parts = arcname.split("_", 2)
                        if len(parts) >= 3:
                            arcname = parts[2]
                        
                        tar.add(file_path, arcname=arcname)
                        logger.info(f"  ✅ Added: {arcname}")
            
            logger.info(f"✅ TAR archive created: {archive_path}")
            return archive_path
            
        except Exception as e:
            logger.error(f"❌ Error creating TAR: {e}")
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
roxybot_tarmaker = RoxyTarMaker()


# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Follow me on:
# YouTube: @roxybasicneedbot | Instagram: roxybasicneedbot1
# Telegram: https://t.me/roxybasicneedbot1
# © 2025 RoxyBasicNeedBot. All Rights Reserved.
