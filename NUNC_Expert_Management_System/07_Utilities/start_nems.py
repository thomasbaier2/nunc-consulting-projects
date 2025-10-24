#!/usr/bin/env python3
"""
NUNC Expert Management System - Starter
"""

import os
import sys
import webbrowser
import time
import threading
from pathlib import Path

def main():
    print("Starting NUNC Expert Management System...")
    
    # Web-Interface starten
    web_script = Path("NUNC_Expert_Management_System/05_Shared_Components/web_interface.py")
    
    if web_script.exists():
        print("Web-Interface found")
        
        # Browser öffnen
        def open_browser():
            time.sleep(3)
            try:
                webbrowser.open('http://127.0.0.1:9000')
                print("Browser opened: http://127.0.0.1:9000")
            except Exception as e:
                print(f"Error opening browser: {e}")
                print("Please open manually: http://127.0.0.1:9000")
        
        threading.Thread(target=open_browser).start()
        
        # Flask App starten
        print("Starting Flask on port 9000...")
        os.system(f'python "{web_script}"')
    else:
        print("Web-Interface not found")

if __name__ == "__main__":
    main()

