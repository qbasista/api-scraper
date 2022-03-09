from src.utils import add_prefix_to_keys


class TestUtils:
    def test_add_prefix_to_keys(self):
        data = {
            "one": 1,
            "two": 2,
        }

        assert add_prefix_to_keys(data=data, prefix="new") == {
            "new_one": 1,
            "new_two": 2,
        }
