import { CsvFile } from "./fileWriter";
import { rowToUser, User } from "./statistic";
import * as fs from "fs";
import * as csv from "fast-csv";
import path = require("node:path");

export const prepareTransitivity = (filePath: string) => {
  return new Promise(
    (
      resolve: (result: {
        reacted: string[];
        reactedAndFollowed: User[];
      }) => void
    ) => {
      const interactors = new Set<string>(); //all parent IDs
      const followerMap = new Map<string, User>();

      fs.createReadStream(filePath)
        .pipe(csv.parse())
        .on("error", (error) => console.error(error))
        .on("data", (row) => {
          const followerId: string = row[0];
          const interactorId: string = row[3];
          if (!followerMap.has(followerId)) {
            const user = rowToUser(row);
            followerMap.set(followerId, user);
          } else {
            followerMap.get(followerId)?.parents.push(interactorId);
          }
          if (!interactors.has(interactorId)) {
            interactors.add(interactorId);
          }
        })
        .on("end", (_: number) => {
          console.log("Number of interactors: " + interactors.size);
          console.log("Number of followers: " + followerMap.size);

          const reactedAndFollowed: User[] = [];
          const reacted: string[] = [];
          const result = {
            reacted: reacted,
            reactedAndFollowed: reactedAndFollowed,
          };

          for (const interactor of interactors) {
            console.log(interactor);
            reacted.push(interactor);
            if (followerMap.has(interactor)) {
              reactedAndFollowed.push(followerMap.get(interactor)!);
            }
          }
          console.log(reactedAndFollowed);
          resolve(result);
        });
    }
  );
};

export const getNodeAndEdgePaths = (filePath: string) => {
  const p = path.parse(filePath);
  const nodePath = p.dir + "/" + p.name + "-nodes.csv"
  const edgePath = p.dir + "/" + p.name + "-edges.csv"

  return {nodePath, edgePath};
}

export const saveTransitivity = (
  pathNodes: string,
  pathEdges: string,
  data: {
    reacted: string[];
    reactedAndFollowed: User[];
  }
) => {
  const csvFileNodes = new CsvFile({
    path: pathNodes,
    headers: ["id"],
  });

  const csvFileEdges = new CsvFile({
    path: pathEdges,
    headers: ["source", "target"],
  });

  const nodes: any = [];
  const edges: any = [];
  data.reacted.forEach((id) => {
    data.reactedAndFollowed.forEach((user) => {
      for (const parentId of user.parents) {
        if (id == parentId) {
          edges.push({ source: id, target: user.id });
        }
      }
    });
    nodes.push({ id: id });
  });
  console.log(nodes);
  console.log(edges);
  csvFileNodes.create([]);
  csvFileNodes.append(nodes);

  csvFileEdges.create([]);
  csvFileEdges.append(edges);
};
