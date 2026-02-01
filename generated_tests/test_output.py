import pytest
import sys

def add(a, b):
    """Returns sum of two integers."""
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("Both arguments must be integers")
    return a + b

class TestAdd:
    
    # Normal operation tests
    def test_add_positive_numbers(self):
        assert add(2, 3) == 5
        assert add(10, 20) == 30
        assert add(1, 1) == 2
    
    def test_add_negative_numbers(self):
        assert add(-2, -3) == -5
        assert add(-10, -20) == -30
    
    def test_add_positive_and_negative(self):
        assert add(5, -3) == 2
        assert add(-5, 3) == -2
        assert add(10, -10) == 0
    
    def test_add_with_zero(self):
        assert add(0, 0) == 0
        assert add(0, 5) == 5
        assert add(5, 0) == 5
        assert add(0, -5) == -5
        assert add(-5, 0) == -5
    
    # Edge cases
    def test_add_large_numbers(self):
        assert add(1000000, 2000000) == 3000000
        assert add(sys.maxsize - 1, 1) == sys.maxsize
    
    def test_add_very_negative_numbers(self):
        assert add(-1000000, -2000000) == -3000000
        assert add(-sys.maxsize - 1, 0) == -sys.maxsize - 1
    
    def test_add_max_int_values(self):
        # Test with maximum integer values
        max_int = sys.maxsize
        min_int = -sys.maxsize - 1
        assert add(max_int, 0) == max_int
        assert add(min_int, 0) == min_int
        assert add(max_int, min_int) == -1
    
    # Error conditions
    def test_add_with_float_arguments(self):
        with pytest.raises(TypeError, match="Both arguments must be integers"):
            add(2.5, 3)
        with pytest.raises(TypeError, match="Both arguments must be integers"):
            add(2, 3.5)
        with pytest.raises(TypeError, match="Both arguments must be integers"):
            add(2.5, 3.5)
    
    def test_add_with_string_arguments(self):
        with pytest.raises(TypeError, match="Both arguments must be integers"):
            add("2", 3)
        with pytest.raises(TypeError, match="Both arguments must be integers"):
            add(2, "3")
        with pytest.raises(TypeError, match="Both arguments must be integers"):
            add("2", "3")
    
    def test_add_with_none_arguments(self):
        with pytest.raises(TypeError, match="Both arguments must be integers"):
            add(None, 3)
        with pytest.raises(TypeError, match="Both arguments must be integers"):
            add(2, None)
        with pytest.raises(TypeError, match="Both arguments must be integers"):
            add(None, None)
    
    def test_add_with_boolean_arguments(self):
        # Note: In Python, bool is a subclass of int, so this might pass
        # depending on implementation. Testing the current behavior.
        with pytest.raises(TypeError, match="Both arguments must be integers"):
            add(True, 3)
        with pytest.raises(TypeError, match="Both arguments must be integers"):
            add(2, False)
    
    def test_add_with_list_arguments(self):
        with pytest.raises(TypeError, match="Both arguments must be integers"):
            add([1, 2], 3)
        with pytest.raises(TypeError, match="Both arguments must be integers"):
            add(2, [3, 4])
    
    def test_add_with_missing_arguments(self):
        with pytest.raises(TypeError):
            add(5)  # Missing second argument
        with pytest.raises(TypeError):
            add()   # Missing both arguments

    # Parametrized tests for comprehensive coverage
    @pytest.mark.parametrize("a,b,expected", [
        (0, 0, 0),
        (1, 2, 3),
        (-1, -2, -3),
        (100, -50, 50),
        (-100, 100, 0),
        (999999, 1, 1000000),
    ])
    def test_add_parametrized(self, a, b, expected):
        assert add(a, b) == expected