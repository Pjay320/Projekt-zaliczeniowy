import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CurrencyRate } from '../models/currency.model';

@Injectable({
  providedIn: 'root'
})
export class CurrencyService {
  private apiUrl = 'http://localhost:8000/currencies';

  constructor(private http: HttpClient) { }

  fetchRange(start: string, end: string): Observable<any> {
    let params = new HttpParams().set('start_date', start).set('end_date', end);
    return this.http.post(`${this.apiUrl}/fetch/range`, {}, { params: params });
  }

  getStats(start: string, end: string): Observable<any[]> {
    let params = new HttpParams().set('start_date', start).set('end_date', end);
    return this.http.get<any[]>(`${this.apiUrl}/stats`, { params: params });
  }

  
  getRawRange(start: string, end: string): Observable<CurrencyRate[]> {
    let params = new HttpParams().set('start_date', start).set('end_date', end);
    return this.http.get<CurrencyRate[]>(this.apiUrl, { params: params });
  }
}