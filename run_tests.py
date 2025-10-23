import sys
import pytest

if __name__ == '__main__':
    # Run pytest programmatically
    ret = pytest.main(['-q'])
    if ret == 0:
        print('All tests passed.')
        sys.exit(0)
    else:
        print('Some tests failed.')
        sys.exit(ret)
