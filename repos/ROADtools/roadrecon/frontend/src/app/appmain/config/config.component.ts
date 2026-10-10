import { Component, OnInit } from '@angular/core';
import { LocalStorage } from 'ngx-webstorage';

@Component({
  selector: 'app-config',
  templateUrl: './config.component.html',
  styleUrls: ['./config.component.less']
})
export class ConfigComponent implements OnInit {
  @LocalStorage()
  public mfa;
  @LocalStorage()
  public portallinks;
  @LocalStorage()
  public paging;
  @LocalStorage()
  public blueteam;

  constructor() { }

  ngOnInit(): void {
  }

}
