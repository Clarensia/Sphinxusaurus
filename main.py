from dataclasses import asdict
import json

from src.parser.ProjectParser import ProjectParser

def main():
    parser = ProjectParser()
    full_project = parser.parse_project("input/")
    print(json.dumps(asdict(full_project), indent=4))

if __name__ == "__main__":
    main()
