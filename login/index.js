import express from "express";
import bodyParser from "body-parser";
import path from "path";
import pg from "pg";

const app = express();
const port = 3000;

const db = new pg.Client({
  user: "postgres",
  host: "localhost",
  database: "Hackathon Users",
  password: "12345678",
  port: 5432,
});

db.connect();


app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static("public"));
app.set('view engine', 'ejs');
app.get("/", async (req, res) => {
  res.render("index.ejs", { message: "" }); // Initialize message to empty string
});

app.get("/front.ejs", async (req, res) => {
  // Here you can render your "front.ejs" file
  res.render("front.ejs");
});

app.post("/login", async (req, res) => {
  const username = req.body.u_name;
  const password = req.body.pass;

   
    // Query the database to check if the user exists
    const result = await db.query("SELECT * FROM users WHERE email = $1 AND password = $2", [username, password]); // Pass parameters as an array
  console.log(result.rows);
    if (result.rows.length > 0) {
      // If user exists, redirect to dashboard or home page
      res.render("/dashboard");
    } 
    else {
      // If user doesn't exist or credentials are incorrect, render the login page with an error message
      res.render("index.ejs", { message: "User does not exist. Please sign up." });
    }

  
});

app.post("/submit", async (req, res) => {
  const yesNoValue = req.body.yesno;
  const username = req.body.username;
  const password = req.body.password;
  console.log(req.body);
 console.log(`'${yesNoValue}'`);
    // Execute a parameterized query to insert user data into the database
    const query = "INSERT INTO users (email, password, insurance) VALUES ($1, $2, $3)";
    await db.query(query, [username, password, yesNoValue]);

    if (yesNoValue == 'Y') {
      // If insurance value is 'Y', render the check.ejs file
      console.log("yes");
      res.render("check.ejs");
      res.render("check.ejs", { registrationSuccessfully: "registrationSuccessful" });
    } else {
      // If insurance value is 'N', redirect to front.ejs
      res.redirect("/front.ejs");
    }
 
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server is listening at http://localhost:${port}`);
});
