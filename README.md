# bcomp-decoder
Расшифровщик команд БЭВМ. Переводит код команды в мнемонику, наименование и комментарий (информация из презентации).

Ошибки не обрабатываются. Каждая строка должна содержать ТОЛЬКО четырехзначное шестнадцатеричное число. 

Каждое такое число программа распознает как команду, а не данные (переменные и тд).

Команды ввода-вывода не поддерживаются.

Стек/подпрограммы/прерывание не поддерживаются.