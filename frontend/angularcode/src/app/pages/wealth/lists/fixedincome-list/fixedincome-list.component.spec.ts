/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { FixedincomeListComponent } from './fixedincome-list.component';

describe('FixedincomeListComponent', () => {
  let component: FixedincomeListComponent;
  let fixture: ComponentFixture<FixedincomeListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [FixedincomeListComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FixedincomeListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
