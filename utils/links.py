import csv


class Link:
    def __init__(self, movieId: int, imdbId: int, tmdbId: int):
        self.movieId, self.imdbId, self.tmdbId = movieId, imdbId, tmdbId


def load_from_file(filename: str = "links.csv") -> list[Link]:
    links_list = []
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movieId = int(row["movieId"])
            imdbId = int(row["imdbId"])
            try:
                tmdbId = float(row["tmdbId"])
            except Exception:
                tmdbId = 0.0
            links_list.append(Link(movieId, imdbId, tmdbId))

    return links_list
