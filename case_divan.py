import requests
import csv
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

BASE_URL = "https://www.divan.ru/category/divany/page-"
OUTPUT_FILE = "divan_prices.csv"

def get_price(price_tag):
    """Обрабатывает цену: убирает символ рубля и пробелы, преобразует в int."""
    price_text = price_tag.text.replace("руб.", "").replace(" ", "").strip()
    return int(price_text)

def scrape_page(page_number):
    """Парсит страницу и возвращает список цен."""
    url = f"{BASE_URL}{page_number}"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

    if response.status_code != 200:
        print(f"Ошибка при загрузке страницы {page_number}: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    prices = []

    for price_tag in soup.find_all("span", class_="ui-LD-ZU"):
        try:
            price = get_price(price_tag)
            prices.append(price)
        except ValueError:
            continue

    return prices

def read_prices(filename):
    """Читает цены из CSV-файла и возвращает список."""
    prices = []
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # Пропускаем заголовок
        for row in reader:
            try:
                prices.append(int(row[0]))
            except ValueError:
                continue
    return prices

def plot_histogram(prices):
    """Рисует гистограмму цен."""
    plt.figure(figsize=(10, 5))
    plt.hist(prices, bins=20, edgecolor="black", alpha=0.7)
    plt.xlabel("Цена (руб.)")
    plt.ylabel("Количество диванов")
    plt.title("Распределение цен на диваны")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()

def main():
    """Парсит цены и сохраняет их в CSV после каждой страницы."""
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Цена"])  # Записываем заголовок CSV

        for page in range(1, 68):  # 67 страниц включительно
            print(f"Парсим страницу {page}...")
            prices = scrape_page(page)
            for price in prices:
                writer.writerow([price])  # Сохраняем цены в файл сразу

    print(f"Готово! Цены сохранены в {OUTPUT_FILE}")

    # Анализируем данные после парсинга
    prices = read_prices(OUTPUT_FILE)

    if not prices:
        print("Файл пуст или содержит некорректные данные.")
        return

    avg_price = sum(prices) / len(prices)
    print(f"Средняя цена дивана: {round(avg_price)} руб.")

    plot_histogram(prices)

if __name__ == "__main__":
    main()

