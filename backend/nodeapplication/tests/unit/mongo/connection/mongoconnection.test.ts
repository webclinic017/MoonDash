require("module-alias/register");
import { expect } from "chai";
import { MongoConnection } from "@src/mongo/connection/MongoConnection";

describe("Mongo Connection Test", () => {
  it("It Should Connect to Mongo Database Successfully!", async () => {
    let ins = new MongoConnection();
    let conn = await ins.getConnection("test");

    let collection = await conn.collection("test");
    let docs = await collection.find({});
    expect(docs).to.not.be.undefined;
    docs.forEach((el) => {
      expect(el.testString).to.be.equal("Test Successful");
    });
  });
});
