#!/usr/bin/env python3
"""
Immich Partner Sharing - Community Docker App
Uses the existing immich-face-to-album package
"""

import os
import sys
import time
import logging
import schedule
import subprocess
from datetime import datetime
from typing import Dict, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class ImmichFaceSync:
    def __init__(self):
        """Initialize the Partner Sharing application"""
        self.server = os.getenv('IMMICH_SERVER', 'http://localhost:2283')
        self.dry_run = os.getenv('DRY_RUN', 'false').lower() == 'true'
        
        # Parse sync mappings from environment variables
        self.sync_mappings = self._parse_sync_mappings()
        
        if not self.sync_mappings:
            logger.error("No valid sync mappings found. Please check your configuration.")
            sys.exit(1)
            
        logger.info(f"Initialized with {len(self.sync_mappings)} sync mappings")
        if self.dry_run:
            logger.info("🏃 DRY RUN MODE - Commands will be shown but not executed")

    def _parse_sync_mappings(self) -> List[Dict]:
        """
        Parse sync mappings from environment variables
        Format: SYNC_MAPPING_1=api_key:face_id:album_id:description
        """
        mappings = []
        i = 1
        
        while True:
            mapping_key = f'SYNC_MAPPING_{i}'
            mapping_value = os.getenv(mapping_key)
            
            if not mapping_value:
                break
                
            try:
                parts = mapping_value.split(':')
                if len(parts) == 4:
                    api_key, face_id, album_id, description = parts
                    mappings.append({
                        'api_key': api_key.strip(),
                        'face_id': face_id.strip(),
                        'album_id': album_id.strip(),
                        'description': description.strip(),
                        'mapping_number': i
                    })
                    logger.info(f"✅ Parsed mapping {i}: {description}")
                else:
                    logger.warning(f"⚠️  Invalid format for {mapping_key}: {mapping_value}")
            except Exception as e:
                logger.error(f"❌ Error parsing {mapping_key}: {e}")
            
            i += 1
            
        return mappings

    def run_immich_face_to_album(self, mapping: Dict) -> bool:
        """Run immich-face-to-album command for a mapping"""
        api_key = mapping['api_key']
        face_id = mapping['face_id']
        album_id = mapping['album_id']
        description = mapping['description']
        mapping_num = mapping['mapping_number']
        
        logger.info(f"🔄 [{mapping_num}] Starting: {description}")
        
        # Build the command
        cmd = [
            'immich-face-to-album',
            '--key', api_key,
            '--server', self.server,
            '--face', face_id,
            '--album', album_id
        ]
        
        if self.dry_run:
            logger.info(f"🏃 DRY RUN [{mapping_num}]: Would run: {' '.join(cmd)}")
            return True
        
        try:
            # Run the command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120  # 2 minute timeout
            )
            
            if result.returncode == 0:
                logger.info(f"✅ [{mapping_num}] {description} - Success")
                if result.stdout.strip():
                    logger.info(f"📝 [{mapping_num}] Output: {result.stdout.strip()}")
                return True
            else:
                logger.error(f"❌ [{mapping_num}] {description} - Failed (exit code: {result.returncode})")
                if result.stderr.strip():
                    logger.error(f"📝 [{mapping_num}] Error: {result.stderr.strip()}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error(f"❌ [{mapping_num}] {description} - Timeout after 2 minutes")
            return False
        except Exception as e:
            logger.error(f"❌ [{mapping_num}] {description} - Unexpected error: {e}")
            return False

    def run_sync_cycle(self):
        """Run a complete sync cycle for all mappings"""
        logger.info("🚀 Starting Partner Sharing cycle")
        start_time = datetime.now()
        
        results = []
        for mapping in self.sync_mappings:
            try:
                result = self.run_immich_face_to_album(mapping)
                results.append(result)
                
                # Small delay between mappings to be nice to the server
                if not self.dry_run:
                    time.sleep(2)
                
            except Exception as e:
                logger.error(f"❌ Unexpected error in mapping {mapping['mapping_number']}: {e}")
                results.append(False)
        
        # Summary
        successful = sum(results)
        total = len(results)
        duration = datetime.now() - start_time
        
        if successful == total:
            logger.info(f"🎉 All {total} sync mappings completed successfully! (took {duration.total_seconds():.1f}s)")
        else:
            logger.warning(f"⚠️  {successful}/{total} sync mappings succeeded (took {duration.total_seconds():.1f}s)")

    def run_scheduler(self):
        """Run the scheduled sync process"""
        sync_interval = int(os.getenv('SYNC_INTERVAL_MINUTES', '60'))
        logger.info(f"📅 Scheduling sync every {sync_interval} minutes")
        
        # Schedule the sync
        schedule.every(sync_interval).minutes.do(self.run_sync_cycle)
        
        # Run initial sync
        self.run_sync_cycle()
        
        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

def main():
    """Main application entry point"""
    logger.info("🌟 Immich Partner Sharing - Community Edition")
    logger.info("ℹ️  Using immich-face-to-album package")
    
    try:
        app = ImmichFaceSync()
        
        # Check if this is a one-time run or scheduled
        run_once = os.getenv('RUN_ONCE', 'false').lower() == 'true'
        
        if run_once:
            logger.info("▶️  Running one-time sync")
            app.run_sync_cycle()
        else:
            logger.info("🔄 Running in scheduled mode")
            app.run_scheduler()
            
    except KeyboardInterrupt:
        logger.info("👋 Gracefully shutting down...")
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()