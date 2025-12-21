import csv


class Movie:
    def __init__(self, id: int, name: str, genre: list[str]):
        self.id, self.name, self.genre = id, name, genre


def load_from_file(filename: str = "movies.csv") -> list[Movie]:
    movie_list = []
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            id = int(row["movieId"])
            name = row["title"]
            genres = row["genres"].split('|')
            movie_list.append(Movie(id, name, genres))

    return movie_list
