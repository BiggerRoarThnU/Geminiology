import datetime
import os

class MasterLog:
    """
    The Master Log: The absolute record of Sovereign Nexus operations.
    Maintains 100% accurate bot and agent behavior data.
    AXIOM: 1=1=1.
    """
    def __init__(self, log_path=r"C:\Users\Ofthe\SovereignNexus\src\Logs\MASTER_LOG_SYMMETRICAL.md"):
        self.log_path = log_path
        self.axiom = "1=1=1"
        # Ensure the Logs directory exists
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def register(self, level, message):
        """ Registers a measurable event into the Master Log. """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] [{level.upper()}] {message}\n"
        
        with open(self.log_path, "a", encoding="utf-8") as log_file:
            log_file.write(entry)
        
        # Mirror to terminal for immediate observation
        try:
            print(entry.strip())
        except UnicodeEncodeError:
            # Fallback for environments that don't support UTF-8 display
            print(entry.encode('ascii', 'ignore').decode('ascii').strip())

    def info(self, message):
        """ INFO: Business-as-usual and successful data assimilation. """
        self.register("INFO", message)

    def warn(self, message):
        """ WARN: Early warning system for anomalies. """
        self.register("WARN", message)

    def error(self, message):
        """ ERROR: Critical problems or service crashes. """
        self.register("ERROR", message)

    def get_intent_summary(self, n_lines=100):
        """ 
        [SEMANTIC EXTRACTION] - Scans the last N lines for Weights, Stars, and Intent. 
        Returns a high-density primitive of the current state.
        """
        if not os.path.exists(self.log_path):
            return "LOG_NOT_FOUND"
        
        try:
            with open(self.log_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                relevant = lines[-n_lines:]
                
                weights = [l.strip() for l in relevant if "Weight" in l]
                stars = [l.strip() for l in relevant if "Star_" in l]
                
                return {
                    "last_weights": weights[-5:],
                    "last_stars": list(set([s.split("Star_")[1].split(" ")[0] for s in stars if "Star_" in s]))[-10:],
                    "intent_marker": "ACTIVE" if len(relevant) > 0 else "STAGNANT"
                }
        except Exception as e:
            return f"EXTRACTION_ERROR: {str(e)}"

if __name__ == "__main__":
    # Initialize the Master Log
    logger = MasterLog()
    logger.info("Master Log Synchronized. Standing Secured.")
    logger.warn("Simulating Gray Zone coercion detection.")
    logger.error("Thermal Threshold Breach Simulation.")
