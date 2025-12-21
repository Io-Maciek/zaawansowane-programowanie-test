import csv


class Tag:
    def __init__(self, userId: int, movieId: int, tag: str, timestamp: int):
        self.userId, self.movieId, self.tag, self.timestamp = userId, movieId, tag, timestamp


def load_from_file(filename: str = "tags.csv") -> list[Tag]:
    tag_list = []
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movieId = int(row["movieId"])
            userId = int(row["userId"])
            tag = row["tag"]
            timestamp = int(row["timestamp"])
            tag_list.append(Tag(userId, movieId, tag, timestamp))

    return tag_list
