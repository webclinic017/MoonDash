import { AbstractRouteController } from "../AbstractRouteController";
import { AbstractMongoController } from "@mongo/controller/AbstractMongoController";
import express = require("express");

export abstract class AbstractDBRouteController<
  I
> extends AbstractRouteController {
  protected mongoController: AbstractMongoController<I>;
  constructor(path: string, _mongoController: AbstractMongoController<I>) {
    super(path);
    this.mongoController = _mongoController;
  }

  public async InitializeController() {
    this.router.get(this.path, this.GetAllDocs.bind(this)).bind(this);
    this.router
      .post(this.path + "/save", this.saveDocument.bind(this))
      .bind(this);
  }

  public async GetAllDocs(req: express.Request, resp: express.Response) {
    if (req.query.id) {
      console.log("Getting Document With ID " + req.query.id + "...");
      let allDocs = await this.mongoController.getDocumentWithId(req.query.id);

      resp.send(allDocs);
    } else {
      console.log("Getting All Docs From Collection...");
      let allDocs = await this.mongoController.getAllDocs();

      resp.send(allDocs);
    }
  }

  public async saveDocument(req: express.Request, resp: express.Response) {
    let document = req.body;
    //let res = await this.mongoController.insertDocument(document);
    document = await this.formatDoc(document);
    let res = await this.mongoController.upsertDocument(document);

    resp.send(res);
  }

  public async formatDoc(doc: I) {
    return Promise.resolve(doc);
  }
}
