import { Routes, RouterModule } from '@angular/router';
import { WealthComponent } from './wealth.component';
import { extract } from '@app/i18n';
import { NgModule } from '@angular/core';
import { AssetFormComponent } from './forms/asset-form/asset-form.component';

const routes: Routes = [
  {
    path: '',
    component: WealthComponent,
    data: { title: extract('Wealth') },
    children: [
      {
        path: 'assetform',
        component: AssetFormComponent,
      },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
  providers: [],
})
export class WealthRoutingModule {}
