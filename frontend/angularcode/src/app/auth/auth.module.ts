import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { TranslateModule } from '@ngx-translate/core';
import { FlexLayoutModule } from '@angular/flex-layout';

import { SharedModule } from '@shared';
import { MaterialModule } from '@app/material.module';
import { I18nModule } from '@app/i18n';
import { AuthRoutingModule } from './auth-routing.module';
import { LoginComponent } from './login.component';
import {
  NbThemeModule,
  NbLayoutModule,
  NbCardModule,
  NbDialogModule,
  NbInputModule,
  NbCheckboxModule,
  NbButtonModule,
  NbSidebarModule,
} from '@nebular/theme';
import { FormsModule as ngFormsModule } from '@angular/forms';

@NgModule({
  imports: [
    NbThemeModule,
    NbLayoutModule,
    NbSidebarModule,
    NbCardModule,
    NbDialogModule,
    NbInputModule,
    NbCheckboxModule,
    NbButtonModule,
    ngFormsModule,
    CommonModule,
    ReactiveFormsModule,
    TranslateModule,
    SharedModule,
    FlexLayoutModule,
    MaterialModule,
    I18nModule,
    AuthRoutingModule,
  ],
  declarations: [LoginComponent],
})
export class AuthModule {}
