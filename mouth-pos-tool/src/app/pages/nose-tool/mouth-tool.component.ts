import { Component, OnInit } from '@angular/core';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';

type imageType = "body" | "mouth";

@Component({
  selector: 'app-mouth-tool',
  templateUrl: './mouth-tool.component.html',
  styleUrls: ['./mouth-tool.component.scss']
})
export class MouthToolComponent implements OnInit {

  constructor(private sanitization: DomSanitizer) { }

  bodyImage: SafeUrl = "";
  mouthImage: SafeUrl = "";

  x: number = 0.5;
  y: number = 0.5;

  ngOnInit(): void {
  }

  onFileUploaded(type: imageType, event: Event) {
    const fileList = (event.target as HTMLInputElement).files;
    if (fileList) {
      const file = fileList[0];

      const reader = new FileReader();

      reader.onload = () => {
        if (type === "body") {
          this.bodyImage = this.sanitization.bypassSecurityTrustUrl(reader.result as string);
        } else {
          this.mouthImage = this.sanitization.bypassSecurityTrustUrl(reader.result as string);
        }
      }

      reader.readAsDataURL(file);
    }
  }

  getMouthStyle(): any {
    return {
      "top": ""+(this.y*100)+"%",
      "left": ""+(this.x*100)+"%"
    }
  }

}
