import hw
import pytest


# do not need to change this
def check_result(actual, expected):
    """
    Checks the actual result of a test to the expected and either outputs
    no error message if they match or the appropriate error message.
    
    Inputs:
        actual [Any]: the result of the function being tested
        expected [Any]: the correct value that the function should output
    """
    # Case #1: if expected is None
    #   a: if actual is None, return None
    #   b: if actual is not None, return an error message
    if expected is None:
        if actual is None:
            return None
        else:
            return "The function returned a value other than the expected value: None."
    # Case #2: if actual is None, return an error message
    if actual is None:
        return "The function returned None when a value other than None was expected."
    # Case #3: check that the type of expected == type of actual
    actual_type = type(actual)
    expected_type = type(expected)
    if actual_type != expected_type:
        return (f"\n\nThe function returned a value of the wrong type.\n"
           f"  Expected return type: {expected_type.__name__}\n"
           f"  Actual return type: {actual_type.__name__}\n")
    # Case #4: if expected is a float, check that actual is within delta of expected
    if isinstance(expected, float):
        if pytest.approx(expected) == actual:
            return None
        else:
            return (f"\n\nActual ({actual}) and expected ({expected}) "
           f"values do not match.\n")
    # Case #5: check that the actual value is equal to the expected value
    if expected == actual:
        return None
    else:
        return (f"\n\nActual ({actual}) and expected ({expected}) "
        f"values do not match.\n")

# CHANGE this to have the right parameters and test cases
@pytest.mark.parametrize("x, expected",
                         [[1, 2],
                          [3, 4],
                          [7, 8],
                          [100, 101],
                          [1234, 1235]])
# CHANGE the name of this to test_[name of function]
def test_f1(x, expected):
    # CHANGE this to hw#.[name of function]([parameters])
    actual = hw.f1(x)
    error_msg = check_result(actual, expected)
    if error_msg is not None:
        pytest.fail(error_msg)

# testing None functions
@pytest.mark.parametrize("expected",
                          [None, None])
def test_f2(expected):
    actual = hw.f2()
    error_msg = check_result(actual, expected)
    if error_msg is not None:
        pytest.fail(error_msg)