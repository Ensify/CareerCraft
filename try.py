from app.utils.recommend import Recommender

recommender = Recommender()
user = recommender.mongo.get_user_object("66a7d42b58534c67a510e731")
print(recommender.getRecommendations(user, 1))