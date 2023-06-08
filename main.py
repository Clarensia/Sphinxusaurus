from dataclasses import asdict
import json

from src.parser.ProjectParser import ProjectParser
from src.writer.Writer import Writer

def main():
    dest_writer = Writer("dest/")
    parser = ProjectParser()
    full_project = parser.parse_project("input/")
    dest_writer.write(full_project)

if __name__ == "__main__":
    main()
