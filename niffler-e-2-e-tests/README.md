# niffler-e-2-e-tests

End-to-end tests for Niffler.

Установка и запуск (Mac OS)

Для корректного запуска требуется Java 21
установить Java 21 для текущнго терминала 

```posh
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH=$JAVA_HOME/bin:$PATH
```

Проверить что версия изменилась

```posh
java -version
```

В корне проекта (niffler-py-st3)
```posh
% bash docker-compose-dev.sh
```
Установка зависимостей Python Переход в папку с E2E тестами
```posh
cd niffler-e-2-e-tests
```
Установка зависимостей через Poetry
```posh
poetry install
```

Установка браузеров для Playwright

```posh
poetry run playwright install
```
Запуск тестов
```posh
poetry run pytest
```
Запуск с медленным выполнением для отладки
```posh
poetry run pytest --headed --slowmo 1000
```