"""Build Gmeek with owner-only, explicitly published articles."""
import os
from pathlib import Path
import shutil
import subprocess
import sys


def prepare(source: Path, workspace: Path) -> None:
    shutil.copy2(workspace / 'config.json', source / 'config.json')
    shutil.copytree(workspace / 'static', source / 'static', dirs_exist_ok=True)
    generator = source / 'Gmeek.py'
    code = generator.read_text(encoding='utf-8')
    original = 'issues=self.repo.get_issues()'
    replacement = (
        'issues=(issue for issue in self.repo.get_issues(state="open", labels=["blog"]) '
        'if issue.user.login.casefold() == self.repo.owner.login.casefold() '
        'and not issue.pull_request)'
    )
    if code.count(original) != 1:
        raise RuntimeError('Gmeek article selection changed; review before building.')
    generator.write_text(code.replace(original, replacement), encoding='utf-8')

    template = source / 'templates' / 'plist.html'
    html = template.read_text(encoding='utf-8')
    marker = '{% block content %}'
    intro = '''{% block content %}
<nav class="author-tools" aria-label="博客管理">
  <a class="btn btn-primary" href="/write.html">✎ 写文章</a>
  <a href="https://github.com/1024971823/1024971823.github.io/issues?q=is%3Aissue+author%3A1024971823">管理文章</a>
  <a href="/writing.html">写作指南</a>
</nav>
{% if not postListJson %}
<section class="empty-state"><h2>故事，从第一篇开始。</h2>
<p>这里即将记录技术探索、项目笔记与生活中的小发现。</p></section>
{% endif %}'''
    if html.count(marker) != 1:
        raise RuntimeError('Gmeek homepage template changed; review before building.')
    template.write_text(html.replace(marker, intro), encoding='utf-8')


if __name__ == '__main__':
    workspace = Path(__file__).resolve().parents[1]
    source = Path(sys.argv[1]).resolve()
    prepare(source, workspace)
    # Gmeek writes transient backups and README to GITHUB_WORKSPACE.
    # Isolate these from the checked-out source repository.
    env = os.environ.copy()
    scratch = source / 'workspace'
    scratch.mkdir(exist_ok=True)
    env['GITHUB_WORKSPACE'] = str(scratch)
    subprocess.run(
        [sys.executable, 'Gmeek.py', os.environ['BLOG_TOKEN'],
         os.environ['BLOG_REPOSITORY'], '--issue_number', '0'],
        cwd=source, env=env, check=True,
    )
    docs = source / 'docs'
    blog = docs / 'blog'
    blog.mkdir()
    for item in list(docs.iterdir()):
        if item.name != 'blog':
            shutil.move(str(item), str(blog / item.name))
    shutil.copy2(workspace / 'static' / 'index.html', docs / 'index.html')

