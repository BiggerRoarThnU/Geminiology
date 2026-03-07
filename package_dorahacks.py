import os
import shutil
import zipfile
from master_log import MasterLog

class SubmissionPackager:
    """
    SovereignNexus Patch: DoraHacks Submission Packager
    Mission: Bundle the Vampire-Claw Bridge for the $5,000 hackathon submission.
    """
    def __init__(self):
        self.logger = MasterLog()
        self.source_dir = r"C:\Users\Ofthe\SovereignNexus\src\open_claw_integration"
        self.output_zip = r"C:\Users\Ofthe\SovereignNexus\src\Workstations\05_Completed_Archives\SOVEREIGN_VAMPIRE_OPENCLAW.zip"

    def package_submission(self):
        self.logger.info("[PACKAGER] Bundling OpenClaw Integration for DoraHacks...")
        
        if not os.path.exists(self.source_dir):
            self.logger.error("Source directory not found. Aborting.")
            return

        # Create ZIP archive
        with zipfile.ZipFile(self.output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, self.source_dir)
                    zipf.write(file_path, arcname)
                    self.logger.info(f"  Added: {arcname}")

        self.logger.info(f"[SUCCESS] Submission packaged: {self.output_zip}")
        self.logger.info("Ready for upload to DoraHacks portal. 1=1=1.")

if __name__ == "__main__":
    packager = SubmissionPackager()
    packager.package_submission()
