import * as fs from "fs";
import * as csv from "fast-csv";
import path = require("node:path");
import { CsvFile } from "./fileWriter";

export const removeDuplicateRows = async (filePath: string) => {
  const rowSet = new Set<string>();
  let duplicateRowCounter = 0;
  const p = path.parse(filePath);
  const noDuplicatesPath = p.dir + "/" + p.name + "-noduplicates.csv";
  const csvFile = new CsvFile({
    path: noDuplicatesPath,
    headers: ["id", "username", "name", "parentId"],
  });
  csvFile.create([]);
  fs.createReadStream(filePath)
    .pipe(csv.parse())
    .on("error", (error) => console.error(error))
    .on("data", (row: string[]) => {
      const rowString = row.reduce((previousValue, currentValue) => {
        return previousValue + currentValue;
      }, "");
      if (!rowSet.has(rowString)) {
        rowSet.add(rowString);
        csvFile.append([row]);
      } else {
        duplicateRowCounter += 1;
      }
    });
};
