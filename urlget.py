import subprocess
import re
import sys

def start_cloudflared(port):
    try:
        # Start the cloudflared tunnel process
        process = subprocess.Popen(
            ['cloudflared', 'tunnel', '--url', f'http://localhost:{port}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        # Wait and read output line by line
        public_url = None
        for line in process.stdout:
            # Look for the public URL in output
            match = re.search(r'https://[a-zA-Z0-9\-]+\.trycloudflare\.com', line)
            if match:
                public_url = match.group(0)
                return public_url
                break

        if not public_url:
            print("Public URL not found.")
            process.terminate()
            sys.exit()

    except FileNotFoundError:
        print("cloudflared is not installed or not in PATH.")
        sys.exit()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit()
