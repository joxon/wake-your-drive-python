
import argparse
import time
import sys

from app.config import DEFAULT_INTERVAL
from app.disk import DiskPulseThread
from app.settings import ensure_config
from app.tray import TrayApp, is_tray_supported

class WakeTheDrive:
    def __init__(self, interval):
        self.interval = interval
        self.pulse_thread = None
        self.tray_app = None
        self._running = True

    def run(self):
        """Starts the application."""
        print("Starting WakeTheDrive...")

        # Initialize and start the disk pulse thread
        self.pulse_thread = DiskPulseThread(self.interval)

        if is_tray_supported():
            # If tray is supported, let it manage the main loop
            self.tray_app = TrayApp(stop_callback=self.stop, pulse_thread=self.pulse_thread)
            self.pulse_thread.tray_icon = self.tray_app
            self.pulse_thread.start()
            self.tray_app.run() # This blocks until the tray icon is stopped
        else:
            # Otherwise, run in CLI mode
            print("pystray not found. Running in CLI mode. Press Ctrl+C to exit.")
            self.pulse_thread.start()
            try:
                # Keep the main thread alive to catch Ctrl+C
                while self._running:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nCtrl+C detected.")
                self.stop()

        # Wait for the pulse thread to finish its cleanup
        self.pulse_thread.join()
        print("WakeTheDrive has stopped.")

    def stop(self):
        """Stops the application."""
        if not self._running:
            return

        print("Stopping WakeTheDrive...")
        self._running = False

        # Signal the pulse thread to stop
        if self.pulse_thread:
            self.pulse_thread.stop()

        # The tray app will be stopped by its own exit handler
        # In CLI mode, the main loop will terminate

def main():
    parser = argparse.ArgumentParser(
        description="A tool to prevent a drive from sleeping by periodically writing a small file."
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=DEFAULT_INTERVAL,
        help=f"The interval in seconds between disk pulses. Default: {DEFAULT_INTERVAL}",
    )
    args = parser.parse_args()

    # Check for frozen (PyInstaller) environment
    if getattr(sys, 'frozen', False):
        # In a bundled app, we might not want any console output unless for errors
        # For now, we keep it for visibility.
        pass

    # Load (or create) the config file; CLI args take precedence over config values
    cfg = ensure_config()
    interval = args.interval if args.interval != DEFAULT_INTERVAL else cfg.get("interval_seconds", DEFAULT_INTERVAL)

    app = WakeTheDrive(interval=interval)
    app.run()

if __name__ == "__main__":
    main()
