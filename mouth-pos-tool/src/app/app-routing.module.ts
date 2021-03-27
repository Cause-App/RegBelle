import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { MouthToolComponent } from './pages/nose-tool/mouth-tool.component';

const routes: Routes = [
  {path: "", component: MouthToolComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
