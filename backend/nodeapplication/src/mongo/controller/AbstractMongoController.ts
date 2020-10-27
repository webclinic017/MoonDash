import { Model, Schema, Document } from "mongoose";

export abstract class AbstractMongoController<I> {
  protected _schema: Schema;
  protected _model: Model<Document, {}>;
  protected idProperty: string = "";
  constructor(schema: Schema, model: Model<Document, {}>) {
    this._schema = schema;
    this._model = model;
  }

  public async insertDocument(document: I) {
    let doc = new this._model(document);

    let _id = this.getId(document);
    if (_id) {
      doc._id = _id;
    }

    try {
      console.log("Saving Document to Mongo ...");
      let savedDoc = await doc.save();
      console.log("Document Saved with ID -" + savedDoc.id);
      return Promise.resolve({ id: savedDoc.id });
    } catch (e) {
      throw new Error("Could Not Save Document to DB " + e);
    }
  }

  public async upsertDocument(document: any) {
    let _id = this.getId(document);
    if (_id) {
      document._id = _id;
    }
    //let doc = new this._model(document);

    try {
      console.log("Saving Document to Mongo ...");
      let savedDoc = await this._model.findOneAndUpdate(
        { _id: _id },
        document,
        {
          upsert: true,
        }
      );

      console.log("Document Saved with ID -" + _id);
      return Promise.resolve({ id: _id });
    } catch (e) {
      throw new Error("Could Not Save Document to DB " + e);
    }
  }

  public async getAllDocs(): Promise<Array<I>> {
    let docs = await this._model.find({});
    return Promise.resolve((docs as any) as Array<I>);
  }

  public async getDocumentWithId(id: any): Promise<Array<I>> {
    let docs = await this._model.find({ _id: id });
    return Promise.resolve((docs as any) as Array<I>);
  }

  public getId(doc: any) {
    return doc[this.idProperty];
  }
}
