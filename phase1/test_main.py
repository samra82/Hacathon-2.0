"""Test script for main.py - Demonstrates all features"""
import subprocess
import sys

def test_main():
    """Test main.py with scripted commands."""

    # Commands to test all features
    commands = [
        "help",
        "list",
        "add Buy groceries",
        "add Call dentist",
        "add Finish report",
        "list",
        "complete 1",
        "list",
        "update 2 Call dentist about appointment",
        "list",
        "delete 3",
        "list",
        "exit"
    ]

    # Create input string
    input_str = "\n".join(commands) + "\n"

    print("=" * 60)
    print("Testing main.py with all features")
    print("=" * 60)
    print("\nCommands to execute:")
    for cmd in commands:
        print(f"  > {cmd}")
    print("\n" + "=" * 60)
    print("Output:")
    print("=" * 60 + "\n")

    # Run main.py with input
    result = subprocess.run(
        [sys.executable, "main.py"],
        input=input_str,
        capture_output=True,
        text=True,
        cwd="C:/Users/Queen_tiara/Documents/samra/Quater-4-hacathon/Hacathon-2/phase1"
    )

    print(result.stdout)

    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("✓ main.py executed successfully!")
        print("=" * 60)
        return True
    else:
        print("\n" + "=" * 60)
        print("✗ main.py failed with errors:")
        print(result.stderr)
        print("=" * 60)
        return False

if __name__ == "__main__":
    success = test_main()
    sys.exit(0 if success else 1)
