import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { WealthComponent } from './wealth.component';
import { TranslateModule } from '@ngx-translate/core';
import { FlexLayoutModule } from '@angular/flex-layout';
import { MaterialModule } from '@app/material.module';
import { WealthRoutingModule } from './wealth.routing';
import {
  NbLayoutModule,
  NbCardModule,
  NbTabsetModule,
  NbButtonModule,
  NbDialogModule,
  NbTabsetComponent,
  NbInputModule,
  NbPopoverModule,
  NbSelectModule,
  NbTooltipModule,
  NbWindowModule,
  NbRouteTabsetModule,
  NbActionsModule,
  NbUserModule,
  NbCheckboxModule,
  NbRadioModule,
  NbDatepickerModule,
  NbIconModule,
  NbThemeModule,
  NbFormFieldModule,
  NbListModule,
  NbToastrModule,
  NbAutocompleteModule,
  NbOptionModule,
} from '@nebular/theme';
import { AssetFormComponent } from './forms/asset-form/asset-form.component';
import { FormsModule as ngFormsModule } from '@angular/forms';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { FixedincomeListComponent } from './lists/fixedincome-list/fixedincome-list.component';
import { StockListComponent } from './lists/stock-list/stock-list.component';
import { TotalAssetsComponent } from './lists/totalassets/total-assets/total-assets.component';
import { MfListComponent } from './lists/mf-list/mf-list.component';

@NgModule({
  imports: [
    NbThemeModule,
    NbListModule,
    NbActionsModule,
    NbUserModule,
    NbCheckboxModule,
    NbRadioModule,
    NbDatepickerModule,
    NbIconModule,
    ngFormsModule,
    CommonModule,
    TranslateModule,
    FlexLayoutModule,
    MaterialModule,
    WealthRoutingModule,
    NbTabsetModule,
    NbButtonModule,
    NbLayoutModule,
    NbCardModule,
    NbDialogModule,
    NbInputModule,
    FontAwesomeModule,
    NbIconModule,
    NbFormFieldModule,
    NbPopoverModule,
    NbSelectModule,
    NbTooltipModule,
    NbDialogModule.forChild(),
    NbWindowModule.forChild(),
    NbRouteTabsetModule,
    NbAutocompleteModule,
    NbOptionModule,
    NbToastrModule.forRoot(),
  ],
  declarations: [
    WealthComponent,
    AssetFormComponent,
    FixedincomeListComponent,
    StockListComponent,
    TotalAssetsComponent,
    MfListComponent,
  ],
  entryComponents: [AssetFormComponent],
})
export class WealthModule {}
