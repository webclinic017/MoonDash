import { Component, OnInit, Input, ViewChild } from '@angular/core';
import { StockListService } from './services/stocklist.service';
import { finalize, map } from 'rxjs/operators';
import { Observable, of } from 'rxjs';

@Component({
  selector: 'app-analysis',
  templateUrl: './analysis.component.html',
  styleUrls: ['./analysis.component.css'],
})
export class AnalysisComponent implements OnInit {
  constructor(private stockListService: StockListService) {}

  selectedOption: any = 1;
  stocks: Array<string>;
  @Input() selectedStock: string;
  filteredOptions$: Observable<string[]>;
  isLoading = false;
  @ViewChild('autoInput') input: any;
  ngOnInit() {
    this.isLoading = true;
    this.stockListService
      .getStockList()
      .pipe(
        finalize(() => {
          this.isLoading = false;
        })
      )
      .subscribe((stocks: any) => {
        this.stocks = stocks;
      });
    this.filteredOptions$ = of(this.stocks);
  }

  getStock(stock: string) {
    this.selectedStock = stock;
  }

  onChange() {
    this.filteredOptions$ = this.getFilteredOptions(this.input.nativeElement.value);
  }

  getFilteredOptions(value: string): Observable<string[]> {
    return of(value).pipe(map((filterString) => this.filter(filterString)));
  }

  private filter(value: string): string[] {
    const filterValue = value.toLowerCase();
    return this.stocks.filter((optionValue) => optionValue.toLowerCase().includes(filterValue));
  }

  optionTypeChange($event: any) {
    console.log($event);
  }
}
