import { Component, OnInit, Inject, PLATFORM_ID, ChangeDetectorRef } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CurrencyService } from './services/currency.service';
import { CurrencyRate } from './models/currency.model';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {
  stats: any[] = [];
  currencies: CurrencyRate[] = []; 
  
  mode: string = 'month';
  year: number = new Date().getFullYear();
  quarter: string = '1';
  month: string = '01';
  startDate: string = '';
  endDate: string = '';
  
  isLoading: boolean = false;
  showRaw: boolean = false;
  hasSearched: boolean = false; 
  message: string = ''; 

  constructor(
    private currencyService: CurrencyService,
    @Inject(PLATFORM_ID) private platformId: Object,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {}

  resetInputs() {
    this.startDate = '';
    this.endDate = '';
    this.message = '';
    this.hasSearched = false;
  }

  // KLUCZOWA ZMIANA: Przycisk pobierania sam wylicza daty przed akcją
  downloadData() {
    this.calculateDates();
    if (!this.startDate || !this.endDate) return;

    this.isLoading = true;
    this.message = 'Pobieram dane z NBP...';
    
    this.currencyService.fetchRange(this.startDate, this.endDate).subscribe({
      next: (res) => {
        if (res.added > 0) {
          this.message = `Sukces! Dodano ${res.added} rekordów. Ładuję zestawienie...`;
        } else {
          this.message = "Brak nowych danych do pobrania w tym zakresie.";
        }
        this.loadData(); 
      },
      error: () => {
        this.message = "Błąd komunikacji z serwerem NBP lub brak publikacji w te dni.";
        this.isLoading = false;
        this.cdr.detectChanges();
      }
    });
  }

  prepareAndLoad() {
    this.calculateDates();
    this.loadData();
  }

  calculateDates() {
    switch(this.mode) {
      case 'day': 
        this.endDate = this.startDate; 
        break;
      case 'year': 
        this.startDate = `${this.year}-01-01`; 
        this.endDate = `${this.year}-12-31`; 
        break;
      case 'month': 
        const yearNum = parseInt(this.year.toString());
        const monthNum = parseInt(this.month);
        const lastDay = new Date(yearNum, monthNum, 0).getDate(); 
        this.startDate = `${this.year}-${this.month}-01`; 
        this.endDate = `${this.year}-${this.month}-${lastDay}`; 
        break;
      case 'quarter':
        const starts = ['01-01', '04-01', '07-01', '10-01'];
        const ends = ['03-31', '06-30', '09-30', '12-31'];
        this.startDate = `${this.year}-${starts[parseInt(this.quarter)-1]}`;
        this.endDate = `${this.year}-${ends[parseInt(this.quarter)-1]}`;
        break;
    }
  }

  loadData() {
    if (!this.startDate || !this.endDate) {
      this.message = "Wybierz zakres dat przed wyświetleniem danych!";
      this.cdr.detectChanges();
      return; 
    }

    this.isLoading = true;
    this.hasSearched = true;
    
    this.currencyService.getStats(this.startDate, this.endDate).subscribe(data => {
      this.stats = data;
      this.isLoading = false;
      this.cdr.detectChanges();
    });
    
    this.currencyService.getRawRange(this.startDate, this.endDate).subscribe(data => {
      this.currencies = data;
      this.cdr.detectChanges();
    });
  }
}