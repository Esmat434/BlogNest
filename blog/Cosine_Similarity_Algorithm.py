from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import Prefetch
from .models import Post, PostImage


def get_similar_posts(post_id):
    # تمام پست‌ها را از دیتابیس می‌خوانیم و تبدیل به لیست می‌کنیم
    posts = list(Post.objects.all())

    # محتواهای تمام پست‌ها را به یک لیست تبدیل می‌کنیم
    post_contents = [post.title + " " + post.content for post in posts]

    # با استفاده از TfidfVectorizer متن‌ها را به بردارهای عددی تبدیل می‌کنیم
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(post_contents)

    # پیدا کردن ایندکس پست جاری
    post_index = next(
        (index for index, post in enumerate(posts) if post.id == post_id), None
    )

    # محاسبه شباهت Cosine بین پست‌ها
    cosine_similarities = cosine_similarity(
        tfidf_matrix[post_index : post_index + 1], tfidf_matrix
    )

    # استخراج ایندکس‌های پست‌های مشابه
    similar_indices = cosine_similarities.argsort()[0][-6:-1]  # گرفتن 5 پست مشابه

    # گرفتن پست‌های مشابه از ایندکس‌ها
    similar_posts = [posts[i] for i in similar_indices]

    # پیش‌خوانی تصاویر به ازای پست‌های مشابه
    similar_posts = Post.objects.prefetch_related(
        Prefetch("image", queryset=PostImage.objects.all())
    ).filter(id__in=[posts[i].id for i in similar_indices])

    return similar_posts
