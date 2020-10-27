import { ServiceFileLocations } from "./ServiceFileLocations";
import {
  readdirSync,
  readFileSync,
  writeFileSync,
  mkdirSync,
  existsSync,
} from "fs-extra";
import Mustache from "mustache";
import _ from "lodash";

export class GenerateServiceCode {
  static async listModels() {
    let folder = ServiceFileLocations.ServiceModelSource;
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
      SchemaName: o.Service.charAt(0).toUpperCase() + o.Service.slice(1),
      SchemaNameSmall: o.Service.toLowerCase(),
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

        await this.generateOtherFiles(model);
      })
    );
  }

  static async generateOtherFiles(model: any) {
    let x = [];
    x.push(ServiceFileLocations.ServiceMustache);
    x.push(ServiceFileLocations.RouteControllerMustache);

    await Promise.all(
      x.map((f) => {
        let mustacheLoc = ServiceFileLocations.ServiceCodeMustaches + f;
        let mustache = readFileSync(mustacheLoc, "utf8");

        let k = f.replace(".mustache", "SaveLoc");
        let svLocRaw = _.get(ServiceFileLocations, k);
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
}
