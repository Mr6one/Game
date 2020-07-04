Игра, созданная в рамках курса "Технологии программирования". By me and Alexey Strashnov.

Вместе с паттернами реализован графический интерфейс.

В начале вам дается одно здание, которое может создавать рабочих (оно основное, и задача противника - разрушить его). Кроме того, дается 5 рабочих. Их главная задача - добыча ресурсов. На карте расположены 3 типа ресурсов:
овцы для добычи еды, деревья - для дерева, шахты - для золота. Для их добычи необходимо поставить юнита на соответствующий ресурс. Ресурсов неограничено, каждые 2 секунды каждый юнит добывает +10 золота, +20 дерева и +15 еды.
Количесво добываемых ресурсов возрастает пропорционально количеству юнитов, которые этот ресурс добывают. Справа находится меню для постройки зданий. На каждом здании написано количество русурсов для его постройки (сверху вниз:
количество зотота, дерева, еды). Юниты могут создаваться 1-м (баррак), 3-м (ратуша) и 6-м (стрельбище) зданиями в меню. Меню можно прокручивать. Снятие выделения с меню осуществляется нажатием левой кнопкой мыши. Решена проблема коллизии: здания и юниты при 
создании не накладываются друг на друга.

После постройки здания внизу появится меню с доступными для покупки юнитами и полоска здоровья наверху. Сверху юнитов прописаны их 
стоимости: количество золота, дерева и еды, необходимых для их создания (слева направо). Слева от юнитов прописаны их характеристики: здоровье, сила и скорость (сверху вниз). Для создания нужного юнита просто выбираете его 
в панели. Остальные здания здания ничего не делают (не хватило времени, но общая идея понятна, добавить им функциональность - вопрос времени). Реализовано перемещение юнитов. Для передвижения юнитов по полю необходимо нажать 
на левую кнопку мыши, после чего переместить мышку в произвольное место экрана и отпустить кнопку. Тем самым будут выделены все юниты, оказавшиеся внутри появившегося прямоугольника. После этого правой кнопкой мыши нужно указать на поле точку, в которую необходимо переместить юниты. Можно осуществлять передвижение камеры по игровому полю (стрелочками на клавиатуре).

Вы играете против бота, которые создает свою колонию в противоположном углу (вначале вы находитесь в в верхнем левом углу). Периодически бот посылает волны своих отрядов для разрушения ваших зданий. Также он периодически создаёт здания на своей территории. Ставить здания на территории врага нельзя, граница обозначена белой линией. Цель игры - разрушить основное здание врага. Если их несколько, то все.

В программе используется фабричный метод для создания юнитов. Фабричный метод для заданий не был реализован, поскольку он вырождается в обычный конструктор ("фабрика" задний не нуждается в дополнительных методах).
Выделение и перемещение юнитов реализовано при помощи компоновщика. Выделеные юниты образуют отряд, для которого можно задать цель и организовать перемещение.
Классы игрового мира и меню реализованы на основе фасада. Они объединяют и используют множество других объектов. В частности, чтобы обновить игровой мир (переместить юнитов, атаковать других юнитов, обновить ресурсы) используетсяметод класса World update
Также в программе используется паттерн Команда. Когда пользователь щёлкает кнопкой мыши или нажимает на клавишу клавиатуры, вызывается метод объекта конкретной команды, который делегирует выполнение объектам классов World и Menu.
При помощи паттерна Наблюдатель реализовано взаимодействие между панелью ресурсов и ресурсмим игрока (ResourceMenu и Resources соответственно).

Следите за обновлениями:)

*При запуске второго и третьего стресс-тестов запускается черное окно pygame. Такой костыль нужен для корректной работы необходимых для тестирования функций. Без этого
программа выдаст ошибку.

