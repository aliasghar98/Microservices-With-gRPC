import os

from flask import Flask, render_template, request
import grpc

from recommendations_pb2 import MovieCategory, RecommendationRequest
from recommendations_pb2_grpc import RecommendationsStub

app = Flask(__name__)

recommendations_host = os.getenv("RECOMMENDATIONS_HOST", "localhost")
recommendations_channel = grpc.insecure_channel(
    f"{recommendations_host}:50051"
)
recommendations_client = RecommendationsStub(recommendations_channel)


@app.route('/')
def form():
    return render_template('form.html')

@app.route('/data/',methods=['POST','GET'])
def data():
    if request.method == 'GET':
        return f"Please fill the form first!"
    if request.method == 'POST':
        user_id = int(request.form.get("ID"))
        category = request.form.get("Category")
        max_results = int(request.form.get("Results"))
        recommendations_request = RecommendationRequest(
            user_id=user_id, category=category, max_results=max_results
        )
        recommendations_response = recommendations_client.Recommend(
            recommendations_request
        )
        return render_template(
            "data.html",
            recommendations=recommendations_response.recommendations,
        )