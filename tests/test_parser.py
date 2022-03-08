from models.photo import Photo
from parsers.parser import CSVParser
from tests.mocks.photo_mock import photo, photo_other


class TestCSVParser:
    def setup(self):
        self.parser = CSVParser()

    def test_sort(self):
        data = [
            {"id": 3},
            {"id": 1},
            {"id": 2},
        ]

        assert self.parser._sort(data=data, by="id") == [
            {"id": 1},
            {"id": 2},
            {"id": 3},
        ]

    def test_remove_duplicates(self):
        data = [{"id": 3}, {"id": 3}, {"id": 1}, {"id": 2}, {"id": 2}]

        result = self.parser._remove_duplicates(data)
        assert len(result) == 3
        for item in result:
            assert item["id"] in [1, 2, 3]

    def test_prepare_data_and_save(self):
        obj_one = Photo(**photo)
        obj_one.set_file_path('path')
        obj_two = Photo(**photo_other)
        obj_two.set_file_path('path')

        data = [obj_two, obj_one, obj_two]

        assert self.parser._prepare_data(data=data) == {
            "fieldnames": ['id', 'title', 'url', 'thumbnailUrl', 'albumId', 'filePath'],
            "data": [
                {
                    **photo,
                    "filePath": "path"
                }, {
                    **photo_other,
                    "filePath": "path"
                }
            ]
        }
