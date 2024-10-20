import express from "express";
import {
  createPersonEntityAccount,
  createPoolEntities,
} from "../tiger-beetle/createEntities.js";

const tigerRouter = express.Router();

tigerRouter.get("/createPersonEntity", async (req, res) => {
  try {
    const personEntityId = await createPersonEntityAccount();
    if (personEntityId === -1) {
      return res.status(500).json({ error: "Failed to create account" });
    }

    return res
      .status(200)
      .json({ personEntityId: personEntityId, message: "success" });
  } catch (error) {
    console.log(error);
    return res.status(500).json({ error: "Failed to create account" });
  }
});

tigerRouter.get("/createPoolEntities", async (req, res) => {
  try {
    const poolEntityId = await createPoolEntities();
    if (poolEntityId === -1) {
      return res.status(500).json({ error: "Failed to create account" });
    }

    return res
      .status(200)
      .json({ poolEntityId: poolEntityId, message: "success" });
  } catch (error) {
    console.log(error);
    return res.status(500).json({ error: "Failed to create account" });
  }
});

tigerRouter.post("/transerBetweenEntities", (req, res) => {});

tigerRouter.post("/transferToContributionPool", (req, res) => {});

tigerRouter.post("/transferFromContributionPool", (req, res) => {});

tigerRouter.post("/transferToPayoutPool", (req, res) => {});

tigerRouter.post("/transferFromPayoutPool", (req, res) => {});

export default tigerRouter;
