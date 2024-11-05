import argparse
import http.server
import os
import socketserver
import threading
import time
import webbrowser

import pkg_resources


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", type=str, required=True, help="Path to the spec directory"
    )
    return parser.parse_args()


def get_specs(input_dir):
    specs = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith("spec.json"):
                specs.append(os.path.join(root.replace(input_dir, ""), file))
    return list(sorted(specs))


def specs_to_options(specs):
    return "\n".join([f'<option value="{spec}">{spec}</option>' for spec in specs])


def insert_options_to_html(options):
    template_path = pkg_resources.resource_filename("gs_me", "genomespy/index.html")
    with open(template_path, "r") as f:
        html = f.read()
    return html.replace("<!-- Options will be inserted here -->", options)


class HTMLHandler(http.server.SimpleHTTPRequestHandler):
    html_content = ""  # Class variable to store HTML content

    def do_GET(self):
        if self.path == "/":
            # Serve our HTML content
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(self.html_content.encode())
        else:
            # Serve other files from directory as usual
            super().do_GET()


def start_server(input_dir, html_content):
    # Set the HTML content for our handler
    HTMLHandler.html_content = html_content

    # Change to input directory for serving spec files
    os.chdir(input_dir)

    # Create and start the server
    with socketserver.TCPServer(("", 8000), HTMLHandler) as httpd:
        httpd.serve_forever()


def main():
    args = parse_args()

    specs = get_specs(args.input)
    options = specs_to_options(specs)
    html_data = insert_options_to_html(options)

    # Start server in background
    server_thread = threading.Thread(
        target=start_server, args=(args.input, html_data), daemon=True
    )
    server_thread.start()

    # Wait a moment for server to start
    time.sleep(1)

    # Open browser
    webbrowser.open("http://localhost:8000")

    print("Server started at http://localhost:8000")
    print("Press Ctrl+C to stop the server...")

    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down server...")


if __name__ == "__main__":
    main()
