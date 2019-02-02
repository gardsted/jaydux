template="""\
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Search</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.2/css/bulma.min.css">
    <script defer src="https://use.fontawesome.com/releases/v5.3.1/js/all.js"></script>
  </head>
  <body>
    <section>
    {_nav}
    {_articles}
   </section>
  </body>
</html>
"""
_nav = """\
<div class="container">
<nav class="level">
  <!-- Left side -->
  <div class="level-left">
    <div class="level-item">
      <form>
      <div class="field has-addons">
        <p class="control">
          <input class="input" type="text" placeholder="Find artikler" name=q>
        </p>
        <p class="control">
          <button class="button">søg</button>
        </p>
      </div>
      </form>
    </div>
  </div>
</nav>
</div>
"""
_articles = """\
<div class="container">
{articles}
</div>
"""

_article = """\
<article><img src="{img}"><p class="subtitle is-{level}">{title}</p>(<a href="{url}">@{netloc}</a>) {text}</article>
"""

_media = """\
<article class="media">
  <figure class="media-left"><p class="image is-128x128"><img src="{img}"></p></figure>
  <div class="media-content">
    <div class="content"><p><strong>{title}</strong> <br>(<a href="{url}">@{netloc}</a>) {text} </div>
  </div>
</article>
"""

_columns = """\
<div class="columns">
{columns}
</div>
"""
_column = """\
<div class="column">{column}</div>
"""

def columns(template, horizontal, vertical, level, searchresult):
    articles = [searchresult.pop(False) for i in range(horizontal*vertical) if len(searchresult)]
    articles = [template.format(level=level, **a) for a in articles if a]
    columns = [[] for h in range(horizontal)]
    for h in range(horizontal):
        columns[h].extend(articles[h::horizontal])
    return _columns.format(
        columns="\n".join([
            _column.format(column="\n".join(c))
            for c in columns
        ]))


def render(searchresult):
    articles=[]
    articles.append(_article.format(level=3, **(searchresult.pop())))
    articles.append(columns(_article, 2, 1, 4, searchresult))
    articles.append(columns(_article, 3, 1, 5, searchresult))
    articles.append(columns(_article, 3, 1, 5, searchresult))
    articles.append(columns(_media, 2, 50, 6, searchresult))

    #print(searchresult)
    return template.format(
        _nav=_nav,
        _articles=_articles.format(articles="\n".join(articles))
    )

