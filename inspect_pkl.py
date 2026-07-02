import argparse
import pickle
import sys
import types

if sys.platform == "win32":
    # The executor imports resource, but inspection does not use it.
    sys.modules["resource"] = types.ModuleType("resource")

parser = argparse.ArgumentParser()
parser.add_argument("file")
parser.add_argument("--limit", type=int, default=3)
args = parser.parse_args()

# Warning: pickle.load can execute malicious code.
with open(args.file, "rb") as f:
    records = pickle.load(f)

print(f"Records: {len(records)}")

for index, record in enumerate(records[:args.limit]):
    print(f"\n{'=' * 20} RECORD {index} {'=' * 20}")
    print("\nPROMPT:\n", getattr(record, "prompt", "N/A"))
    print("\nCANONICAL SOLUTION:\n", getattr(record, "solution", "N/A"))

    print("\nGENERATED TESTS:")
    for test_index, test in enumerate(getattr(record, "testcases", [])):
        # Raw pickle uses strings; processed pickle uses TestCase objects.
        if isinstance(test, str):
            print(f"\n[{test_index}]\n{test}")
        else:
            print(f"\n[{test_index}] {test.text}")
            print(f"Ground-truth valid: {test.is_valid}")
            print(f"Predicted valid:    {test.prediction_is_valid}")
            print(f"Predicted score:    {test.prediction_y_prob}")

    generated = getattr(record, "generated_solutions", [])
    if generated:
        print("\nGENERATED SOLUTIONS:")
        for solution_index, solution in enumerate(generated):
            print(f"\n--- Candidate {solution_index} ---\n{solution}")