import csv


class Rating:
    def __init__(self, userId: int, movieId: int, rating: float, timestamp: int):
        self.userId, self.movieId, self.rating, self.timestamp = userId, movieId, rating, timestamp


def load_from_file(filename: str = "ratings.csv") -> list[Rating]:
    ratings_list = []
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            id = int(row["userId"])
            movie = int(row["movieId"])
            rating = float(row["rating"])
            time = row["timestamp"]
            ratings_list.append(Rating(id, movie, rating, time))

    return ratings_list
