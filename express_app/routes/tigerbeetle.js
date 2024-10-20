import express from "express";
import {
  createPersonEntityAccount,
  createPoolEntities,
} from "../tiger-beetle/createEntities.js";
import { recordTransaction } from "../tiger-beetle/utils.js";

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

tigerRouter.post("/transferBetweenEntities", async (req, res) => {
  const { sourceAccountId, destinationAccountId, amount } = req.body;

  if (!sourceAccountId || !destinationAccountId || !amount) {
    return res.status(400).json({ error: "Missing required fields" });
  }

  try {
    const result = await recordTransaction(
      sourceAccountId,
      destinationAccountId,
      amount
    );
    if (!result.success) {
      return res.status(500).json({ error: result.error });
    }

    return res
      .status(200)
      .json({ message: "Transaction successful", result: result.result });
  } catch (error) {
    console.log(error);
    return res.status(500).json({ error: "Failed to process transaction" });
  }
});

tigerRouter.post("/transferToContributionPool", (req, res) => {});

tigerRouter.post("/transferFromContributionPool", (req, res) => {});

tigerRouter.post("/transferToPayoutPool", (req, res) => {});

tigerRouter.post("/transferFromPayoutPool", (req, res) => {});

export default tigerRouter;
