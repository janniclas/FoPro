import * as fs from "fs";
import * as csv from "fast-csv";
import { CsvFile } from "./fileWriter";

export interface User {
  id: string;
  userName: string;
  name: string;
  parents: string[];
}

interface Statistic {
  set: Map<string, User>;
}

export const rowToUser = (row: any): User => {
  const parents = [];
  parents.push(row[3]);
  return {
    id: row[0],
    userName: row[1],
    name: row[2],
    parents: parents,
  };
};

export const calculateStatistics = (path: string) => {
  return new Promise((resolve: (result: Statistic) => void) => {
    const followerMap = new Map<string, User>();
    let duplicateCounter = 0;

    fs.createReadStream(path)
      .pipe(csv.parse())
      .on("error", (error) => console.error(error))
      .on("data", (row) => {
        const id: string = row[0];
        if (!followerMap.has(id)) {
          const user = rowToUser(row);
          followerMap.set(id, user);
        } else {
          const parents = followerMap.get(id)?.parents;
          const parent = row[3];
          if (!parents?.includes(parent)) {
            parents?.push(parent);
            duplicateCounter += 1;
          }
        }
      })
      .on("end", (rowCount: number) => {
        console.log("statistic for " + path);
        console.log("overall followers with duplicates: " + rowCount);
        console.log("unique follower count: " + followerMap.size);
        console.log("duplicate counter " + duplicateCounter);
        const percentageDuplicateUsers = (duplicateCounter / rowCount) * 100;
        console.log(
          "Percentage of duplicates " + percentageDuplicateUsers + "\n"
        );
        resolve({ set: followerMap });
      });
  });
};

const getUniquePath = (path: string) => {
  const splits = path.split(".");
  return splits[0] + "-unique." + splits[1];
};

export const saveUniqueFollower = (path: string, statistic: Statistic) => {
  const csvFile = new CsvFile({
    path: getUniquePath(path),
    headers: ["id", "userName", "name", "parents"],
  });
  const rows = [];
  for (const user of statistic.set.values()) {
    let parentString = "";
    user.parents.forEach((parent) => {
      parentString += parent + "-";
    });
    rows.push({ ...user, parents: parentString });
  }
  csvFile.create([]);
  csvFile.append(rows);
};
