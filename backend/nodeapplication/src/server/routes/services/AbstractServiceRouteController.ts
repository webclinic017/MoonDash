import { AbstractRouteController } from "../AbstractRouteController";
import express = require("express");

export abstract class AbstractServiceRouteController extends AbstractRouteController {
  constructor(path: string) {
    super(path);
  }

  public async InitializeController() {
    await this.InitializeGet();
    await this.InitializePost();
  }

  public async runService(
    req: express.Request,
    resp: express.Response
  ): Promise<any> {
    resp.send("runService Method for " + this.path + "does not exist !");
  }

  public async InitializeGet() {
    this.router.get(this.path, this.runService.bind(this)).bind(this);
  }

  public async InitializePost() {
    this.router.post(this.path, this.runService.bind(this)).bind(this);
  }
}
