/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { WealthserviceService } from './wealthservice.service';

describe('Service: Wealthservice', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [WealthserviceService],
    });
  });

  it('should ...', inject([WealthserviceService], (service: WealthserviceService) => {
    expect(service).toBeTruthy();
  }));
});
