import { MongoFileLocations } from "./MongoFileLocations";
import {
  readdirSync,
  readFileSync,
  writeFileSync,
  mkdirSync,
  existsSync,
} from "fs-extra";
import Mustache from "mustache";
import _ from "lodash";

export class GenerateMongoCode {
  static async listModels() {
    let folder = MongoFileLocations.MongoModelSource;
    let files = readdirSync(folder);
    files = files.map((f) => folder + f);
    return Promise.resolve(files);
  }

  static async getObjFromFile(file: string) {
    let fileContent = readFileSync(file, "utf8");
    let x = require(file);
    console.log(fileContent);
    return Promise.resolve(x);
  }

  static async generateCompleteModel(o: any) {
    let model = {
      SchemaName: o.Collection.charAt(0).toUpperCase() + o.Collection.slice(1),
      SchemaNameSmall: o.Collection.toLowerCase(),
      DBName: o.DBName,
    };

    return Promise.resolve(model);
  }

  static async codeGenAllFile() {
    let files = await this.listModels();
    // let collectionMap = new Map<string,string>()
    let dbMap = new Map<string, Map<string, string>>();

    await Promise.all(
      files.map(async (file) => {
        let o = await this.getObjFromFile(file);
        let model = await this.generateCompleteModel(o);
        let collectionMap = new Map<string, string>();
        collectionMap.set(model.SchemaName, model.SchemaName);

        if (dbMap.has(model.DBName)) {
          let cMap = dbMap.get(model.DBName);
          if (cMap) {
            collectionMap = cMap;
            collectionMap.set(model.SchemaName, model.SchemaName);
          }
        }

        dbMap.set(model.DBName, collectionMap);
        await this.generateOtherFiles(model);
      })
    );

    let dbNames = Array.from(dbMap.keys());

    await this.generateDBFiles(dbMap);
    await this.generateDBListFile(dbNames);

    console.log(dbMap);
  }

  static async generateOtherFiles(model: any) {
    let x = [];
    x.push(MongoFileLocations.SchemaMustache);
    x.push(MongoFileLocations.SchemaInterfaceMustache);
    x.push(MongoFileLocations.MongooseModelMustache);
    x.push(MongoFileLocations.MongoControllerMustache);
    x.push(MongoFileLocations.DBRouteControllerMustache);

    await Promise.all(
      x.map((f) => {
        let mustacheLoc = MongoFileLocations.MongoCodeMustaches + f;
        let mustache = readFileSync(mustacheLoc, "utf8");

        let k = f.replace(".mustache", "SaveLoc");
        let svLocRaw = _.get(MongoFileLocations, k);
        let svLoc = Mustache.render(svLocRaw, model);
        let dir = svLoc.replace(/\/\w+\.ts/, "");

        let save_ = true;
        if (existsSync(svLoc)) {
          let existingFile = readFileSync(svLoc, "utf8");

          if (/^(\/\/Modified)/.exec(existingFile)) {
            save_ = false;
          }
        }

        if (save_) {
          let r = Mustache.render(mustache, model);
          r = "//Generated \n" + r;
          mkdirSync(dir, { recursive: true });
          writeFileSync(svLoc, r, "utf8");
          console.log(svLoc);
        }
      })
    );
  }

  static async generateDBListFile(dbNames: Array<string>) {
    let dbModel = {
      DBNames: dbNames.map((d) => Object({ DB: d })),
    };

    let dbs = Mustache.render(
      readFileSync(
        MongoFileLocations.MongoCodeMustaches +
          MongoFileLocations.DatabaseListMustache,
        "utf8"
      ),
      dbModel
    );

    writeFileSync(MongoFileLocations.DatabaseListSaveLoc, dbs, "utf8");
  }

  static async generateDBFiles(dbMap: Map<string, Map<string, string>>) {
    await Promise.all(
      Array.from(dbMap).map(async ([dbName, collectionMap]) => {
        let model = await this.generateDBFilesModel(dbName, collectionMap);
        let svLocation = MongoFileLocations.DatabaseSaveLoc.replace(
          "{{DBName}}",
          model.DBName
        );
        let r = Mustache.render(
          readFileSync(
            MongoFileLocations.MongoCodeMustaches +
              MongoFileLocations.DatabaseMustache,
            "utf8"
          ),
          model
        );

        writeFileSync(svLocation, r, "utf8");
      })
    );
  }

  static async generateDBFilesModel(
    dbName: string,
    collectionMap: Map<string, string>
  ) {
    let model = {
      DBName: dbName,
      DBNameSmall: dbName.toLowerCase(),
      Collections: Array.from(collectionMap.keys()).map((c) =>
        Object({ CollectionName: c })
      ),
    };

    return Promise.resolve(model);
  }
}
