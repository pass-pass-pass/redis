from flask import Flask, request, jsonify,render_template, redirect, url_for
import redis
from redis_manager import RedisManager

app = Flask(__name__)



redis_manager = RedisManager()  



@app.route('/article/<id>', methods=['GET'])
def display_article(id):
    article_content = redis_manager.get_article(id)
    comments = redis_manager.get_comments_for_article(id) if article_content else []
    return render_template('article.html', id=id, content=article_content.decode() if article_content else "Article not found", comments=[comment.decode() for comment in comments])

@app.route('/article/<id>/comment', methods=['POST'])
def add_comment_to_article_web(id):
    comment = request.form['comment']
    redis_manager.add_comment_to_article(id, comment)
    return redirect(url_for('display_article', id=id))

@app.route('/article/<id>/tag', methods=['POST'])
def add_tag_to_article_web(id):
    tag = request.form['tag']
    redis_manager.add_tag_to_article(id, tag)
    return redirect(url_for('display_article', id=id))

@app.route('/article/<id>/view', methods=['GET'])  
def increase_view_web(id):
    redis_manager.increase_article_views(id)
    return redirect(url_for('display_article', id=id))

@app.route('/articles/most_viewed', methods=['GET'])
def display_most_viewed():
    articles = redis_manager.get_most_viewed_articles()
    return render_template('most_viewed.html', articles=[article.decode() for article in articles])


@app.route('/')
def index():

    article_ids = [article_id.decode() for article_id in redis_manager.get_tags_for_article()]
    return render_template('index.html', article_ids=article_ids)

@app.route('/create_post')
def create_post():
    return render_template('create_post.html')

@app.route('/post', methods=['POST'])
def post_article():
    article_id = request.form['id']
    content = request.form['content']
    redis_manager.save_article(article_id, content)
    return redirect(url_for('index'))

@app.route('/view_post', methods=['POST'])
def view_post():
    article_id = request.form['article_id']
    content = redis_manager.get_article(article_id)
    if content:
        content = content.decode()
    else:
        content = "Post not found"
    return render_template('view_post.html', content=content)

