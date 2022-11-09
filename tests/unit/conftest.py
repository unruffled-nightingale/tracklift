import pytest

SKIP_TESTS = True


requires_login = pytest.mark.skipif(
    SKIP_TESTS, reason="Test requires Spotify login. Used for manual testing."
)
