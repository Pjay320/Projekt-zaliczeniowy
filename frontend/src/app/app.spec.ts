import { ComponentFixture, TestBed } from '@angular/core/testing';
import { App } from './app';
import { CurrencyService } from './services/currency.service';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { FormsModule } from '@angular/forms';
import { By } from '@angular/platform-browser';

describe('App Component - Wymagania Zaliczeniowe', () => {
  let component: App;
  let fixture: ComponentFixture<App>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [App, HttpClientTestingModule, FormsModule],
      providers: [CurrencyService]
    }).compileComponents();

    fixture = TestBed.createComponent(App);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('powinien wywołać funkcję downloadData() po kliknięciu "Pobierz z NBP i pokaż"', () => {
  
    let isCalled = false;
    
  
    component.downloadData = () => { isCalled = true; };
    
  
    const button = fixture.debugElement.query(By.css('.btn-secondary')).nativeElement;
    button.click();
    

    expect(isCalled).toBe(true);
  });


  it('powinien wyświetlić dane w tabeli, gdy tablica stats nie jest pusta', () => {
  
    component.stats = [
      { code: 'USD', name: 'dolar amerykański', avg: 4.05 }
    ];
    

    fixture.detectChanges();

    
    const tableRows = fixture.debugElement.queryAll(By.css('table tbody tr'));
    expect(tableRows.length).toBe(1);
    
    
    expect(tableRows[0].nativeElement.textContent).toContain('USD');
  });
});