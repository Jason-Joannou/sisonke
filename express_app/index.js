import express from "express";
import bodyParser from "body-parser";
import tigerRouter from "./routes/tigerbeetle.js";

const port = 3001;
// Initialize app
const app = express();

// Middleware
app.use(bodyParser.json());

// Mount routers to base paths
app.use("/tiger-beetle", tigerRouter);

app.get("/", (req, res) => {
  res.json({
    message: "Welcome to the API! This is the base endpoint.",
  });
});

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
