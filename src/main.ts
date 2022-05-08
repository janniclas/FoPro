import "dotenv/config";
import * as fs from "fs";
import Client from "twitter-api-sdk";

import { getRawRecords } from "./fileReader";
import { CsvFile } from "./fileWriter";
import { Position, queryFollowers } from "./twitterQuery";

export const main = async () => {
  const bearerToken = process.env.BEARER_TOKEN;

  if (bearerToken) {
    const filePath = "/usr/app/data/deuxcvsix.csv";
    const rawRecords = await getRawRecords(filePath);
    const originalAuthorId = rawRecords[0];
    console.log(`read ids from file. Parent id ${originalAuthorId}`);
    const outputPath =
      "/usr/app/data/followers/" + originalAuthorId + ".csv";
    const appendMode = fs.existsSync(outputPath);
    const logPath =
      "/usr/app/data/followers/" + originalAuthorId + ".log";
    let pagination_token: string | undefined = undefined;
    const csvFile = new CsvFile({
      path: outputPath,
      headers: ["id", "username", "name", "parentId"],
    });

    if (!appendMode) {
      console.log("A new file is created to store the data");
      csvFile.create([]);
    } else {
      console.log(
        "A log file has been found and the start parameter are read."
      );
      const logContent = fs.readFileSync(logPath, "utf8");
      const currentPosition: Position = JSON.parse(logContent);
      console.log(
        `log content ${currentPosition.id} ${currentPosition.pagination_token}`
      );
      const startElement = rawRecords.indexOf(currentPosition.id);
      rawRecords.splice(0, startElement);
      pagination_token = currentPosition.pagination_token;
    }
    console.log(rawRecords);
    const client = new Client(bearerToken);
    for (const value of rawRecords) {
      console.log(`start query for user with id ${value}`);
      let hasNext = true;
      while (hasNext) {
        const { followers, nextToken } = await queryFollowers(
          client,
          value,
          logPath,
          pagination_token
        );
        console.log(
          `query result for user with id ${value} and token ${pagination_token}`
        );
        if (followers) {
          const essentialData = followers.map((follower: any) => {
            return {
              id: follower.id,
              username: follower.username,
              name: follower.name,
              parentId: value,
            };
          });
          console.log(`start writing results to file for user ${value}`);
          await csvFile.append(essentialData);
          console.log(`finished writing results to file for user ${value}`);
        }
        if (nextToken) {
          pagination_token = nextToken;
        } else {
          hasNext = false;
        }
      }
    }
  } else {
    console.error("No bearer token found");
  }
};

main();
