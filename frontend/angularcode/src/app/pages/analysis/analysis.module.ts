import { NgModule, Injectable } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AnalysisComponent } from './analysis.component';
import {
  NbThemeModule,
  NbCardModule,
  NbSelectModule,
  NbListModule,
  NbOptionModule,
  NbLayoutModule,
  NbInputModule,
  NbAutocompleteModule,
  NbRadioModule,
} from '@nebular/theme';
import { TranslateModule } from '@ngx-translate/core';
import { FlexLayoutModule } from '@angular/flex-layout';
import { MaterialModule } from '@app/material.module';
import { AnalysisRoutingModule } from './analysis-routing.module';
import { OptionchainComponent } from './optionchain/optionchain.component';
import { FormsModule as ngFormsModule } from '@angular/forms';
@NgModule({
  imports: [
    NbLayoutModule,
    NbCardModule,
    NbSelectModule,
    NbInputModule,
    NbRadioModule,
    NbAutocompleteModule,
    NbOptionModule,
    CommonModule,
    TranslateModule,
    FlexLayoutModule,
    MaterialModule,
    ngFormsModule,
    AnalysisRoutingModule,
  ],
  declarations: [AnalysisComponent, OptionchainComponent],
})
export class AnalysisModule {}
