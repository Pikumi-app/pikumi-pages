# Публичные страницы Pikumi

Статус: тексты повторно вычитаны для версии **без рекламы**. Дата редакции: 2026-11-17. Обновлённый архив для GitHub Pages загружает пользователь.

Разработчик: Nikita Novikov. Название: Pikumi. Контакт: mobilesupportforeveryone@gmail.com. Письма и вложения поддержки удаляются после решения вопроса — по подтверждённому правилу разработчика.

## Открыть и проверить

Откройте `index.html`, `privacy.html` или `support.html` в Safari. Сервер, JavaScript, сборка и доступ к интернету для самих страниц не нужны. Отдельные ссылки на Apple и отправку почты требуют соответствующего подключения/почтового приложения.

| Язык | Главная | Политика | Поддержка |
| --- | --- | --- | --- |
| English | [index.html](index.html) | [privacy.html](privacy.html) | [support.html](support.html) |
| Русский | [ru/index.html](ru/index.html) | [ru/privacy.html](ru/privacy.html) | [ru/support.html](ru/support.html) |
| Français | [fr/index.html](fr/index.html) | [fr/privacy.html](fr/privacy.html) | [fr/support.html](fr/support.html) |
| Español | [es/index.html](es/index.html) | [es/privacy.html](es/privacy.html) | [es/support.html](es/support.html) |
| 简体中文 | [zh-Hans/index.html](zh-Hans/index.html) | [zh-Hans/privacy.html](zh-Hans/privacy.html) | [zh-Hans/support.html](zh-Hans/support.html) |

Английский — основной язык корневых адресов. Ссылки выбора языка открывают тот же документ на выбранном языке. Общий `styles.css` должен оставаться рядом с корневыми страницами. Все внутренние адреса относительные: сайт работает и в корне домена, и в подкаталоге, и через `file://`.

## Редактирование и архив

Полные тексты переводов находятся в `src/content.json`; контактные сведения и подтверждённые условия — в `src/site.json`. После изменения данных нужно синхронно обновить соответствующие тексты всех языков и дату политики. Перегенерируйте готовые HTML стандартным Python 3.12+ (без установки библиотек):

```sh
python3 pikumi-pages/build.py
python3 pikumi-pages/build.py --output /tmp/PikumiPagesRevised --zip /tmp/pikumi-pages-revised.zip
python3 scripts/check-public-pages.py /tmp/PikumiPagesRevised
```

Архив содержит ровно 15 HTML и `styles.css`. Исходники генератора, README, CI, содержимое iOS-проекта и локальные настройки в публичный архив не входят. Загружайте **содержимое** архива с сохранением папок языков в выбранный каталог статического хостинга. Никакие перенаправления или настройка маршрутизации не требуются.

Сайт пользователя размещён на [GitHub Pages](https://pikumi-app.github.io/pikumi-pages/). Адреса для App Store Connect: [политика](https://pikumi-app.github.io/pikumi-pages/privacy.html) и [поддержка](https://pikumi-app.github.io/pikumi-pages/support.html). Замените содержимое репозитория `Pikumi-app/pikumi-pages` файлами из нового архива с сохранением папок языков. После обновления проверьте страницы без входа в аккаунт. Ссылка в приложении находится в меню → помощь → политика конфиденциальности и ведёт на указанный HTTPS-адрес. Доставку почты проверьте обычным письмом на указанный адрес; инструмент проверки HTML сам письма не отправляет.

## Необязательный GitLab Pages

В `.gitlab-ci.yml` подготовлен job для статических файлов. В отдельном репозитории сайта поместите его и содержимое `pikumi-pages/` в корень. Для текущего репозитория подключите файл из корневой CI-конфигурации. Job сам определяет расположение HTML, копирует только публичные файлы и запускается на default branch. Он не загружает iOS-исходники и `src/` в Pages.

Конфигурация соответствует [GitLab Pages](https://docs.gitlab.com/user/project/pages/), но удалённый pipeline не запускался. Пользователь самостоятельно обновляет GitHub Pages. Этот необязательный GitLab job не запускается при слиянии приложения.

## Область действия

Политика относится к `SwipeToCleanNoAds`: Google AdMob и UMP исключены из этой схемы. Её нельзя использовать для рекламной схемы без изменения описания обработки данных. Текст сверён с PhotoKitLibrary, PhotoVideoRequest, FileProgressStore, CleaningProgress и AppComposition; работа iCloud и «Недавно удалённых» сверена с [Apple](https://support.apple.com/104967). [Журнал задачи](../docs/journal/2026-11-17-public-pages.md).
