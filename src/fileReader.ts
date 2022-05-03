import * as fs from "fs";
import { parse } from "fast-csv";

export const getRawRecords = async (filePath: string) => {
  return new Promise((resolve: (value: string[]) => void, reject) => {
    const rawRecords: string[] = [];
    fs.createReadStream(filePath)
      .pipe(parse({ headers: false }))
      .on("error", (error: any) => {
        console.error(error);
        reject();
      })
      .on("data", (row: any) => {
        rawRecords.push(row[0]);
      })
      .on("end", (rowCount: number) => {
        console.log(`Parsed ${rowCount} rows`);
        resolve(rawRecords);
      });
  });
};
