﻿# Codenames Captain API
Связь с API осуществляется путем обмена объектами JSON с сервером.
 ## Функционал:
Сервер отвечает на следующие запросы:
 ### 1. Семантика
 #### 1.1. /associations/\<obj>
 Пример:
 ```js
obj = {
   "words": ["сталь_NOUN"],
   "count": 10
}
 ```
 Возвращает массив из count ассоциаций к словам массива words в формате json. 
 При неправильных входных данных возвращает строку "ValueError".
 При отсутствии слова в словаре вернёт строку "VocabularyError".
 
 ### 1.2. /vectors/\<obj>
  Пример:
 ```js
obj = {
   "words": ["сталь_NOUN", "цех_NOUN"]
}
 ```
 Возвращает массив векторов в формате json.
 При неправильных входных данных возвращает строку "ValueError".
 При отсутствии элементов массива в словаре вернёт строку "VocabularyError".
  
   ### 1.3. /similarity/\<obj>
  Пример:
 ```js
obj = {
   "word1": "сталь_NOUN",
   "word2": "цех_NOUN"
}
 ```
 Возвращает косинусное расстояние между словами в формате json.
 При неправильных входных данных возвращает строку "ValueError".
 При отсутствии элементов массива в словаре вернёт строку "VocabularyError".

 ### 2. Морфология
 #### 2.1. /part_of_speech/\<obj>
  Пример:
 ```js
obj = {
   "words": ["сталь", "цех"]
}
 ```
 Возвращает массив с размеченными частями речи слов массива __words__ в формате json.
 При неправильных входных данных возвращает строку "ValueError".
 
  ### 2.2. /same_stem_russian/\<obj>
 Пример:
  ```js
obj = {
   "word1": "сталь_NOUN",
   "word2": "цех_NOUN"
}
 ```
 Возвращает вероятность того, что слова однокоренные в формате json.
 При неправильных входных данных возвращает строку "ValueError".
 Слова с омонимичными корнями будут проходить проверку аналогично однокоренным словам.
 
 ### 3. Стратегия
 #### 3.1. /make_a_move/\<obj>
  Пример:
 ```js
obj = {
   "words": {
     "red": ["сталь_NOUN"],
     "blue": [],
     "white": [],
     "black": ["цех_NOUN"]
   }
}
 ```
 Возвращает ассоциацию и число в формате json.
 При неправильных входных данных возвращает строку "ValueError".
 При отсутствии слов в словаре вернёт строку "VocabularyError".

 #### 3.2. /game_generator/
 Возвращает игровое поле в формате json.
 Все слова с игрового поля гарантированно работают с моделью w2v.

 #### 3.3. /player_simulator/\<obj>
  Пример:
 ```js
obj = {
   "words": ['среда_NOUN', 'площадь_NOUN', 'зебра_NOUN'],  
   "association": "дорога_NOUN",  
   "count": 2
}
 ```
 Возвращает наиболее вероятный ход игрока в формате json.
 При неправильных входных данных возвращает строку "ValueError".
 При отсутствии слов в словаре вернёт строку "VocabularyError".

