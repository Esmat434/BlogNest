from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from django.db.models import Prefetch, Count
import numpy as np
from .models import Post

posts = Post.objects.all()

X = np.array([post.get_features() for post in posts])
Y = np.array([post.likes.count() + post.views.count() for post in posts])

x_train, x_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(x_train, y_train)

y_pred = model.predict(x_test)


def rank_posts():
    posts = (
        Post.objects.filter(status="published")
        .annotate(comment_count=Count("Comment"))
        .prefetch_related(Prefetch("image"))
    )
    features = [post.get_features() for post in posts]
    predicted_socres = model.predict(features)

    for post, score in zip(posts, predicted_socres):
        post.predicted_score = score

    ranked_posts = sorted(posts, key=lambda post: post.predicted_score, reverse=True)

    return ranked_posts
