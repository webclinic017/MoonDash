export const ServiceFileLocations = {
  ServiceModelSource: process.cwd() + "/generatorschema/Servicecode/",

  ServiceCodeMustaches: process.cwd() + "/codetemplates/Servicecode/",

  ServiceMustache: "Service.mustache",
  RouteControllerMustache: "ServiceRouteController.mustache",

  ServiceSaveLoc:
    process.cwd() + "/src/services/{{SchemaNameSmall}}/{{SchemaName}}.ts",

  ServiceRouteControllerSaveLoc:
    process.cwd() +
    "/src/server/routes/services/{{SchemaNameSmall}}/{{SchemaName}}RouteController.ts",
};
