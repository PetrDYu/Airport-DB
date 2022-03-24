UPDATE [Модели самолётов] SET [Бортпроводники] = 10 
WHERE [Пассажиры эконом] < 300 AND [Пассажиры эконом] > 200;

SELECT COUNT() FROM 'Самолёты'
GROUP BY [Авиакомпания-владелец];

SELECT [Имя], COUNT() FROM 'Пассажиры'
WHERE [Фамилия] = 'Гарбирошвили'
GROUP BY [Имя];

UPDATE [События] SET [Бригада] = NULL WHERE [Бригада] = 'NULL';

SELECT [Бригада],COUNT() FROM [События]
WHERE [Бригада] IN (60, 61, 62, 63, 64, 65)
GROUP BY [Бригада];