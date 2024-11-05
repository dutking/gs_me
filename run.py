import argparse
import os


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
    with open("genomespy/index.html", "r") as f:
        html = f.read()
    return html.replace("<!-- Options will be inserted here -->", options)


def output_files(input_dir, html_data):
    abs_input_dir = os.path.abspath(input_dir)
    with open(os.path.join(input_dir, "run.sh"), "w") as f:
        f.write("#!/bin/bash\n")
        f.write(f"cd {abs_input_dir}\n")
        f.write("python3 -m http.server 8000 & \n")
        f.write(
            "python3 -c \"import webbrowser; webbrowser.open('http://localhost:8000')\"\n"
        )

    with open(os.path.join(input_dir, "index.html"), "w") as f:
        f.write(html_data)


def main():
    args = parse_args()

    specs = get_specs(args.input)
    options = specs_to_options(specs)
    html_data = insert_options_to_html(options)
    output_files(args.input, html_data)
    print("Done!")


if __name__ == "__main__":
    main()
