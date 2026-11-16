# Pikumi legal & support pages

Bilingual (RU/EN) static pages for App Store publishing.

## Before publishing
1. Replace `[EMAIL]`, `[ИМЯ РАЗРАБОТЧИКА ИЛИ НАЗВАНИЕ КОМПАНИИ]`, and `[DEVELOPER LEGAL NAME]` in all HTML files.
2. Confirm privacy claims against app code and all SDKs. If analytics/ads are present, update policy sections 3–4.
3. Remove the yellow **Before publishing** notices in both languages from `privacy.html`.
4. Confirm the feature statements on the support page match the shipped app.
5. Test the support email and both languages after publishing.

## GitHub Pages
Create a public repository, upload `index.html`, `privacy.html`, `support.html` to its root. Settings → Pages → Deploy from a branch → main / (root).
URLs will be `https://USERNAME.github.io/REPOSITORY/privacy.html` and `.../support.html`.

## GitLab Pages
Create a project and upload the three HTML files plus `.gitlab-ci.yml` to the root. Check Build → Pipelines; then Deploy → Pages for your live site URL.

Note: these are drafts for a local-only app without analytics or ads. Have the final policy reviewed against actual operations and applicable law.
