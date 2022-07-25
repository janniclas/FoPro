import { Position } from "./twitterQuery";
import * as fs from "fs";
import path = require("node:path");

export const readConfig = () => {
  const bearerToken = process.env.BEARER_TOKEN;
  const customArgs = process.argv.slice(2);
  const pathString = customArgs[1];
  const mode = customArgs[0];

  if (bearerToken && pathString && mode) {
    return { bearerToken: bearerToken, filePath: pathString, mode: mode };
  } else {
    throw Error("Not all input params were provided correctly.");
  }
};

export const getPaths = (filePath: string, originalAuthorId: string) => {
  const p = path.parse(filePath);
  return {
    outputPath: p.dir + "/" + originalAuthorId + ".csv",
    logPath: p.dir + "/" + originalAuthorId + ".log",
  };
};

export const getStartParameters = (rawRecords: string[], logPath: string) => {
  const appendMode = fs.existsSync(logPath);
  let pagination_token: string | undefined = undefined;
  if (appendMode) {
    console.log("A log file has been found and the start parameter are read.");
    const logContent = fs.readFileSync(logPath, "utf8");
    const currentPosition: Position = JSON.parse(logContent);
    console.log(
      `log content ${currentPosition.id} ${currentPosition.pagination_token}`
    );
    const startElement = rawRecords.indexOf(currentPosition.id);
    rawRecords.splice(0, startElement);
    pagination_token = currentPosition.pagination_token;
  }
  return { appendMode, pagination_token, ids: rawRecords };
};
