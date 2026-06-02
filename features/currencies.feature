Feature: Obsługa kursów walut NBP
  Jako użytkownik aplikacji
  Chcę mieć możliwość pobierania i przeglądania kursów walut z podziałem na daty
  Aby móc analizować średnie wartości w wybranych okresach

  Scenario: Pobieranie danych dla konkretnego zakresu dat
    Given użytkownik znajduje się na głównym dashboardzie
    When użytkownik wybiera okres od "2026-05-01" do "2026-05-31"
    And klika przycisk "Pobierz z NBP i pokaż"
    Then system pobiera brakujące kursy z API NBP
    And zapisuje je w bazie danych PostgreSQL
    And wyświetla komunikat o sukcesie pobierania

  Scenario: Wyświetlanie danych w tabeli statystyk
    Given baza danych zawiera pobrane kursy walut
    When użytkownik wybiera tryb filtrowania "Miesiąc"
    And klika przycisk służący do wyświetlania średnich
    Then aplikacja wylicza średni kurs dla każdej waluty
    And tabela zostaje zaktualizowana o nowe wiersze z nazwami walut i wyliczoną średnią