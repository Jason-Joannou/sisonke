import express from "express";
import { validateWalletAddress } from "../utils/wallet.js";

const validationRouter = express.Router();

validationRouter.post("/wallet", async (req, res) => {
  const { wallet_address } = req.body;

  try {
    const validationResult = await validateWalletAddress(wallet_address);
    console.log(validationResult);

    return res.status(200).json({
      message:
        "Wallet address is valid, please wait while be onboard your account...",
      data: validationResult,
    });
  } catch (error) {
    return res.status(error.status || 500).json({
      message: "Wallet address validation failed, please try again",
    });
  }
});

export default validationRouter;
