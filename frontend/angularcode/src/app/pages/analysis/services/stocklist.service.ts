import { Injectable, Injector } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { map, catchError } from 'rxjs/operators';

const routes = {
  securities: '/mainbase/securities',
  searchFunds: '/MFQuotes/Search',
};

@Injectable({
  providedIn: 'root',
})
export class StockListService {
  constructor(private httpClient: HttpClient) {}

  getStockList(): Observable<string> {
    return this.httpClient.get(routes.securities).pipe(
      map((body: any) => body[0].securitiesList),
      catchError(() => of('Error, could not load stocks :-('))
    );
  }
  getFundList(q: string): Observable<string> {
    return this.httpClient.get(routes.searchFunds + '?q=' + q).pipe(
      map((body: any) => body),
      catchError(() => of('Error, could not load stocks :-('))
    );
  }
}
