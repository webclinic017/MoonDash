export const MongoFileLocations = {
  MongoModelSource: process.cwd() + "/generatorschema/mongocode/",

  MongoCodeMustaches: process.cwd() + "/codetemplates/mongocode/",

  SchemaMustache: "Schema.mustache",
  SchemaInterfaceMustache: "SchemaInterface.mustache",
  MongooseModelMustache: "MongooseModel.mustache",
  MongoControllerMustache: "MongoController.mustache",
  DBRouteControllerMustache: "DBRouteController.mustache",
  DatabaseListMustache: "DatabaseList.mustache",
  DatabaseMustache: "Database.mustache",

  SchemaSaveLoc:
    process.cwd() +
    "/src/mongo/schemas/{{SchemaNameSmall}}/{{SchemaName}}Schema.ts",
  SchemaInterfaceSaveLoc:
    process.cwd() +
    "/src/mongo/schemas/{{SchemaNameSmall}}/I{{SchemaName}}Schema.ts",
  MongooseModelSaveLoc:
    process.cwd() +
    "/src/mongo/models/{{SchemaNameSmall}}/{{SchemaName}}Model.ts",
  MongoControllerSaveLoc:
    process.cwd() +
    "/src/mongo/controller/{{SchemaNameSmall}}/{{SchemaName}}MongoController.ts",
  DBRouteControllerSaveLoc:
    process.cwd() +
    "/src/server/routes/databaseaccess/{{SchemaNameSmall}}/{{SchemaName}}RouteController.ts",
  DatabaseListSaveLoc: process.cwd() + "/src/mongo/databases/DatabaseList.ts",
  DatabaseSaveLoc: process.cwd() + "/src/mongo/databases/{{DBName}}.ts",
};
