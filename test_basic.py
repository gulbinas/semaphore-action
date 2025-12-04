def test_basic():
    assert 1 + 1 == 2

def test_string_operations():
    assert "hello" + " world" == "hello world"

if __name__ == "__main__":
    test_basic()
    test_string_operations()
    print("All tests passed!")
