import argparse
import http.server
import os
import socketserver
import threading
import time
import webbrowser
from importlib import resources


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", type=str, required=True, help="Path to the directory"
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
    with resources.files("gs_me").joinpath("genomespy/index.html").open("r") as f:
        html = f.read()
    return html.replace("<!-- Options will be inserted here -->", options)


class HTMLHandler(http.server.SimpleHTTPRequestHandler):
    html_content = ""

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(self.html_content.encode())
        else:
            super().do_GET()

    def log_message(self, format, *args):
        pass


def find_free_port(start_port=8000, max_tries=100):
    for port in range(start_port, start_port + max_tries):
        try:
            with socketserver.TCPServer(("", port), None) as s:
                return port
        except OSError:
            continue
    raise RuntimeError(f"Could not find a free port after {max_tries} attempts")


def start_server(input_dir, html_content, port):
    HTMLHandler.html_content = html_content
    os.chdir(input_dir)

    try:
        with socketserver.TCPServer(("", port), HTMLHandler) as httpd:
            httpd.serve_forever()
    except OSError:
        new_port = find_free_port(port + 1)
        start_server(input_dir, html_content, new_port)


def main():
    args = parse_args()
    specs = get_specs(args.input)
    options = specs_to_options(specs)
    html_data = insert_options_to_html(options)
    print("Starting server...")
    try:
        port = find_free_port()
    except RuntimeError as e:
        print(f"Error: {e}")
        return

    server_thread = threading.Thread(
        target=start_server, args=(args.input, html_data, port), daemon=True
    )
    server_thread.start()
    time.sleep(1)

    webbrowser.open(f"http://localhost:{port}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down server...")

    print("Press Ctrl+C to stop the server.")


if __name__ == "__main__":
    main()