# Основания рекомендаций

Официальные источники Figma прочитаны 2026-11-15. Они описывают возможности и рекомендуемые приёмы; конкретная декомпозиция, имена страниц и критерии читаемости остаются соглашением проекта. Для спорного или зависящего от версии поведения открывай актуальную первичную документацию.

| Источник и раздел | Что подтверждает |
|---|---|
| [Create and manage pages](https://help.figma.com/hc/en-us/articles/360038511293-Create-and-manage-pages), введение и View pages | Страницы как уровень организации; разделение по этапам, сценариям, компонентам и стилям |
| [Organize your canvas with sections](https://help.figma.com/hc/en-us/articles/9771500257687-Organize-your-canvas-with-sections), введение и Create a section | Смысловые группы, навигация и ссылки; допустимая вложенность секций |
| [Optimize design files for developer handoff](https://help.figma.com/hc/en-us/articles/360040521453-Optimize-design-files-for-developer-handoff), Set up files for Collaboration | Описательные названия, секции, каталог компонентов и обозначение готовности |
| [Name and organize components](https://help.figma.com/hc/en-us/articles/360038663994-Name-and-organize-components), Component organization / Organize components by name | Согласованный словарь, группировка имён через `/`, связь структуры файла и каталога ресурсов |
| [Guide to components in Figma](https://help.figma.com/hc/en-us/articles/360038662654-Guide-to-components-in-Figma), Overview | Основной компонент и связанные экземпляры; локальные компоненты и библиотеки между файлами |
| [Create and use variants](https://help.figma.com/hc/en-us/articles/360056440594-Create-and-use-variants), Variant properties and values | Родственные состояния и размеры, свойства вариантов; граница группировки разных иконок |
| [Apply changes to instances](https://help.figma.com/hc/en-us/articles/360039150733-Apply-changes-to-instances), Supported properties / Change preservation | Допустимые переопределения; зависимость их сохранения от имён, свойств и иерархии при замене |
| [Guide to auto layout](https://help.figma.com/hc/en-us/articles/360040451373-Guide-to-auto-layout-in-Figma), введение / Ignore auto layout / Nest auto layout frames | Компоновка связанных элементов, реакция на контент, обоснованное абсолютное позиционирование |
| [Guide to styles](https://help.figma.com/hc/en-us/articles/360039238753-Guide-to-styles-in-Figma), введение и Text styles | Общие наборы свойств и их применение к слоям и фрагментам текста |
| [The difference between variables and styles](https://help.figma.com/hc/en-us/articles/15871097384471-The-difference-between-variables-and-styles), Foundational differences | Различие набора свойств стиля, отдельного значения переменной и режима |
| [Modes for variables](https://help.figma.com/hc/en-us/articles/15343816063383-Modes-for-variables/), Set to auto mode | Наследование режима от родителя и переход к режиму коллекции по умолчанию |
| [Plugin API: id](https://developers.figma.com/docs/plugins/api/properties/nodes-id/), Signature / Remarks | Уникальный неизменяемый ID узла, поиск по нему и представление ID в ссылках |
| [Guide to prototyping](https://help.figma.com/hc/en-us/articles/360040314193-Guide-to-prototyping-in-Figma), Flows and starting points | Поток как сеть фреймов одной страницы; точки входа и связи |
| [Change the background color of the canvas](https://help.figma.com/hc/en-us/articles/360041064814-Change-the-background-color-of-the-canvas), основная инструкция | Настраиваемый фон холста; его отличие от содержимого экранов |

## Организационные соглашения скилла

Декомпозиция по самостоятельно понимаемой и принимаемой функции — инженерный критерий этого скилла. Документация Figma предоставляет страницы, секции и связи, но не предписывает указанную предметную классификацию.

Порядок страниц, числовые префиксы, название «Обзор», выбранный фон образцов и интервалы между экранами адаптируй к проекту. Отдельный библиотечный файл, архивная страница и заданное число слоёв не являются универсальными требованиями.

Сохранение опорных ID, проверка переопределений, режимов и переходов — процедура контроля последствий реорганизации, выведенная из документированных механизмов. Ссылки выше не гарантируют сохранение любой связи при произвольном переносе: результат подтверждай в затронутой области.

Файлы конкретных проектов, их названия, идентификаторы, снимки и данные в состав скилла не входят.
