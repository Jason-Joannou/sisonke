import express from "express";
import { validateWalletAddress } from "../utils/wallet";

const validationRouter = express.Router();

validationRouter.post("/wallet", async (req, res) => {
  const { walletAddress } = req.body;

  try {
    const validationResult = await validateWalletAddress(walletAddress);

    if (validationResult.isValid) {
      return res.status(200).json({
        message: "Wallet address is valid",
        data: validationResult.data,
      });
    }
  } catch (error) {
    return res.status(error.status || 500).json({
      message: error.description || "Validation failed",
    });
  }
});

export default validationRouter;
