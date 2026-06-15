import unittest
import sys
import os
from datetime import datetime

# Define report paths
WORKSPACE_REPORT = "test_report.md"
ARTIFACTS_DIR = "C:/Users/atulp/.gemini/antigravity-ide/brain/341ec7b1-9646-40b1-9d17-9bb9c0105781"
ARTIFACTS_REPORT = os.path.join(ARTIFACTS_DIR, "test_report.md")


def generate_report(result):
    print("[Test Runner] Generating test report...")

    # Calculate statistics
    total = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passes = total - failures - errors

    # Gather test results
    all_results = getattr(result, "results", [])

    # Construct Markdown content
    md = []
    md.append("# SnapRenamr - Production Readiness Test Report")
    md.append(f"\n**Generated on**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    md.append("\n## Summary")
    md.append(f"- **Total Tests Run**: {total}")
    md.append(f"- **Passes**: {passes} ({(passes/total*100):.1f}%)")
    md.append(f"- **Failures**: {failures}")
    md.append(f"- **Errors**: {errors}")
    md.append(f"- **Overall Status**: {'🟢 PASS' if result.wasSuccessful() else '🔴 FAIL'}")

    md.append("\n## Test Details")
    md.append("| Test Class | Test Case | Status | Error Details |")
    md.append("| --- | --- | --- | --- |")

    for test, status, detail in all_results:
        class_name = test.__class__.__name__
        method_name = test._testMethodName
        detail_clean = detail.replace("\n", "<br>").replace("|", "\\|") if detail else ""
        status_icon = "🟢 PASS" if status == "PASS" else ("🔴 FAIL" if status == "FAIL" else "🟡 ERROR")
        md.append(f"| {class_name} | {method_name} | {status_icon} | {detail_clean} |")

    report_content = "\n".join(md)

    # Save to workspace
    with open(WORKSPACE_REPORT, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"[Test Runner] Workspace report saved to {WORKSPACE_REPORT}")

    # Save to artifacts directory
    try:
        os.makedirs(ARTIFACTS_DIR, exist_ok=True)
        with open(ARTIFACTS_REPORT, "w", encoding="utf-8") as f:
            f.write(report_content)
        print(f"[Test Runner] Artifacts report saved to {ARTIFACTS_REPORT}")
    except Exception as e:
        print(f"[Test Runner] Warning: could not write to artifacts dir: {e}")


def main():
    loader = unittest.TestLoader()
    suite = loader.discover('tests')

    # Custom test result class to track individual test runs
    class CaptureResult(unittest.TextTestResult):
        def __init__(self, stream, descriptions, verbosity):
            super().__init__(stream, descriptions, verbosity)
            self.results = []

        def addSuccess(self, test):
            super().addSuccess(test)
            self.results.append((test, "PASS", ""))

        def addFailure(self, test, err):
            super().addFailure(test, err)
            self.results.append((test, "FAIL", self._exc_info_to_string(err, test)))

        def addError(self, test, err):
            super().addError(test, err)
            self.results.append((test, "ERROR", self._exc_info_to_string(err, test)))

    runner = unittest.TextTestRunner(resultclass=CaptureResult, verbosity=2)
    result = runner.run(suite)

    generate_report(result)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
