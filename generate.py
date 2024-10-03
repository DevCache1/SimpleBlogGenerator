import os
import markdown
from datetime import datetime

# Constants for directories
POSTS_DIR = 'posts'
OUTPUT_DIR = 'output'
INDEX_FILE = os.path.join(OUTPUT_DIR, 'index.html')

def ensure_output_directory():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def format_date(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%B %d, %Y')

def render_post(title, content, date):
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <a href="index.html" class="back-link">Back to Home</a>
        <p class="date"><i>published on {date}</i></p>
        <hr>
        <div>{content}</div>
    </div>
</body>
</html>
"""

def render_index(posts):
    post_links = "\n".join([f'<li><a href="{post["slug"]}.html">{post["title"]}</a> - <span class="date">{post["date"]}</span></li>' for post in posts])
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>thoughtStorm</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>irrelevant thoughts about anything or everything</h1>
        <ul>
            {post_links}
        </ul>
    </div>
</body>
</html>
"""

def generate_blog():
    ensure_output_directory()
    posts = []

    # Read all markdown files from the posts directory
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith('.md'):
            filepath = os.path.join(POSTS_DIR, filename)
            creation_time = os.path.getctime(filepath)  # Get creation time
            formatted_date = format_date(creation_time)  # Format date
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                title = content.split('\n')[0].lstrip('# ').strip()  # Extract title from the first line
                html_content = markdown.markdown(content[len(title)+2:])  # Remove title line
                slug = filename[:-3]  # Remove .md extension

                # Generate individual post HTML
                post_html = render_post(title, html_content, formatted_date)
                post_output_path = os.path.join(OUTPUT_DIR, f'{slug}.html')
                with open(post_output_path, 'w', encoding='utf-8') as post_file:
                    post_file.write(post_html)

                # Add to posts list for index
                posts.append({"title": title, "slug": slug, "date": formatted_date})

    # Generate index HTML
    index_html = render_index(posts)
    with open(INDEX_FILE, 'w', encoding='utf-8') as index_file:
        index_file.write(index_html)

if __name__ == '__main__':
    generate_blog()
    print("Blog generated in the 'output' directory.")
