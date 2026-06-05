Dashboard Kursów NBP - Projekt Zaliczeniowy
W pełni skonteneryzowana aplikacja webowa, umożliwiająca pobieranie, archiwizację oraz analizę historycznych kursów walut z publicznego API Narodowego Banku Polskiego.

Projekt został zrealizowany w ramach zaliczenia przedmiotu na uczelni WSB Merito. Zbudowany w oparciu o architekturę trójwarstwową z wykorzystaniem wzorca Dependency Injection oraz metodyki testowania BDD (Behavior-Driven Development).

Technologie i Narzędzia
Aplikacja składa się z trzech odseparowanych modułów:

Frontend: Angular 17+, TypeScript, HTML/CSS

Backend: Python, FastAPI, SQLAlchemy (ORM)

Baza danych: PostgreSQL

Infrastruktura: Docker, Docker Compose

Testowanie: Pytest (Backend), Jasmine & Karma (Frontend)

Funkcjonalności
Integracja z API NBP: Zautomatyzowane pobieranie średnich kursów walut dla dowolnie zdefiniowanego zakresu dat.

Baza danych: Weryfikacja duplikatów i bezpieczny, trwały zapis pobranych kursów w relacyjnej bazie danych.

Analiza i filtrowanie: Możliwość przeglądania uśrednionych kursów z podziałem na:

Lata

Kwartały

Miesiące

Dni

Responsywny interfejs: Czytelne tabele z dynamicznym wyliczaniem średnich dla wybranych okresów.

Uruchomienie projektu
Cały system uruchamiany jest za pomocą środowiska Docker. Nie wymaga instalacji lokalnych zależności (poza Dockerem i ewentualnie Node.js do testów frontendu).

Wymagania wstępne
Zainstalowany Docker Desktop

Wolne porty na maszynie hosta: 4200 (Angular), 8000 (FastAPI), 5432 (PostgreSQL)

Instrukcja
Sklonuj repozytorium na swój dysk lokalny.

Otwórz terminal w głównym katalogu projektu.

Zbuduj i uruchom kontenery poleceniem:

docker-compose up -d --build
Aplikacja będzie dostępna pod adresami:

Frontend (Aplikacja UI): http://localhost:4200

Backend (Swagger API Docs): http://localhost:8000/docs

Aby zatrzymać aplikację, użyj polecenia:

docker-compose down

Uruchamianie testów
Projekt posiada 100% pokrycia dla wymaganych ścieżek testowych.

1. Testy Backendu (Pytest)
Testy weryfikujące połączenie z bazą danych oraz poprawność endpointów API. Uruchamiane bezpośrednio wewnątrz działającego kontenera Dockera.

Upewnij się, że kontenery są uruchomione, a następnie wpisz:
docker exec -it nbp_backend pytest
2. Testy Frontendu (Jasmine/Karma)
Testy weryfikujące logikę komponentów Angulara, renderowanie tabeli oraz wstrzykiwanie zależności. Wymagają lokalnego środowiska Node.js.


Wejdź do folderu frontendu
cd frontend

Pobierz paczki (tylko za pierwszym razem)
npm install

Uruchom testy z wykorzystaniem lokalnego Angular CLI
npx ng test

Autor
Paweł Piotr Szafrański Uniwersytet WSB Merito Chorzów Katowice
