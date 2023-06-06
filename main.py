from dataclasses import asdict
import json
from src.parser.MainClassParser import MainClassParser

def main():
    parser = MainClassParser()
    main_file = parser.parse_file("input/BlockchainAPIs.py")
    print(json.dumps(asdict(main_file), indent=4))

if __name__ == "__main__":
    main()
