# Srakoul 的博客

使用 [Gmeek v2.22](https://github.com/Meekdai/Gmeek) + GitHub Issues + GitHub Pages。

- [写文章](https://1024971823.github.io/write.html)
- [管理文章](https://github.com/1024971823/1024971823.github.io/issues?q=is%3Aissue+author%3A1024971823)
- [写作指南](https://1024971823.github.io/writing.html)
- [发布进度](https://github.com/1024971823/1024971823.github.io/actions/workflows/blog.yml)

仅发布仓库所有者创建、带 `blog` 标签且处于打开状态的 Issues。文章编辑、添加/移除标签、关闭/重开会触发全量重新生成。无需个人访问令牌或额外后端。

Pages 来源为 GitHub Actions，部署内容为生成的 `docs` artifact；根目录的旧 HTML 保留为迁移前的源码，不再作为站点发布入口。
