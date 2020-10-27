/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { OptionchainComponent } from './optionchain.component';

describe('OptionchainComponent', () => {
  let component: OptionchainComponent;
  let fixture: ComponentFixture<OptionchainComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [OptionchainComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OptionchainComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
