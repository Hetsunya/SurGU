import matplotlib.pyplot as plt

# Данные для примера, ваши реальные данные будут отличаться
years = [1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009]
drownings = [109, 102, 98, 85, 95, 96, 98, 123, 94, 102, 103]  # Количество утонувших
films = [2, 2, 2, 3, 1, 1, 2, 3, 4, 1, 4]  # Количество фильмов с Николасом Кейджем

fig, ax1 = plt.subplots()

color = 'red'
ax1.set_xlabel('Год')
ax1.set_ylabel('Количество утонувших', color=color)
ax1.plot(years, drownings, color=color, marker='o')
ax1.tick_params(axis='y', labelcolor=color)


ax2 = ax1.twinx()  # Создаем вторую ось Y
color = 'yellow'
ax2.set_ylabel('Количество фильмов', color=color) 
ax2.plot(years, films, color=color, marker='o')
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # Для того, чтобы подписи не перекрывались
plt.title('Ложная корреляция между утонувшими и фильмами с Николасом Кейджем')
plt.show()
