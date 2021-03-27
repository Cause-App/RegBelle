import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MouthToolComponent } from './mouth-tool.component';

describe('NoseToolComponent', () => {
  let component: MouthToolComponent;
  let fixture: ComponentFixture<MouthToolComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MouthToolComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MouthToolComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
