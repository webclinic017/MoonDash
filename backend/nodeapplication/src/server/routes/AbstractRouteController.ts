import express = require("express");
import * as ServerConfig from "@configs/ServerConfig.json";

export abstract class AbstractRouteController {
  router = express.Router();
  path!: string;
  link: string;
  serverLink: string;
  constructor(_path: string) {
    let host = ServerConfig.host;
    let port = ServerConfig.port;

    this.path = _path;
    this.serverLink = "http://" + host + ":" + port.toString();
    this.link = "http://" + host + ":" + port.toString() + this.path;

    console.log(this.link);
    this.InitializeController();
  }

  public async InitializeController() {
    throw new Error("Controller Initializing Code Pending for " + this.path);
  }
}
