require("module-alias/register");
require("dotenv").config();
import { mkdirSync } from "fs-extra";
import { MongoConnection } from "./src/mongo/connection/MongoConnection";
import { server } from "@server/core/Server";
import { UsersModel } from "./src/mongo/models/users/UsersModel";
import { MainBase } from "@mongo/databases/MainBase";
import { MongoConnectionFactory } from "@mongo/connection/MongoConnectionFactory";
import { SecuritiesMongoController } from "@mongo/controller/securities/SecuritiesMongoController";
import { CSVToJSON } from "@utils/csvtojson/CSVToJSON";
import { ISecuritiesSchema } from "@mongo/schemas/securities/ISecuritiesSchema";
import { GenerateMongoCode } from "@src/generator/mongocode/GenerateMongoCode";
import { GenerateServiceCode } from "@src/generator/servicecode/GeneratorServiceCode";

let aps = server();
MongoConnectionFactory.initializeAllConnections();
export const apserver = aps;
// async function main() {
//   let eq = await CSVToJSON("C:\\Users\\dhair\\Downloads\\EQUITY_L.csv");
//   let securities: ISecuritiesSchema = {
//     securityType: "Stocks",
//     securitiesList: [],
//   };
//   await Promise.all(
//     eq.map(async (e: { SYMBOL: string }) => {
//       securities.securitiesList.push(e.SYMBOL);
//     })
//   );
//   let conn = await MongoConnectionFactory.getConnection({
//     dbName: MainBase.dbName,
//   });

//   // let smc = new SecuritiesMongoController()
//   // await smc.insertDocument(securities)
// }
// main();

// async function gen(){
//   // await GenerateMongoCode.codeGenAllFile()
//   await GenerateServiceCode.codeGenAllFile()
// }
// gen()
