import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CredentialsService } from '@app/auth';
import { BehaviorSubject } from 'rxjs';

const routes = {
  nseIndexOptionChain: '/nsequotes/optionchain?symbol=',
  nseEquityOptionChain: '/nsequotes/optionchain?symbol=',
  nseIndexInfo: 'https://www.nseindia.com/api/allIndices',
};

@Injectable({
  providedIn: 'root',
})
export class OptionDataService {
  constructor(private httpClient: HttpClient, private credentialsService: CredentialsService) {}

  callback: any = {};
  // private messageSource = new BehaviorSubject<any>({});
  // currentMessage = this.messageSource.asObservable();

  get username(): string | null {
    const credentials = this.credentialsService.credentials;
    return credentials ? credentials.username : null;
  }

  getNSEIndexOptionQuotes(symbol: string) {
    return this.httpClient.get(routes.nseIndexOptionChain + symbol).toPromise();
  }

  getNSEAllIndices(symbol: string) {
    return this.httpClient.get(routes.nseIndexInfo).toPromise();
  }
}
