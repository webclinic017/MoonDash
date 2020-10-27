/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { TotalAssetsComponent } from './total-assets.component';

describe('TotalAssetsComponent', () => {
  let component: TotalAssetsComponent;
  let fixture: ComponentFixture<TotalAssetsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [TotalAssetsComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TotalAssetsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
