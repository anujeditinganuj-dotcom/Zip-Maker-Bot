# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Created by: RoxyBasicNeedBot
# GitHub: https://github.com/RoxyBasicNeedBot
# Telegram: https://t.me/roxybasicneedbot1
# Website: https://roxybasicneedbot.unaux.com/?i=1
# YouTube: @roxybasicneedbot
# Instagram: roxybasicneedbot1
# Portfolio: https://aratt.ai/@roxybasicneedbot
# 
# Bot & Website Developer 🤖
# Creator of Roxy BasicNeedBot & many automation tools ⚡
# Skilled in Python, APIs, and Web Development
# 
# © 2025 RoxyBasicNeedBot. All Rights Reserved.

import os
import zipfile
import time
from datetime import datetime
from config import RoxyBotConfig
from enum import Enum

# Try to import pyzipper for password-protected zips
try:
    import pyzipper
    PYZIPPER_AVAILABLE = True
except ImportError:
    PYZIPPER_AVAILABLE = False


class EncryptionType(Enum):
    """Encryption types for ZIP files"""
    NONE = "none"
    ZIPCRYPTO = "zipcrypto"  # Standard ZIP encryption (legacy, less secure)
    AES_128 = "aes128"       # AES-128 encryption
    AES_256 = "aes256"       # AES-256 encryption (most secure)


# Encryption type display names for UI
ENCRYPTION_DISPLAY_NAMES = {
    EncryptionType.NONE: "Nᴏ Eɴᴄʀʏᴘᴛɪᴏɴ",
    EncryptionType.ZIPCRYPTO: "ZɪᴘCʀʏᴘᴛᴏ (Sᴛᴀɴᴅᴀʀᴅ)",
    EncryptionType.AES_128: "AES-128",
    EncryptionType.AES_256: "AES-256 (Mᴏꜱᴛ Sᴇᴄᴜʀᴇ)"
}


class RoxyBotZipMaker:
    """Zip Maker Module for creating zip files with multiple encryption options"""
    
    def __init__(self):
        self.roxybot_ensure_dirs()
    
    def roxybot_ensure_dirs(self):
        """Ensure download and zip directories exist"""
        os.makedirs(RoxyBotConfig.ROXYBOT_DOWNLOAD_PATH, exist_ok=True)
        os.makedirs(RoxyBotConfig.ROXYBOT_ZIP_PATH, exist_ok=True)
    
    def roxybot_is_encryption_available(self) -> bool:
        """Check if encryption is available (pyzipper installed)"""
        return PYZIPPER_AVAILABLE
    
    def roxybot_get_available_encryptions(self) -> list:
        """Get list of available encryption types"""
        encryptions = [EncryptionType.NONE]
        if PYZIPPER_AVAILABLE:
            encryptions.extend([
                EncryptionType.ZIPCRYPTO,
                EncryptionType.AES_128,
                EncryptionType.AES_256
            ])
        return encryptions
    
    async def roxybot_create_zip(
        self, 
        file_paths: list, 
        zip_name: str = None, 
        password: str = None,
        encryption_type: EncryptionType = EncryptionType.AES_256
    ) -> str:
        """
        Create a zip file from given file paths with optional encryption
        
        Args:
            file_paths: List of file paths to include in zip
            zip_name: Custom name for zip file
            password: Optional password for encryption
            encryption_type: Type of encryption to use (AES-256, AES-128, ZipCrypto, or None)
            
        Returns:
            Path to created zip file
        """
        try:
            # Generate zip name if not provided
            if not zip_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                zip_name = f"RoxyBot_Archive_{timestamp}.zip"
            
            # Ensure .zip extension
            if not zip_name.endswith('.zip'):
                zip_name += '.zip'
            
            # Create zip file path
            zip_file_path = os.path.join(RoxyBotConfig.ROXYBOT_ZIP_PATH, zip_name)
            
            # 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
            # Creating zip file with selected encryption
            
            if password and PYZIPPER_AVAILABLE and encryption_type != EncryptionType.NONE:
                # Create password-protected zip with selected encryption
                if encryption_type == EncryptionType.AES_256:
                    # AES-256 encryption (most secure)
                    with pyzipper.AESZipFile(
                        zip_file_path,
                        'w',
                        compression=pyzipper.ZIP_DEFLATED,
                        encryption=pyzipper.WZ_AES,
                        compresslevel=9
                    ) as zipf:
                        zipf.setpassword(password.encode('utf-8'))
                        zipf.setencryption(pyzipper.WZ_AES, nbits=256)
                        for file_path in file_paths:
                            if os.path.exists(file_path):
                                file_name = os.path.basename(file_path)
                                zipf.write(file_path, file_name)
                
                elif encryption_type == EncryptionType.AES_128:
                    # AES-128 encryption
                    with pyzipper.AESZipFile(
                        zip_file_path,
                        'w',
                        compression=pyzipper.ZIP_DEFLATED,
                        encryption=pyzipper.WZ_AES,
                        compresslevel=9
                    ) as zipf:
                        zipf.setpassword(password.encode('utf-8'))
                        zipf.setencryption(pyzipper.WZ_AES, nbits=128)
                        for file_path in file_paths:
                            if os.path.exists(file_path):
                                file_name = os.path.basename(file_path)
                                zipf.write(file_path, file_name)
                
                elif encryption_type == EncryptionType.ZIPCRYPTO:
                    # Standard ZipCrypto encryption (legacy, compatible)
                    with zipfile.ZipFile(
                        zip_file_path,
                        'w',
                        compression=zipfile.ZIP_DEFLATED
                    ) as zipf:
                        zipf.setpassword(password.encode('utf-8'))
                        for file_path in file_paths:
                            if os.path.exists(file_path):
                                file_name = os.path.basename(file_path)
                                zipf.write(file_path, file_name)
            else:
                # Create normal zip archive without encryption
                with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file_path in file_paths:
                        if os.path.exists(file_path):
                            # Get filename from path
                            file_name = os.path.basename(file_path)
                            # Add file to zip
                            zipf.write(file_path, file_name)
            
            return zip_file_path
            
        except Exception as e:
            print(f"❌ RoxyBot: Error creating zip: {e}")
            raise
    
    async def roxybot_read_encrypted_zip(self, zip_path: str, password: str = None) -> list:
        """
        Read and extract contents from an encrypted ZIP file
        Supports AES-128, AES-256, and ZipCrypto encryption
        
        Args:
            zip_path: Path to the encrypted ZIP file
            password: Password to decrypt the ZIP
            
        Returns:
            List of extracted file paths
        """
        extracted_files = []
        extract_dir = os.path.join(RoxyBotConfig.ROXYBOT_DOWNLOAD_PATH, f"extracted_{int(time.time())}")
        os.makedirs(extract_dir, exist_ok=True)
        
        try:
            if PYZIPPER_AVAILABLE:
                # Try with pyzipper for AES encrypted files
                with pyzipper.AESZipFile(zip_path, 'r') as zipf:
                    if password:
                        zipf.setpassword(password.encode('utf-8'))
                    zipf.extractall(extract_dir)
                    extracted_files = [os.path.join(extract_dir, name) for name in zipf.namelist()]
            else:
                # Fallback to standard zipfile
                with zipfile.ZipFile(zip_path, 'r') as zipf:
                    if password:
                        zipf.setpassword(password.encode('utf-8'))
                    zipf.extractall(extract_dir)
                    extracted_files = [os.path.join(extract_dir, name) for name in zipf.namelist()]
            
            return extracted_files
            
        except Exception as e:
            print(f"❌ RoxyBot: Error reading encrypted zip: {e}")
            raise
    
    def roxybot_get_zip_size(self, zip_path: str) -> int:
        """Get size of zip file in bytes"""
        try:
            return os.path.getsize(zip_path)
        except:
            return 0
    
    def roxybot_format_size(self, size_bytes: int) -> str:
        """Format size in bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    
    def roxybot_cleanup_files(self, file_paths: list):
        """Clean up downloaded files"""
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"❌ RoxyBot: Error deleting file {file_path}: {e}")
    
    def roxybot_cleanup_zip(self, zip_path: str):
        """Clean up created zip file"""
        try:
            if os.path.exists(zip_path):
                os.remove(zip_path)
        except Exception as e:
            print(f"❌ RoxyBot: Error deleting zip {zip_path}: {e}")

# Initialize zip maker instance
roxybot_zipmaker = RoxyBotZipMaker()

# 𝕽𝕺𝕏𝖄•𝔹𝕒𝕤𝕚𝕔ℕ𝕖𝕖𝕕𝔹𝕠𝕥 ⚡️
# Follow me on:
# YouTube: @roxybasicneedbot | Instagram: roxybasicneedbot1
# Telegram: https://t.me/roxybasicneedbot1
# © 2025 RoxyBasicNeedBot. All Rights Reserved.
