import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CurrencyService } from './services/currency.service';
import { CurrencyRate } from './models/currency.model';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html',   // <--- Zmienione na Twoją nazwę
  styleUrl: './app.css'        // <--- Zmienione na Twoją nazwę
})
export class App implements OnInit {
  currencies: CurrencyRate[] = [];
  selectedDate: string = '';
  isLoading: boolean = false;
  message: string = '';

  constructor(private currencyService: CurrencyService) {}

  ngOnInit() {
    this.loadAllCurrencies();
  }

  loadAllCurrencies() {
    this.isLoading = true;
    this.currencyService.getAllCurrencies().subscribe({
      next: (data) => {
        this.currencies = data;
        this.isLoading = false;
      },
      error: (err) => {
        this.message = 'Błąd podczas pobierania danych z bazy.';
        this.isLoading = false;
      }
    });
  }

  fetchFromNbp() {
    this.isLoading = true;
    this.message = 'Pobieranie danych z NBP...';
    this.currencyService.fetchFromNbp().subscribe({
      next: (res) => {
        this.message = `Sukces! Dodano ${res.added} nowych kursów z dnia ${res.date}.`;
        this.loadAllCurrencies();
      },
      error: (err) => {
        this.message = 'Błąd podczas łączenia z NBP.';
        this.isLoading = false;
      }
    });
  }

  filterByDate() {
    if (!this.selectedDate) {
      this.loadAllCurrencies();
      return;
    }
    this.isLoading = true;
    this.currencyService.getCurrenciesByDate(this.selectedDate).subscribe({
      next: (data) => {
        this.currencies = data;
        this.message = `Znaleziono ${data.length} kursów dla daty ${this.selectedDate}.`;
        this.isLoading = false;
      },
      error: (err) => {
        this.message = 'Błąd podczas filtrowania po dacie.';
        this.isLoading = false;
      }
    });
  }
}