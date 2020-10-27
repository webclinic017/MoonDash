import { Injectable } from '@angular/core';
import { NbToastrService, NbGlobalPhysicalPosition } from '@nebular/theme';
import { ToastConstants } from 'src/constants/ToastConstants';

@Injectable({
  providedIn: 'root',
})
export class ToastService {
  private index: number = 0;
  constructor(private toastrService: NbToastrService) {}

  showSuccessToast(message: any) {
    this.toastrService.show(null, message, { status: 'success', position: NbGlobalPhysicalPosition.BOTTOM_RIGHT });
  }
  showFailToast(message: any) {
    this.toastrService.show(null, message, { status: 'danger', position: NbGlobalPhysicalPosition.BOTTOM_RIGHT });
  }

  showErrorWhileSaving() {
    this.showFailToast(ToastConstants.ErrorWhileSaving);
  }
  showErrorWhileRetrieving() {
    this.showFailToast(ToastConstants.ErrorWhileRetrieving);
  }
  showErrorWhileDeleting() {
    this.showFailToast(ToastConstants.ErrorWhileDeleting);
  }
  showSuccessWhileDeleting() {
    this.showSuccessToast(ToastConstants.SuccessDeleting);
  }
  showWealthAdditionToast() {
    this.showSuccessToast(ToastConstants.WealthAddition);
  }
}
