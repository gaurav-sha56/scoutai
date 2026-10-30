import os
import sys
import pytest
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv
from scoutai_backend.main import run, test as run_test_function

load_dotenv()


@pytest.mark.parametrize("domain, startup_name", [
    ("artificial intelligence", "ScoutAI"),
    ("healthcare", "MedScout"),
])
def test_run_crew(domain: str, startup_name: str):
    """
    Test 2: Test the run function and test function in main.py.

    Contains two parameters: domain and startup_name.
    """
    with patch("scoutai_backend.main.ScoutaiBackend") as mock_backend_cls:
        # Mock backend, crew, and kickoff return value
        mock_backend_instance = MagicMock()
        mock_crew_instance = MagicMock()
        mock_result = MagicMock()
        mock_result.raw = f"Report for {startup_name} in domain {domain}"

        mock_crew_instance.kickoff.return_value = mock_result
        mock_backend_instance.crew.return_value = mock_crew_instance
        mock_backend_cls.return_value = mock_backend_instance

        # 1. Test calling run() directly with domain and startup_name
        result = run(domain=domain, startup_name=startup_name)
        expected_inputs = {
            'domain': domain,
            'our_startup': startup_name
        }
        mock_crew_instance.kickoff.assert_called_once_with(inputs=expected_inputs)
        assert result == mock_result

        # 2. Test calling test() function from main.py with domain and startup_name
        mock_crew_instance.kickoff.reset_mock()
        test_result = run_test_function(domain=domain, startup_name=startup_name)
        mock_crew_instance.kickoff.assert_called_once_with(inputs=expected_inputs)
        assert test_result == mock_result


@pytest.mark.parametrize("domain, startup_name", [
    ("artificial intelligence", "ScoutAI"),
])
def test_run_live(domain: str, startup_name: str):
    """
    Optional live end-to-end integration test.
    Only runs when RUN_LIVE_CREW=1 is set in the environment or .env file,
    since a live crew run performs real web searches and LLM generation.
    """
    if os.getenv("RUN_LIVE_CREW", "0") != "1":
        pytest.skip("Skipping live crew test. Set RUN_LIVE_CREW=1 in .env to run real execution.")

    result = run(domain=domain, startup_name=startup_name)
    assert result is not None
    assert hasattr(result, "raw")
    assert len(str(result.raw).strip()) > 0


if __name__ == "__main__":
    # Support running this test directly as a script:
    # python tests/test_run.py [domain] [startup_name]
    arg_domain = sys.argv[1] if len(sys.argv) > 1 else "artificial intelligence"
    arg_startup = sys.argv[2] if len(sys.argv) > 2 else "ScoutAI"
    print(f"Running test with domain='{arg_domain}' and startup_name='{arg_startup}'...")
    test_run_crew(domain=arg_domain, startup_name=arg_startup)
    print("Test passed successfully!")
