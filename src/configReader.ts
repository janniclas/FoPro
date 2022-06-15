import { Position } from "./twitterQuery";
import * as fs from "fs";

export const readConfig = () => {
  const bearerToken = process.env.BEARER_TOKEN;
  if (bearerToken) {
    return { bearerToken: bearerToken, filePath: process.argv.slice(2)[0] };
  } else {
    throw Error("No Bearer Token Provided.");
  }
};

export const getPaths = (originalAuthorId: string) => {
  return {
    outputPath: "/usr/app/data/followers/" + originalAuthorId + ".csv",
    logPath: "/usr/app/data/followers/" + originalAuthorId + ".log",
  };
};

export const getStartParameters = (
  rawRecords: string[],
  logPath: string
) => {
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
