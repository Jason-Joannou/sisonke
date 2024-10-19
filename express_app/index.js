import { getEnviromentVariables } from "../enviroment/index";
import express, { Response, Request } from "express";
import bodyParser from "body-parser";

// Initialize app
const app = express();

// Middleware
app.use(bodyParser.json());

// Mount routers to base paths
app.use("/tiger-beetle", payments);

app.get("/", (req, res) => {
  res.json({
    message: "Welcome to the API! This is the base endpoint.",
  });
});
