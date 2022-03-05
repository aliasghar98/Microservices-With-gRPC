from concurrent import futures
import random

import grpc

from recommendations_pb2 import (
    MovieCategory,
    MovieRecommendation,
    RecommendationResponse,
)
import recommendations_pb2_grpc

movies_by_category = {
    MovieCategory.Action: [
        MovieRecommendation(id=100, title="The Batman", rating = 8.0),
        MovieRecommendation(id=101, title="Eternals", rating = 6.7),
        MovieRecommendation(id=102, title="Kingsman: The Secret Service",rating = 6.9),
    ],
    MovieCategory.Adventure: [
        MovieRecommendation(id=200, title="The Last Samurai", rating = 7.5),
        MovieRecommendation(id=201, title="The Revenant", rating = 8.9),
        MovieRecommendation(id=202, title="Blood Diamond", rating = 7.2),
    ],
    MovieCategory.Comedy: [
        MovieRecommendation(id=300, title="Central Intelligence", rating = 6.1),
        MovieRecommendation(id=301, title="Mr. Bean's Holiday",rating = 6.8),
        MovieRecommendation(id=302, title="Rush Hour",rating = 7.1),
    ],
    MovieCategory.Thriller: [
        MovieRecommendation(id=400, title="The Dark Knight", rating = 8.4),
        MovieRecommendation(id=401, title="Inception", rating = 8.5),
        MovieRecommendation(id=402, title="Se7en", rating = 8.1),
    ],
    MovieCategory.Fantasy: [
        MovieRecommendation(id=500, title="Spider-Man: No Way Home", rating = 7.9),
        MovieRecommendation(id=501, title="Fantastic Beasts and Where to Find Them" , rating= 7.2),
        MovieRecommendation(id=502, title="Lord of the Rings: The Fellowship of the Ring", rating = 9.1),
    ],
    MovieCategory.Horror: [
        MovieRecommendation(id=600, title="Scream", rating = 6.5),
        MovieRecommendation(id=601, title="Insidious", rating = 6.4),
        MovieRecommendation(id=602, title="The Conjuring", rating = 6.8),
    ],
}

class RecommendationService(
    recommendations_pb2_grpc.RecommendationsServicer
):
    def Recommend(self, request, context):
        if request.category not in movies_by_category:
            context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")

        movies_for_category = movies_by_category[request.category]
        num_results = min(request.max_results, len(movies_for_category))
        movies_to_recommend = random.sample(
            movies_for_category, num_results
        )

        return RecommendationResponse(recommendations=movies_to_recommend)


def runService():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    recommendations_pb2_grpc.add_RecommendationsServicer_to_server(
        RecommendationService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Recommendation service server running...")
    server.wait_for_termination()


if __name__ == "__main__":
    runService()