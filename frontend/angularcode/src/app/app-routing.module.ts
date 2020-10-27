import { NgModule } from '@angular/core';
import { Routes, RouterModule, PreloadAllModules } from '@angular/router';
import { Shell } from '@app/shell/shell.service';
import { AnalysisComponent } from './pages/analysis/analysis.component';

const routes: Routes = [
  Shell.childRoutes([
    { path: 'about', loadChildren: () => import('./about/about.module').then((m) => m.AboutModule) },
    { path: 'analysis', loadChildren: () => import('./pages/analysis/analysis.module').then((m) => m.AnalysisModule) },
    { path: 'wealth', loadChildren: () => import('./pages/wealth/wealth.module').then((m) => m.WealthModule) },
  ]),

  { path: '**', redirectTo: '', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { preloadingStrategy: PreloadAllModules })],
  exports: [RouterModule],
  providers: [],
})
export class AppRoutingModule {}
