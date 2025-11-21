import os
import subprocess

def test_mvp_end_to_end():
    """
    Tests the MVP's end-to-end functionality.
    """
    # 1. Set up the input
    input_text = "I need to improve the agent's performance."
    with open("input.txt", "w") as f:
        f.write(input_text)

    # 2. Run the agent
    subprocess.run(["python3", "main.py"])

    # 3. Verify the output
    with open("output.txt", "r") as f:
        output_text = f.read().strip()

    expected_output = "The agent has decided to work on: 'Develop new feature X'."
    assert output_text == expected_output

    # 4. Clean up
    os.remove("input.txt")
    os.remove("output.txt")

if __name__ == "__main__":
    test_mvp_end_to_end()
