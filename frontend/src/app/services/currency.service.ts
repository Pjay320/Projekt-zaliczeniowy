import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CurrencyRate } from '../models/currency.model';

@Injectable({
  providedIn: 'root'
})
export class CurrencyService {
  // Adres Twojego backendu FastAPI
  private apiUrl = 'http://localhost:8000/currencies';

  constructor(private http: HttpClient) { }

  // 1. Endpoint do pobierania nowych danych z NBP i zapisu w bazie
  fetchFromNbp(): Observable<any> {
    return this.http.post(`${this.apiUrl}/fetch`, {});
  }

  // 2. Endpoint do pobierania wszystkich walut z bazy
  getAllCurrencies(): Observable<CurrencyRate[]> {
    return this.http.get<CurrencyRate[]>(this.apiUrl);
  }

  // 3. Endpoint do pobierania walut z konkretnego dnia
  getCurrenciesByDate(date: string): Observable<CurrencyRate[]> {
    return this.http.get<CurrencyRate[]>(`${this.apiUrl}/${date}`);
  }
}