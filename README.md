# Анализ температурных данных и мониторинг текущей температуры через OpenWeatherMap API
[Ссылка на Streamlit приложение](https://weatherapplicationhw.streamlit.app/)
___
* В ходе выполнения домашнего задания был проведен анализ синхронных и асинхронных запросов:
  - Синхронные запросы дожидаются выполнения предыдущих (2 запроса выполнено за 0.6213209629058838)
  - Асинхронные запросы могут выполняться без ожидания (2 запроса выполнено за 0.4738776683807373)
    
  **Вывод: Асинхронные запросы работают быстрее.**  
  Это происходит из-за того, что приложению не приходится ждать завершения предыдущего запроса для начала выполнения следующего

* Также было проверено распараллеливание тяжелой функции:
  - Без распараллеливания функция выполняется за 0.047365427017211914 сек
  - С распараллеливанием с помощью modin - 0.33873558044433594 сек
  - С распараеллеливанием с помощью multiprocessing - 0.699282169342041 сек
    
  **Вывод:** Обычные операции с DataFrame без распараллеливания работают быстрее в данном случае

  [Проведенный анализ...](./weather_eda.ipynb)
