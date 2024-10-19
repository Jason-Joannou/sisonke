import express from "express";
import {
  createPersonEntityAccount,
  createPoolEntities,
} from "../tiger-beetle/createEntities";

const router = express.Router();

router.post("/createPersonEntity", (req, res) => {});

router.post("/createPoolEntities", (req, res) => {});

router.post("/transerBetweenEntities", (req, res) => {});

router.post("/transferToContributionPool", (req, res) => {});

router.post("/transferFromContributionPool", (req, res) => {});

router.post("/transferToPayoutPool", (req, res) => {});

router.post("/transferFromPayoutPool", (req, res) => {});

export default router;
