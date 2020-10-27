/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { MfListComponent } from './mf-list.component';

describe('MfListComponent', () => {
  let component: MfListComponent;
  let fixture: ComponentFixture<MfListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [MfListComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MfListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
